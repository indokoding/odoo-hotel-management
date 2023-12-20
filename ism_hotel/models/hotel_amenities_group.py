from odoo import models, fields, api, _

class HotelAmenitiesGroup(models.Model):
    _name = 'hotel.amenities.group'
    _description = 'Hotel Amenities Group'
    
    name = fields.Char(string="Name", required=True)