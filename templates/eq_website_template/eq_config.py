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
import requests
from openerp.osv import osv
from openerp.addons.eq_web_search.models.es_helper import es_helper
from openerp.addons.eq_web_search.models.eq_odoo_helper import eq_odoo_helper

import logging
_logger = logging.getLogger(__name__)

"""
class eq_config(models.TransientModel):
    _name = 'eq.config'
    _inherit = 'res.config.settings'


    # Protokollierung aktivieren/deaktivieren
    eq_website_toolbox_active_log = fields.Boolean(string= "Activate protocol for eq_website_toolbox [eq_web_search]")

    #------------------------ LOGS ----------------------------
    @api.multi
    def get_default_eq_website_toolbox_active_log(self):
        res = self.env['ir.config_parameter'].get_param("eq.website.toolbox.active.log")
        if res == 'True':
            return {'eq_website_toolbox_active_log': True}
        return {'eq_website_toolbox_active_log': False}

    @api.multi
    def set_eq_eq_website_toolbox_active_log(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
            config_parameters.set_param("eq.website.toolbox.active.log", str(record.eq_website_toolbox_active_log), )
"""