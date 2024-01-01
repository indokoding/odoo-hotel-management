from odoo import models, fields, api, _
from odoo.http import request

class HotelBookHistory(models.Model):
    _name = 'hotel.book.history'
    _description = 'Hotel Book History'
    
    name = fields.Char(string="Name", required=True, copy=False, readonly=True)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    room_ids = fields.Many2many('hotel.room', string="Room", required=True)
    check_in = fields.Date(string="Check In", required=True)
    check_out = fields.Date(string="Check Out", required=True)
    state = fields.Selection([
        ('booked', 'Booked'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ], string="State", default='booked', required=True)
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hotel.booking.number') or _('New')
        result = super(HotelBookHistory, self).create(vals)
        
        # change state of room
        for room in result.room_ids:
            room.state = 'reserved'
        
        # create new sale order
        order_lines = []
        room_types = []
        room_type_dict_qty = {}
        for room in result.room_ids:
            if room.room_type.name not in room_type_dict_qty:
                room_types.append(room.room_type)
                room_type_dict_qty[room.room_type.name] = 1
            else:
                room_type_dict_qty[room.room_type.name] += 1
                
        for room_type in room_types:
            order_lines.append((0, 0, {
                'product_template_id': room_type.id,
                'product_id': room_type.product_variant_ids[0].id,
                'name': room_type.name,
                'product_uom_qty': room_type_dict_qty[room_type.name],
                'price_unit': room_type.list_price,
            }))
        
        sale_order = self.env['sale.order'].create({
            'partner_id': result.partner_id.id,
            'date_order': result.check_in,
            'order_line': order_lines,
        })
        
        return result
    
    def create_room_booking(self):
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