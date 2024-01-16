from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import datetime

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    duration = fields.Integer(string="Duration", required=True, default=1)
    
    # override _compute_amount
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'duration')
    def _compute_amount(self):
        for line in self:
            tax_base_line_dict = line._convert_to_tax_base_line_dict()
            
            # print('before compute taxes : ', tax_base_line_dict)
            tax_base_line_dict['quantity'] *= line.duration
            tax_results = self.env['account.tax']._compute_taxes([tax_base_line_dict])
            # print('after compute taxes : ', tax_results)
            
            totals = list(tax_results['totals'].values())[0]
            amount_untaxed = totals['amount_untaxed']
            amount_tax = totals['amount_tax']

            line.update({
                'price_subtotal': amount_untaxed,
                'price_tax': amount_tax,
                'price_total': amount_untaxed + amount_tax,
            })
            