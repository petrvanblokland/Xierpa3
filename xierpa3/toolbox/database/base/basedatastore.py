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
#     datastore.py
#
#     Partly based on http://code.google.com/appengine/docs/python/datastore/
#
from noneselection import NoneSelection
from nonerecord import NoneRecord
from recordcache import RecordCache

class BaseDatastore(object):
    u"""
    <doc>
    The abstract <code>BaseDatastore</code> class as defined by <code>xierpad.db.basedatastore</code>
    implements the generic behavior of all types of datastores.
    </doc>
    """
    # Storage of cached records. Initialized also by Datastore.clearCache()
    CACHE = RecordCache()
    ENCRYPTION_KEYS = {}

    def __init__(self, name, models, databases=None):
        u"""
        <doc>
        The <code>__init__</code> constructor creates a new <code>ModelDatastore</code> instance. The <attr>name</attr>
        attribute is the name of the database to connect to. The <attr>models</attr> attribute holds a dictionary with
        table name and Model instances. The optional <attr>databases</attr> dictionary of descriptors must be defined if
        the application does not run as server but as stand-alone application.
        </doc>
        """
        self.name = name
        self.models = models
        self.initialize(databases)

    def __repr__(self):
        u"""
        <doc>
        The <code>__repr__</code> method shows that datastore by its name.
        </doc>
        """
        return '[%s name="%s"]' % (self.__class__.__name__, self.getDatabaseName())

    def initialize(self, databases):
        u"""
        <doc>
        The <code>initialize</code> method does initialize the attributes of the datastore. The type of attribute
        depends on the type of datastore. Used if a datastore needs one-time initialization. This method needs to be
        redefined by the inheriting datastore class. The default behavior is to do nothing.<br/>
        The <attr>database</attr> dictionary of descriptors is used when the application is not a server, but running as
        stand-alone.
        </doc>
        """
        pass

    def setEncryptionKey(self, field, key):
        self.ENCRYPTION_KEYS[field] = key

    def getEncryptionKeys(self):
        return self.ENCRYPTION_KEYS


    def getDatabaseName(self):
        u"""
        <doc>
        The <code>getDatabaseName</code> method answers the name of the database or datastore.
        </doc>
        """
        return self.name

    def getRecordTable(self, record):
        u"""
        <doc>
        The <code>getRecordTable</code> method answers the name of the model of <attr>record</attr> in the context of
        the current database.
        </doc>
        """
        table = record._getTable()
        if table in self.getModels().keys():
            return table
        return None

    def newRecord(self, table, id=None, selector=None, **args):
        u"""
        <doc>
        The <code>newRecord</code> method answers the a new record with empty <attr>id</attr> and
        <code>self.FIELD_READONLY</code> set to <code>False</code>.
        </doc>
        """
        return self.getRecord(table, id=None, readonly=False, inherit=False, forceinsert=True, **args)

    def duplicateRecord(self, table, id=None):
        u"""
        <doc>
        Get record with the id in the <attr>id</attr> attribute and duplicate it in the database. Answer a copy of the
        record, with cleared id field.
        </doc>
        """
        record = self.getRecord(table, id)
        if not record:
            return None
        return record._copy()

    def getModels(self):
        u"""
        <doc>
        The <code>getModels</code> method answers the <code>self.models</code> dictionary of the modeled datastore.
        </doc>
        """
        return self.models

    def getModel(self, table):
        u"""
        <doc>
        The <code>getModel</code> method answers the <code>self.models[table]</code> model of the modeled datastore.
        </doc>
        """
        return self.getModels().get(table)

    def getFieldNames(self, table):
        u"""
        <doc>
        The <code>getFieldNames</code> method answers the list of fields for <attr>table</attr> as defined in
        <code>self.getFieldNames(table)</code>
        </doc>        
        """
        return self.getModel(table)._getFieldNames()

    def tableHasField(self, table, field):
        u"""
        <doc>
        The <code>tableHasField</code> method answers the boolean flag id the <attr>table</attr> has a field named
        <attr>field</attr>. 
        </doc>
        """
        return field in self.getFieldNames(table)

    def getTableNames(self):
        u"""
        <doc>
        The <code>getTableNames</code> method answers an unordered list with table names.
        </doc>
        """
        return self.getModels().keys()

    def fields2Update(self, model, fields, allowid=False):
        u"""
        <doc>
        The <code>fields2Update</code> method converts the fields dictionary of <code>Field</code> instances to the
        value part of an update query. If the changedfields attribute is omitted or empty, then use all map keys.
        </doc>
        """
        t = []
        #@@@ Remove? id = fields['id']
        for field, value in fields.items():
            if field == 'id' and not allowid: # Never change id value
                continue
            t.append(model[field].value2SqlUpdate(field, value, key=self.ENCRYPTION_KEYS.get(field)))
        return ', '.join(t)

    def fields2Insert(self, model, fields, allowid=False):
        u"""
        <doc>
        The <code>map2insert</code> method converts the mapping dictionary to the value part of an insert query. If the
        changedfields attribute is omitted or empty, then use all map keys.
        </doc>
        """
        k = []
        v = []

        for field, value in fields.items():
            if field == 'id' and not allowid: # Never change id value
                continue
            k.append(field)
            v.append(model[field].value2SqlInsert(field, value, key=self.ENCRYPTION_KEYS.get(field)))
        return u'("' + u'", "'.join(k) + u'") VALUES (' + u', '.join(v) + u')'

    # ---------------------------------------------------------------------------------------------------------
    #     N O N E  S T U F F

    def getNoneSelection(self, table):
        u"""
        <doc>
        The <code>getNoneSelection</code> method answers a <code>NoneSelection</code> instance.
        </doc>
        """
        return NoneSelection(self, table)

    def getNoneRecord(self, table):
        u"""
        <doc>
        The <code>getNoneRecord</code> method answers an initialized <code>NoneRecord</code> instance.
        </doc>
        """
        return NoneRecord(self, table)

    # ---------------------------------------------------------------------------------------------------------
    #     C A C H I N G

    def getRecordCache(self):
        u"""
        <doc>
        The <code>getRecordCache</code> method answers the global <code>RecordCache</code> instance that contains all
        cached records.
        </doc>
        """
        # FIXME: missing code?
        pass

    def getCache(self, table, id):
        u"""
        <doc>
        The <code>getChache</code> method tries to get a record for the current database from the cache of
        <attr>table</attr> for record id <attr>id</attr>.
        </doc>
        """
        return self.CACHE.get(self.name, table, id)

    def putCache(self, table, id, record):
        u"""
        <doc>
        The <code>putCache</code> method tries to put a record for the current database in the cache of
        <attr>table</attr> for record id <attr>id</attr>.
        </doc>
        """
        self.CACHE.put(self.name, table, id, record)

    def deleteCache(self, table, id):
        u"""
        <doc>
        Delete all records from the cache (thus making them save themselves if changed and if there is not other
        reference to any of them).
        </doc>
        """
        self.CACHE.delete(self.name, table, id)

    @classmethod
    def clearCache(cls):
        u"""
        <doc>
        The <code>clearCache</code> method clears the cache of this datastore.
        </doc>
        """
        cls.CACHE = RecordCache()

    # ---------------------------------------------------------------------------------------------------------
    #     Q U E R I E S

    def startTransaction(self):
        self.cursor.setAutocommit(False)

    def commit(self):
        self.cursor.commit()

    def rollback(self):
        self.cursor.rollback()


    def rawQuery(self, query):
        u"""
        <doc>
        The <code>rawQuery</code> method executes the raw query. 
        """
        self._lastquery = query
        self.cursor.query(query.encode('utf-8'))

    def getQuery(self, query):
        u"""
        <doc>
        The <code>getQuery</code> does execute <attr>query</attr> and then answers the result. Transform the unicode
        query to UTF-8 before calling the database driver. The last query executed can be retrieved with
        <code>db.getLastQuery()</code>. Note that executing the raw <attr>query</attr> answers a list of values, not
        <code>Record</code> or <code>Selection</code> instances. Also no caching is performed on the result of the
        query.
        </doc>
        """
        self.rawQuery(query)
        return self.cursor.fetchall()

    def query(self, query):
        u"""
        <doc>
        The <code>query</code> executes the <attr>query</attr> attribute. Transform the unicode query to UTF-8 before
        calling the database driver. The last query executed can be retrieved with <code>db.getLastQuery()</code>.
        Note that executing the raw <attr>query</attr> answers a list of values, not <code>Record</code> or
        <code>Selection</code> instances. Also, no caching is performed on the result of the query.
        </doc>
        """
        self.rawQuery(query)

    def getLastQuery(self):
        u"""
        <doc>
        The <code>getLastQuery</code> method answers the last executed query.
        </doc>
        """
        return self._lastquery
