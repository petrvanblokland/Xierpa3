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
#      baserecord.py
#
class BaseRecord(object):

    # NO REGULAR CLASS VALUES
    # They interfere with field names, if we want to allow field names with initialize capitals.

    def _getAgent(self):
        u"""
        <doc>
        The <code>_getTable</code> method answers the name of the datastore of the record instance. Typically the
        value <code>self._db</code> is answered.
        </doc>
        """
        return self._db

    def _getTable(self):
        u"""
        <doc>
        The <code>_getTable</code> method answers the name of the table of the record instance. Typically the
        value <code>self._table</code> is answered.
        </doc>
        """
        return self._table

    def _getModel(self):
        u"""
        <doc>
        The <code>_getModel</code> method answers the model of the record. Typically the value <code>self.__model</code>
        is answered.
        </doc>
        """
        if not self._db:
            from basemodel import BaseModel
            return BaseModel()
        return self._db.getModel(self._table)

    def _getFieldModel(self, field):
        u"""
        <doc>
        The <code>_getFieldModel</code> method answers the field model of the <attr>field</attr> of this record.
        If the model does not exist or if the field does not exist, then answer <code>None</code>.
        </doc>
        """
        return self._getModel()._fields.get(field)

    def _getIndexOfField(self, field):
        u"""
        <doc>
        The <code>_getIndexOfField</code> method answers the index of <attr>field</attr> in the record
        list of fields. If the field cannot be found, then answer <code>None</code>.
        </doc>
        """
        try:
            return list(self._getFieldNames()).index(field)
        except IndexError:
            pass
        return None

    def _hasField(self, field):
        u"""
        <doc>
        The <code>_hasField</code> answers a boolean id the key is available as field. We want records
        to be compatible with regular <code>dict</code> objects, so also <code>has_key</code> is defined
        as method. This implies that field names are restricted not to be named "get" or "has_key".
        Note that the following notations are all equivalent:
        <python>
        record._hasField('lastname')<br/>
        record._has_key('lastname')<br/>
        record.has_key('lastname')<br/>
        </python>
        </doc>
        """
        self._readdata()
        return field in self._getFieldNames()

    # To make a record compatible with a dictionary, we allow get as method.
    # This implies that field names are restricted not to be named "get" or "has_key"
    has_key = _hasField
    _has_key = _hasField

    def _getFieldNames(self):
        u"""
        <doc>The <code>_getFieldNames</code> method answers an unsorted list of field names of the record as defined in
        the model. It answers <code>self._fields or self._getModel()._getFieldNames()</code>.<br/>
        <python>
        record._getFieldNames()<br/>
        </python>
        </doc>
        """
        # return self._getModel()._getFieldNames()
        return self._fieldnames or self._getModel()._getFieldNames()

    def _getFields(self):
        u"""
        <doc>
        The <code>_getFields</code> method answers a dictionary with field names as key and rendered SQL
        values.
        </doc>
        """
        fields = {}
        for fieldname in self._getFieldNames():
            fields[fieldname] = self.get(fieldname)
        return fields

    def _isNoneRecord(self):
        u"""
        <doc>
        The <code>isNoneRecord</code> method answers the boolean flag if this record is an instance of
        <code>NoneRecord</code>. The behavior is to answer <code>False</code>.
        </doc>
        """
        return False
