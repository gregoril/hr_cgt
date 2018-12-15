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
        'hr', 'hr_contract', 'hr_holidays',
        'hr_attendance'
    ],

    'data': [
        # views
        'views/hr_contract.xml',
        'views/hr_documents.xml',
        'views/hr_document_type.xml',
        'views/hr_employee.xml',

        # security
        'security/ir.model.access.csv',

        # menu
        'views/dashboard_menu.xml',
    ],

    'installable': True,
    'application': True,
}
