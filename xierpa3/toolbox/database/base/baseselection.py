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
#     baseselection.py
#
class BaseSelection(object):
    u"""
    <doc>
    The <code>BaseSelection</code> class defines the generic behavior of a selection of <code>Record</code>
    instances from the database.
    </doc>
    """
    def _getTable(self):
        u"""
        <doc>
        The <code>_getTable</code> method answers the table of the <code>Selection</code> instance
        as defined by <code>self._table</code>.
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
        return self._db.getModel(self._getTable())

    def _getFieldModel(self, field):
        u"""
        <doc>
        The <code>_getFieldModel</code> method answers the field model of the <attr>field</attr> of this record.
        </doc>
        """
        return self._getModel().get(field)

    def _isNoneSelection(self):
        u"""
        <doc>
        The <code>_isNoneRecord</code> method answers the boolean flag if this record is an instance of <code>NoneSelection</code>.
        The behavior is to answer <code>False</code>.
        </doc>
        """
        return False
