from odoo import api, fields, models, _

class CreateRoomBookingWizard(models.TransientModel):
    _name = "create.room.booking.wizard"
    _description = "Create Room Booking Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CreateRoomBookingWizard, self).default_get(fields)
        if self._context.get('active_id'):
            res['partner_id'] = self._context.get('active_id')
        return res

    date_reservation = fields.Date(string='Date', required=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    check_in = fields.Date(string="Check In", required=True)
    check_out = fields.Date(string="Check Out", required=True)
    room_ids = fields.Many2many('hotel.room', string="Room", required=True)
    
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