# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------

from xierpa3.server.twistedmatrix.twistedclient import TwistedClient
from xierpa3.sites.doingbydesign.doingbydesign import DoingByDesign

class Client(TwistedClient):

    # Other examples to be added here as soon as they work.
    doingByDesign = DoingByDesign(title='Doing by Design')
    
    THEMES = {
        # Matching theme names with Theme instances.
        TwistedClient.DEFAULTTHEME: doingByDesign,
        'dbd': doingByDesign,  # http://localhost:8050/dbd (same as default site)
    }
