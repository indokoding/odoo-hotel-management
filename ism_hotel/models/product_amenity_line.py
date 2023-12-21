from odoo import models, fields, api, _

class ProductAmenityLine(models.Model):
    _name = 'product.amenity.line'
    _description = 'Hotel Amenities Group Line'
    
    product_id = fields.Many2one('product.template', string="Product", index=True)
    sequence = fields.Integer(string="Sequence")
    hotel_amenity_id = fields.Many2one('hotel.amenity', string="Hotel Amenity")