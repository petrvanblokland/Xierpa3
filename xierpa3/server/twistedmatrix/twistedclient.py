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
#     twistedclient.py
#
import sys, os
from xierpa3.server.base.baseclient import BaseClient
#from xierpa3.server.base.httpclient import HttpClient
from twisted.web.resource import Resource
from twisted.internet import reactor

class TwistedClient(BaseClient, Resource):

    def isLeaf(self):
        u"""
        The ``isLeaf`` method is required for Twisted clients, inheriting from ``Resource``.
        """
        return True

    def reload(self):
        self.showStopLabel()
        args = [sys.executable] + sys.argv
        new_environ = os.environ.copy()
        print args, new_environ
        getattr(reactor, 'stop')()
