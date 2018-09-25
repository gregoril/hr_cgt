# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FullEmployee(models.Model):
	_inherit = 'hr.employee'


	@api.multi
	def _compute_documents_count(self):
		docs = self.env['hr.documents']
		for employee in self:
			employee.documents_count = docs.search_count([('employee', '=', employee.id)])


	@api.multi
	@api.depends('log_documents')
	def _compute_documents_reminder(self):
		today = fields.Date.from_string(fields.Date.today())
		for record in self:

			# init
			deadline_expired = False
			deadline_warning = False
			deadline_total = 0
			deadline_name = ''
			diff_record = float("inf")
            
			log_documents = self.env['hr.documents'].search(
				[
					('employee', '=', record.id),
					('state', '=', 'todo')
				]
			)
            
			# for each documents linked
			for document in log_documents:

				# check deadline by date
				if document.deadline_date:
					deadline_date_obj = fields.Date.from_string(document.deadline_date)
					diff = (deadline_date_obj - today).days

					if diff < 0:
						# deadline per data scaduta
						deadline_expired = True
						deadline_total +=1

					elif diff >= 0 and diff < document.default_warning_limit_date_hr:
						# deadline per data in scadenza
						deadline_warning = True
						deadline_total +=1
					
					if diff < diff_record:
						# save documents name if this is a more immediate deadline
						deadline_name = document.document_type.name
						diff_record = diff

			record.deadline_expired = deadline_expired
			record.deadline_warning = deadline_warning
			record.deadline_total = deadline_total -1
			record.deadline_name = deadline_name


	# new fields
	driver_vector_info = fields.Text(
		string='Driver Vector info'
	)

	documents_count = fields.Integer(
		string='Documents',
		compute=_compute_documents_count
	)

	log_documents = fields.One2many(
		comodel_name='hr.documents',
		inverse_name='employee', 
		string='Documents'
	)

	deadline_expired = fields.Boolean(
		string='Document Expired',
		compute=_compute_documents_reminder
	)

	deadline_warning = fields.Boolean(
		string='Document Expiration Warning',
		compute=_compute_documents_reminder
	)

	deadline_total = fields.Integer(
		compute=_compute_documents_reminder
	)

	deadline_name = fields.Char(
		compute=_compute_documents_reminder
	)
	
    
	@api.multi
	def return_action_to_open_empl(self):
		self.ensure_one()
		xml_id = self.env.context.get('xml_id')
		if xml_id:
			res = self.env['ir.actions.act_window'].for_xml_id('hr_cgt', xml_id)
			res.update(
				context=dict(self.env.context, default_employee=self.id, group_by=False),
				domain=[('employee', '=', self.id)]
			)
			return res
		return False
