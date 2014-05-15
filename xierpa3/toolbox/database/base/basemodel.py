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
#      basemodel.py
#
class BaseModel(object):

    def __init__(self):
        self._fields = {}

    def __repr__(self):
        return 'Model-%s' % self.__class__.__name__

    def get(self, field):
        return getattr(self, field, None)
