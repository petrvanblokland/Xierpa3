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
#    datastore.py
#
from xierpa3.constants.config.config import Config

from xierpalib.database.drivers.postgres import Postgres
from xierpalib.constants.constants import Constants
from xierpalib.database.base.basedatastore import BaseDatastore
from xierpalib.database.base.record import Record
from xierpalib.database.base.selection import Selection


class SqlDatastore(BaseDatastore):
    u"""
    <doc>
    The <code>XierpaDatastore</code> class implements the Xierpa database access, based on <code>Record</code> and
    <code>Selection</code> instances.<br/>
    A <code>XierpaDatastore</code> instance is the core container of a database connection. It not only knows set of
    models and modelfields, but also does selection, caching, etc.<br/>
    The record caching is through weak references only, so records get called by <code>__del__</code> when deleted. They
    will ask the datastore to write them to the database if changed.

    What happens:
    
    - 1    Single record, unknown id 
            db.getRecord()
            db.getRecord(data)

        - Create an instance of Record, with id = None, _data may be empty
        - Don't cache the record
        - When attribute names do not start with "_" set/get the value from self._data
        - Setting an attribute is only allowed when the record has 'rw' mode and set:
            record._changed = True
        - Upon _put() the record will perform an SQL insert, get an id and become (2) type
            db.putrecord(record)
        - Else when instance is deleted by calling __del__, perform an SQL update
            db.putrecord(record)

    - 2    Single record, known id
            db.getRecord(id)
            db.getRecord(id, data)

        - When there is a record with this id in the cache:
            - Answer that record (leave the existing r/w mode unchanged
        - When there is not a record with this id in cache and data is None:
            - Create an instance of Record and read the data from the database with a SQL select
            - Store the instance in the cache under "db.table.id"
        - When there is not a record with this id in cache and data is not None:
            (this happens when there is a whole set of records selected at once by Selection instance)
            - Create an instance of Record, with the defined id.
            - Store the instance in the cache under "db.table.id"
        - If attribute names do not start with "_" set/get the value from record._data
        - Setting an attribute is only allowed when the record has 'rw' mode
        - Upon _put() the record will perform an SQL update and set 
            record._changed = True
            db.putrecord(record)
        - Else when instance is deleted by calling __del__, perform an SQL update
            db.putrecord(record)
        - Deleting a record will delete the record from the database and from the cache.
            db.deleteRecord(record)

    - 3 Selection of records
        - Get a list of raw data for records
        - If a record is needed by index, then get an (existing) instance of the record
            db.getRecord(id, data)

    - 4 Relations are handled automatically by 4 difference subclasses of Field:
        Many2OneField, One2ManyField, One2OneField and Many2ManyField. Some specialized other reference classes inherit
        from these, such as self-referencing parent and children fields.
        These relation object come from the the model descriptor class. This allows direct access in a “chain” of
        records and relations.
        Example:
            Many2One and One2One relations perform as: aa.bb.cc.city
            where "aa", "bb", "cc" are record of a specific table.
            One2Many and Many2Many relations perform as aa.bb[2].cc[3].city but
            also could be address by aa.bb.cc.city, creating a a flat list of
            all the cc.city in the tree
        To achieve such a simple syntax, some complicated handling must be done
        by the record attribute methods.

    </doc>
    """
    # Storage of opened database connections. There is one for every database name.
    CONNECTIONS = {}

		# Initialize from config. Can be redefined by inheriting classes.
    DATABASE_HOST = C.DATABASE_HOST 
	  DATABASE_PORT = C.DATABASE_PORT
	  DATABASE_USER = C.DATABASE_USER
    DATABASE_PASSWORD = C.DATABASE_PASSWORD

    def initialize(self, databases):
        u"""
        <doc>
        The closing tag is the <code>closedatabase</code> finally called by the <code>close</code> method.<br/>
        The database connection is available under <code>self.cursor</code>. The instance attribute
        <code>self._allowtabledrop</code> is initialized to <code>False</code> to protect accidentally dropping of table
        content. The value has to be explicitly set to <code>True</code> in order to make <code>self.dropTable(model) to
        work.<br/>
        If the database engine is of type MySql, then always set quotes to ANSI_QUOTES. The <attr>databases</attr>
        dictionary of descriptors is used in case the cursor is not defined (e.g. when the application is not a server
        but running and stand-alone).
        </doc>
        """
        name = self.getDatabaseName()

        self._lastquery = None            # Storage of the last query requested, even when SQL raises an error.
        self._allowtabledrop = False    # Protect from accidental table drop.

        # For now make sure there are no leftovers from previous sessions.
        # TODO: with multi-threading we can use this feature to check if records are currently open and thus locked.
        self.clearCache()

        # Get the database connection (cursor) for this page.
        try:
            self.cursor = self.getNewCursor(name, databases)
        except Exception, e:
            print e

    def getNewCursor(self, name, databases=None):
        u"""
        <doc>
        The <code>getNewCursor</code> method answers the Postgres database connection (cursor) for this page.
        </doc>
        """
        connection = self.CONNECTIONS.get(name)
        if connection is None:
            connection = self.CONNECTIONS[self.name] = Postgres(self.name, ip=self.DATABASE_HOST,
                            port=self.DATABASE_PORT, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD)
        return connection
        
    # ---------------------------------------------------------------------------------------------------------
    #    G L O B A L S

    @classmethod
    def getConnections(self):
        u"""
        <doc>
        The <code>getConnections</code> method answers the dictionary with open connections.
        </doc>
        """
        global cursors
        return cursors

    def getModel(self, table):
        u"""
        <doc>
        The <code>getModel</code> method answers the model of the table named <attr>table</attr>. If the descriptor does
        not exist (e.g. if no graffle was defined) or if it the descriptor does not contain the request table name, then
        answer None.
        </doc>
        """
        models = self.getModels()
        if table is not None and models is not None:
            return models.get(table.lower())
        return None

    def dropTable(self, table):
        u"""
        <doc>
        The <code>dropTable</code> method drops the content and definition of the table defined by <attr>table</attr>.
        The method will only work if the <code>self._allowtabledrop</code> is set to <code>True</code>.
        </doc>
        """
        if not self._allowtabledrop:
            raise ValueError('[SqlDatastore.dropTable] Not allowed to drop table "%s" in the datastore' % table)
        self.query('DROP TABLE "%s"' % table)

    def createTable(self, table):
        u"""
        <doc>
        The <code>createTable</code> method creates the table as defined by <attr>table</attr>.
        </doc>
        """
        model = self.getModel(table)
        self.query(model.createSql())

    # ---------------------------------------------------------------------------------------------------------
    #    F I E L D  S T U F F

    def tableHasField(self, table, field):
        u"""
        <doc>
        The <code>tableHasField</code> method answers the boolean flag id the <attr>table</attr> has a field named
        <attr>field</attr>. Also assumed is that the field name does not start with a <code>'_'</code>.
        </doc>
        """
        if field.startswith('_'):
            return False
        model = self.getModel(table)
        if model:
            return model.has_key(field)
        return False

    # ---------------------------------------------------------------------------------------------------------
    #    S E L E C T I O N

    def getSelectionSize(self, table, where=None):
        u"""
        <doc>
        The <code>getSelectionSize</code> method answers the size of the selection that fits the attribute definitions
        composed as a SQL query.
        </doc>
        """
        return self.count(table, where=where)

    def getSelection(self, table, fields, astable=None, order=None, slice=None, start=None, readonly=True, where=None,
            distinct=None, query=None):
        u"""
        <doc>
        The <code>getSelection</code> method answers the selection of records from <attr>table</attr>, where only the
        fields indicated by <attr>fields</attr> are read. If <attr>readonly</attr> is False, then mark the records as
        such.
        </doc>
        """
        return Selection(self, table=table, fields=fields, astable=astable, order=order, slice=slice, start=start,
            where=where, distinct=distinct, readonly=readonly, query=query)

    def getSelectedRecord(self, table, fields, astable=None, mode=None, where=None, order=None, start=None,
            slice=None, readonly=True, initialized=False, query=None, distinct=None):
        u"""
        <doc>
        The <code>getSelectedRecord</code> method answers the selection of the first record that fits the attribute
        definitions composed as SQL query. If the <attr>checkonsingle</attr> attribute is <code>True</code>
        (default is <code>False</code>), then an error is raised if there is more than one record selected with the
        defined clause.
        </doc>
        """
        selection = self.getSelection(table, fields, astable=astable, order=order, slice=slice, start=start,
            readonly=readonly, where=where, distinct=distinct, query=query)
        if selection:
            return selection[0]
        return self.getNoneRecord(table)

    # ---------------------------------------------------------------------------------------------------------
    #    R E C O R D

    def getRecord(self, table, id=None, data=None, readonly=True, forceinsert=False, nocache=False, fields=None,
            **args):
        u"""
        <doc>
        The <code>getRecord</code> method answers the instantiated <code>Record</code> object of this <attr>id</attr> if
        it exists. Make sure to convert <attr>id</attr> into a real integer id, or else the cache may think a string id
        is different. Else create a new record with this data, store it in the cache, and answer it. id can be either
        None, int or string.<br/>
        If the <attr>cache</code> is <code>True</code> (default), then try to read the record from cache first. If the
        record is already in cache, then still set the readonly flag from the <attr>readonly</attr>, otherwise cached
        records, that previously were used for reading only, will still not be writable.<br/>
        If the <attr>forceinsert</attr> attribute is set, then always insert the record. This is used when initializing
        a table from an application.<br/>
        </doc>
        """
        record = self.getCache(table, id)
        # Try to read from internal database cache, if the record was read before. Note that this is different from the
        # page cache record, as stored in a cache record engine.
        if not nocache and record is not None:
            record._setReadOnly(readonly)    # Take over the requested readonly flag
            return record

        # Record is not in cache of datastore. Create an instance.
        record = Record(self, table, id=id, readonly=readonly, data=data, forceinsert=forceinsert, fields=fields, **args)
        self.putCache(table, id, record)
        return record

    def read(self, table, id, fields):
        u"""
        <doc>
        The <code>read</code> method reads actual data from database when not done before.<br/>
        Make sure there is only one record result. Or else we have a non-existing id or there are multiples.<br/>
        <note>All fields of a record are used as plain names, so all other attributes have a preceding "_".</note>
        The field list <attr>fields</attr> attribute can be either a comma separated string of field names or a list of
        field names. The field list <attr>fields</attr>  be defined. For efficiency reasons we don’t want to use the
        global <code>'*'</code>, since too much data returns and the order of the answered tuple if data is not clear
        and needs to be sorted out.<br/>
        This is one method of the three basis operations of the datastore: <code>self.read(...)</code>,
        <code>self.write(...)</code> and <code>self.select(...)</code>.
        </doc>
        """
        if isinstance(fields, (tuple, list)):
            fields = '"' + '", "'.join(fields) + '"'

        q = u'SELECT %s FROM "%s" WHERE id = %s' % (fields, table, id)
        result = self.getQuery(q)
        if not result:
            return None
        assert len(result) == 1, u'[Agent.read] Duplicate records in table "%s" with id "%s"' % (table, id)
        return list(result[0])

    def write(self, table, id, fields, forceinsert=False):
        u"""
        <doc>
        The <code>write</code> method of the datastore actually writes the record in the database. This is done here,
        in order to keep the <code>Record</code> and <code>Selection</code> classes absolutely generic. The datastore is
        dependent on the kind of database running on the server hardware. Writing of the record only takes place when it
        is changed _and_ when the record is writable _and_ there is any data to write (this record may already have been
        deleted). Do an insert or update depending on the value of <attr>id</attr>. Only write the fields which names
        are in the <attr>changedfields</attr> list.<br/>
        Fields that contain None are set as SQL <code>NULL</code>.<br/>
        This is one method of the three basis operations of the datastore: <code>self.read(...)</code>,
        <code>self.write(...)</code> and <code>self.select(...)</code>.
        <todo>Better to block the record between insert and getting max id value,
        since in theory another record can be made by another application.</todo>
        </doc>
        """
        if id is not None and forceinsert:
            # Make sure to delete all records with this id first to avoid doubles. The insert with known id
            self.deleteRecord(table, id)
            if 'id' not in fields:
                fields['id'] = id
            insert = self.fields2Insert(self.getModel(table), fields, allowid=True)
            q = u'INSERT INTO "%s" %s' % (table, insert)
            #print '##1##', q
            self.query(q)
            # We have set the id on insert. No need to get it from the table.
        elif id is not None:
            # Id is known so record must exist. Just update.
            update = self.fields2Update(self.getModel(table), fields)
            q = u'UPDATE "%s" SET %s WHERE id = %s' % (table, update, id)
            #print '##2##', q
            self.query(q)
            #print q
        else:
            # Unknown id, insert and get resulting (max) id to answer.
            insert = self.fields2Insert(self.getModel(table), fields)
            q = u'INSERT INTO "%s" %s' % (table, insert)
            #print '##3##', q
            self.query(q)
            # @@@ This is postgres specific
            id = self.getQuery("select lastval()")[0][0]
        return id

    def select(self, table, fields, astable=None, order=None, slice=None, start=None, readonly=True, where=None,
            distinct=None):
        u"""
        <doc>
        The <code>select</code> method answers the selection of records from <attr>table</attr>, where only the fields
        indicated by <attr>fields</attr> are read. If <attr>readonly</attr> is False, then mark the records as such.
        <br/>
        This is one method of the three basis operations of the datastore: <code>self.read(...)</code>,
        <code>self.write(...)</code> and <code>self.select(...)</code>.
        </doc>
        """
        assert fields
        if isinstance(fields, (list, tuple)):
            fields = '"' + '","'.join(fields) + '"'
        # If order is a list of field names, then combine it first.
        if isinstance(order, (list, tuple)):
            order = ','.join(order)

        query = [u'SELECT ']
        if isinstance(distinct, basestring):
            query.append(u' DISTINCT NO (%s) ' % distinct)
        elif distinct:
            query.append(u' DISTINCT')
        query.append(u' %s FROM "%s"' % (fields, table))
        if astable is not None:
            query.append(u' AS "%s"' % astable)
        if where is not None:
            query.append(u' WHERE %s' % where)
        if order is not None:
            query.append(u' ORDER by %s' % order)
        if slice is not None: # Limit + Order: MySQL must have this sequence.
            query.append(u' LIMIT %s' % slice)
        if start is not None:
            query.append(u' OFFSET %s' % start)
        return self.getQuery(''.join(query))

    def deleteRecord(self, table, id=None, where=None):
        u"""
        <doc>
        The <code>deleteRecord</code> method first deletes all records the cache, to make there there are no links to
        the record to be deleted.<br/>
        Then delete the record for the table defined by <attr>table</attr> with id <attr>id</attr>.<br/>
        <note>We assume here that the record has <code>record._readonly</code> set to <code>False</code>.</note>
        </doc>
        """
        if where is not None:
            q = u'DELETE FROM "%s" WHERE %s' % (table, where)
        elif id is not None:
            self.deleteCache(table, id)
            q = u'DELETE FROM "%s" WHERE id = %s' % (table, id)
        #print q
        self.query(q)

    def _newSingleXRefRecord(self, table1, field1, id1, table2, field2, id2, notes=None, sortorder=None):
        if not self.getXRef(table1, field1, id1, table2, field2, id2):
            q = u"""INSERT INTO "{xref}" ({srctable}, {srcfield}, {srcid}, {dsttable}, {dstfield}, {dstid}{notesfield}{sortfield}) VALUES ('{t1}', '{f1}', {id1}, '{t2}', '{f2}', {id2}{notes}{sort})""".format(
                xref=Constants.TABLE_XREF, 
                srctable=Constants.FIELD_XSRCTABLE, 
                srcfield=Constants.FIELD_XSRCFIELD, 
                srcid=Constants.FIELD_XREFSRCID,
                dsttable=Constants.FIELD_XDSTTABLE, 
                dstfield=Constants.FIELD_XDSTFIELD, 
                dstid=Constants.FIELD_XREFDSTID, 
                t1=table1, f1=field1, id1=id1,
                t2=table2, f2=field2, id2=id2,
                notesfield = ', notes' if self.getModel(Constants.TABLE_XREF)._hasField('notes') and notes else '',
                notes = ', $XierpaQuote${0}$XierpaQuote$'.format(notes) if self.getModel(Constants.TABLE_XREF)._hasField('notes') and notes else "",
                sortfield = ', sortorder' if self.getModel(Constants.TABLE_XREF)._hasField('sortorder') and sortorder else '',
                sort = ', {0}'.format(sortorder) if self.getModel(Constants.TABLE_XREF)._hasField('sortorder') and sortorder else "",
            )
            #print q
            self.query(q)

    def updateXRefSortOrder(self, table1, field1, id1, table2, field2, sorts):
        u"""
        <doc>
        The <code>updateXRefSortOrder</code> method updates the sortorder field for all records associated with
        <attr>table1</attr>, <attr>field1</attr>, <attr>id1</attr>, to a particular 
        <attr>table2</attr>, <attr>table2</attr>. For example: on a particular record page where a bunch of
        related records are shown, an editor could rearrange the list, and the new order would be submitted to this method.
        <attr>sorts</attr> is a dictionary whose keys are the related record ids (<attr>id2</attr> in other XRef methods)
        and values are integers representing the sort order. 
        </doc>
        """
        for id2, sort in sorts.items():
            self.updateXRef(table1,field1,id1,table2,field2,id2,sortorder=sort)

    def updateXRef(self, table1, field1, id1, table2, field2, id2, **args):
        q = u"""UPDATE "{xref}" set {setfields} WHERE {srctable}='{t1}' AND {srcfield}='{f1}' AND {srcid}={id1} AND {dsttable}='{t2}' AND {dstfield}='{f2}' AND {dstid}={id2}""".format(
            xref=Constants.TABLE_XREF, 
            srctable=Constants.FIELD_XSRCTABLE, 
            srcfield=Constants.FIELD_XSRCFIELD, 
            srcid=Constants.FIELD_XREFSRCID,
            dsttable=Constants.FIELD_XDSTTABLE, 
            dstfield=Constants.FIELD_XDSTFIELD, 
            dstid=Constants.FIELD_XREFDSTID, 
            t1=table1, f1=field1, id1=id1,
            t2=table2, f2=field2, id2=id2,
            setfields=', '.join(["{k}={v}".format(k=k,v="$XierpaQuote${0}$XierpaQuote$".format(v) if isinstance(v,basestring) else v) for k,v in args.items()]),
        )
        #print q
        self.query(q)

    def newXRef(self, table1, field1, id1, table2, field2, id2, notes=None):
        u"""
        <doc>
        The <code>getXRef</code> method answers the cross reference (as selection, which allows the application to check
        if the amount really is 0 or 1, as it should be) that fit the attributes <code>(table1, field1, id1, table2,
        field2, id2)</code>. Note that the use of table and field fields, the <code>TABLE_XREF</code> is generic for
        the cross reference record for the entire database. For each cross references, two records are inserted. This
        makes selecting from one side easier and faster.<br/>
        The method checks to make sure there is no self-reference of any record requested.
        </doc>
        """
        hasnotes = self.getModel(Constants.TABLE_XREF)._hasField('notes')

        #first check to see if there is an existing relation
        xref1 = self.getXRef(table1, field1, id1, table2, field2, id2, field='notes' if hasnotes else '*')
        xref2 = self.getXRef(table2, field2, id2, table1, field1, id1, field='notes' if hasnotes else '*')

        #if so, see if anything has changed
        if xref1 and xref2:
            #print xref1
            if hasnotes and notes is not None and notes != xref1[0][0]:
                self.updateXRef(table1,field1,id1,table2,field2,id2,notes=notes)
                self.updateXRef(table2,field2,id2,table1,field1,id1,notes=notes)
        else:
            #just to be safe
            self.deleteXRef(table1, field1, id1, table2, field2, id2)
    
            if id1 != id2 or field1 != field2 or table1 != table2:
                self._newSingleXRefRecord(table1, field1, id1, table2, field2, id2, notes)
                self._newSingleXRefRecord(table2, field2, id2, table1, field1, id1, notes)

    def getXRef(self, table1, field1, id1, table2, field2, id2, field='*'):
        u"""
        <doc>
        The <code>getXRef</code> method answers the cross reference (as selection, which allows the application to check
        if the amount really is 0 or 1, as it should be) that fits the attributes <code>(table1, field1, id1, table2,
        field2, id2)</code>. Note that the use of table and field fields, the <code>TABLE_XREF</code> is generic for the
        cross reference record for the entire database.
        </doc>
        """
        q = u"""SELECT %s FROM "%s" WHERE %s='%s' AND %s='%s' AND %s=%s AND %s='%s' AND %s='%s' AND %s=%s""" % \
            (field, Constants.TABLE_XREF,
                Constants.FIELD_XSRCTABLE, table1, Constants.FIELD_XSRCFIELD, field1, Constants.FIELD_XREFSRCID, id1,
                Constants.FIELD_XDSTTABLE, table2, Constants.FIELD_XDSTFIELD, field2, Constants.FIELD_XREFDSTID, id2)
        return self.getQuery(q)

    def deleteXRef(self, table1, field1, id1, table2, field2, id2):
        u"""
        <doc>
        The <code>deleteXRef</code> method deletes the cross references (in both directions) that connect
        <code>(table1, field1, id1, table2, field2, id2)</code>.
        </doc>
        """
        self.deleteRecord(Constants.TABLE_XREF,where=u"""%s='%s' AND %s='%s' AND %s=%s AND %s='%s' AND %s='%s' AND %s=%s""" % (
            Constants.FIELD_XSRCTABLE, table1, Constants.FIELD_XSRCFIELD, field1, Constants.FIELD_XREFSRCID, id1,
            Constants.FIELD_XDSTTABLE, table2, Constants.FIELD_XDSTFIELD, field2, Constants.FIELD_XREFDSTID, id2
        ))

        self.deleteRecord(Constants.TABLE_XREF,where=u"""%s='%s' AND %s='%s' AND %s=%s AND %s='%s' AND %s='%s' AND %s=%s""" % (
            Constants.FIELD_XSRCTABLE, table2, Constants.FIELD_XSRCFIELD, field2, Constants.FIELD_XREFSRCID, id2,
            Constants.FIELD_XDSTTABLE, table1, Constants.FIELD_XDSTFIELD, field1, Constants.FIELD_XREFDSTID, id1
        ))

    def min(self, table, where=None, field=None):
        u"""
        <doc>
        The <code>min</code> method answers the minimum value of <attr>field</attr> (default value is
        <code>self.FIELD_ID</code> of all selected records. Together with the id field, this can be used to get the
        <attr>id</attr> of the latest inserted record.
        </doc>
        """
        if where is None:
            where = 'True'
        if field is None:
            field = 'id'
        q = u'SELECT MIN(%s) FROM "%s" WHERE %s' % (field, table, where)
        return self.getQuery(q)[0][0]

    def max(self, table, where=None, field=None):
        u"""
        <doc>
        The <code>max</code> method answers the max value of <attr>field</attr> (default value is
        <code>self.FIELD_ID</code> of all selected records. Used with the id field, this can be used to get the
        <attr>id</attr> of the latest inserted record.
        </doc>
        """
        if where is None:
            where = 'True'
        if field is None:
            field = 'id'
        q = u'SELECT MAX(%s) FROM "%s" WHERE %s' % (field, table, where)
        result = self.getQuery(q)
        return result[0][0]

    def exists(self, table, id=None, where='True'):
        u"""
        <doc>
        The <code>exists</code> method answers the boolean flag if there are records that fit this 
        <attr>where</attr> clause.<br/>            
        If <attr>id</attr> is defined, then add this to the defined <attr>where</attr> clause as rule.
        The attribute <attr>id</attr> can be either <code>None</code>, <code>int</code> and <code>string</code>.
        </doc>
        """
        assert id is None or isinstance(id, (int, long, basestring)), '[Agent.exists] Id "%s" must be one of (None, \
                                                                        int, long, basestring)' % id
        if id is not None:
            where += u' AND id = %s' % id
        return self.count(table, where) > 0

    def count(self, table, where=None):
        u"""
        <doc>
        The <code>count</code> method answers the size of the selection in <attr>table</attr> using
        the optional <attr>where</attr> as clause.
        </doc>
        """
        if where is None:
            where = 'TRUE'
        return self.getQuery(u'SELECT count(*) FROM "%s" WHERE %s' % (table, where))[0]
