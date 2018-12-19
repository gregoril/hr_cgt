# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
import pytz
from datetime import datetime


class FullAttendance(models.Model):
    _inherit = 'hr.attendance'

    _sql_constraints = [
        (
            'employee_check_id_unique',
            'unique(employee_id, check_in)',
            'Check in must be unique for employee'
        ),
    ]

    attendance_day_id = fields.Many2one(
        'hr.attendance.day',
        string="Attendance day",
    )

    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record

            @return: returns a id of new record
        """

        result = super(FullAttendance, self).create(values)

        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)

        day = datetime.strftime(
            pytz.utc.localize(
                datetime.strptime(
                    result.check_in,
                    DEFAULT_SERVER_DATETIME_FORMAT
                )
            ).astimezone(local), DEFAULT_SERVER_DATE_FORMAT)

        attendance_day = self.env['hr.attendance.day'].search([
            ('employee_id', '=', result.employee_id.id),
            ('day', '=', day),
        ])

        if not attendance_day:
            attendance_day = self.env['hr.attendance.day'].create(
                {
                    'attendance_id': result.id,
                    'employee_id': result.employee_id.id,
                }
            )

        result.attendance_day_id = attendance_day.id

        return result
