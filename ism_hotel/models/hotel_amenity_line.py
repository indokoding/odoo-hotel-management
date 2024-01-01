from odoo import models, fields, api, _

class HotelAmenityLine(models.Model):
    _name = 'hotel.amenity.line'
    _description = 'Hotel Amenities Group Line'
    
    product_id = fields.Many2one('product.template', string="Product", index=True)
    sequence = fields.Integer(string="Sequence")
    amenity_id = fields.Many2one('hotel.amenity', string="Hotel Amenity")