# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
# New API, Remove Old API import if the New API is used. Otherwise you'll get an import error.
from openerp import models, fields, api, _


class eq_list_print_wiz(models.Model):
    _name = 'eq_list.print.wiz'

    @api.multi
    def print_list(self):
        self._cr.execute('delete from eq_buffer_order_line_list where create_uid = %s and write_uid = %s', (self._uid,self._uid))

        list_pool = self.env['eq_open_sale_order_line']
        selected_ids = list_pool.browse(self.env.context['active_ids'])
        for item in selected_ids:

            vals = {
                'eq_order_id': item.eq_order_id.id,
                'eq_client_order_ref': item.eq_client_order_ref,
                'eq_customer_no': item.eq_customer_no,
                'eq_customer': item.eq_customer.id,
                'eq_delivery_date': item.eq_delivery_date,
                'eq_pos': item.eq_pos,
                'eq_quantity': item.eq_quantity,
                'eq_quantity_left': item.eq_quantity_left,
                'eq_product_no': item.eq_product_no.id,
                'eq_drawing_no': item.eq_drawing_no,
            }

            self.env['eq_buffer_order_line_list'].create(vals)



        search_result = self.env['eq_buffer_order_line_list'].search([])[0]

        return self.env['report'].get_action(search_result,'equitania.report_open_sale_order_line')

class eq_list_transient_model(models.Model):
    _name = 'eq_buffer_order_line_list'

    eq_order_id = fields.Many2one('sale.order', string="Sale Order")
    eq_client_order_ref = fields.Char(string="Client Order Reference")
    eq_customer_no = fields.Char(size=64, string="Customer No")
    eq_customer = fields.Many2one('res.partner', string="Customer")
    eq_delivery_date = fields.Date(string="Delivery date")
    eq_pos = fields.Integer(string="Seq")
    eq_quantity = fields.Integer(string="Quantity")
    eq_quantity_left = fields.Integer(string="Quantity left")
    eq_product_no = fields.Many2one('product.product', string="Product number")
    eq_drawing_no = fields.Char(size=100, string="Drawing number")
