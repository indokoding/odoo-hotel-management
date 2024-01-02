from odoo import models, fields, api, _

class HotelBookHistoryLine(models.Model):
    _name = 'hotel.book.history.line'
    _description = 'Hotel Book History Line'
    
    name = fields.Char(string="Guest Name")
    book_history_id = fields.Many2one('hotel.book.history', string="Book History")
    room_id = fields.Many2one('hotel.room', string="Room")