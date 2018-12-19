# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
import pytz
from datetime import datetime


class FullAttendanceDay(models.Model):
    _name = 'hr.attendance.day'
    _description = "Attendance by Day"
    _order = "day desc"

    _sql_constraints = [
        (
            'employee_day_unique',
            'unique(employee_id, day)',
            'Day be unique for employee'
        ),
    ]

    @api.multi
    def name_get(self):
        result = []
        for attendance in self:
            result.append((attendance.id, _("%(empl_name)s for %(day)s") % {
                'empl_name': attendance.employee_id.name_related,
                'day': fields.Date.to_string(
                    datetime.strptime(
                        attendance.day,
                        DEFAULT_SERVER_DATE_FORMAT
                    )
                ),
            }))
        return result

    @api.depends('attendance_ids.check_in',
                 'attendance_ids.check_out',
                 'attendance_id.check_in')
    def _compute_day(self):

        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)

        for r in self:

            if isinstance(r.id, models.NewId):
                continue

            attendances = self.env['hr.attendance'].search(
                [('attendance_day_id', '=', r.id)],
                order="check_in asc",
            )
            tot_worked = 0
            tot_break = 0
            check_in = False
            check_out = False

            if not attendances:
                attendances = [r.attendance_id]

            first_a = attendances[0]
            check_in = first_a.check_in
            day = datetime.strftime(
                pytz.utc.localize(
                    datetime.strptime(
                        check_in,
                        DEFAULT_SERVER_DATETIME_FORMAT
                    )
                ).astimezone(local), DEFAULT_SERVER_DATE_FORMAT)

            prev = False
            for a in attendances:

                if prev:
                    delta = datetime.strptime(
                            a.check_in, DEFAULT_SERVER_DATETIME_FORMAT
                        ) - datetime.strptime(
                            prev.check_out, DEFAULT_SERVER_DATETIME_FORMAT
                        )
                    tot_break += delta.total_seconds() / 3600.0
                tot_worked += a.worked_hours
                check_out = a.check_out
                prev = a

            r.day = day
            r.check_in = check_in
            r.check_out = check_out
            r.worked_hours = tot_worked
            r.break_hours = tot_break

    # Fields

    day = fields.Date(
        string=u'Day',
        compute=_compute_day,
        store=True,
        readonly=True
    )

    worked_hours = fields.Float(
        string='Worked Hours',
        compute=_compute_day,
        store=True,
        readonly=True
    )

    break_hours = fields.Float(
        string='Break Hours',
        compute=_compute_day,
        store=True,
        readonly=True
    )

    check_in = fields.Datetime(
        string="Check In",
        compute=_compute_day,
        store=True,
        readonly=True
    )

    check_out = fields.Datetime(
        string="Check Out",
        compute=_compute_day,
        store=True,
        readonly=True
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string="Employee",
        required=True,
        ondelete='cascade',
        index=True,
        readonly=True
    )

    attendance_ids = fields.One2many(
        string=u'Attendance',
        comodel_name='hr.attendance',
        inverse_name='attendance_day_id',
    )

    attendance_id = fields.Many2one(
        'hr.attendance',
        string="Creating attendance",
        required=True,
    )
