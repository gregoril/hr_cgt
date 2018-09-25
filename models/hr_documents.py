# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

import logging
_logger = logging.getLogger(__name__)


class FullHrDocuments(models.Model):
    _name = 'hr.documents'


    @api.depends('deadline_date')   
    def _compute_days_left(self):
		"""return a dict with as value for each service an integer
		if service is in an open state and is overdue, return 0
		if service not date dependent or done, return -1
		otherwise return the number of days before the service expires
		"""
		
		for record in self:
			if (record.deadline_date and (record.state == 'todo')):
				today = fields.Date.from_string(fields.Date.today())
				renew_date = fields.Date.from_string(record.deadline_date)
				diff_time = (renew_date - today).days

				record.days_left = diff_time > 0 and diff_time or 0
			else:
				record.days_left = -1


    # new fields
    name = fields.Char(
        string='Name', required=True,
        track_visibility='onchange'
    )

    deadline_date = fields.Date(
        string='Deadline date',
        track_visibility='onchange'
    )

    default_warning_limit_date_hr = fields.Integer(
        related='document_type.warning_limit_date_hr'
    )

    employee = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        track_visibility='onchange'
    )

    document_type = fields.Many2one(
        comodel_name='hr.document.type',
        string='Document type',
        track_visibility='onchange',
        required=True
    )
    
    state = fields.Selection(
        selection=[('todo', 'To do'), ('done', 'Done')],
        string='Status', default='todo', copy=False, index=True
    )

    # computed fields
    days_left = fields.Integer(
        string='Warning Date',
        compute=_compute_days_left
    )


    @api.multi
    def todo_state(self):
        for record in self:
            record.state = 'todo'

    @api.multi
    def set_done(self):
        for record in self:
            record.state = 'done'
