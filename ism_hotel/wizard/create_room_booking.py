from odoo import api, fields, models, _

import datetime
class CreateRoomBookingWizard(models.TransientModel):
    _name = "create.room.booking.wizard"
    _description = "Create Room Booking Wizard"

    @api.model
    def default_get_room(self):
        room_id = self.env['hotel.room'].browse(self._context.get('active_id'))
        print(room_id)
        return room_id    

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    check_in = fields.Date(string="Check In", required=True)
    check_out = fields.Date(string="Check Out", required=True)
    duration = fields.Integer(string="Duration", compute='_compute_duration')
    room_ids = fields.Many2many('hotel.room', string="Room", required=True, default=default_get_room)
    
    def action_create_room_booking(self):
        self.ensure_one()
        room_booking = self.env['hotel.book.history'].create({
            'partner_id': self.partner_id.id,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'room_ids': self.room_ids
        })
        return {
            'name': _('Room Booking'),
            'view_mode': 'form',
            'res_model': 'hotel.book.history',
            'res_id': room_booking.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        
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
                
    @api.depends('check_in', 'check_out')
    def _compute_duration(self):
        for record in self:
            if record.check_in and record.check_out:
                record.duration = (record.check_out - record.check_in).days
            else:
                record.duration = 0