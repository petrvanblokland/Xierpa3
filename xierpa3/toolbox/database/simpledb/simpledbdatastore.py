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
#    simpledbdatastore.py
#
from xierpa3.toolbox.database.base.basedatastore import BaseDatastore
from xierpa3.toolbox.database.base.record import Record
from xierpa3.toolbox.database.simpledb.simpledbconnector import SimpleDBConnector
from xierpa3.toolbox.tools.dating import uniqueId

class SimpleDBDatastore(BaseDatastore):

    def __init__(self, name, models, accesskey, secretaccesskey, databases=None,):
        BaseDatastore.__init__(self, name, models, databases)
        name = self.getDatabaseName()
        self.connector = SdbConnector(name, accesskey, secretaccesskey)

    # ------------------------------------------------------------------------------------------------------------------
    #    G L O B A L S
    
    def createTable(self, table):
        pass
    
    def dropTable(self, table):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    #    R E C O R D

    def getUniqueId(self):
        u"""
        <doc>
        The <code>getUniqueId</code> method answers a unique id for a new record.
        </doc>
        """
        return uniqueId()

    def getRecord(self, table, id=None, data=None, readonly=True, forceinsert=False, nocache=False, fields=None, **args):
        u"""
        <doc>
        The <code>getRecord</code> method answers the instantiated <code>Record</code> object of this <attr>id</attr> if
        it exists. Make sure to convert <attr>id</attr> into a  real integer id, or else the cache may think a string id
        is different. Else create a new record with this data, store it in the cache, and answer it. id can be either
        None, int or string.<br/>
        If the record is already in cache, then still set the readonly flag from the <attr>readonly</attr>, otherwise
        cached records, that previously were used for reading only, will still not be writable.<br/>
        If the <attr>forceinsert</attr> attribute is set, then always insert the record. This is used when initializing
        a table from an application.<br/>
        </doc>
        """
        record = self.getCache(table, id)
        if not nocache and record is not None:
            record._setReadOnly(readonly)    # Take over the requested readonly flag
            return record

        # Record is not in cache of datastore. Create an instance.
        record = Record(self, table, id=id, readonly=readonly, data=data, forceinsert=forceinsert, fields=fields,
                                                                                                            **args)
        self.putCache(table, id, record)
        return record

    def deleteRecord(self, table, id=None, where=None):
        pass

    def rawQuery(self, query):
        u"""
        <doc>
        The <code>rawQuery</code> method executes the raw query. 
        """
        self._lastquery = query
        return SimpleDBDatastore.sdb.select(self.domain, query, 0)

    def read(self, table, id, fields):
        u"""
        <doc>
        The <code>read</code> method reads actual data from database when not done before.<br/>
        Make sure there is only one record result. Or else we have a non-existing id or there are multiples.<br/>
        <note>All fields of a record are used as plain names, so all other attributes have a preceding "_".</note>
        The field list <attr>fields</attr> attribute can be either a comma separated string of field names or a list of
        field names. The field list <attr>fields</attr> must be defined. For efficiency reasons we don’t want to use the
        global <code>'*'</code>, since too much data returns and the order of the answered tuple if data is not clear
        and needs to be sorted out.<br/>
        This is one method of the three basis operations of the datastore: <code>self.read(...)</code>,
        <code>self.write(...)</code> and <code>self.select(...)</code>.
        </doc>
        """
        if isinstance(fields, (tuple, list)):
            fields = '"' + '", "'.join(fields) + '"'

        q = u"""SELECT %s FROM  "%s" WHERE id = '%s'""" % (fields, table, id)
        result = self.getQuery(q)
        if not result:
            return None
        assert len(result) == 1, u'[Agent.read] Duplicate records in table "%s" with id "%s"' % (table, id)
        return list(result[0])

    def write(self, table, id, fields, forceinsert=False):
        u"""
        <doc>
        The <code>write</code> method of the datastore actually writes the record in the database. This is done here,
        in order to keep the <code>Record</code> and <code>Selection</code> classes absolutely generic. The datastore
        is dependent on the kind of database running on the server hardware. Writing of the record only takes place
        when it is changed AND when the record is writable AND there is any data to write (this record may already have
        been deleted). Do an insert or update depending on the value of <attr>id</attr>. Only write the fields which
        names are in the <attr>changedfields</attr> list.<br/>
        Fields that contain None are set as SQL <code>NULL</code>.<br/>
        This is one method of the three basis operations of the datastore: <code>self.read(...)</code>,
        <code>self.write(...)</code> and <code>self.select(...)</code>.
        <todo>to block the record between insert and getting max id value, since in theory another record can be made by
        another application.</todo>
        </doc>
        """
        self.connector.write(table, id, fields, forceinsert)

    def count(self, table, where=None):
        pass
    
    def exists(self, table, id=None, where='True'):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    #    S E L E C T I O N

    def getSelection(self, table, fields, astable=None, order=None, slice=None, start=None, readonly=True, where=None,
            distinct=None):
        pass
    
    def getSelectedRecord(self, table, fields, astable=None, mode=None, where=None, order=None, start=None,
        slice=None, readonly=True, initialized=False, query=None, distinct=None):
        pass
    
    def getSelectionSize(self, table, where=None):
        pass
