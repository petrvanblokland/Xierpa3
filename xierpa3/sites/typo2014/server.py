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
#    server.py
#
from client import Client
from xierpa3.server.twistedmatrix.twistedserver import TwistedServer

class Server(TwistedServer):
    pass

if __name__ == '__main__':
    client = Client()
    port = 2014
    Server().start(client, port)
