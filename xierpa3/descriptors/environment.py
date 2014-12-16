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
from xierpa3.toolbox.parsers.c_json import cjson # Load cjson or json if available.
from xierpa3.descriptors.state import State
from xierpa3.toolbox.formdict import FormDict
import urllib

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

        The ``initializeForm`` method initializes the ``self.form`` instance of ``FormDict``.

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
        <p>The ``setParams`` method sets the ``self.params`` of the of environment to ``
        params``. This method can be redefined to get the parameters string from the ``params`` tuple.
        The tuple is based on from the standard definition in the application module.</p>

        <p>``urlpatterns = patterns('', (r'^(.*)$', build))``</p>

        <p>that generates a tuple with a single parameter set.</p>
        """
        if params:
            params = params[0]
        self.params = params

    def handleGetPostParams(self):
        u"""
        The ``handleGetPostParams`` method adds any GET or POST parameters to the ``self.form``
        instance of ``FormDict``.
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
                if not self.isCodeInjection(value):
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

    def isCodeInjection(self, value):
        u"""
        To protect from attempted code injection, filter HTML tags and quotes.
        Also maybe single quotes, parentheses and such?
        """
        if value.startswith('<'):
            return True
        elif value.startswith('"'):
            return True

        return False

    def handleUrlParams(self):
        """
        The ``handleUrlParams`` method gets the parameters from the path.
        """
        try:
            path = self.request.path
        except AttributeError:
            return

        path = urllib.unquote(path)

        for query in path.split('/'):
            if not query:
                continue

            parts = query.split('-')

            if len(parts) == 1:
                self.form[query] = '1'                # Default value for single name parameters, always as string
            else:
                newparts = []
                for part in parts[1:]:
                    if not self.isCodeInjection(part):
                        newparts.append(part)

                self.form[parts[0]] = '-'.join(newparts)

    def getRequestValue(self, key):
        u"""
        The ``getRequestValue`` method answers the ``self.request`` value of ``key``.

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
        The ``getFullPath`` method answers the plain full ``path`` as it appears in the browser.

        """
        return self[self.PATH] or '/'

    def getServer(self):
        u"""
        The ``getServer`` method answers the name of the server domain ``self[self.HTTP_HOST]``

        """
        return self[self.HTTP_HOST]

    def getServerClient(self):
        u"""

        The ``getServerClient`` method answers the ``BaseCient`` instance that is running the server
        of ``self.request``. Note that the path to this client is depending on the (current version of) Twisted
        Matrix.
        """
        try:
            return self.request.transport.server.factory.resource
        except:
            raise ValueError('[Environment.getServerClient] Error finding the server client as "self.request.transport.server.factory.resource')

    def getUserAgent(self):
        u"""
        The ``getUserAgent`` method answers the user-agent string that contains info about the browser and
        OS type as defined by ``self[self.HTTP_USER_AGENT]``.

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
        The ``getCookies`` method answers the cookies dictionary of the current request. The default
        behavior is to answer ``self.request.received_cookies``.

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
        The ``getCookie`` method answers the cookie indicated by ``name``. If there is no
        attribute in the request (e.g. because the builder is created by a parallel process), then answer ``None
        ``.
        """
        try:
            return self.getCookies().get(name)
        except AttributeError:
            pass
        return None

    # value must be first as existing session code doesn't send a name
    def setCookie(self, value=None, expires=None, url='/', name=None, **args):
        u"""
        The ``setCookie`` method saves the cookie indicated by ``name`` with ``value``,
        using the ``expires`` and ``url`` attributes.
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
