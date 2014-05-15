# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------

#first try loading native OrderedDict (requires Python2.7)
try:
    from collections import OrderedDict
except:
    from twisted.python.util import OrderedDict    
