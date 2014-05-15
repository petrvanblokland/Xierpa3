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
#    nonerecord.py
#
from baserecord import BaseRecord
from noneselection import NoneSelection

class NoneKey(object):

    def _id(self):
        return 0

class NoneRecord(BaseRecord):

    def __init__(self, db, table, id=None, readonly=False, data=None, forceinsert=False, **args):
        u"""
        <doc>
        Create a <code>NoneRecord</code> instance that behaves exactly as a normal record of type <attr>table</attr>
        except that is does not save to the database and all behavior is <code>None</code> and empty.<br/>
        Since the behavior of the <code>NoneRecord</code> requires methods to be present, the record
        stores attributes just like normal records do. The difference is that they never will save
        to the database.</doc>
        """
        self._table = table                # Name of the table of this record.
        self._db = db

    def __str__(self):
        return '0'

    def __repr__(self):
        return 'NoneRecord-%s(id=%s)' % (self._table or None, self._id())

    def __bool__(self):
        return False

    def __nonzero__(self):
        return False

    def __getitem__(self, field):
        if field == 'id':
            return 0
        fieldmodel = self._getFieldModel(field)
        if fieldmodel is None or fieldmodel.isIdField():
            return None

        if fieldmodel.isMany2OneField():
            # Create a new NoneRecord instance that fits the model of the reference.
            return NoneRecord(self._getAgent(), fieldmodel.getToModel())

        if fieldmodel.isOne2ManyField():
            # Create a new NoneSelection instance that fits the model of the reference.
            return NoneSelection(self._getAgent(), fieldmodel.getFromModel())

        return None

    def __setitem__(self, field, value):
        pass

    def __len__(self):
        return 0

    def __long__(self):
        return 0

    __int__ = __long__

    def __hash__(self):
        return 0

    def __ne__(self, r):
        return True

    def __eq__(self, r):
        return False

    def __getattr__(self, field):
        fieldvalue = self[field]
        if fieldvalue is not None:
            return fieldvalue
        if field.startswith('_'):
            if not self.__dict__.has_key(field):
                return None
        return None

    def __setattr__(self, field, value):
        if field.startswith('_'):
            self.__dict__[field] = value

    def _get(self, field):
        return None

    def _getalien(self, field):
        return None

    def _getParent(self, table=None):
        return NoneRecord()

    def _setparent(self):
        pass

    def _getchildren(self, where=None, order=None, start=0, slice=None):
        return NoneSelection()

    def _copy(self):
        return self

    def _new(self):
        return self

    def _dict(self):
        return {}

    def _id(self):
        return 0

    def _setReadOnly(self, readonly):
        pass

    def _relatetTo(self, record=None, relation=None):
        pass

    def _newRelation(self, table, relation=None, readonly=True):
        return NoneRecord(self._db, table)


    def _forceid(self, id):
        pass

    def _isNew(self):
        return True

    def _readdata(self):
        pass

    def _setdata(self, data):
        pass

    def _close(self):
        pass

    def _delete(self):
        pass

    delete = _delete

    def key(self):
        return NoneKey()

    def put(self):
        pass

    _save = put

    def _isNoneRecord(self):
        return True

