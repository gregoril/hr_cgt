# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FullEmployee(models.Model):
    _inherit = 'hr.employee'

    driver_vector_info = fields.Text(string='Driver Vector info')
