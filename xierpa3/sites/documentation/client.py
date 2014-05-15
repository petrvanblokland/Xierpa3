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
from xierpa3.server.twistedmatrix.twistedclient import TwistedClient
from documentation import Documentation  

class Client(TwistedClient):

    documentation = Documentation()

    THEMES = {
        # Matching theme names with Theme instances.
        TwistedClient.DEFAULTTHEME: documentation,
        'documentation': documentation,
        'doc': documentation,
    }
