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
#     selection.py
#
import sys
from baseselection import BaseSelection

class Selection(BaseSelection):
    u"""
    <doc>
    The <code>Selection</code> class implements the behavior of an SQL selection of records.<br/>
    Best usage is to get a selection by calling the function <code>getSelection</code><br/>
    <python>
    getSelection(agent, tablename, where=where, order=order, start=start, slice=slice)<br/>
    getSelection(agent, query=query)
    </python>
    <br/>
    A <code>Selection</code> instance behaves “lazy”: it does not actually read from the database, until
    it really needs the information. And then the following happens:
    <list>
        <sep>Read a selection of (raw) records using SQL <attr>where</attr> as clause.</sep>
        <sep>The raw data of records are stored as tuple.</sep>
        <sep>Only when a record is referred to by an index, then it gets instantiated to a <code>Record</code> 
        instance, where it will replace the original tuple data in the selection list.</sep>
    </list>
    Set the <attr>initialized</attr> attribute to <code>True</code> to prevent the selection to read from the
    database. This option is used, when the application wants to fill the selection with the <code>_appendraw</code>
    method. Default value for <attr>initialized</attr> is <code>False</code><br/>
    If the <code>query</code> attribute is defined, that this string is used as SQL query. The attributes <attr>where</attr>,
    <attr>order</attr>, <attr>start</attr> and <attr>slice</attr> are ignored then.<br/>
    <br/>
    All method names start with an underscore to avoid collision with all possible field names. 
    The record is constructed in such a way, that all fields are available as object attribute names.<br/>
    <br/>
    TODO:
    If the tablename of a selection contains one or more periods, then it is assumed that the selection is a result of
    a join operation. All fields in are then available with periods. @@@
    Better than a separate Join class?
    
    Selection(self._db, 'element.item_id', where='...', order='item.name')
    

        #     Inner join
        #     SELECT column_name(s)
        #     FROM table_name1
        #     INNER JOIN table_name2 
        #     ON table_name1.column_name=table_name2.column_name
        #     
        #     Left join
        #     SELECT column_name(s)
        #     FROM table_name1
        #     LEFT JOIN table_name2 
        #     ON table_name1.column_name=table_name2.column_name
        #     
        #     RIght join
        #     SELECT column_name(s)
        #     FROM table_name1
        #     RIGHT JOIN table_name2 
        #     ON table_name1.column_name=table_name2.column_name
        #     
        #     Full join
        #     SELECT column_name(s)
        #     FROM table_name1
        #     FULL JOIN table_name2 
        #     ON table_name1.column_name=table_name2.column_name

    </doc>
    """
    def __init__(self, agent, table, mode=None, where=None, order=None, start=None, slice=None, readonly=True,
        initialized=False, query=None, fields=None, distinct=None, astable=None):
        u"""
        <doc>
        The <code>__init__</code> constructor creates a new <code>Selection</code> instance from the accumulated
        query as constructed from the attributes. The actual query is performed upon the first record access.
        This allows the redefinition of the attributes by using methods like <code>self._where</code> and
        <code>__order</code>.<br/>
        The <attr>agent</attr> is supposed to handle the actual constructed query.<br/>
        </doc>
        """
        self._index = 0                # Used to iterate
        
        self._initialized = initialized
        self._db = agent
        self._table = table
        self._astable = astable
        self._fieldnames = fields or agent.getFieldNames(table)
        self._readonly = readonly
        self._records = []                # Initial raw list that comes from the agent. Mark that we need initialization.
        self._mode = mode                # Optional mode flag to use in hooks
        self._where = where
        self._order = order
        self._start = start
        self._slice = slice
        self._distinct = distinct
        self._query = query                # Optional query. If defined, then use this instead of anything else.

    def __repr__(self):
        return (u'%s(%s)[table=%s where=%s fieldnames=%s]' % (self.__class__.__name__, len(self) or '?', self._table, self._where, self._fieldnames)).encode('utf-8')

    def __str__(self):
        return `self`

    def __len__(self):
        u"""
        <doc>
        The <code>__len__</code> (<code>len(self)</code>) method answers the length of the selection.
        If the selection it not instantiated, then it is initialized first.
        </doc>
        """
        self._initialize()
        if not self._records:
            return 0
        return len(self._records)

    def __setitem__(self, index, item):
        #     Used by random.choice
        self._records[index] = item

    def __getitem__(self, index):
        u"""
        <doc>
        The <code>self[index]</code> (<code>self.__getitem__(index)</code> answers the record at <attr>index</attr> if the attribute is a
        number. Otherwise the <attr>index</attr> is used as a field in combination with <code>getattr(self, index)</code> to answer a
        selection of values.
        </doc>
        """
        if isinstance(index, basestring):
            return getattr(self, index)
        return self._instantiate(index)

    def __getattr__(self, name):
        u"""
        <doc>
        The <code>selection[name]</code> (<code>__getattr__</code>) method answers a list of the field
        values indicated by <attr>name</attr> of all selected records.<br/>
        Check if this is a private field request (text on initial <code>'_'</code>).
        </doc>
        """
        if not name.startswith('_') and not name in ('has_key', 'get'):
            # Make sure we got the record data from the database
            fieldModel = self._getModel()[name]
            values = []
            if fieldModel:
                for record in self:
                    values.append(record[name])
            return values

        # This name refer to a method or another private method, answer this method.
        return self.__dict__[name]

    def __nonzero__(self):
        self._initialize()
        return bool(self._records)

    def __coerce__(self, other):
        return self._records, other

    def __iter__(self):
        self._initialize()
        for _, record in enumerate(self._instantiateAll()):
            yield record

    def __getslice__(self, i, j):
        u"""
        <doc>
        The <code>self[i:j]</code> method (<code>__getslice__</code>) answers a slice of the current selection
        as new <code>Selection</code> instance.
        </doc>
        """
        selection = Selection(self._db, self._table, readonly=self._readonly, initialized=True)
        for index in range(i, min(len(selection), j)):
            selection._append(self[index])
        return selection

    def __contains__(self, r):
        self._initialize()
        for record in self:
            if record.id == r:
                return True
        return False

    def _instantiate(self, index):
        self._initialize()
        if index >= len(self._records):
            raise IndexError('[Selection._instantiate] Index "%s" is out of range' % index)
        r = self._records[index]
        if isinstance(r, (tuple, list)):
            data = self._records[index]
            fieldnames = self._getFieldNames()
            r = self._records[index] = self._db.getRecord(self._table, id=data[fieldnames.index('id')],
                data=data, fields=fieldnames, readonly=self._readonly)
        return r

    def _instantiateAll(self):
        records = []
        for index, _ in enumerate(self._records):
            records.append(self._instantiate(index))
        return records

    def _initialize(self):
        u"""
        <doc>
        The <code>_initialize</code> method checks if the accumulated query was already performed. 
        Otherwise construct the query and get the selection from the agent.
        </doc>
        """
        # Make sure that we have read the data.
        if not self._initialized:
            if self._query:
                self._records = self._db.getQuery(self._query)
            else:
                self._records = self._db.select(table=self._table, fields=self._getFieldNames(), astable=self._astable, order=self._order,
                    slice=self._slice, start=self._start, readonly=self._readonly, where=self._where, distinct=self._distinct)
            self._initialized = True

    def _where(self, where):
        u"""
        <doc>
        The primary usage of the <code>_where</code> method is to modify the <attr>where</attr> clause of the current 
        <code>Selection</code> instance if it is generated by a <code>one2many</code> reference. The method
        answers a new <code>Selection</code> instance with all values copied from <code>self</code> except
        for the changed <attr>where</attr> clause. Note that there is not really overhead creating a new
        <code>Selection</code> instance, since a selection only reads data when the content is actually referenced.<br/>
        If the current selection already has a where clause defined, then merge the two clauses with a bracket <code>(...) and (...)</code>.
        If <attr>where</attr> is <code>None</code>, then ignore the clause and only use the existing internal <code>self._where</code>.<br/>
        <seealso>select</seealso>
        <python>
        organization.department_id._where("name = 'Sales'")
        </python>
        </doc>
        """
        if self._where and where is not None:
            where = '(' + self._where + ') AND (' + where + ')'
        else:
            where = where or self._where
        return Selection(self._db, self._table, self._mode, where, self._order, self._start, self._slice, self._readonly)

    def _getWhere(self):
        u"""
        <doc>
        The <code>_getWhere</code> method answers the <code>self._where</code> clause of the selection.
        This method is here mostly for debugging reasons, since the moment a <code>Selection</code> is
        generated and the actual reading of record is not the same. The method allows the programmer
        to see what the actual where clause is that the selection <em>will</em> be selecting with.
        </doc>
        """
        return self._where

    def _order(self, order):
        u"""
        <doc>
        The primary usage of the <code>_order</code> method is to modify the <attr>order</attr> value of the current 
        <code>Selection</code> instance if it is generated by a <code>one2many</code> reference. The method
        answers a new <code>Selection</code> instance with all values copied from <code>self</code> except
        for the changed <attr>order</attr> value. Note that there is not really overhead creating a new
        <code>Selection</code> instance, since a selection only reads data when the content is actually referenced.<br/>
        If the <attr>order</attr> attribute is a list, then convert it to a comma separated string. Otherwise
        the <attr>order</attr> attribute has the standard SQL syntax.<br/>
        <seealso>select</seealso>
        <python>
        organization.order('id')<br/>
        organization.department_id.order('name DESC')<br/>
        organization.department_id.address_id.order('lastname, firstname ASC')<br/>
        </python>
        </doc>
        """
        if isinstance(order, (list, tuple)):
            order = ','.join(order)
        return Selection(self._db, self._table, self._mode, self._where, order, self._start, self._slice, self._readonly)

    def _start(self, start):
        u"""
        <doc>
        The primary usage of the <code>_start</code> method is to modify the <attr>start</attr> value of the current 
        <code>Selection</code> instance if it is generated by a <code>one2many</code> reference. The method
        answers a new <code>Selection</code> instance with all values copied from <code>self</code> except
        for the changed <attr>start</attr> value. Note that there is not really overhead creating a new
        <code>Selection</code> instance, since a selection only reads data when the content is actually referenced.<br/>
        <seealso>select</seealso>
        <python>
        organization.department_id.order('name')
        </python>
        </doc>
        """
        return Selection(self._db, self._table, self._mode, self._where, self._order, start, self._slice, self._readonly)

    def _slice(self, slice):
        u"""
        <doc>
        The primary usage of the <code>_slice</code> method is to modify the <attr>slice</attr> value of the current 
        <code>Selection</code> instance if it is generated by a <code>one2many</code> reference. The method
        answers a new <code>Selection</code> instance with all values copied from <code>self</code> except
        for the changed <attr>slice</attr> value. Note that there is not really overhead creating a new
        <code>Selection</code> instance, since a selection only reads data when the content is actually referenced.<br/>
        <seealso>select</seealso>
        <python>
        organization.department_id.order('name')
        </python>
        </doc>
        """
        return Selection(self._db, self._table, self._mode, self._where, self._order, self._start, slice, self._readonly)

    def _select(self, where=None, order=None, start=None, slice=None):
        u"""
        <doc>
        The primary usage of the <code>_select</code> method is modify (a combination of) the <attr>where</attr>, <attr>order</attr>,
        <attr>start</attr> and <attr>slice</attr> values of the current 
        <code>Selection</code> instance if it is generated by a <code>one2many</code> reference. The method
        answers a new <code>Selection</code> instance with all values copied from <code>self</code> except
        the values of the defined attributes. Note that there is not really overhead creating a new
        <code>Selection</code> instance, since a selection only reads data when the content is actually referenced.<br/>
        If the current selection already has a where clause defined, then merge the two clauses with an <code>AND</code>.
        <seealso>select</seealso>
        <python>
        organization.department_id.address._select(where="firstname ~* 'Jan'", order='lastname', start=10).
        </python>
        </doc>
        """
        if where and self._where:
            where = self._where + ' AND ' + where
        return Selection(self._db, self._table, self._mode, where or self._where, order or self._order, start or self._start, slice or self._slice, self._readonly)

    def _keys(self):
        u"""
        <doc>
        Ansert a unsorted list of fields name for the table of this selection.
        </doc>
        """
        return self._db.getDescriptor(self._table).keys()

    def _append(self, item):
        u"""
        <doc>
        The <code>_append</code> method appends the record or selection to the current record list.
        </doc>
        """
        if isinstance(item, Selection):
            self._records += item._getRecords()
        else: # Assume it is an instance of Record
            self._records.append(item)

    def _getRecords(self):
        u"""
        <doc>
        The <code>_getRecords</code> answers the current list of (all instantiated) records.
        </doc>
        """
        return self._records

    def _getFieldNames(self):
        u"""
        <doc>
        The <code>_fieldNames</code> method does answer an unsorted list of fieldnames of the record as defined
        in the model. The method makes sure that <code>self._filenames</codeL is cast to a list, to
        allow indexing the position of specific field names.
        </doc>
        """
        return list(self._fieldnames)

    def _dict(self, field=None):
        u"""
        <doc>
        Answer a dictionary where the key the content of the defined field and the values are a new <code>Selection</code>
        instances of records.<br/>
        The order of of the records in the selections is identical as they came from the query result.<br/>
        If the <attr>fields</attr> is omitted of <code>None</code>, then use the <code>'id'</code> as field name.<br/>
        <note>We don’t need to instantiate the records, since we put them directly into the new selection.
        This selection instance will instantiate <code>Record</code> objects if needed.</note>
        </doc>
        """
        if field is None:
            field = 'id'
        d = {}

        for record in self:
            d[field]._append(record[field])
        return d

    def _deleteAll(self):
        u"""
        <doc>
        The <code>_deleteAll</code> method deletes all records in the current selection.
        </doc>
        """
        for record in self:
            record._delete()
        self._records = []

    def _list(self, field=None):
        u"""
        <doc>
        The <code>_list</code> method does answer a list of the values of the named <attr>field</attr> for all records
        in the current selection. The <code>_list</code> method is equivalent to the use of field names directly as
        attributes to a <code>Selection</code> instance. 
        The following lines are equivalent.
        <python>
        selection._list('lastname')<br/>
        selection.lastname
        </python>
        </doc>
        """
        if field is None:
            return [record._dict() for record in self]
        else:
            return [record[field] for record in self]

    def _listNotEmpty(self, field=None):
        u"""
        <doc>
        The <code>_listNotEmpty</code> method does answer a list of the not-empty values of the named <attr>field</attr> for all records.<br/>
        If the <attr>fields</attr> is omitted of <code>None</code>, then use the <code>'id'</code> as field name.<br/>
        </doc>
        """
        if field is None:
            field = 'id'
        result = []

        for record in self:
            value = record[field]
            if not value is None:
                result.append(value)
        return result

    def _find(self, field, value, operator='='):
        u"""
        <doc>
        The <code>_find</code> does answer a new <code>Selection</code> with only the records that fit the field/value combination as compared
        by the value of the <attr>operator</attr> attribute.<br/>
        The <attr>operator</attr> attribute can be <code>=</code> (default), <code>~*</code>
        and <code>~</code>, so the comparison behaves identical to SQL queries.
        </doc>
        """
        # Create a new empty selection (set the initialized attribute to True, to prevent the selection read from the database).
        s = Selection(self._db, self._table, readonly=self._readonly, initialized=True)
        for record in self:
            v = record[field]
            if operator == '=':
                if v == value:
                    s._append(record)
            elif operator == '~*':
                if v and str(v).lower() == str(value).lower():
                    s._append(record)
            elif operator == '~':
                if v and str(v) == str(value):
                    s._append(record)
        return s

    def _sum(self, field):
        u"""
        <doc>
        Answer the total sum of the value of <attr>field</attr>. 
        </doc>
        """
        sum = 0

        for record in self:
            sum += record[field] or 0
        return sum

    def _max(self, field):
        u"""
        <doc>
        Answer the maximum value of the <attr>field</attr> content as interpreted as number. 
        </doc>
        """
        maxvalue = -sys.maxint

        for record in self:
            try:
                maxvalue = max(maxvalue, float(record[field]))
            except TypeError, ValueError:
                pass
        return maxvalue

    def _min(self, field):
        u"""
        <doc>
        Answer the minimum value of the <attr>field</attr> content as interpreted as number.
        </doc>
        """
        minvalue = sys.maxint

        for record in self:
            try:
                minvalue = min(minvalue, float(record[field]))
            except TypeError, ValueError:
                pass
        return minvalue

    def _set(self, field):
        u"""
        <doc>
        Answer an unsorted list of the unique values of the named <attr>field</attr> for all records.<br/>
        <note>We don’t need to instantiate the records, since we get them directly from the raw selected data.</note>
        </doc>
        """
        return set(self._list(field))

    def _get(self, index):
        u""" 
        <doc>
        Answer the record at position <attr>index</attr>. We want selections
        to be compatible with regular <code>dict</code> objects, so also <code>get</code> is defined
        as method. This implies that field names are restricted not to be named "get" or "has_key".
        </doc>
        """
        return self[index]

    # To make a recor compatible with a dictionary, we allow get as method.     
    # This implies that field names are restricted not to be named "get" or "has_key"
    get = _get

    def _getids(self):
        u"""
        <doc>
        Answer a list of all ids of the current selection.<br/> 
        <note>We don’t need to instantiate the records, since we get them directly from the raw selected data.</note>
        </doc>
        """
        #
        self._initialize()
        ids = []
        for record in self:
            ids.append(record.id)
        return ids

