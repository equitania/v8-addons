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

###19.07.2017 Workaround bezügl. Ticket #4569 => Es konnte nicht mehr in der "Erweiterten Suche" nach einem Datum (z.B. größer als) gefiltert werden
###Folglich wird bei den wichtigsten Modellen die search_read Methode nochmals implementiert, welches die beschriebene Problematik behoben hat.

class eq_sale_order_sr(models.Model):
    _inherit = 'sale.order'

    def search_read(self, cr, uid, domain=None, fields=None, offset=0, limit=None, order=None, context=None):
        """
        Performs a ``search()`` followed by a ``read()``.

        :param cr: database cursor
        :param user: current user id
        :param domain: Search domain, see ``args`` parameter in ``search()``. Defaults to an empty domain that will match all records.
        :param fields: List of fields to read, see ``fields`` parameter in ``read()``. Defaults to all fields.
        :param offset: Number of records to skip, see ``offset`` parameter in ``search()``. Defaults to 0.
        :param limit: Maximum number of records to return, see ``limit`` parameter in ``search()``. Defaults to no limit.
        :param order: Columns to sort result, see ``order`` parameter in ``search()``. Defaults to no sort.
        :param context: context arguments.
        :return: List of dictionaries containing the asked fields.
        :rtype: List of dictionaries.

        """


        record_ids = self.search(cr, uid, domain or [], offset=offset, limit=limit, order=order, context=context)
        if not record_ids:
            return []

        if fields and fields == ['id']:
            # shortcut read if we only want the ids
            return [{'id': id} for id in record_ids]

        # read() ignores active_test, but it would forward it to any downstream search call
        # (e.g. for x2m or function fields), and this is not the desired behavior, the flag
        # was presumably only meant for the main search().
        # TODO: Move this to read() directly?
        read_ctx = dict(context or {})
        read_ctx.pop('active_test', None)

        result = self.read(cr, uid, record_ids, fields, context=read_ctx)
        if len(result) <= 1:
            return result

        # reorder read
        index = dict((r['id'], r) for r in result)
        return [index[x] for x in record_ids if x in index]


class eq_stock_move_sr(models.Model):
    _inherit = 'stock.move'

    def search_read(self, cr, uid, domain=None, fields=None, offset=0, limit=None, order=None, context=None):
        """
        Performs a ``search()`` followed by a ``read()``.

        :param cr: database cursor
        :param user: current user id
        :param domain: Search domain, see ``args`` parameter in ``search()``. Defaults to an empty domain that will match all records.
        :param fields: List of fields to read, see ``fields`` parameter in ``read()``. Defaults to all fields.
        :param offset: Number of records to skip, see ``offset`` parameter in ``search()``. Defaults to 0.
        :param limit: Maximum number of records to return, see ``limit`` parameter in ``search()``. Defaults to no limit.
        :param order: Columns to sort result, see ``order`` parameter in ``search()``. Defaults to no sort.
        :param context: context arguments.
        :return: List of dictionaries containing the asked fields.
        :rtype: List of dictionaries.

        """


        record_ids = self.search(cr, uid, domain or [], offset=offset, limit=limit, order=order, context=context)
        if not record_ids:
            return []

        if fields and fields == ['id']:
            # shortcut read if we only want the ids
            return [{'id': id} for id in record_ids]

        # read() ignores active_test, but it would forward it to any downstream search call
        # (e.g. for x2m or function fields), and this is not the desired behavior, the flag
        # was presumably only meant for the main search().
        # TODO: Move this to read() directly?
        read_ctx = dict(context or {})
        read_ctx.pop('active_test', None)

        result = self.read(cr, uid, record_ids, fields, context=read_ctx)
        if len(result) <= 1:
            return result

        # reorder read
        index = dict((r['id'], r) for r in result)
        return [index[x] for x in record_ids if x in index]

class eq_stock_quant_sr(models.Model):
    _inherit = 'stock.quant'

    def search_read(self, cr, uid, domain=None, fields=None, offset=0, limit=None, order=None, context=None):
        """
        Performs a ``search()`` followed by a ``read()``.

        :param cr: database cursor
        :param user: current user id
        :param domain: Search domain, see ``args`` parameter in ``search()``. Defaults to an empty domain that will match all records.
        :param fields: List of fields to read, see ``fields`` parameter in ``read()``. Defaults to all fields.
        :param offset: Number of records to skip, see ``offset`` parameter in ``search()``. Defaults to 0.
        :param limit: Maximum number of records to return, see ``limit`` parameter in ``search()``. Defaults to no limit.
        :param order: Columns to sort result, see ``order`` parameter in ``search()``. Defaults to no sort.
        :param context: context arguments.
        :return: List of dictionaries containing the asked fields.
        :rtype: List of dictionaries.

        """


        record_ids = self.search(cr, uid, domain or [], offset=offset, limit=limit, order=order, context=context)
        if not record_ids:
            return []

        if fields and fields == ['id']:
            # shortcut read if we only want the ids
            return [{'id': id} for id in record_ids]

        # read() ignores active_test, but it would forward it to any downstream search call
        # (e.g. for x2m or function fields), and this is not the desired behavior, the flag
        # was presumably only meant for the main search().
        # TODO: Move this to read() directly?
        read_ctx = dict(context or {})
        read_ctx.pop('active_test', None)

        result = self.read(cr, uid, record_ids, fields, context=read_ctx)
        if len(result) <= 1:
            return result

        # reorder read
        index = dict((r['id'], r) for r in result)
        return [index[x] for x in record_ids if x in index]

class eq_purchase_order_sr(models.Model):
    _inherit = 'purchase.order'

    def search_read(self, cr, uid, domain=None, fields=None, offset=0, limit=None, order=None, context=None):
        """
        Performs a ``search()`` followed by a ``read()``.

        :param cr: database cursor
        :param user: current user id
        :param domain: Search domain, see ``args`` parameter in ``search()``. Defaults to an empty domain that will match all records.
        :param fields: List of fields to read, see ``fields`` parameter in ``read()``. Defaults to all fields.
        :param offset: Number of records to skip, see ``offset`` parameter in ``search()``. Defaults to 0.
        :param limit: Maximum number of records to return, see ``limit`` parameter in ``search()``. Defaults to no limit.
        :param order: Columns to sort result, see ``order`` parameter in ``search()``. Defaults to no sort.
        :param context: context arguments.
        :return: List of dictionaries containing the asked fields.
        :rtype: List of dictionaries.

        """


        record_ids = self.search(cr, uid, domain or [], offset=offset, limit=limit, order=order, context=context)
        if not record_ids:
            return []

        if fields and fields == ['id']:
            # shortcut read if we only want the ids
            return [{'id': id} for id in record_ids]

        # read() ignores active_test, but it would forward it to any downstream search call
        # (e.g. for x2m or function fields), and this is not the desired behavior, the flag
        # was presumably only meant for the main search().
        # TODO: Move this to read() directly?
        read_ctx = dict(context or {})
        read_ctx.pop('active_test', None)

        result = self.read(cr, uid, record_ids, fields, context=read_ctx)
        if len(result) <= 1:
            return result

        # reorder read
        index = dict((r['id'], r) for r in result)
        return [index[x] for x in record_ids if x in index]


class eq_stock_picking_sr(models.Model):
    _inherit = 'stock.picking'

    def search_read(self, cr, uid, domain=None, fields=None, offset=0, limit=None, order=None, context=None):
        """
        Performs a ``search()`` followed by a ``read()``.

        :param cr: database cursor
        :param user: current user id
        :param domain: Search domain, see ``args`` parameter in ``search()``. Defaults to an empty domain that will match all records.
        :param fields: List of fields to read, see ``fields`` parameter in ``read()``. Defaults to all fields.
        :param offset: Number of records to skip, see ``offset`` parameter in ``search()``. Defaults to 0.
        :param limit: Maximum number of records to return, see ``limit`` parameter in ``search()``. Defaults to no limit.
        :param order: Columns to sort result, see ``order`` parameter in ``search()``. Defaults to no sort.
        :param context: context arguments.
        :return: List of dictionaries containing the asked fields.
        :rtype: List of dictionaries.

        """


        record_ids = self.search(cr, uid, domain or [], offset=offset, limit=limit, order=order, context=context)
        if not record_ids:
            return []

        if fields and fields == ['id']:
            # shortcut read if we only want the ids
            return [{'id': id} for id in record_ids]

        # read() ignores active_test, but it would forward it to any downstream search call
        # (e.g. for x2m or function fields), and this is not the desired behavior, the flag
        # was presumably only meant for the main search().
        # TODO: Move this to read() directly?
        read_ctx = dict(context or {})
        read_ctx.pop('active_test', None)

        result = self.read(cr, uid, record_ids, fields, context=read_ctx)
        if len(result) <= 1:
            return result

        # reorder read
        index = dict((r['id'], r) for r in result)
        return [index[x] for x in record_ids if x in index]


class eq_account_invoice_sr(models.Model):
    _inherit = 'account.invoice'

    def search_read(self, cr, uid, domain=None, fields=None, offset=0, limit=None, order=None, context=None):
        """
        Performs a ``search()`` followed by a ``read()``.

        :param cr: database cursor
        :param user: current user id
        :param domain: Search domain, see ``args`` parameter in ``search()``. Defaults to an empty domain that will match all records.
        :param fields: List of fields to read, see ``fields`` parameter in ``read()``. Defaults to all fields.
        :param offset: Number of records to skip, see ``offset`` parameter in ``search()``. Defaults to 0.
        :param limit: Maximum number of records to return, see ``limit`` parameter in ``search()``. Defaults to no limit.
        :param order: Columns to sort result, see ``order`` parameter in ``search()``. Defaults to no sort.
        :param context: context arguments.
        :return: List of dictionaries containing the asked fields.
        :rtype: List of dictionaries.

        """


        record_ids = self.search(cr, uid, domain or [], offset=offset, limit=limit, order=order, context=context)
        if not record_ids:
            return []

        if fields and fields == ['id']:
            # shortcut read if we only want the ids
            return [{'id': id} for id in record_ids]

        # read() ignores active_test, but it would forward it to any downstream search call
        # (e.g. for x2m or function fields), and this is not the desired behavior, the flag
        # was presumably only meant for the main search().
        # TODO: Move this to read() directly?
        read_ctx = dict(context or {})
        read_ctx.pop('active_test', None)

        result = self.read(cr, uid, record_ids, fields, context=read_ctx)
        if len(result) <= 1:
            return result

        # reorder read
        index = dict((r['id'], r) for r in result)
        return [index[x] for x in record_ids if x in index]

# class eq_mrp_production_sr(models.Model):
#     _inherit = 'mrp.production'
#
#     def search_read(self, cr, uid, domain=None, fields=None, offset=0, limit=None, order=None, context=None):
#         """
#         Performs a ``search()`` followed by a ``read()``.
#
#         :param cr: database cursor
#         :param user: current user id
#         :param domain: Search domain, see ``args`` parameter in ``search()``. Defaults to an empty domain that will match all records.
#         :param fields: List of fields to read, see ``fields`` parameter in ``read()``. Defaults to all fields.
#         :param offset: Number of records to skip, see ``offset`` parameter in ``search()``. Defaults to 0.
#         :param limit: Maximum number of records to return, see ``limit`` parameter in ``search()``. Defaults to no limit.
#         :param order: Columns to sort result, see ``order`` parameter in ``search()``. Defaults to no sort.
#         :param context: context arguments.
#         :return: List of dictionaries containing the asked fields.
#         :rtype: List of dictionaries.
#
#         """
#
#
#         record_ids = self.search(cr, uid, domain or [], offset=offset, limit=limit, order=order, context=context)
#         if not record_ids:
#             return []
#
#         if fields and fields == ['id']:
#             # shortcut read if we only want the ids
#             return [{'id': id} for id in record_ids]
#
#         # read() ignores active_test, but it would forward it to any downstream search call
#         # (e.g. for x2m or function fields), and this is not the desired behavior, the flag
#         # was presumably only meant for the main search().
#         # TODO: Move this to read() directly?
#         read_ctx = dict(context or {})
#         read_ctx.pop('active_test', None)
#
#         result = self.read(cr, uid, record_ids, fields, context=read_ctx)
#         if len(result) <= 1:
#             return result
#
#         # reorder read
#         index = dict((r['id'], r) for r in result)
#         return [index[x] for x in record_ids if x in index]
#
#
# class eq_mrp_production_workcenter_line_sr(models.Model):
#     _inherit = 'mrp.production.workcenter.line'
#
#     def search_read(self, cr, uid, domain=None, fields=None, offset=0, limit=None, order=None, context=None):
#         """
#         Performs a ``search()`` followed by a ``read()``.
#
#         :param cr: database cursor
#         :param user: current user id
#         :param domain: Search domain, see ``args`` parameter in ``search()``. Defaults to an empty domain that will match all records.
#         :param fields: List of fields to read, see ``fields`` parameter in ``read()``. Defaults to all fields.
#         :param offset: Number of records to skip, see ``offset`` parameter in ``search()``. Defaults to 0.
#         :param limit: Maximum number of records to return, see ``limit`` parameter in ``search()``. Defaults to no limit.
#         :param order: Columns to sort result, see ``order`` parameter in ``search()``. Defaults to no sort.
#         :param context: context arguments.
#         :return: List of dictionaries containing the asked fields.
#         :rtype: List of dictionaries.
#
#         """
#
#
#         record_ids = self.search(cr, uid, domain or [], offset=offset, limit=limit, order=order, context=context)
#         if not record_ids:
#             return []
#
#         if fields and fields == ['id']:
#             # shortcut read if we only want the ids
#             return [{'id': id} for id in record_ids]
#
#         # read() ignores active_test, but it would forward it to any downstream search call
#         # (e.g. for x2m or function fields), and this is not the desired behavior, the flag
#         # was presumably only meant for the main search().
#         # TODO: Move this to read() directly?
#         read_ctx = dict(context or {})
#         read_ctx.pop('active_test', None)
#
#         result = self.read(cr, uid, record_ids, fields, context=read_ctx)
#         if len(result) <= 1:
#             return result
#
#         # reorder read
#         index = dict((r['id'], r) for r in result)
#         return [index[x] for x in record_ids if x in index]


class eq_report_stock_lines_date_sr(models.Model):
    _inherit = 'report.stock.lines.date'

    def search_read(self, cr, uid, domain=None, fields=None, offset=0, limit=None, order=None, context=None):
        """
        Performs a ``search()`` followed by a ``read()``.

        :param cr: database cursor
        :param user: current user id
        :param domain: Search domain, see ``args`` parameter in ``search()``. Defaults to an empty domain that will match all records.
        :param fields: List of fields to read, see ``fields`` parameter in ``read()``. Defaults to all fields.
        :param offset: Number of records to skip, see ``offset`` parameter in ``search()``. Defaults to 0.
        :param limit: Maximum number of records to return, see ``limit`` parameter in ``search()``. Defaults to no limit.
        :param order: Columns to sort result, see ``order`` parameter in ``search()``. Defaults to no sort.
        :param context: context arguments.
        :return: List of dictionaries containing the asked fields.
        :rtype: List of dictionaries.

        """


        record_ids = self.search(cr, uid, domain or [], offset=offset, limit=limit, order=order, context=context)
        if not record_ids:
            return []

        if fields and fields == ['id']:
            # shortcut read if we only want the ids
            return [{'id': id} for id in record_ids]

        # read() ignores active_test, but it would forward it to any downstream search call
        # (e.g. for x2m or function fields), and this is not the desired behavior, the flag
        # was presumably only meant for the main search().
        # TODO: Move this to read() directly?
        read_ctx = dict(context or {})
        read_ctx.pop('active_test', None)

        result = self.read(cr, uid, record_ids, fields, context=read_ctx)
        if len(result) <= 1:
            return result

        # reorder read
        index = dict((r['id'], r) for r in result)
        return [index[x] for x in record_ids if x in index]

