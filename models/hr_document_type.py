# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FullHrDocumentType(models.Model):
    _name = 'hr.document.type'

    # Fields

    name = fields.Char(string='Name', required=True)
    warning_limit_date_hr = fields.Integer(
        string='Warning limit date', default=15
    )
