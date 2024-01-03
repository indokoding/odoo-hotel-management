from odoo import models, fields, api, _
import datetime

class CheckinRoomBooking(models.TransientModel):
    _name = 'checkin.room.booking'
    _description = 'Checkin Room Booking'
    
    @api.model
    def _get_default_name(self):
        room_booking = self._get_default_booking()
        return room_booking.name
    
    @api.model
    def _get_default_room_ids(self):
        room_booking = self._get_default_booking()
        if not room_booking:
            return self.env['hotel.room'].browse(self._context.get('active_id'))
        return room_booking.room_ids
        
    @api.model
    def _get_default_checkin(self):
        room_booking = self._get_default_booking()
        return room_booking.check_in
    
    @api.model
    def _get_default_checkout(self):
        room_booking = self._get_default_booking()
        return room_booking.check_out
    
    @api.model
    def _get_default_partner(self):
        room_booking = self._get_default_booking()
        return room_booking.partner_id
    
    name = fields.Char(string="Name", copy=False, readonly=True, default=_get_default_name)
    room_ids = fields.Many2many('hotel.room', string="Selected Room", required=True, default=_get_default_room_ids)
    check_in = fields.Date(string="Checkin Date", required=True, default=_get_default_checkin)
    check_out = fields.Date(string="Checkout Date", required=True, default=_get_default_checkout)
    partner_id = fields.Many2one('res.partner', string="Guest", required=True, default=_get_default_partner)
    
    def action_checkin(self):
        self.ensure_one()
        room_booking = self._get_default_booking()
        
        # if room booking exists update, if not create new
        if room_booking:
            room_booking.write({
                'state': 'checked_in',
                'check_in': self.check_in,
                'check_out': self.check_out,
                'room_ids': self.room_ids
            })
        else:
            room_booking = self.env['hotel.book.history'].create({
                'partner_id': self.partner_id.id,
                'room_ids': self.room_ids,
                'check_in': self.check_in,
                'check_out': self.check_out,
                'state': 'checked_in'
            })
        
        for room in self.room_ids:
            room.state = 'occupied'
            
        # sale.order to confirm
        room_booking.sale_order_id.action_confirm()
            
        return {
            'name': _('Room Booking'),
            'view_mode': 'form',
            'res_model': 'hotel.book.history',
            'res_id': room_booking.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
    
    def _get_default_booking(self):
        room_id = self.env['hotel.room'].browse(self._context.get('active_id'))
        # look for the first room booking that is available or reserved
        room_booking = self.env['hotel.book.history'].search([('room_ids', 'in', room_id.id), ('state', '=', 'booked')], limit=1)
        return room_booking
    
    @api.onchange('check_in')
    def onchange_check_in(self):
        if self.check_in:
            if not self.check_out or (self.check_out and self.check_out < self.check_in):
                self.check_out = self.check_in + datetime.timedelta(days=1)
                
    @api.onchange('check_out')
    def onchange_check_out(self):
        if self.check_out:
            if not self.check_in or (self.check_in and self.check_out < self.check_in):
                self.check_in = self.check_out - datetime.timedelta(days=1)