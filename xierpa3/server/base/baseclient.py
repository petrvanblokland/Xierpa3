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
#     baseclient.py
#
import sys, os
import traceback
import cStringIO as StringIO

import xierpa3 # To get the root for /xierpa3/resource file request.
from xierpa3.constants.constants import Constants
from xierpa3.toolbox.dating import DateTime
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.descriptors.environment import Environment
from xierpa3.toolbox.transformer import TX

class BaseClient(object):
    u"""
    Connects the SiteBuilder to Twisted client.
    """
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Constants

    MTIMES = {}
    LINE = '-' * 80
    DO_INDENT = True # Boolean flag if the build code should be indented.
    DEFAULTTHEME = 'default'
    THEMES = None # Name-class of the theme component trees, redefined by inheriting classes.
    
    def __repr__(self):
        u"""
        The <code>__repr__</code> answers the info string about this <code>Client</code> instance.
        """
        return u'Client for %s sites' % len(self.getThemes())

    def getDefaultSiteClass(self):
        u"""
        The <code>getDefaultSiteClass</code> method is used by the task daemon, to get access to the current set of
        constants. Since the site class contains the specific constants of the site, it can be used to derive the path
        of DATA storage and to create a shadow builder in the remote process to be called with the <code>task.method
        </code>.
        """
        return self.THEMES.get(self.DEFAULTTHEME)

    def showStartLabel(self, port):
        u"""
        The <code>showStartLabel</code> method is used by the client to show the server information at startup.
        
        """
        print self.LINE
        date = str(DateTime(date='now'))
        print u'... Start %s on [%s:%s] %s' % (self, 'localhost', port, date)
        print self.LINE

        for siteName, theme in self.getThemes().items():
            siteName = siteName.encode('utf-8')
            print u'... %s "%s"' % (siteName, theme.title)
        print self.LINE

    def showStopLabel(self):
        u"""
        The <code>showStopLabel</code> method is used by the client to show the server information at startup.
        
        """
        print self.LINE
        print u'... Stop Client' # on %s' % DateTime(date='now')
        print self.LINE

    def getThemeName(self, httprequest):
        u"""
        The <code>getThemeName</code> method answers the name of the current theme. This method should be redefined
        if there is more than one site to be served through this client, depending on a pattern in the <attr>httprequest
        </attr> URL. Default behavior is to answer the result of <code>self.getDefaultSiteName()</code>.<br/>
        Note we cannot use <code>self.e</code> to parse the URL, since it cannot be created without a defined site
        class.
        """
        import re

        host = httprequest.getHeader('Host')
        if host:
            for key in self.getThemes().keys():
                if re.search(r'(^|\.){0}\.'.format(key), host):
                    return key
        return httprequest.path.split('/')[1]

    def getTheme(self, name):
        themes = self.getThemes()
        return themes.get(name) or themes.get(self.getDefaultThemeName())

    def getDefaultThemeName(self):
        u"""
        The <code>getDefaultThemeName</code> method answers the default site name <code>self.DEFAULTTHEME</code>.
        
        """
        return self.DEFAULTTHEME

    def getThemes(self):
        u"""
        The <code>getSites</code> answers dictionary with the sites this client runs.
        """
        return self.THEMES

    def getThemeNames(self):
        u"""
        The <code>getThemeNames</code> method answers the names (keys) of the available sites of this server.
        Typically this is the list of keys from the dictionary answered by <code>self.getSites()</code>.
        """
        return self.getThemes().keys()

    def getThemeTitle(self, name):
        u"""
        The <code>getThemeTitle</code> method answers the class title of named site <attr>name</attr>. The default
        behavior is to answer <code>self.getSiteClass(name).getTitle()</code>.
        """
        return self.getTheme().getTitle()

    def getDoIndent(self):
        u"""
        The <code>getDoIndent</code> method answers the boolean flag if the output code building should include indents.
        """
        return self.DO_INDENT
    
    def getSite(self, httprequest):
        u"""
        The <code>getSite</code> method answers a new instance of the site class that is indicated by the result of
        <code>e.getSiteName()</code>. This site instance typically is derived from the first part of the URL
        or by the matching domain name. This allows the running of multiple domain names (all with port 80)
        on the same server.
        """
        themeName = self.getThemeName(httprequest)
        theme = self.getTheme(themeName)
        '''
        Plug the current environment into the template for rendering. This allows the static components of the site
        template conditionally respond to settings of the current request.
        TODO: Make this work with sessions too, using the old E manager.
        '''
        theme.e = Environment(request=httprequest)
        return theme

    def setMimeTypeEncoding(self, mimeType, request):
        u"""
        <doc>The <code>getMimeTypeEncoding</code> method answers the MIME type and coding in format <code>'text/css;
        charset-utf-8'</code>.</doc>
        """
        if mimeType:
            if 'text' in mimeType:
                mimeType += '; charset=utf-8'
            request.setHeader('content-type', mimeType)

    def buildResource(self, site):
        u"""The url requested a xierpa3 resource, try to find it and answer the result
        with the appropriate mime type."""
        path = TX.path2ParentDirectory(TX.module2Path(xierpa3)) + site.e.request.path
        if os.path.exists(path):
            f = open(path, 'rb')
            result = f.read()
            f.close()
            return result, self.C.MIMETYPE_PNG
        return '', self.C.MIMETYPE_HTML

    def buildCss(self, site):
        u"""Build the site to CSS."""
        doIndent = self.getDoIndent() # Boolean flag if indenting should be in output.
        builder = CssBuilder(e=site.e, doIndent=doIndent)
        filePath = builder.getFilePath(site)
        result = self.resolveByFile(site, filePath)
        if site.e.form[self.C.PARAM_DOCUMENTATION]:
            site.buildDocumentation(builder) # Build the live documentation page from the site
            builder.save(site, path=filePath.replace('.css', '_doc.css')) # Compile resulting Sass to Css  
            result = builder.getResult() 
        elif site.e.form[self.C.PARAM_FORCE] or result is None:
            # Forced or no cached CSS, so try to build is and save it in the cache.
            site.build(builder) # Build from entire site theme, not just from template. Result is stream in builder.
            builder.save(site, path=filePath) # Compile resulting Sass to Css  
            result = builder.getResult() # Get the resulting Sass.
        return result, self.C.MIMETYPE_CSS
    
    def buildHtml(self, site):
        u"""Build the site for HTML."""
        doIndent = self.getDoIndent() # Boolean flag if indenting should be in output.
        site.reset() # Allow the theme to reset values for every page request, depending on url parameters. 
        builder = HtmlBuilder(e=site.e, doIndent=doIndent)
        filePath = builder.getFilePath(site)
        result = self.resolveByFile(site, filePath)
        if site.e.form[self.C.PARAM_DOCUMENTATION]:
            site.buildDocumentation(builder)
            result = builder.getResult()
        elif site.e.form[self.C.PARAM_FORCE] or result is None:
            # Find the matching template for the current site and build from there.
            template = site.getMatchingTemplate(builder)
            builder.pushResult()
            template.build(builder)
            result = builder.popResult()
        return result, self.C.MIMETYPE_HTML
    
    def render_GET(self, httprequest):
        u"""
        The <code>render_GET</code> method is called by Twisted to handle the GET <attr>httprequest</attr>. 
        It is the main loop (besides the <code>self.render_POST</code>) that builds pages from url requests.
        The site instance is called by <code>b.build()</code>. The result (this can be HTML, JSON or binary data) is
        answered. The application needs to have the right MIME type in the output.
        """
        site = self.getSite(httprequest) # Site is Theme instance
        try:
            path = site.e.request.path
            if path.startswith(self.C.URL_XIERPA3RESOURCES):
                result, mimeType = self.buildResource(site)
            # If there is a matching file in the site root/files folder, then answer this.
            elif path.endswith('.css'):
                result, mimeType = self.buildCss(site)
            else: # Not CSS, request must be HTML. This could be an extended choice in the future.
                result, mimeType = self.buildHtml(site)
        except Exception, e:
            t = traceback.format_exc()
            result = self.renderError(e, t)
            mimeType = self.C.MIMETYPE_HTML

        # if b.shouldBeCompressed():
        #    httprequest.setHeader("Content-Encoding", "gzip")
        #    result = b.getResult().getCompressedValue()
        # else:
        #    result = b.getResult().getValue()
        self.setMimeTypeEncoding(mimeType, httprequest)        
        return result
    
    def render_POST(self, httprequest):
        u"""
        The <code>render_POST</code> method is called by Twisted to handle the POST <attr>httprequest</attr>. The
        site instance is called with <code>b.build()</code>. The result (this can be HTML, JSON or binary data) is
        answered. The application is supposed to have the the right MIME type in the output. The data of the post is
        located in the file object <code>httprequest.content</code>. The data can be read by <code>
        httprequest.content.read()</code>.
        """
        site = self.getSite(httprequest)  # Site is Theme instance
        site.handlePost()

        if isinstance(httprequest.content, StringIO.OutputType):
            # Probably JSON.
            json = httprequest.content.getvalue()
            # print json
            # b.buildJSON(json)
        try:
            path = site.e.request.path
            if path.startswith(self.C.URL_XIERPA3RESOURCES):
                result, mimeType = self.buildResource(site)
            # If there is a matching file in the site root/files folder, then answer this.
            if site.e.request.path.endswith('.css'):
                result, mimeType = self.buildCss(site)
            else: # Not CSS, request must be HTML. This could be an extended choice in the future.
                result, mimeType = self.buildHtml(site)
        except Exception, e:
            t = traceback.format_exc()
            result = self.renderError(e, t)
            mimeType = self.C.MIMETYPE_HTML
        self.setMimeTypeEncoding(mimeType, httprequest)        
        return result
    
        # if b.shouldBeCompressed():
        #    httprequest.setHeader("Content-Encoding", "gzip")
        #    return b.getResult().getCompressedValue()
        # else:
        #    return builder.getResult().getValue()

    def renderErrorHead(self):
        return """
        <head>
            <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
            <link href="http://data.xierpa.com.s3.amazonaws.com/_images/xierpa-icon.ico" rel="shortcut icon"/>
            <title>404 Page</title>
        
            <style type="text/css">
            body { font-family: Verdana; font-size: 10pt; color: black; background: grey; }
            pre { background: #eee; padding: 6px; border: 1px dotted #ccc; overflow: auto }
            a:link { color:#007d2f; text-decoration: none; }
            a:visited { color:#99c421; text-decoration: none; }
            a:active { color:#64c324; text-decoration: none; }
            a:hover { color:#64c324; text-decoration: none; }
            #content { position: relative; margin-left: auto; margin-right: auto; top: 20px; margin-bottom: 40px;
                border: 1px solid #aaa; background: white; padding: 20px;}
            </style>
        
        </head>
        """

    def renderError(self, e, t):
        head = self.renderErrorHead()
        print t
        return """
        <html>%s<body>
        <div id="content">
        <h2>Error</h2>
        <p>The following error occurred:</p>
        <pre>%s</pre>
        <p>Please contact the system administrator.</p>
        <pre>%s</pre>
        <p>
        <img src="http://data.xierpa.com.s3.amazonaws.com/_images/grid.png">
        </p>

        <div id="footer" style="font-size: 8px; text-align: right">
        Powered by <a href="http://www.xierpa.com"> Xierpa <img id="xierpafootericon" height="15" alt="$"
        src="http://xierpa.petr.com.s3.amazonaws.com/_root/_lib2/images/xierpa/xierpa_x_green.png">
        </a>
        </div>
        </div>
        </body></html>
        """ % (head, e, t)

    # ---------------------------------------------------------------------------------------------------------
    #    R E S O L V E R

    def resolveByFile(self, site, path):
        """Test if the path exists as file. If it does, then answer the content. If forcing then skip. If in /ie then read."""
        if path is not None and (not site.e.form[self.C.PARAM_FORCE] or '/ie' in path) and os.path.exists(path) and not os.path.isdir(path):
            f = open(path, 'rb')
            result = f.read()
            f.close()
            return result
        return None

    # ---------------------------------------------------------------------------------------------------------
    #     R E L O A D E R

    """
    def checkExit(self, e):
        if self.e.form['exitserver']:                    # Requested to exit server?
            sessionpath = e.path2fspath(SESSIONSTORAGE)
            e.sm.writetofile(sessionpath)
            reactor.stop()                            # The mark reactor to stop after this page
    """

    def reload(self):
        self.showStopLabel()
        sys.exit(0)

    @classmethod
    def codeChanged(cls):
        u"""
        
        Auto-reloading launcher.

         Borrowed from Peter Hunt and the CherryPy project (http://www.cherrypy.org). Some taken from Ian Bicking's Paste
        (http://pythonpaste.org/).
 
        Portions copyright (c) 2004, CherryPy Team (team@cherrypy.org). All rights reserved.

        Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
        following conditions are met:

        * Redistributions of source code must retain the above copyright notice, this list of conditions and the
          following disclaimer.
        * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
          following disclaimer in the documentation and/or other materials provided with the distribution.
        * Neither the name of the CherryPy Team nor the names of its contributors may be used to endorse or promote
          products derived from this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
        WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
        PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY
        DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
        PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
        CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
        OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
        DAMAGE.
        
        """
        for filename in filter(lambda v: v, map(lambda m: getattr(m, "__file__", None), sys.modules.values())):
            if filename.endswith(".pyc") or filename.endswith(".pyo"):
                filename = filename[:-1]
            if not os.path.exists(filename):
                continue # File might be in an egg, so it can't be reloaded.
            stat = os.stat(filename)
            mtime = stat.st_mtime
            if filename not in cls.MTIMES:
                cls.MTIMES[filename] = mtime
                continue
            if mtime != cls.MTIMES[filename]:
                cls.MTIMES = {}
                return True
        return False
