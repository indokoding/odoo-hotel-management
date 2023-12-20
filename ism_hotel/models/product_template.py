from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_room = fields.Boolean(string="Is room")
    max_allowed_person = fields.Integer(string="Max allowed person")