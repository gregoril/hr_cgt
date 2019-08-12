# -*- coding: utf-8 -*-
{
    'name': 'Employee Full',
    'description': """
        Jobs, Departments and Employees Details from OCA and custom.
        Original module from Cogito
    """,

    'author': "Cogito / IDSYS",
    

    'license': 'OPL-1',
    'category': 'Human Resources',
    'version': '0.1',

    'depends': [
        'hr', 'hr_contract', 'hr_holidays',
        'hr_attendance'
    ],

    'data': [
        # views
        'views/hr_attendance_day.xml',
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
