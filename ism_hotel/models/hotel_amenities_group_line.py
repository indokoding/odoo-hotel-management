from odoo import models, fields, api, _

class HotelAmenitiesGroupLine(models.Model):
    _name = 'hotel.amenities.group.line'
    _description = 'Hotel Amenities Group Line'
    
    hotel_amenities_group_id = fields.Many2one('hotel.amenities.group', string="Hotel Amenities Group", index=True)
    sequence = fields.Integer(string="Sequence")
    hotel_amenity_id = fields.Many2one('hotel.amenity', string="Hotel Amenity")