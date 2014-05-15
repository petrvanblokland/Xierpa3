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
#    recordcache.py
#
import weakref
from xierpa3.toolbox.transformer import TX

class RecordCache(object):
    u"""
    <doc>
    The <code>RecordCache</code> class implements the cache the records "outside" the database as weakref, 
    so record get called on __del__ when deleted, although the cache still has a reference to the record.
    Note that there can only be one record cache in a running system, since there may be read/write operations
    on the same database by several websites simultaneously.<br/>
    @@@ It may be a good addition to keep some size and successfully-gets statistics.
    <python>    
    *** class R:
    ...     def __del__(self):
    ...         print 'Deleting r'
    ...     def __repr__(self):
    ...         return 'Instance of R'
    *** r = R()
    *** cache = RecordCache()
    *** cache.put('aaa', 'bbb', 23, r)
    *** r2 = cache.get('aaa', 'bbb', 23)
    *** r is r2
    True
    *** print r2
    Instance of R
    *** r = r2 = None
    Deleting r
    *** r2 = cache.get('aaa', 'bbb', 23)
    *** print r2
    None
    </python>
    """    
    def __init__(self):
        u"""
        <doc>
        The <code>__init__</code> constructor installs the actual <code>self.records</code>.
        </doc>
        """
        self.records = {}

    def __len__(self):
        return len(self.records)

    def __repr__(self):
        return 'RecordCache:%s' % `self.getRecords()`

    def makekey(self, db, table, id):
        return '%s.%s.%s' % (db, table, self.TX.asId(id))

    def get(self, db, table, id):
        u"""
        <doc>
        The <code>get</code> method gets the record from the weakref in cache. But only if 
        <attr>id</attr> is not <code>None</code>. Otherwise answer <code>None</code>.
        </doc>
        """
        if id is None:
            return None
        weakrecord = self.records.get(self.makekey(db, table, id))
        if weakrecord is None:
            return None
        return weakrecord()

    def put(self, db, table, id, record):
        u"""
        <doc>
        The <code>put</code> method puts the record as weakref in cache, only of <attr>id</attr> 
        is not <code>None</code>.
        </doc>
        """
        if id is not None:
            self.records[self.makekey(db, table, id)] = weakref.ref(record)

    def delete(self, db, table, id):
        u"""
        <doc>
        The <code>delete</code> method deletes the record only if it actually exists.
        </doc>
        """
        key = self.makekey(db, table, id)
        if self.records.has_key(key):
            del self.records[key]

    def clear(self):
        u"""
        <doc>
        The <code>clear</code> method clears all records from cache. Use for debugging only.
        </doc>
        """
        self.records = {}

    def getRecords(self):
        u"""
        <doc>
        The <code>getRecords</code> method answers the a list of actual records.
        </doc>
        """
        t = []
        for w in self.records.values():
            t.append(w())
        return t
