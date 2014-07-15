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
#    http://twistedmatrix.com/documents/10.1.0/web/howto/using-twistedweb.html
#
# ----------------------------------------------------------------------------------------------------------------------

from twisted.internet import reactor
from twisted.web import server

from xierpa3.server.base.baseserver import BaseServer
from xierpa3.server.base.scheduler import Scheduler

class TwistedServer(BaseServer):

    C = BaseServer.C 
    
    def start(self, client, port=80):
        u"""
        Start the server by creating a parallel process and then starting the server. The multi-processing only
        starts if configuration value <code>Constants.USE_MULTIPROCESSING</code> is <code>True</code>. Note that Eclipse
        crashes Python when debugging the child process. For debugging that part of the code, the server has to run in
        single-process mode.
        """
        print '... Starting Xierpa 3 server'
        if self.C.USE_MULTIPROCESSING:
            print '... Starting multi-processing'
            from multiprocessing import Process
            p = Process(target=self.startScheduler, args=(client,))
            p.start()
        else:
            print '... Running in single process mode (Multi-processing disabled)'

        self.startServer(client, port)

    def startScheduler(self, client):
        u"""
        The <code>startScheduler</code> method is called from the <code>self.start</code> through are multiprocess.
        This way the client and depending builders are a clone copy of self. The Scheduler is used to perform
        time-consuming tasks. It communicates through records/fields of a tasks table.
        """
        self.getScheduler(client).run()

    def startServer(self, client, port=80):
        u"""
        The <code>start</code> method starts the <code>TwistedServer</code> instance. The <attr>port</attr>
        (default value is <code>80</code>) defines the main port of the web server.
        """
        client.showStartLabel(port)

        # Create a Twisted server reactor and subscribe our leaf server
        site = server.Site(client)
        reactor.listenTCP(port, site) # @UndefinedVariable

        # Start running the server
        reactor.run() # @UndefinedVariable

    def getScheduler(self, client):
        u"""
        The <code>getScheduler</code> method answers a <code>Scheduler</code> instance, that will run as daemon /
        tasks server, to perform background tasks for the main site server. The method can be redefined but the
        inheriting application server class.
        """
        return Scheduler(client)

if __name__ == '__main__':
    from twistedclient import TwistedClient
    client = TwistedClient()
    twistedserver = TwistedServer()
    twistedserver.start(client, 8001)
