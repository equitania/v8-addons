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

import unittest
import openerp.tests.common as common


class test_res_partner(common.TransactionCase):
    """
    Unittests für unsere Erweiterung der Klasse res_partner
    """

    @classmethod
    def setUpClass(cls):
        print "-- EQ-UNITTESTS - test_res_partner - START ---"

    @classmethod
    def tearDownClass(cls):
        print "-- EQ-UNITTESTS - test_res_partner - END ---"

    def test_function_get_one(self):
        # Test der Funktion function_get_one()
        record = self.env['res.partner']
        result = record.function_get_one()
        self.assertEqual(result, 1)                                                             # stimmt Ergebnis ?

    @unittest.skip("SKIPPING THIS TEST")
    def test_function_two_test_fail(self):
        # Test der Funktion function_two(), die einen Wert 2 zurückliefern soll aber in diesem Fall wollen wir einen FAIL erreichen
        record = self.env['res.partner']
        result = record.function_get_one()
        self.assertEqual(result, 9, "Wrong result from function_two()")  # hier wollen wir mit Absicht einen FAIL erreichen