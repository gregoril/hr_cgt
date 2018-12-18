# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FullAttendance(models.Model):
    _inherit = 'hr.attendance'

    _sql_constraints = [
        (
            'employee_check_id_unique',
            'unique(employee_id, check_in)',
            'Check in must be unique for employee'
        ),
    ]
