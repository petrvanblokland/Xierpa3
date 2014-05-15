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
#    noneselection.py
#
from baseselection import BaseSelection

class NoneSelection(BaseSelection):

    def __init__(self, db, table):
        u"""
        <doc>
        Create a <code>NoneSelection</code> instance that behaves exactly as a normal selection of type <attr>table</attr>
        except that is does not save to the database and all behavior is <code>None</code> and empty. The idea
        that whatever method or action performed on a <code>NoneSelection</code> instance, nothing happens,
        but also never an error will occur. This allows the use of selections in chain queries, without
        intermediate testing for valid results.
        </doc>
        """
        self._table = table                # Name of the table of this record.
        self._db = db
        
    def __str__(self):
        return `self`
        
    def __repr__(self):
        # Using self._getTable() does not work here.
        return '[NoneSelection-%s]' % self._table
    
    def __setitem__(self, index, nonerecord):
        pass

    def __getitem__(self, index):
        return None

    def __setattr__(self, field, value):
        self.__dict__[field] = value
        
    def __getattr__(self, field):
        if field.startswith('_'):
            return self.__dict__[field]
        return []
        
    def __iter__(self):
        return self

    def next(self):
        raise StopIteration
        
    def __len__(self):
        return 0
        
    len = __len__

    def _isNoneSelection(self):
        u"""
        <doc>
        The <code>_isNoneRecord</code> method answers the boolean flag if this record is an instance of <code>NoneSelection</code>.
        The behavior is to answer <code>True</code>.
        </doc>
        """
        return True

