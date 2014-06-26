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
#   simpledbadapter.py
#
from random import randint
from xierpa3.adapters.adapter import Adapter
#from xierpa3.toolbox.database.simpledb.simpledbdict import SimpleDBDict

class SimpleDBAdapter(Adapter):

    #    @@@ Under development

    def __init__(self):
        Adapter.__init__(self)
        #self.blurb = SimpleDBDict

if __name__ == "__main__":
    """
    from xierpa3.toolbox.database.simpledb.simpledbdict import SimpleDBDict
    db = SimpleDBDict('petr.com', {}, C.ACCESSKEYID, C.SECRETACCESSKEY)
    domain = db.getDomain('petr.com')
    # item = domain.new_item('record1')
    item = domain.get_item('record1')
    # item['text'] = 1234
    print item
    """

