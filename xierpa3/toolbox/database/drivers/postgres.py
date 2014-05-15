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
#   postgres.py
#
#    /usr/local/pgsql/bin/postmaster -D /usr/local/pgsql/data
#
import psycopg2

class Postgres(object):

    def __init__(self, name, ip, port, user, password):
        self.name = name
        s = "dbname=%s user=%s password='%s' host=%s port=%s" % (name, user, password, ip, port)

        try:
            self.connection = psycopg2.connect(s)
            self.setAutocommit(True)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print e
#           print s
        #self.pg.execute("SET client_encoding to 'UNICODE'")
    
    def __repr__(self):
        return '[Postgres-psycopg2] %s' % self.name

    def setAutocommit(self,autocommit=True):
        # after psycopg2 2.4.2 we can do it this way
        #self.connection.autocommit = autocommit
    
        if autocommit:
            self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        else:
            self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)

    def startTransaction(self):
        self.setAutocommit(False)

    def commit(self):
        self.connection.commit()
        self.setAutocommit(True)
        
    def rollback(self):
        self.connection.rollback()
        self.setAutocommit(True)
        
    def query(self, query):
        self.cursor.execute(query)
                  
    def fetchone(self):
        return self.cursor.fetchone()

    def fetchmany(self):
        return self.cursor.fetchmany()

    def fetchall(self):
        return self.cursor.fetchall()

    def getQuery(self, query):
        try:
            self.cursor.execute(query)
            return self.fetchall()
        except:
            pass
