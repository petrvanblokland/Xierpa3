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
#   sqladapter.py
#
from xierpa3.adapters.adapter import Adapter
#from xierpa3.toolbox.database.sql.sqldatastore import SqlDatastore
#from xierpa3.toolbox.database.base.defaultmodels import Item
#from xierpa3.toolbox.database.base.selector import Selector

class Selector():
    #    @@@ Under development
    pass

class SqlDatastore():
    #    @@@ Under development
    pass

class SQLAdapter(Adapter):

    #    @@@ Under development

    SQL_NOTDELETED = 'deleted is not TRUE'

    def __init__(self, database_name, model=None):
        Adapter.__init__(self)
        self._db = self.openDatabase(database_name, model)

    def getModel(self):
        u"""
        Model of the database for Python representation and operation of data set. By default represent Item table only.
        """
        #return {'item': Item}

    def openDatabase(self, database_name, model):
        return SqlDatastore(database_name, model)

    def getRecord(self, table='item', id=None, readonly=True, data=None, fields=None, **args):
        u"""
        The <code>getRecord</code> method answers the result of <code>self._db.getRecord</code>. If <attr>id</attr> is
        not defined, then create a new record, using the optional <attr>args</attr> as values to initialize. If the record
        cannot be found, then answer an instance if <code>NoneRecord</code>.
        """
        return self._db.getRecord(table=table, id=id, readonly=readonly,
                                  fields=fields or self._db.getFieldNames(table), data=data, **args)

    def getSelection(self, table=None, selector=None, where=None, order=None, slice=None, start=None,
            parentid=None, readonly=True, query=None, fields=None, deleted=False, andor='AND',
            selectall=False, *args, **kwargs):
        u"""
        The <code>getSelection</code> method is a front for <code>self._db.getSelection()</code>. The difference is that
        it allows three ways to defined the selection clause: <attr>**args</attr> is the dictionary of additional
        attributes that will be composed into an AND clause <attr>where</attr>, or the <attr>selector</attr> instance or
        the raw <attr>where</attr>. If one of these attributes is defined, then the value of the preceding ones are
        ignored.<br/>
        """
        if not query:
            table = table or 'item'
            if kwargs:
                selector = Selector(kwargs, andor=andor)

        if not deleted:
            if not selector and selectall:
                selector = Selector()
            if selector:
                selector = self.addNotDeleted(table, selector)

        if selector:
            where = selector.getClause()

        if self._db is None:
            return self.getNoneRecord(table)

        if not fields:
            fields = self._db.getFieldNames(table)

        return self._db.getSelection(table=table, fields=fields, where=where,
            order=order, slice=slice, start=start, readonly=readonly, query=query)

    def getEmptySelection(self, table='item', fields=None, **args):
        if not fields:
            fields = self._db.getFieldNames(table)
        return self._db.getEmptySelection(table=table, fields=fields, **args)

if __name__ == "__main__":
    pass
