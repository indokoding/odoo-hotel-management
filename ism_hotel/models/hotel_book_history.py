from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import datetime

class HotelBookHistory(models.Model):
    _name = 'hotel.book.history'
    _description = 'Hotel Book History'
    
    @api.model
    def default_get_room(self):
        room_id = self.env['hotel.room'].browse(self._context.get('active_room_id'))
        return room_id    
    
    name = fields.Char(string="Name", required=True, default="New Booking", copy=False, readonly=True)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    room_ids = fields.Many2many('hotel.room', string="Room", required=True, default=default_get_room)
    history_line_ids = fields.One2many('hotel.book.history.line', 'book_history_id', string="History Line")
    check_in = fields.Date(string="Check In", required=True)
    check_out = fields.Date(string="Check Out", required=True)
    duration = fields.Integer(string="Duration", compute='_compute_duration')
    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    has_sale_order = fields.Boolean(string="Has Sale Order", default=False, compute='_compute_has_sale_order')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('booked', 'Booked'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ], string="State", default='draft', required=True)

    @api.depends('sale_order_id')
    def _compute_has_sale_order(self):
        for record in self:
            record.has_sale_order = record.sale_order_id and True or False
                
    @api.depends('check_in', 'check_out')
    def _compute_duration(self):
        for record in self:
            if record.check_in and record.check_out:
                record.duration = (record.check_out - record.check_in).days
            else:
                record.duration = 0
    
    @api.model
    def create(self, vals):
        if vals.get('check_in') and vals.get('check_out'):
            if vals.get('check_in') > vals.get('check_out'):
                raise ValidationError(_("Check In date must be less than Check Out date"))
        
        vals['state'] = 'booked'
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hotel.booking.number') or _('New')
        result = super(HotelBookHistory, self).create(vals)
        
        sale_order = self._create_sale_order(result)
        result.sale_order_id = sale_order.id
        
        # get context state if so set state immediately
        if self._context.get('state'):
            result.state = self._context.get('state')
        
        # change state of room
        # for room in result.room_ids:
        #     room.state = 'reserved'
        
        return result
    
    @api.onchange('check_in')
    def onchange_check_in(self):
        self._auto_assign_check_out()
        self._check_availability()
                
    @api.onchange('check_out')
    def onchange_check_out(self):
        self._auto_assign_check_in()
        self._check_availability()
        
    def action_book(self):
        for record in self:
            record.state = 'booked'
            
            # change state of room
            for room in record.room_ids:
                room.state = 'reserved'
    
    def action_checkin(self):
        for record in self:
            record.state = 'checked_in'
            
            # change state of room
            for room in record.room_ids:
                room.state = 'occupied'
                
            # sale.order to confirm
            if record.sale_order_id.state == 'draft':
                record.sale_order_id.action_confirm()
            
    def action_checkout(self):
        for record in self:
            record.state = 'checked_out'
            
            # change state of room
            for room in record.room_ids:
                room.state = 'available'
    
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
                
    def _auto_assign_check_in(self):
        if self.check_out:
            if not self.check_in or (self.check_in and self.check_out < self.check_in):
                self.check_in = self.check_out - datetime.timedelta(days=1)
                
    def _auto_assign_check_out(self):
        if self.check_in:
            if not self.check_out or (self.check_out and self.check_out < self.check_in):
                self.check_out = self.check_in + datetime.timedelta(days=1)
                
    def _check_availability(self):
        pass
        # self.ensure_one()
        # room_booking = self.env['hotel.book.history'].search([('room_ids', 'in', self.room_ids.id), ('state', '=', 'booked'), ('check_in', '<=', self.check_in), ('check_out', '>=', self.check_out)], limit=1)
        # print( bool(room_booking) )
        # if room_booking:
        #     raise ValidationError(_('Room is not available for the selected dates.'))
        # else:
        #     return True
        
    def action_view_sale_order(self):
        self.ensure_one()
        return {
            'name': _('Sale Order'),
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': self.sale_order_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }