from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    company_second_currency_id = fields.Many2one(string='Company Second Currency', readonly=True,
                                                 related='company_id.second_currency_id')

    enable_second_currency_for_company = fields.Boolean(related='company_id.enable_second_currency_for_company',
                                                        store=True)


class AccountMove(models.Model):
    _inherit = 'account.move.line'

    exchange_amount = fields.Float(compute='_compute_exchange_amount', store=True, readonly=False)  #
    debit_exchange = fields.Float(compute='_compute_exchange_amount', store=True, readonly=False)  #
    credit_exchange = fields.Float(compute='_compute_exchange_amount', store=True, readonly=False)  #

    exchange_currency = fields.Many2one(
        'res.currency',
        related='company_id.second_currency_id',
        string="Company Second Currency",
        readonly=True,
        store=True
    )

    @api.depends('debit', 'credit', 'currency_id', 'price_subtotal', 'amount_currency', 'date', 'move_id.invoice_date')
    def _compute_exchange_amount(self):
        for rec in self:
            rec.exchange_amount = amount = amount_deb = amount_cred = rec.debit_exchange = rec.credit_exchange = 0

            CURR = self.exchange_currency
            # if CURR.name == self.company_id.currency_id.name:
            #     CURR = self.company_id.currency_id

            if rec.debit != 0:
                amount = rec.debit
            if rec.credit != 0:
                amount = rec.credit
            if rec.price_subtotal != 0:
                amount = rec.price_subtotal
            if rec.currency_id.name != CURR.name:
                if rec.date:
                    rec.exchange_amount = rec.company_id.currency_id._convert(amount, CURR, rec.company_id, rec.date)
                    rec.debit_exchange = rec.company_id.currency_id._convert(rec.debit, CURR, rec.company_id, rec.date)
                    rec.credit_exchange = rec.company_id.currency_id._convert(rec.credit, CURR, rec.company_id,
                                                                              rec.date)
                else:
                    rec.exchange_amount = rec.company_id.currency_id._convert(amount, CURR, rec.company_id,
                                                                              fields.Date.context_today(
                                                                                  self))
                    rec.debit_exchange = rec.company_id.currency_id._convert(rec.debit, CURR, rec.company_id, rec.date)
                    rec.credit_exchange = rec.company_id.currency_id._convert(rec.credit, CURR, rec.company_id,
                                                                              fields.Date.context_today(
                                                                                  self))
            else:
                if rec.amount_currency >= 0:
                    rec.exchange_amount = rec.amount_currency
                    rec.debit_exchange = rec.amount_currency
                    rec.credit_exchange = 0
                else:
                    rec.exchange_amount = rec.amount_currency
                    rec.debit_exchange = 0
                    rec.credit_exchange = rec.amount_currency * -1


class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.constrains('tax_group_id')
    def validate_tax_group_id(self):
        for record in self:
            if record.tax_group_id.country_id and record.country_id and record.tax_group_id.country_id != record.country_id:
                raise ValidationError(_("The tax group " + str(
                    record.tax_group_id.name) + " must have the same country_id " + str(
                    record.tax_group_id.country_id.name) + " as the tax using it " + str(
                    record.name) + " " + str(record.country_id.name) + "."))