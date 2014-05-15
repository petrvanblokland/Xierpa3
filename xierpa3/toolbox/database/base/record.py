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
#     record.py
#
#     TODO:
#     In case there is a hierarchy, the record should cache the _getChildren result.
#
from xierpa3.toolbox.dating import DateTime
from nonerecord import NoneRecord
from baserecord import BaseRecord

class Record(BaseRecord):
    u"""
    <doc>
    The <code>Record</code> class implements the behavior of a new or existing SQL record. All method names start with
    an underscore to avoid collision with all possible field name. The record is constructed in such a way, that all
    fields are available as object attribute names.<br/>
    <br/>
    Create a new record instance. <br/>
    All attributes that don't start with '_' are assumed to be fields.<br/>
    <python>        
    record['abc']<br/>
    record.abc<br/>
    </python>
            
    There are 3 different strategies to fill the fields:
    <table>
    <row><col><b>id</b></col><col><b>_initialized</b></col>col/></row>    
    <row><col>None</col>    <col>False</col>        <col>Fields are empty and can be changed individually.</col></row>
    <row><col>&gt;0</col>    <col>False</col>        <col>Try to read from the database upon first attribute get, then set _initialized to <code>True</code></col></row>
    <row><col>&gt;0</col>    <col>True</col>            <col>No change</col></row>
    </table>
    
    If the <attr>id</attr> is <code>None</code>, then insert a new record in the database upon writing (e.g. deletion)
    and set the new created id.    If the <attr>id</attr> is set and he <attr>forceinsert</attr> attribute is <code>True
    </code>, then insert a new record with this id. Note that this is mainly used when initializing a table from an
    application. Or else there may be duplicate id’s in the database. Otherwise just perform an update in the database
    for the defined id.<br/>
    <br/>
    Fields hold the raw data as it comes from the database driver. The field model is used to convert between the raw
    SQL value and Python objects, using respectively <code>fieldmodel.sql2Value(sqlvalue, id, self._db)</code> and
    <code>fieldmodel.value2Sql(value, id, db)</code> at the first time that the value is retrieved. This approach saves
    unnecessary conversion of field values that are not used.<br/>
    The record instance keeps track if values change, so on updating the record, only the changed values are actually
    written to the database.
    </doc>
    """
    CLEAR_ORIGINAL_DATA = True

    def __init__(self, agent, table, id=None, readonly=False, data=None, forceinsert=False, dummy=False,
            fields=None, astable=None, inherit=True, **args):
        u"""
        <doc>
        </doc>
        """
        self._table = table                    # Name of the table of this record.
        #self._astable = astable            # Optional alias table name, used in the "...tablename as astable..." query construction
        self._fieldnames = fields            # Storage of specific field name list of only part of the fields needs reading
        self._fields = {}                    # Dict storage of retrieved and converted field values as raw-->Python/Xierpa instances.
        self._encryptionkeys = {}            # for EncryptedFields, key needs to be set before storing the value
        self._changedfields = set()            # Keep track of the fields that were changed to optimize writing an update
        self._readonly = readonly            # Writing is default disabled
        self._inherit = inherit                # If set to False, then will disable inheritance on inheritable fields
        self._dummy = False                    # If set to True, then the record finally will not be written in _sync()
        self._forceinsert = forceinsert        # If set, then always perform an insert, even when the id is set.
        self._db = agent

        self._initialized = bool(data)        # If there is external data, no more reading. Or set to True after reading from the database
        self._setData(data)                    # store the raw data in the record. record[field] will retrieve and convert, each field separate, once.
        self._forceId(id)                    # Not allowed to change the id through normal attribute methods

        for field, value in args.items():
            self[field] = value

    def __repr__(self):
        return '%s(id=%s, changed=%s, readonly=%s, model=%s, fields=%s, data=%s)' % (self._table or None, self._id(),
            tuple(self._getChangedFields()),
            self._readonly,
            self._getModel(),
            self._fields,
            self._getData(),
        )

    def __str__(self):
        u"""
        <doc>
        Just answer the id as string. This way special records such as many2one relations will behave as plain id
        references.
        </doc>
        """
        return str(self._id())

    def __del__(self):
        u"""
        <doc>This record is about to be deleted by garbage collection.</doc>
        """
        self._close()

    def __nonzero__(self):
        return True

    def __getitem__(self, name):
        u"""
        <doc>
        The <code>__getitem__</code> (<code>self[name]</code>) method answers the content of <code>self._fields[name]
        </code> if the name does not start with a <code>'_'</code>. If the <code>self._fields[name]</code> value does
        not exist yet, and when the name has a valid field model, then convert the value through the field model from
        the raw <code>self._getData()</code> storage (list of initial database values to the <code>self._fields</code>
        dict. If <attr>name</code> starts with a <code>'_'</code>, then it must be a regular method or instance
        variable. Otherwise the name is interpreted as field name.
        </doc>
        """
        assert isinstance(name, basestring) and not name.startswith('_')
        if name == 'id':
            return self._id()

        if not name in self._getFieldNames():
            # This is not a known field name
            raise KeyError('[Record.__getattr__] Unknown requested field "%s" in table "%s"' % (name, self._table))

        fields = self._fields

        if fields.has_key(name):
            # If the field value is not None, then the field value is already converted from raw 
            # data, because it was earlier accessed. Just answer this value. Otherwise try to
            # initialize the value (again).

            #value = fields[name]
            #if value is not None:
            #    return value
            
            #above code doesn't work for NULL fields that might legitimately be None
            # as far as I can tell, if self._fields[name] is set, then it has already been initialized
            return fields[name]

        # The field exists in this record, but there was no value yet initialized from raw data.
        # Make sure that the data is read from the database for this record and get the raw SQL value
        # This will deleted the self._getData() and initialize the dictionary self._fields with converted
        # data values.

        return self._initializeField(name)

    def __setitem__(self, field, value):
        # Setting a normal field. 
        # Do some checking here
        assert not self._readonly, ('[Record.__setattr__] Record is readonly. Set record._readonly = False to write records.')
        assert field != 'id', ('[Record.__setattr__] Not allowed to change the id field')
        assert self._getModel().has_key(field), ('[Record.__setattr__] Unknown requested field "%s" in table "%s"' % (field, self._table))

        # If the new value is different from the existing value, then mark this field as changed 
        # And store the new value. Note that this is the Python value, so it can be used as record[field]
        # without saving. The conversion to raw SQL value is done on actual save.
        # If one of the two values not a 
        originalvalue = self[field]
        if originalvalue != value:
            self._setChangedField(field)
            self._fields[field] = value

    def __long__(self):
        return long(self._id())

    __int__ = __long__

    def __hash__(self):
        return int(self._id())

    def __ne__(self, r):
        if not self._id():
            return False
        if isinstance(r, (int, long)):
            return int(self._id()) != r
        return not self is r

    def __eq__(self, r):
        if not self._id():
            return False
        if isinstance(r, (int, long)):
            return int(self._id()) == r
        return self is r

    def __setattr__(self, name, value):
        u"""
        <doc>
        Set the field of the record named <attr>name</attr> to <attr>value</attr> if <attr>name</attr> does not start
        with a <code>'_'</code>. Otherwise assume that it is a regular attribute of the record.
        </doc>
        """
        if name.startswith('_') or name in ['has_key', 'get']:
            # This is a regular attribute of the record instance.
            self.__dict__[name] = value
        else:
            # This is a field set, identical to and handled by __setitem__
            self[name] = value

    def __getattr__(self, name):
        u"""
        <doc>
        Check if this is a private or field request (test on initial '_')
        <table>
            <row><col>Fieldname</col><col><code>record.field</code></col><col/></row>
            <row><col>Method</col><col><code>record._where()</code></col><col/></row>
        </table>
        If there is a <code>self._id()</code> and record was not initialized, then read from the database. If the
        resulting value is a text string, then convert to unicode.<br/>
        The record performs as a “lazy” raw data container: only when fields are actually requested for their value,
        then the data is read from the database, only once.
        </doc>
        """
        if name.startswith('_') or name in ('has_key', 'get'):
            # This is a regular attribute of the record instance.
            # No need to read the data, when we only need the id
            try:
                return self.__dict__[name]
            except KeyError:
                raise AttributeError

        # This is a field request, identical to and handled by __getitem__
        return self[name]

    def _get(self, field):
        u"""
        <doc>
        The <code>get</code> method answers the content of the field <attr>field</attr>. If the field does not exist,
        then answer <code>None</code>. We want records to be compatible with regular Python <code>dict</code> objects,
        so also <code>get</code> is defined as method. This implies that field names are restricted not to be named
        “get” or “has_key”. Note that the following notations are all equivalent:
        <python>
        record._get('lastname')<br/>
        record.get('lastname')<br/>
        record['lastname']<br/>
        record.lastname<br/>
        </python>
        with the standard Python exception that the <code>_get</code> will not raise a <code>KeyError</code> if the key
        does not exist. It answers <code>None</code> instead.
        </doc>
        """
        return self[field]

    # To make a record compatible with a dictionary, we allow get as method.     
    # This implies that field names are restricted not to be named "get" or "has_key"
    get = _get

    def _show(self):
        u"""
        <doc>Show the content of all fields</doc>
        """
        t = ['[Record']
        for field in self._getFieldNames():
            t.append('%s:%r' % (field, self[field]))
        return ', '.join(t) + ']'

    def _isIdField(self,field):
        return field == 'id'
    

    def _new(self, data=None, **args):
        u"""
        <doc>
        Answer a duplicate of the current record where the <attr>id</attr> is set to <code>None</code>, so it will
        be inserted in the table. Dony’t copy any of the other fields, except the <code>many-to-one</code> relations. 
        This means that the location of the new record is equal to self, except that it is empty.<br/>
        The <attr>data</attr> attribute can be used to initialize the fields by supplying a dict with field/value
        pairs.<br/>
        <seealso>_relateTo</seealso><br/>
        <python>
        record = address.department_id._new()
        record = address.department_id._new(data={self.FIELD_NAME: 'New department'})
        record = address.department_id._new(name='New department')
        </python>
        </doc>
        """
        r = Record(self._db, self._table, data=data, readonly=False, **args)
        for field in self._getFieldNames():
            if r._isIdField(field):
                continue
            value = self[field]
            if isinstance(value, (NoneRecord, Record)):
                r[field] = value.id
        r._sync()
        return r

    def _copy(self,id=None):
        u"""
        <doc>
        Answer a duplicate of the current record where the <attr>id</attr> is set to <code>None</code>, so it will be
        inserted in the table.<br/>
        <seealso>_new</seealso><br/>
        </doc>
        """
        r = Record(self._db, self._table, readonly=False, forceinsert=True, id=id)
        for field in self._getFieldNames():
            if self._isIdField(field):
                continue
            value = self[field]
            if isinstance(value, (NoneRecord, Record)):
                r[field] = value.id
            elif self._getFieldModel(field).isUnique():
                #have to assume someone is going to set this later
                import random
                try:
                    r[field] = None
                except:
                    r[field] = self[field] + '-' + str(random.randint(1,9999999)) if isinstance(value,basestring) else random.randint(1,9999999)
            else:
                r[field] = self[field]
        r._sync()
        return r

    def _setDummy(self, dummy):
        u"""
        <doc>
        The <code>_setDummy</code> method sets the <code>_dummy</code> flag of the record to the boolean <attr>dummy
        </attr> attribute value. If the flag is <code>True</code> then the record behaves normally except that it does
        not write in <code>_sync()</code>.
        </doc>
        """
        self._dummy = dummy

    def _setReadOnly(self, readonly):
        u"""
        <doc>
        The <code>_setReadOnly</code> method sets the <code>_readonly</code> flag of the record to the boolean <attr>
        readonly</attr> attribute value.
        </doc>
        """
        self._readonly = readonly

    def _setInherit(self, inherit):
        """
        <doc>
        <code>_setInherit</code> allows one to enable/disable "inheritable" fields from inheriting parent values. The
        default value is True, which only affects inheritable fields. If set to False, inheritance is disabled for all
        fields even if the field model specifies inheritance.
        </doc>
        """
        self._inherit = inherit

    def _getReadOnly(self):
        u"""
        <doc>
        The <code>_getReadOnly</code> method answers the <code>_readonly</code> flag of the record.
        </doc>
        """
        return self._readonly

    # Hack for now, always to answer False. The _readonly seems to be a problem,
    # as it changes value for some reason along the way.
    def _get_readonly(self):
        return False
    
    def _set_readonly(self, flag):
        pass
        
    _readonly = property(_get_readonly, _set_readonly)
    
    def _id(self):
        return self._fields.get('id')

    def _hasField(self, field):
        u"""
        <doc>
        The <code>_hasField</code> method answers the boolean flag if the record has <attr>field</attr> in the list of
        field names as answered by <code>self._getFieldNames()</code>.
        </doc>
        """
        return field in self._getFieldNames()

    __contains__ = _hasField

    def _dict(self):
        """
        <doc>
        The <code>_dict</code> method answers a dict with all field/values.
        </doc>
        """
        from xierpa3.toolbox.database.base.selection import Selection
        d = {}
        for field in self._getFieldNames():
            item = getattr(self, field)
            #recursively convert records
            # or, maybe not, can cause infinite recursion if records reference each other
            #if isinstance(item,Selection):
            #    d[field] = item._list()
            #elif hasattr(item,'_dict'):
            #    d[field] = item._dict()
            #else:
            d[field] = item
        return d

    def _setParent(self, parent):
        u"""
        <doc>
        The <code>_setParent</code> method sets <attr>parent</attr> to be the parent of <code>self</code>.
        </doc>
        """
        if isinstance(parent, self.__class__):
            parent = parent.id
        self[self._getModel()._getParentFieldName()] = parent

    def _newChild(self):
        u"""
        <doc>
        The <code>_newChild</code> answers a new child record of <code>self</code>. The new record hasn't been saved,
        but the parent id is initialized. The <code>self</code> record needs to have a valid id, otherwise an assert
        error is raised.
        </doc>
        """
        assert self.id
        child = self._db.newRecord(self._getTable())
        child._setParent(self.id)
        return child

    def _relateTo(self, record, field, dstfield=None, notes=None):
        """
        <doc>
        Relate the <attr>record</attr> to <code>self</code> using the <attr>field</attr> named field as connection. If
        the field model is a <code>Many2ManyField</code> instance, then check if the X-ref relation does not yet exist.
        Otherwise create a new cross reference between <code>self</code> and <attr>record</attr>. If the field modes is
        a <code>One2ManyField</code> instance, then set the reference <code>self._id()</code> in <attr>record[dstfield]
        </attr>. If the optional <attr>dstfield</attr> is omitted, then pull the value from the source field model.
        <br/>
        If the field model is a <code>Many2OneField</code> instance, then set <code>record.id</code> in <code>
        self[field]</code>. The method does check if the relating record has an <attr>id</attr> value. If not, then the
        record is synchronized (that is performing an SQL <code>insert</code> query).<br/>
        There are several possible relations  depending on the <attr>field</attr> model. Note that the used of table and
        field fields, the <code>TABLE_XREF</code> is generic for the cross reference record for the entire database.
        </doc>
        """
        srcfieldmodel = self._getFieldModel(field)

        if dstfield is None:
            dstfield = srcfieldmodel.getToField()

        dstfieldmodel = record._getFieldModel(dstfield)

        if srcfieldmodel.isMany2ManyField() and dstfieldmodel.isMany2ManyField():
            # self --E XREF E-- record
            id1 = self._id()
            if not id1:
                self._sync(force=True) # Force write, although not changed, to make sure there is an id
                id1 = self._id()
            id2 = record._id()
            if not id2:
                record._sync(force=True) # Force write, although not changed, to make sure there is an id
                id2 = record._id()

            self._db.newXRef(self._getTable(), field, id1, record._getTable(), dstfield, id2, notes)

        elif srcfieldmodel.isMany2OneField():
            # self --E record
            id = record._id()
            if not id:
                record._sync(force=True) # Force write, although not changed, to make sure there is an id
                id = record._id()
            self._setReadOnly(False)
            self[field] = id
            self._sync()

        elif dstfieldmodel.isMany2OneField():
            # record --E self
            id = self._id()
            if not id:
                self._sync(force=True) # Force write, although not changed, to make sure there is an id
                id = self._id()
            record._setReadOnly(False)
            record[dstfield] = id
            record._sync()
        else:
            raise TypeError('[Record._relateTo] Cannot create any relation of between "%s:%s" and "%s:%s"' % (self._getTable(), field, record._getTable(), dstfield))

    def _sortRelations(self, field, sorts=None):
        u"""
        <doc>
        The <code>_sortRelations</code> method updates the sortorder field for all records associated with
        <code>self</code> for a particular <attr>field</attr>. For example: on a particular record page where a bunch of
        related records are shown, an editor could rearrange the list, and the new order would be submitted to this method.
        <attr>sorts</attr> is a dictionary whose keys are the related record ids
        and values are integers representing the sort order. 
        </doc>
        """
        id1 = self._id()
        if not id1:
            self._sync(force=True) # Force write, although not changed, to make sure there is an id
            id1 = self._id()
        srcfieldmodel = self._getFieldModel(field)
        self._db.updateXRefSortOrder(self._getTable(), field, id1, srcfieldmodel.getToModel(), srcfieldmodel.getToField(), sorts)    

    def _removeRelation(self, field, id):
        srcfieldmodel = self._getFieldModel(field)
        self._db.deleteXRef(self._getTable(), field, self._id(), srcfieldmodel.getToModel(), srcfieldmodel.getToField(), id)
    

    def _newRelation(self, table=None, relation=None, readonly=False, **args):
        u"""
        <doc>
        Create a new record from the table named <attr>table</attr> and relate it to <code>self</code> using the
        optional <attr>relation</attr> named field as connection. If the <attr>relation</attr> is not defined, then use
        the default relation name <code>table.name + '_id'</code>.<br/>
        Answer the new record. The <attr>readonly</attr> defines if the new record is readonly or not. Since we can
        assume that the user wants to write in this new record, the default value of the <attr>readonly</attr> attribute
        is <code>False</code>.<br/>
        <seealso>_relateTo</seealso><br/>
        <seealso>_new</seealso><br/>
        <seealso>Agent.getRecord</seealso><br/>
        <python>
        self._newRelation('project')<br/>
        self._newRelation('address_author_responsible')
        </python>
        </doc>"""
        if table is None:
            table = self._getTable()
        newrecord = self._db.getRecord(table, readonly=False, **args)
        self._relateTo(newrecord, relation)
        return newrecord

    def _getRelatedNotes(self, field):
        u"""
        <code>
        Experimental <code>_getRelatedNotes</code> returns the notes field from Xref for each related record if it exists.
        </code>
        """
        from xierpa3.constants.constants import C
        
        fieldmodel = self._getFieldModel(field)
        frommodel = fieldmodel.getFromModel()
        fromfield = fieldmodel.getFromField()
        tomodel = fieldmodel.getToModel() or frommodel
        tofield = fieldmodel.getToField() or fromfield

        if self._id():
            try:
                query = """SELECT %(toid)s as id, notes FROM %(xref)s WHERE
                    %(fromtablename)s='%(fromtable)s' AND %(fromfieldname)s='%(fromfield)s' AND %(fromid)s=%(id)s AND
                    %(totablename)s='%(totable)s' AND %(tofieldname)s='%(tofield)s'""" % \
                    {'xref': C.TABLE_XREF,
                    'fromtablename': C.FIELD_XSRCTABLE, 'fromtable': frommodel,
                    'fromfieldname': C.FIELD_XSRCFIELD, 'fromfield': fromfield,
                    'fromid': C.FIELD_XREFSRCID, 'id': self._id(),
                    'toid': C.FIELD_XREFDSTID,
                    'totablename': C.FIELD_XDSTTABLE, 'totable': tomodel,
                    'tofieldname': C.FIELD_XDSTFIELD, 'tofield': tofield,
                    }
                return dict(self._db.getQuery(query))
            except Exception as e:
                #xref probably doesn't have notes field
                print e
                pass
        # Record is not initialized yet, so there is not id. No XRef can have been created.
        return {}

    def _forceId(self, id):
        """
        <doc>
        It is not allowed to change the <attr>id</attr> field of a record. Any attempt to perform e.g. <code>r.id = 123
        </code> will raise an error. However there are situations in which the record <attr>id</attr> must be set (e.g.
        when a set of records is initialized from an external source or in a Selection. In that situation this method
        can be used.<para/>
        <python>
        record._forceId(123)
        </python>
        </doc>
        """
        self._fields['id'] = id

    def _isNew(self):
        u"""
        <doc>
        Answer a boolean value <code>True</code> if this record will be written with the SQL <code>insert</code> query
        or <code>False</code> with SQL <code>update</code> query. otherwise. This method is equivalent to <code>
        recode.id is None</code>.
        <python>
        record._isNew()
        </python>
        </doc>
        """
        return self._id() is None

    def _getChangedFields(self):
        u"""
        <doc>
        The <code>_getChangedFields</code> method answers the set with field names that have been changed in the record,
        while the record has not been saved. On save this list is cleared. The standard behavior of the method is to
        answer <code>self._changedfields</code>.
        </doc>
        """
        return self._changedfields

    def _setChangedField(self, field):
        u"""
        <doc>
        The <code>_setChangedField</code> method adds the <attr>field</attr> name to the set of changed fields.Since the
        <code>self._changedfields</code> is a set, multiple additions of the same name have not effect on the set
        content.
        </doc>
        """
        return self._changedfields.add(field)

    def _resetChangedFields(self):
        u"""
        <doc>
        The <code>_resetChangedFields</code> method resets the <code>self._changedfields</code> to an empty set.
        </doc>
        """
        self._changedfields = set()

    def    _initializeField(self, field):
        u"""
        <doc>
        The <code>_initializeFields</code> method does initialize the <code>self._fields[field]</code> dictionary from
        raw data list that is the result of <code>self._getData()</code> for <attr>field</attr>. The initialization is
        done if the field values does not exists in <code>self._fields</attr>. So a record that reads but is never
        accessed does not have any overhead from field conversion.<br/>
        The conversion from <code>self._getData()</code> tuple to <code>self._fields</code> dictionary also uses the
        field models to convert to raw SQL data into Python/Xierpa instances, depending on the type of field class by
        filter of <code>fields[name] = fieldmodel.sql2Value(self._getData()[index], id, self._db)</code>.
        <doc>
        """
        fields = self._getFieldNames()
        id = self._id()
        data = []

        if id and not self._initialized:
            # We only need to read the data, if there is an existing database record,
            # so the id must exist.
            # There is an record id, so it must be an existing one, but the data was not read
            # from the database into self._data.
            # Note that if field values have been set already in self._fields, then we never
            # come here to collect the value from the raw self._data, so this allows the application
            # to overwrite values that already exist.
            data = self._readData(id, fields)
            self._setData(data)
            self._initialized = True
        else:
            # Raw data was initialized by an earlier field call.
            # This is a new record, just use the self._data as it may already exists (e.g. by a Selection) 
            data = self._getData()

        if data:
            index = self._getIndexOfField(field)
            sqlvalue = data[index]
            # Delete the original raw to save space for large strings, while keeping the index values in place.
            data[index] = None
        else:
            # Record is new or cannot be initialized by existing values. Just answer the converted
            # default value for this field model.
            sqlvalue = None

        fieldmodel = self._getFieldModel(field)
        if fieldmodel is None:
            # Could not find this field model, raise an error.
            raise ValueError('[Record.initializeField] Cannot find field descriptor of "%s" in model "%s"' % (field, self._getTable()))

        # Note that in case the field is a relation, then a Record or Selection instance is answered
        converted = fieldmodel.sql2Value(sqlvalue, id, self._db, key=self._getEncryptionKeys().get(field))

        #we can just return right now, if any of these are true:
        # the record instance has been explicitly set non-inheritable
        # the field model is not inheritable
        #  added isNoneRecord: funky things can happen inheriting values on a new record
        if self._isNoneRecord() or not self._inherit or not fieldmodel.isInherited():
            self._fields[field] = converted
            return converted


        #if we get here, we have an inherited field that needs to pull from the parent    

        parent = self._getParent()

        #if there's no parent, or the parent field is NULL, return child value directly
        if not parent or parent[field] is None:
            self._fields[field] = converted
            return converted

        #if child value is NULL, just return the parent
        if sqlvalue is None:
            converted = self._fields[field] = parent[field]
            return converted
            
        #if we get here, we have both parent and child in the desired datatype (list, set, string, whatever)
        # note one or both may be "empty" but neither of them is None
        
        def mergevalues(p,c):
            #p is parent, c is child
            assert type(p) == type(c), "Record._initializeField: mergevalues called with different types"

            def cancelnegatives(l):
                assert isinstance(l,(list,set)), "Record._initializeField: cancellation called with non-sequence"
                for v in set(l):
                    negatory = '-'+v
                    if isinstance(v,basestring) and negatory in l:
                        try:
                            l.remove(negatory)
                            l.remove(v)
                        except:
                            pass
                return l
            

            result = None
            if isinstance(p,list):
                #note that we implicitly assume that these are flat lists. Lists of lists will simply be concatenated
                
                #this eliminates duplicates while preserving order
                #seen = set()
                #return [v for v in (p+c) if v not in seen and not seen.add(v)]
                
                return cancelnegatives(p + c)
                
            elif isinstance(p,set):
                #same with sets, assume they are flat
                return cancelnegatives(p.union(c))
            elif isinstance(p,dict):
                #dicts are a little more complex. Go through and merge their elements
                result = {}
                for k in p:
                    if k in c:
                        if type(c[k]) == type(p[k]):
                            result[k] = mergevalues(p[k],c[k])
                        else:
                            result[k] = c[k]
                    else:
                        result[k] = p[k]
                
                for k in c:
                    if k not in result:
                        result[k] = c[k]
                    
                return result

            #when in doubt, return the child
            return c
        
        #return the merged
        self._fields[field] = mergevalues(parent[field],converted)
        
        return self._fields[field]

    
    def _setData(self, data=None):
        u"""
        <doc>
        The <code>_setData</code> method sets the raw <code>self._data</code> storage of the record to the optional
        <attr>data</attr> attribute using <code>list(data)</code>. If the attribute is omitted, then the raw data set is
        emptied. In case the <attr>data</attr> attribute is a tuple, it is converted into a list to allow field
        indexing.
        </doc>
        """
        self._data = list(data or [])

    def _getData(self):
        u"""
        <doc>The <code>_getData</code> method answers the stored raw data list <code>self._data</code>.</doc>
        """
        return list(self._data)

    def _readData(self, id, fields):
        u"""
        <doc>
        The <code>_readData</code> method reads the raw set of data (defined by <attr>fields</attr>) from the database
        record with <attr>id</attr>.
        </doc>
        """
        return self._db.read(self._table, id, fields)

    def _sync(self, force=False, updatemodificationtime=True):
        """
        <doc>
        Recursively synchronize the record and all related records with the database. Then sync the record, but only if
        writeable and something changed. Normally this method is called automatically when the record object is deleted.
        But sometimes it is useful to know the new <attr>id</attr> value of a record.<br/>
        The <attr>force</attr> attribute will overrule the <code>record._getChangedFields()</code>, so the
        synchronization will always be written. The attribute does <em>not</em> overrule the <code>record._readonly
        </code> setting of the record.<br/>
        If the <code>self._dummy</code> is set to <code>True</code> (using <code>self._setDummy(True)</code>) then no
        actual writing takes place. This can be used for testing applications without writing to a database. Also when
        records are not allowed to write themselves while still the record fields need to be changed, then the dummy
        flag can be used.<br/>
        The optional <attr>updatemodificationtime</attr> (with default value <code>True</code>) makes the modification
        date and time update automatically.
        <python>
        record._sync()<br/>
        print record.id
        </python>
        </doc>
        """
        saved = False
        changedFieldValues = {}
        for field in self._getChangedFields():
            if self._fields.has_key(field):
                # Copy the changed field/values
                #don't use self[field] here, because if you have set it to None, it will get re-initialized!
                changedFieldValues[field] = self._fields[field]
        if not self._dummy and not self._readonly and (force or changedFieldValues):
            # Note that we don't have to sync selection instances here, 
            # since the have no influance generating a new record id.    
            # Make sure to write the record, without deleting this instance.
            if not self._id():
                # If first time write, set creation date and time
                self._setCreationDateTime()
                if hasattr(self,'creationdatetime'):
                    changedFieldValues['creationdatetime'] = self._fields['creationdatetime']
            if updatemodificationtime and 'modificationdatetime' not in changedFieldValues: #don't override explicit update
                self._setModificationtDateTime()
                if hasattr(self,'modificationdatetime'):
                    changedFieldValues['modificationdatetime'] = self._fields['modificationdatetime']
            id = self._db.write(table=self._table, id=self._id(), fields=changedFieldValues, forceinsert=self._forceinsert)
            saved = True
            if id != self._id():
                # This is a new record, so the agent did an insert and we got the real id back.
                # Note that the direct change of id is not allowed, so we use the _forceId() method.
                self._forceId(id)
                
            self._resetChangedFields()
            self._db.deleteCache(self._table, id)  # Delete from the cache, to make sure it is read again with the current content.
        #assert saved
        self._forceinsert = False
        return saved
    
    def _close(self):
        """
        <doc>
        Delete the record from the weak agent cache. In earlier versions the record would try to sync itself but this is
        causing problems when the database connection was closed upon deletion earlier than the garbage collection of
        self. So all changed records now should be “manually” saved to the database. This does not seem to be a problem,
        since we generally do a <code>record._sync()</code> anyway.<br/>
        Instead we no raise an error if the record indicates to be changed at this point. If it is a new record (without
        id) and changed then ignore the error message.
        <python>
        record._close()
        </python>
        </doc>
        """
        if self._id():
            if not self._readonly and len(self._getChangedFields()):
                raise ValueError('[Record._close] The record "%s" with id "%s" has changed fields "(%s)" but not saved. Used record._sync to save the changes' % (self._table, self._id(), ', '.join(self._getChangedFields())))
            self._db.deleteCache(self._table, self._id())

    def _delete(self, forceDelete=False):
        """
        <doc>
        The <code>_delete</code> method sets the field <code>self.deleted</code> to <code>True</code> and calls <code>
        self._sync()</code> if the field exists. Otherwise delete the record from the database by the SQL <code>delete
        </code> query.<br/>
        If <attr>forceDelete</attr> is <code>True</code> (default is <code>False</code>) then don’t consider the <code>
        self.deleted</code> if it exists. If the flag is <code>True</code>, then the record is reallt deleted from the
        database.<br/>
        The method requires that the record has a valid <attr>id</attr> and it is not <attr>_readonly</attr>.
        <python>
        record._delete()
        </python>
        </doc>
        """
        if self._readonly:
            raise ValueError('[Record._delete] The record is readonly. Set record._readonly(False) to delete records: "%s"' % repr(self))
        if self._id() is None:
            raise ValueError('[Record._delete] Only records with assigned id can be deleted: "%s"' % repr(self))
        if not forceDelete and self._hasField('deleted'):
            self.deleted = True
            self._sync()
        else:
            self._db.deleteRecord(self._table, self._id())
            # Make the record behave as empty. Note that is may be reused now to insert another one.
            self._forceId(None) # Have to use _forceId or else we run into the protection of id.
            self._setData() # Clear set of raw data too, if there is any.

    def _getParent(self):
        u"""
        <doc>
        The <code>_getParent</code> method answers the content of the parent if (if any can be found in the model).
        Otherwise an error is raised.
        </doc>
        """
        if self._hasField('parent_id'):
            return self.parent_id
        return None

    def _setCreationDateTime(self):
        """
        <doc>
        Set the <attr>_setCreationDateTime</attr> of the record to the current date/time.<br/>
        This method is automatically called when the <code>_sync</code> applies an SQL <code>insert</code> query. No
        check is done if the fields actually exist in the record definition. If they don't, their values are ignored
        when writing the record to database.
        <python>
        record._setCreationDateTime()
        </python>
        </doc>
        """
        # Assume that the model of the record has these fields.
        # Or else they just won't be written.
        # Make sure not to set the _changedfields flag.
        if hasattr(self,'creationdatetime'):
            self.creationdatetime = DateTime(date='now').date_time

    def _setModificationtDateTime(self):
        """
        <doc>
        Set the <attr>_setModificationtDateTime</attr> of the record to the current date/time.<br/>
        This method is always automatically called when the <code>_sync</code> applies writing query. No check is done
        if the fields actually exist in the record definition. If they don't, their values are ignored when writing the
        record to database.
        <python>
        record._setModificationtDateTime()
        </python>
        </doc>
        """
        # Assume that the model of the record has these fields.
        # Or else they just won't be written
        if hasattr(self,'modificationdatetime'):
            self.modificationdatetime = DateTime(date='now').date_time
    
    def _setEncryptionKey(self,field,key):
        """
        <doc>
        For <code>EncryptedField</code fields, encryption key must be set before reading/writing the record.
        </doc>
        """
        return self._db.setEncryptionKey(field,key)

    def _getEncryptionKeys(self):
        return self._db.getEncryptionKeys()
        
