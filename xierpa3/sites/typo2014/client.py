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
from xierpa3.sites.documentation.documentation import Documentation
from typo2014 import Typo2014

class Client(TwistedClient):

    typo2014 = Typo2014()
    documentation = Documentation()

    THEMES = {
        # Matching theme names with Theme instances.
        TwistedClient.DEFAULTTHEME: typo2014,
        'typo': typo2014,
        'doc': documentation,
    }
