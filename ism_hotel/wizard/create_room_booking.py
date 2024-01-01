from odoo import api, fields, models, _

class CreateRroomBookingWizard(models.TransientModel):
    _name = "create.room.booking.wizard"
    _description = "Create Room Booking Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CreateReservationWizard, self).default_get(fields)
        if self._context.get('active_id'):
            res['partner_id'] = self._context.get('active_id')
        return res

    date_reservation = fields.Date(string='Date', required=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)