from odoo import models, fields, api, _

class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'
    
    name = fields.Char(string="Name", required=True)
    room_type = fields.Many2one('product.template', string="Room Type", required=True)