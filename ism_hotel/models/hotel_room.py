from odoo import models, fields, api, _

class HotelRoom(models.Model):
    _name = 'hotel.room'
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
    ], string="State", default='available', compute='_compute_state', store=True)
    
    @api.depends('state')
    def _compute_state(self):
        for record in self:
            record.state = 'available'
        
        is_booked_today = self.env['hotel.book.history'].search([
            ('check_in', '<=', fields.Date.today()),
            ('check_out', '>=', fields.Date.today()),
            ('room_ids', 'in', self.ids),
            ('state', '=', 'booked')
        ])
        print(is_booked_today)
        if is_booked_today:
            for record in self:
                if record.state == 'available':
                    record.state = 'reserved'
    
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
        
    def open_checkin_form(self):
        booking_id = self._search_nearest_booked_rooms()
        if booking_id:
            return {
                'name': _('Check In'),
                'view_mode': 'form',
                'res_model': 'checkin.room.booking',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': {
                    'active_id': booking_id.id
                }
            }
        else:
            return {
                'name': 'Direct Check In',
                'view_mode': 'form',
                'res_model': 'hotel.book.history',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {
                    'active_room_id': self.id,
                    'state': 'checked_in'
                }
            }
        
    def _search_nearest_booked_rooms(self):
        room_id = self._context.get('active_id')
        # look for the first room booking that is available or reserved
        room_booking = self.env['hotel.book.history'].search([
            ('room_ids', 'in', room_id),
            ('state', '=', 'booked'),
            ('check_in', '<=', fields.Date.today()),
            ('check_out', '>=', fields.Date.today())
        ], limit=1)
        return room_booking
    
    def _search_currently_occupied_rooms(self):
        room_id = self._context.get('active_id')
        # look for the first room booking that is available or reserved
        room_booking = self.env['hotel.book.history'].search([
            ('room_ids', 'in', room_id.id),
            ('state', '=', 'checked_in'),
            ('check_in', '<=', fields.Date.today()),
            ('check_out', '>=', fields.Date.today())
        ], limit=1)
        return room_booking
        