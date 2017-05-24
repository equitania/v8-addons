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

from openerp.tools.translate import _
from openerp import api, fields, models
from openerp import SUPERUSER_ID


class eq_odoo_helper(models.TransientModel):
    _name = 'eq_odoo.helper'

    def create_odoo_log(self, name, func, path, level, message, create_log_entry = False):
        """
            Erstellt Logeintrag direkt im Odoo
            @cr: Kursor
            @message: Logeintrag mit allen Daten
        """
        if create_log_entry is False:
            return

        logger_vals = {
            'name': name,
            'func': func,
            'path': path,
            'line': "/",
            'type': 'server',
            'level': level,
            'message': message
        }
        logging_pool = self.pool.get('ir.logging')
        logging_pool.create(self._cr, SUPERUSER_ID, logger_vals)
        self._cr.commit()

    def encode_to_string(self, input_string):
        """
        Wandelt ein UTF-8 in String um
        :param input_string: UTF-8 Text
        :return: string
        """
        if input_string != False:
            result = input_string.encode(encoding = 'UTF-8', errors = 'strict')
            result = result.strip()
            return result
        return ""

    def get_param_value_as_bool(self, param_name):
        """
        Ermittelt den Parameterwert aus der Tabelle ir.config_parameter und wandelt das Ergebenis in Bool um
        :param param_name: Parameter, der in der Tabelle ir.config_parameter gespeichert ist
        :return: Parameterwert als Boolean
        """
        try:
            result = self.env['ir.config_parameter'].get_param(param_name)
            result = self.encode_to_string(result)
            if result == "True" or result == "true" or result == "1":
                return True
        except:
            return False

        return False
