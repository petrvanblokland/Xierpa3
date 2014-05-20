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
#    c_json.py
#
try:
    import cjson #@UnusedImport
except Exception, e:
    print '### Warning: Python cjson not available. Using json instead.'
    # print e
    import json
    
    class cjson(object):
        @classmethod
        def encode(cls, s):
            return json.loads(s)
        @classmethod
        def decode(cls, s):
            return json.dumps(s)
