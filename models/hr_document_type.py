# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class HrDocumentType(models.Model):
    _name = 'hr.document.type'

    name = fields.Char(required=True)
    document_type = fields.Char(string="Type")

