from odoo import models, fields, api, _

class HotelAmenity(models.Model):
    _name = 'hotel.amenity'
    _description = 'Hotel Amenity'
    
    name = fields.Char(string="Name", required=True)