from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HotelRoom(models.Model):
    _name = 'hotel.room'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hotel Room'
    
    # TODO: add a new field called 'status' with the following options:
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
    ], string="State", default='available', store=True)
    booking_ids = fields.Many2many('hotel.book.history', string="Booking History")
    booking_count = fields.Integer(string="Booking Count", compute="_compute_booking_count", store=False)
    
    def _compute_booking_count(self):
        for record in self:
            record.booking_count = len(record.booking_ids)
            
    def action_view_reservations(self):
        self.ensure_one()
        action = self.env.ref('ism_hotel.action_hotel_book_history_all').read()[0]
        action['domain'] = [('room_ids', 'in', self.id)]
        return action
    
    def action_maintenance(self):
        self.ensure_one()
        if self.state == 'occupied':
            raise UserError(_("You cannot set a room to maintenance while it is occupied."))
        
        self.state = 'maintenance'
        
    def action_available(self):
        self.ensure_one()
        self.state = 'available'
        
    def open_booking_form(self):
        return {
            'name': 'Create Room Booking',
            'view_mode': 'form',
            'res_model': 'hotel.book.history',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {
                'active_room_id': self.id
            }
        }
            
    def open_checkout_form(self):
        booking_id = self._search_currently_occupied_rooms()
        print('booking_id', booking_id)
        if booking_id:
            return {
                'name': _('Check Out'),
                'view_mode': 'form',
                'res_model': 'hotel.book.history',
                'res_id': booking_id.id,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {
                    'active_id': booking_id.id
                },
            }
        else:
            raise UserError(_("There is no room currently occupied."))
    
    def _search_currently_occupied_rooms(self):
        room_id = self._context.get('default_room_id')
        # look for the first room booking that is available or reserved
        print('room_id', room_id)
        room_booking = self.env['hotel.book.history'].search([
            ('room_ids', 'in', room_id),
            ('state', '=', 'checked_in'),
        ], limit=1)
        return room_booking
        