# -*- coding: utf-8 -*-
{
    'name': 'Cogito Employee Full',
    'description': """
        Jobs, Departments and Employees Details from OCA and custom.
    """,

    'author': "Cogito",
    'website': "http://www.cogitoweb.it",

    'license': 'AGPL-3',
    'category': 'Human Resources',
    'version': '10.0.1.0.0',

    'depends': [
        'hr'
    ],

    'data': [
        ## security
        #'security/ir.model.access.csv',

        ## menu
        'views/dashboard_menu.xml',
    ],

    'installable': True,
}
