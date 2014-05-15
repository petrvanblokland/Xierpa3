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
#    simpledbdict.py
#
from simpledbconnector import SimpleDBConnector

class SimpleDBDict(SimpleDBConnector):

    TABLE_DICT = 'dict'

    def __init__(self, name, model, accesskey, secretaccesskey):
        self.name = name
        self.model = model
        self.initializeConnector(accesskey, secretaccesskey)

    def __getitem__(self, key):
        result = self.get(key)
        if not result:
            raise KeyError
        return result

    def __setitem__(self, key, value):
        self.set(key, value)

    def get(self, key):
        query = u"""SELECT * FROM  "%s" WHERE id = '%s'""" % (self.TABLE_DICT, key)
        return self.rawQuery(self.name, query)

    def set(self, key, item):
        # TODO: finish this
        pass
