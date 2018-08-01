# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

import logging
_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):

    _inherit = "hr.employee"

    def _compute_documents_count(self):
        
        doc = self.env['hr.documents']
        for employee in self:
            employee.documents_count = doc.search_count([('employee', '=', employee.id)])

    documents_count = fields.Integer(compute='_compute_documents_count', string='Contracts')

class HrDocuments(models.Model):
    _name = 'hr.documents'
    _inherit = ['hr.job', 'mail.thread']
    
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

    deadline_date = fields.Date(track_visibility='onchange')
    days_left = fields.Integer(compute='_compute_days_left',string='Warning Date')
    employee = fields.Many2one(comodel_name='hr.employee',
    string='employee',track_visibility='onchange'
    )
    document_type = fields.Many2one(comodel_name='hr.document.type',
    string = 'document type',track_visibility='onchange'
    )
    default_warning_limit_date_hr = fields.Integer(related='document_type.warning_limit_date_hr') 
    
    state = fields.Selection(selection=[('todo', 'To do'), ('done', 'Done')],
			string='Status', default='todo', copy=False, index=True,
			help='Choose wheter the service is still to be done or not'
            )
    
    @api.multi
    def todo_state(self):
        for record in self:
            record.state = 'todo'

    @api.multi
    def set_done(self):
        for record in self:
            record.state = 'done'

    

