#!/usr/bin/python
# -*- coding: UTF-8 -*-
##############################################################################
#
#    Python Script for Odoo, Open Source Management Solution
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
import xmlrpclib
import csv
import sqlite3 as lite

import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# aktiviert / deaktiviert DEBUG Mode - bitte vor dem Release immer auf FALSE setzen, damit wir kein Prints beim Kunden in der Konsole ausgeben
USE_DEBUG = False

def log(*args):
    """
        Kleine Hilfsfunktion, die wir als Logger in der Konsole verwenden
    """
    if USE_DEBUG:
        print '#>', args

        """
        for a in args:
            print '#>', a
        """

username = "username"
pwd = "pwd"
dbname = "dbname"
baseurl = "http://localhost:8069"
password_for_sql_exec_module = "********"

i = 1  # Zaehlvariable

sock_common = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/common",allow_none=True)

uid = sock_common.login(dbname, username, pwd)

sock = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/object",allow_none=True)

con = lite.connect('set_custom_translation.db')
# Ansteuerung der Felder per Namen
con.row_factory = lite.Row

with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM custom_translation;")
    rows = cur.fetchall()
    for row in rows:
        model = row['name']
        english_translation = row['source']
        #english_translation = english_translation.strip(' ')
        german_translation = row['translation']
        module = row['module']
        lang = row['language']
        type = row['type']
        md5 = row['source_md5']
        value = {'value': german_translation}

        # if english_translation == None:
        #     english_translation == ''
        # if german_translation == None:
        #     german_translation == ''
        # if module == None:
        #     module = ''
        # if model == None:
        #     model = ''
        # if md5 == None:
        #     md5 = ''
        # if type == None:
        #     type = ''
        # if lang == None:
        #     lang = ''

        #german_translation = replace_german_umlaute(german_translation)
        translation_ids = sock.execute(dbname, uid, pwd, 'ir.translation', 'search', [('name', '=', model),('src','=', english_translation),('module','=',module),('lang','=', lang),('type','=',type)])
        if translation_ids:
            for translation_id in translation_ids:
                if translation_id:
                    new_translation_id = sock.execute(dbname, uid, pwd, 'ir.translation', 'write', translation_id, value)
                    log( str(i) + " Model: ", model)
                    log( str(i) + " ID: ", str(translation_id))
                    log( str(i) + " Englischer Wert: ", english_translation)
                    log( str(i) + " Deutscher Wert: ", german_translation)
                    log("----------------------")
        else:
            statement = "Select id From ir_translation where name = '%s' and module = '%s' and md5(src)='%s'" % (model,module,md5)
            result = sock.execute(dbname, uid, pwd, 'eq_sql_exec', 'execute_sql',password_for_sql_exec_module,statement)
            if result == []:
                log("SQLite3-ID:" + str(row['id']) + " Kein Datensatz zu Ihren Daten gefunden")
                log(str(i) + " Englischer Wert: ", english_translation)
                log("----------------------")
            else:
                result = result[0]
                new_translation_id = sock.execute(dbname, uid, pwd, 'ir.translation', 'write', result[0], value)
                log(str(i) + " Model: ", model)
                log(str(i) + " ID: ", str(result[0]))
                log(str(i) + " Englischer Wert: ", english_translation)
                log(str(i) + " Deutscher Wert: ", german_translation)
                log("----------------------")


        i = i + 1

print 'Fertig!'
