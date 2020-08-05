# Copyright 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright Copyright 2020 NeoHan Solutions Cuba
# para GNU Solidario  <health@gnusolidario.org>
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Locale - Default UoM',
    'summary': 'This provides settings to select default UoMs at the '
               'language level.',
    'version': '13.0.0.0.1',
    'category': 'Extra Tools',
    'website': 'https://laslabs.com/',
    'author': 'LasLabs, '
              'Odoo Community Association (OCA)',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'product',
    ],
    'data': [
        'views/res_lang_view.xml',
    ],
    'demo': [
        'demo/res_lang_demo.xml',
    ],
}
