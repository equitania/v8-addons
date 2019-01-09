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

from openerp import models, fields, api, _
from openerp.osv import osv
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as OE_DTFORMAT
from lxml import etree


class eq_sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('discount', 'price_unit', 'product_uom_qty', 'price_subtotal')
    def _compute_discount(self):
        """
        Berechnet den Rabattwert für eine Position
        :return:
        """

        # NOTE: Deactivated on 09.01.2019 because of Ticket 5280
        """        
        for record in self:
            # Ticket 4142: neue Berechnung für Rabatt: Preis * Menge - Betrag inkl. Rabatt
            if record.price_subtotal:
                record.discount_value = record.price_unit * record.product_uom_qty - record.price_subtotal
            else:
                # Falls Betrag noch nicht berchnet wurde, alte Logik nutzen
                # cur_obj = self.pool.get('res.currency')
                # full_price = record.price_unit * record.product_uom_qty
                # subtotal = cur_obj.round(cr, uid, cur, full_price * (1 - (order.eq_percent_discount / 100)))
                # record.discount_value = full_price - subtotal


                record.discount_value = record.discount / 100 * record.price_unit * record.product_uom_qty
        """
        for record in self:
            record.discount_value = record.discount / 100 * record.price_unit * record.product_uom_qty

    @api.depends('discount', 'discount_value')
    def _compute_discount_display(self):
        """
        Berechnet den Rabattwert der einzelnen Positionen in der Treeansicht des Auftragsformulars
        :return:
        """
        currency_symbol = self[0].order_id.company_id.currency_id.symbol
        if (self and self[0].order_id and self[0].order_id.pricelist_id):
            currency_symbol = self[0].order_id.pricelist_id.currency_id.symbol

        lang = self.env['res.users'].sudo().browse(self._uid).lang  # self._context['lang']
        rep_helper_obj = self.env['eq_report_helper']
        for record in self:
            discounted_txt = rep_helper_obj.get_price(record.discount, lang, 'Sale Price Report', False)
            discounted_value_txt = rep_helper_obj.get_price(record.discount_value, lang, 'Sale Price Report', False) + ' ' + currency_symbol

            record.discount_display_text = discounted_txt + " %\n (" + discounted_value_txt + ")"

    eq_optional = fields.Boolean(string="Optional")

    discount_value = fields.Float(compute='_compute_discount', string='Discount value', store=False, readonly=True)
    discount_display_text = fields.Char(compute='_compute_discount_display', string='Discount', store=False, readonly=True)

    @api.multi
    def remove_production(self):
        return True

    def create_order_line_del_message(self):
        message_vals = {
            'body': _('<div><b>Position Storniert</p></div><div>Product: ' + (self.product_id.name if self.product_id.name else self.name) + '\nMenge: ' + str(self.product_uom_qty)),
            'date': datetime.now(),
            'res_id': self.order_id.id,
            'record_name': self.order_id.name,
            'model': 'sale.order',
            'type': 'comment',
        }
        self.env['mail.message'].create(message_vals)

    @api.multi
    def unlink(self):
        # When a order line where an order is already done is removed, the apropriate stock move is canceled
        proc_obj = self.env['procurement.order']
        for rec in self:
            if rec.state in ['confirmed']:
                procurements = proc_obj.search([('sale_line_id', '=', rec.id), ('production_id', '=', False)])
                if any(proc.state in ('done') for proc in procurements):
                    raise osv.except_osv(_('Lieferung durchgeführt!'), _('Eine Teillieferung/Lieferung wurde für das Produkt "%s" mit der Menge "%s" bereits durchgeführt.') % (rec.product_id.name, rec.product_uom_qty))
                else:
                    rec.remove_production()
                    for proc in procurements:
                        proc.cancel()
                        move = self.env['stock.move'].search([('procurement_id', '=', proc.id)])
                        move.unlink()
                    rec.state = 'cancel'
                    rec.order_id.signal_workflow('ship_recreate')
            rec.create_order_line_del_message()
        return super(eq_sale_order_line, self).unlink()


class eq_sale_order(models.Model):
    _inherit = 'sale.order'

    _order = "date_order DESC"

    @api.model
    def default_get(self, fields_list):
        res = super(eq_sale_order, self).default_get(fields_list)
        config_parameter_obj = self.env['ir.config_parameter']

        validation_period_str = config_parameter_obj.get_param('offer.valid.duration') or '0'
        validation_period = float(validation_period_str)

        validity_period = timedelta(days=validation_period)

        validity_data = datetime.now() + validity_period
        res['validity_date'] = validity_data.strftime(OE_DTFORMAT)
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):

        ir_values_obj = self.env['ir.values']

        res = super(eq_sale_order, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)

        if not ir_values_obj.get_default('sale.order', 'default_search_only_company'):
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='partner_id']"):
                node.set('domain', "[('customer', '=', True)]")
            res['arch'] = etree.tostring(doc)

        return res

    eq_customer_ref = fields.Char(string="", related="partner_id.eq_customer_ref")

    def get_setting(self, cr, uid, settingName):
        """
            Get value of actual setting
            @cr:
            @uid:
            @settingName:
            @return:
        """
        result = self.pool.get('ir.config_parameter').get_param(cr, uid, settingName)
        if result == "":
            return None
        return result

    def get_refunds(self, cr, uid, ids):
        so = self.browse(cr, uid, ids, None)
        ids = self.pool('account.invoice').search(cr, uid, [('name', 'like', so.name), ('type', '=', 'out_refund')])

        return ids

    def action_view_invoice(self, cr, uid, ids, context=None):
        '''
        This function returns an action that display existing invoices of given sales order ids. It can either be a in a list or in a form view, if there is only one invoice to show.
        '''
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        result = mod_obj.get_object_reference(cr, uid, 'account', 'action_invoice_tree1')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        # compute the number of invoices to display
        inv_ids = []
        for so in self.browse(cr, uid, ids, context=context):
            inv_ids += [invoice.id for invoice in so.invoice_ids]
            inv_ids += so.get_refunds()

        # choose the view_mode accordingly
        if len(inv_ids) > 1:
            result['domain'] = "[('id','in',[" + ','.join(map(str, inv_ids)) + "])]"
        else:
            res = mod_obj.get_object_reference(cr, uid, 'account', 'invoice_form')
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = inv_ids and inv_ids[0] or False
        return result

    @api.v7
    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        """
            Override of default _prepare_invoice method. We'll set value from 2 new fields from settings (eq_head_text and eq_foo_text)
            @cr: cursor
            @uid: user id
            @order: current sale order
            @lines: lines of current sale order
            @context: context
            @return: dictionary with all values of actual sale order that will be saved during standard create of an invoice
        """
        result = super(eq_sale_order, self)._prepare_invoice(cr, uid, order, lines, context=context)
        eq_use_text_from_order = self.get_setting(cr, uid, "eq.use.text.from.order")  # sollen wir unser Text (eq_head_text) oder standard (head_text) verwenden ?
        if str(eq_use_text_from_order) == "False":  # ok, wir sollen den eq_text verwenden
            head = self.get_setting(cr, uid, "eq.head.text.invoice")
            if head is not None:
                result['eq_head_text'] = head

            foot = self.get_setting(cr, uid, "eq.foot.text.invoice")
            if foot is not None:
                result['comment'] = foot

        return result

    @api.cr_uid_ids_context
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = super(eq_sale_order, self)._amount_all(cr, uid, ids, field_name, arg, context=context)
        for order_id in res:
            val1 = 0
            val = 0
            order = self.browse(cr, uid, order_id, context=context)
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                if line.eq_optional:
                    val1 += line.price_subtotal
                    val += self._amount_line_tax(cr, uid, line, context=context)
            res[order.id]['amount_tax'] -= cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed'] -= cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
        return res

    @api.multi
    def action_button_confirm_optional(self):
        warning_msgs = False
        for line in self.order_line:
            if line.eq_optional:
                warning_msgs = True

        if warning_msgs:
            vals = {
                'eq_info_text': _("All the optional positions will be removed."),
                'eq_sale_id': self.id,
            }
            new_popup = self.env['eq_info_optional'].create(vals)
            view = self.env.ref('equitania.eq_info_optional_form_view')
            return {
                'name': _('Not enough stock !'),
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view.id,
                'res_model': 'eq_info_optional',
                'context': "{}",
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'res_id': new_popup.id,
            }
        else:
            return self.action_button_confirm()


class eq_info_optional(models.TransientModel):
    _name = 'eq_info_optional'

    eq_info_text = fields.Text()
    eq_sale_id = fields.Many2one('sale.order')

    @api.multi
    def action_done(self):
        for line in self.eq_sale_id.order_line:
            if line.eq_optional:
                line.unlink()
        self.eq_sale_id.action_button_confirm()
        return True