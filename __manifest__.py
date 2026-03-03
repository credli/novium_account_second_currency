# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Accounting Second Currency',
    'description': """Enable a second currency for accounting transactions.""",
    'author': "Novium SARL",
    'category': 'Accounting/Accounting',
    'depends': ['base', 'account', 'sale'],
    'data': [
        'views/account_views.xml',
        'views/company.xml',
        'views/res_config_settings_views.xml',
    ],
    'application': False,
    'auto_install': True,
    'license': 'OEEL-1',
}
