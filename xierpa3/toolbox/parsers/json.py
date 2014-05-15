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
#    json.py
#
try:
    import cjson
except Exception, e:
    print 'Error loading python-cjson'
    print e
    import json
    
    class cjson:
        def encode(self, s):
            return json.loads(s)
        def decode(self, s):
            return json.dumps(s)
