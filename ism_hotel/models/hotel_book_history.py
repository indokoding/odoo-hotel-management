from odoo import models, fields, api, _
from odoo.http import request

class HotelBookHistory(models.Model):
    _name = 'hotel.book.history'
    _description = 'Hotel Book History'
    
    name = fields.Char(string="Name", required=True, copy=False, readonly=True)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    room_ids = fields.Many2many('hotel.room', string="Room", required=True)
    history_line_ids = fields.One2many('hotel.book.history.line', 'book_history_id', string="History Line")
    check_in = fields.Date(string="Check In", required=True)
    check_out = fields.Date(string="Check Out", required=True)
    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    has_sale_order = fields.Boolean(string="Has Sale Order", compute='_compute_has_sale_order')
    state = fields.Selection([
        ('booked', 'Booked'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ], string="State", default='booked', required=True)
    
    @api.depends('sale_order_id')
    def _compute_has_sale_order(self):
        for record in self:
            record.has_sale_order = record.sale_order_id and True or False
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hotel.booking.number') or _('New')
        result = super(HotelBookHistory, self).create(vals)
        
        sale_order = self._create_sale_order(result)
        result.sale_order_id = sale_order.id
        
        # change state of room
        for room in result.room_ids:
            room.state = 'reserved'
            
        return result
    
    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'
            
            # change state of room
            for room in record.room_ids:
                room.state = 'available'
                
            # cancel sale order
            record.sale_order_id.action_cancel()
    
    def _create_sale_order(self, result):
        order_lines = []
        room_types = []
        room_type_dict_qty = {}
        room_type_dict_str_join = {}
        
        for room in result.room_ids:
            if room.room_type.name not in room_type_dict_qty:
                room_types.append(room.room_type)
                room_type_dict_qty[room.room_type.name] = 1
                room_type_dict_str_join[room.room_type.name] = [room.name]
            else:
                room_type_dict_qty[room.room_type.name] += 1
                room_type_dict_str_join[room.room_type.name].append(room.name)
                
        # join room name
        for room_type in room_types:
            if len(room_type_dict_str_join[room_type.name]) > 1:
                room_type_dict_str_join[room_type.name] = ', '.join(room_type_dict_str_join[room_type.name])
            else:
                room_type_dict_str_join[room_type.name] = room_type_dict_str_join[room_type.name][0]
                
        for room_type in room_types:
            order_lines.append((0, 0, {
                'product_template_id': room_type.id,
                'product_id': room_type.product_variant_ids[0].id,
                'name': room_type.name,
                'product_uom_qty': room_type_dict_qty[room_type.name],
                'price_unit': room_type.list_price,
            }))
            order_lines.append((0, 0, {
                'display_type': 'line_note',
                'name': room_type.name + ' (' + room_type_dict_str_join[room_type.name] + ')',
            }))
        
        return self.env['sale.order'].create({
            'partner_id': result.partner_id.id,
            'date_order': result.check_in,
            'order_line': order_lines,
        })
        