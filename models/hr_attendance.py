# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
import pytz
from datetime import datetime

import logging
import pprint
_logger = logging.getLogger(__name__)


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

    @api.multi
    def unlink(self):
        """
            Delete all record(s) from recordset
            return True on success, False otherwise

            @return: True on success, False otherwise

            #TODO: process before delete resource
        """

        for r in self:
            attendance_day = self.env['hr.attendance.day'].search([
                ('attendance_id', '=', r.id)
            ])
            if not attendance_day:
                continue

            difss = list(set(attendance_day.attendance_ids.ids)-set(self.ids))

            _logger.info(pprint.pformat(difss))

            # switch or delete
            if difss:
                attendance_day.write({
                    'attendance_id': difss[0]
                })
            else:
                attendance_day.unlink()

        result = super(FullAttendance, self).unlink()

        return result
