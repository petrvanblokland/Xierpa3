# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xpyth: xslt/xml server
#    (c) 2006 buro@petr.com, www.petr.com
#    
#    X I E R P A 3
#
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    xmlfiledict.py
#
#    This is a thin wrapper around xpyth.plistlib, allowing to read and write
#    Python dicts with simple values from and to XML files using the
#    Property List (plist) format.
#
#    This module checks the file's modification time upon each access; if
#    the file has been changed it will be parsed again.
#
import os
from plistlib import readPlist, writePlist

class XMLFileDict:

    def __init__(self, path, create=False, d=None):
        self.path = path                                # Just take path as it is
        self.modified = None                            # Make sure first update works
        self.d = {}                                        # At least we have an empty dict
        if d:
            self.d.update(d)

        if not os.path.exists(path) and create:
            self.save()

    def __getitem__(self, key):
        self._checkmodified()
        return self.d[key]

    def get(self, key, default=None):
        self._checkmodified()
        return self.d.get(key, default)

    def __setitem__(self, key, item):
        # Default is write protected
        raise KeyError, '[XMLFileDict] Cannot write items ("%s" on key "%s")' % (item, key)

    def __repr__(self):
        self._checkmodified()
        return repr(self.d)

    def has_key(self, key):
        self._checkmodified()
        return self.d.has_key(key)

    __contains__ = has_key

    def keys(self):
        self._checkmodified()
        return self.d.keys()

    def _checkmodified(self, create=None):
        try:
            open(self.path, 'rb')
        except IOError:
            if create:
                # the file does not exist yet, but will be created; do nothing.
                return
            else:
                raise IOError, '[XMLFileDict] Cannot find file "%s"' % self.path

        stats = os.stat(self.path)

        if self.modified != stats.st_mtime:
            #print '=4=4=4=2----------- READING', self.path
            d = readPlist(self.path)
            if d is None:
                self.d = {}
            else:
                self.d = dict(d)
            self.modified = stats.st_mtime

    def save(self):
        try:
            f = open(self.path, 'rw')
            writePlist(self.d, f)
            f.close()
        except IOError:
            raise IOError, '[XMLFileDict] Cannot create file "%s"' % self.path

def new(path):
    return XMLFileDict(path)

_cache = {}
def getCachedFileDict(path):
    if path in _cache:
        filedict = _cache[path]
    else:
        filedict = _cache[path] = new(path)
    return filedict
