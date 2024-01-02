from odoo import models, fields, api, _

class CheckinRoomBooking(models.TransientModel):
    _name = 'checkin.room.booking'
    _description = 'Checkin Room Booking'
    
    def _get_default_booking(self):
        room_id = self.env['hotel.room'].browse(self._context.get('active_id'))
        # look for the first room booking that is available or reserved
        room_booking = self.env['hotel.book.history'].search([('room_id', '=', room_id.id), ('state', 'in', ['available', 'reserved'])], limit=1)
        return room_booking.id
    
    room_booking_id = fields.Many2one('hotel.book.history', string="Room Booking", default=_get_default_booking)
    room_id = fields.Many2one('hotel.room', string="Room", required=True)
    checkin_date = fields.Date(string="Checkin Date", required=True)
    checkout_date = fields.Date(string="Checkout Date", required=True)
    partner_id = fields.Many2one('res.partner', string="Guest", required=True)