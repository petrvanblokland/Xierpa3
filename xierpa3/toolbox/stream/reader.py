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
#    writer.py
#
#    Behaves like s cStringIO write buffer, but we need it to check for
#    normal an unicode strings.
#    The stringIO buffer will automatically close when the instance is deleted.
#
from cStringIO import StringIO
import codecs

class Reader:

    def __init__(self, s):
        self.index = 0
        self.size = len(s)
        self.buffer = StringIO(s)
        self.reader = codecs.getreader("utf-8")(self.buffer)    
        
    def __del__(self):
        self.close()
        
    def getc(self):
        return self.reader.read(1)
    
    def read(self, until=None):
        self.index = len(self)
        return self.reader.read()
    
    def seek(self, t):
        self.index = t
        return self.reader.seek(t)
        
    def peek(self, i=None):
        if i is None:
            i = self.index
        c = self.getc()
        self.seek(self.index-1)
        return c
    
    def __len__(self):
        return self.size - self.index
        
    def close(self):
        if self.reader is not None:
            self.buffer.close()
            self.buffer = None
            self.reader = None

