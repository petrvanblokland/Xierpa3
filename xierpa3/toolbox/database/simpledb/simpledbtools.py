# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    simpledbtools.py
#
import boto

class SimpleDBTools:

    def postgres2sdb(self):
        u"""
        <doc>Auxiliary definition that converts a PostgresQL database to an AWS SDB database.</doc>
        """
        sdb = boto.connect_sdb(Config.ACCESSKEYID, Config.SECRETACCESSKEY)

        # Delete domain if it already exists.
        if sdb.lookup(self.DATABASE_NAME, True) != None:
            sdb.delete_domain(self.DATABASE_NAME)
            self.error('Deleted domain %s' % self.DATABASE_NAME)

        domain = sdb.create_domain(self.DATABASE_NAME)
        self.error('Creating new domain %s' % self.DATABASE_NAME)

        number_of_records = 10

        for table in self.getTableNames():
            self.error('table: ' + table)
            i = 0
            for record in self.getSelection(table):
                i += 1
                sdb_item = domain.new_item(record.id)
                sdb_item['table'] = table
                for field in record._getFields():
                    data = record[field]
                    if type(data) == str:
                        self.error('string')
                    elif type(data) == bool:
                        self.error('boolean')
                    elif type(data) == int:
                        self.error('integer')
                    elif type(data) == float:
                        self.error('float')
                    elif type(data) == type(None):
                        self.error('none')
                    elif type(data) == set:
                        self.error('set')
                    else:
                        self.error('some other type')
                        print type(data)

                    if type(data) == str:
                        if len(data) >= 1024:
                            data = data[:1024]
                        #data = urllib.urlencode(data)
                        self.error(data)

                    #sdb_item[field] = urllib.urlencode(data)
                #sdb_item.save()
                if i == number_of_records:
                    break
