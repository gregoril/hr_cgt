# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class FullHrDocumentType(models.Model):
    _name = 'hr.document.type'


    name = fields.Char(string='Name', required=True)
    document_type = fields.Char(string='Type')
    warning_limit_date_hr = fields.Integer(string='Warning limit date', default=15)
