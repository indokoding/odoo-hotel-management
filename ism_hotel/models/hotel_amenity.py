from odoo import models, fields, api, _

class HotelAmenity(models.Model):
    _name = 'hotel.amenity'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hotel Amenity'
    
    name = fields.Char(string="Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)