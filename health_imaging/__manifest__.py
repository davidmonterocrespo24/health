# -*- coding: utf-8 -*-
{
    'name': "gnuhealth_imaging",

    'summary': """
        GNU Health Diagnostic Imaging management package""",

    'description': """
        GNU Health Diagnostic Imaging management package
        - Imaging types and tests.
        - Imaging test requests and results.
    """,

    'author': "GNU Solidario",
    'website': "https://www.gnuhealth.org",

    'category': 'Healthcare Industry',
    'version': '0.0.1',

    # any module necessary for this one to work correctly
    #TODO depends 'health'
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
