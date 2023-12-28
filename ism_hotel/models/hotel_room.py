from odoo import models, fields, api, _

class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'
    
    STATUS_COLOR = {
        'available': 'success',
        'reserved': 'warning',
        'occupied': 'danger',
        'maintenance': 'info',
        'unavailable': 'dark',
    }
    
    name = fields.Char(string="Name", required=True)
    room_type = fields.Many2one('product.template', string="Room Type", required=True)
    state = fields.Selection([
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
        ('unavailable', 'Unavailable'),
    ], string="State", default='available', required=True)