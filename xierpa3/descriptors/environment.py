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
#   environment.py
#
import weakref
from xierpa3.toolbox.parsers.json import cjson # Load cjson or json if available.
from xierpa3.descriptors.state import State
from xierpa3.toolbox.formdict import FormDict

class Environment(State):
    u"""
    The Environment instance e is the common place of the page builder process, holding all dynamic information related
    to session and request.
    """

    HTTP_HOST = 'httphost'
    HTTPHEADERS = 'httpheaders'
    COOKIES = 'cookies'
    PATH = 'path'
    FULLPATH = 'fullpath'
    PARAM_UPLOADPREFIX = 'upload.'

    HTTPKEYS = {
        PATH : 'PATH_INFO',
        HTTPHEADERS : 'received_headers',
        COOKIES : 'received_cookies',
    }

    def __init__(self, **kwargs):
        State.__init__(self)
        for key, value in kwargs.items():
            self[key] = value
        self.initializeForm()

    def __repr__(self):
        return '<Environment e>'

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def initializeForm(self):
        u"""
        
        The <code>initializeForm</code> method initializes the <code>self.form</code> instance of <code>FormDict</code>.
        
        """
        self.form = FormDict()
        self.handleGetPostParams()
        self.handleUrlParams()

    def addComponent(self, component):
        # Store weakref link to components, so they can be reached from all other components
        # as a flat list, where the selector is the key.
        selector = component.selector
        if component.id == selector and self._components.has_key(selector):
            print '### Warning ### Multiple components with id "%d" defined.' % selector
        if not self._components.has_key(selector):
            self._components[selector] = []
        self._components[selector].append(weakref.ref(component))

    def setParams(self, params):
        u"""
        <p>The <code>setParams</code> method sets the <code>self.params</code> of the of environment to <attr>
        params</attr>. This method can be redefined to get the parameters string from the <attr>params</attr> tuple.
        The tuple is based on from the standard definition in the application module.</p>
        
        <p><code>urlpatterns = patterns('', (r'^(.*)$', build))</code></p>
        
        <p>that generates a tuple with a single parameter set.</p>
        """
        if params:
            params = params[0]
        self.params = params

    def handleGetPostParams(self):
        u"""
        The <code>handleGetPostParams</code> method adds any GET or POST parameters to the <code>self.form</code>
        instance of <code>FormDict</code>.
        """
        try:
            path = self.request.path
            args = self.request.args
        except AttributeError:
            return

        self[self.PATH] = path
        for key in args.keys():
            uvalues = []
            for value in args[key]:
                if not key.startswith(self.PARAM_UPLOADPREFIX):
                    value = value.decode('utf-8')
                uvalues.append(value)
            self.form[key] = uvalues

        """
        # If there is any posted file content, then also put this in form. 
        # It's the application responsibility to cover any possible name clashes.
        # Otherwise an error will be raise.
        for key, item in self.request.FILES.items():
            assert self.form[key] is None
            self.form[key] = item
        """

    def handleUrlParams(self):
        """
        The <code>handleQueryStringParams</code> method gets the parameters from the path.
        """
        try:
            path = self.request.path
        except AttributeError:
            return

        for query in path.split('/'):
            if not query:
                continue
            parts = query.split('-')
            if len(parts) == 1:
                self.form[query] = '1'                # Default value for single name parameters, always as string
            else:
                self.form[parts[0]] = '-'.join(parts[1:])

    def getRequestValue(self, key):
        u"""
        The <code>getRequestValue</code> method answers the <code>self.request</code> value of <attr>key</attr>.
        
        """
        return self.request.received_headers[key]

    def getPort(self):
        return self.request.host.port

    def getHost(self):
        port = self.getPort()
        if port == 80:
            port = ''
        else:
            port = ':%s' % port
        return self.getDomain() + port

    def getDomain(self):
        return self.request.received_headers._headers._rawHeaders['host'][0].split(':')[0]

    def getFullUrl(self):
        return self.getHostUrl() + self.getFullPath()

    def getHostUrl(self):
        return self.getPrefix() + self.getHost()

    def isSsl(self):
        # TODO: Fix this
        return False

    def getPrefix(self):
        if self.isSsl():
            return 'https://'
        else:
            return 'http://'

    def getFullPath(self):
        u"""
        The <code>getFullPath</code> method answers the plain full <attr>path</attr> as it appears in the browser.
        
        """
        return self[self.PATH] or '/'

    def getServer(self):
        u"""
        The <code>getServer</code> method answers the name of the server domain <code>self[self.HTTP_HOST]</code>
        
        """
        return self[self.HTTP_HOST]

    def getServerClient(self):
        u"""
        
        The <code>getServerClient</code> method answers the <code>BaseCient</code> instance that is running the server
        of <code>self.request</code>. Note that the path to this client is depending on the (current version of) Twisted
        Matrix.
        """
        try:
            return self.request.transport.server.factory.resource
        except:
            raise ValueError('[Environment.getServerClient] Error finding the server client as "self.request.transport.server.factory.resource')

    def getUserAgent(self):
        u"""
        The <code>getUserAgent</code> method answers the user-agent string that contains info about the browser and
        OS type as defined by <code>self[self.HTTP_USER_AGENT]</code>.
        
        """
        return self.request.received_headers['user-agent']

    # ------------------------------------------------------------------------------------------------------------------
    #    R E S P O N S E

    def setHeader(self, name, value):
        self.request.setHeader(name, value)

    # ------------------------------------------------------------------------------------------------------------------
    #    C O O K I E S
    #
    #    TODO: May need some cleaning; cookie code in other places.
    #
    def getCookies(self):
        u"""
        The <code>getCookies</code> method answers the cookies dictionary of the current request. The default
        behavior is to answer <code>self.request.received_cookies</code>.
        
        """

        import urllib

        result = {}
        for k, v in self.request.received_cookies.items():
            try:
                result[k] = cjson.decode(urllib.unquote(v))
            except:
                result[k] = v

        return result

    def getCookie(self, name):
        u"""
        The <code>getCookie</code> method answers the cookie indicated by <attr>name</attr>. If there is no
        attribute in the request (e.g. because the builder is created by a parallel process), then answer <code>None
        </code>.
        """
        try:
            return self.getCookies().get(name)
        except AttributeError:
            pass
        return None

    # value must be first as existing session code doesn't send a name
    def setCookie(self, value=None, expires=None, url='/', name=None, **args):
        u"""
        The <code>setCookie</code> method saves the cookie indicated by <attr>name</attr> with <attr>value</attr>,
        using the <attr>expires</attr> and <attr>url</attr> attributes.
        """

        import datetime, urllib

        if not name:
            name = self.COOKIENAME

        # allow expires to be specified as number of days
        if expires and not isinstance(expires, basestring):
            try:
                days = int(expires)
                if days > 0:
                    expiry = datetime.datetime.now() + datetime.timedelta(days=days)
                    expires = expiry.strftime("%a, %d %b %Y %H:%M:%S GMT")
            except:
                expires = None

        # encode python objects into string
        value = urllib.quote(cjson.encode(value))

        self.request.addCookie(name, value, expires=expires, path=url, **args)

        # and just make sure it's available to the rest of this request
        self.request.received_cookies[name] = value
