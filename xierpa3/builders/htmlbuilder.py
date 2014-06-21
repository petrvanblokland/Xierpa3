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
#   htmlbuilder.py
#
#   Following standard
#   https://google-styleguide.googlecode.com/svn/trunk/htmlcssguide.xml
#
from xierpa3.builders.builder import Builder
from xierpa3.builders.builderparts.xmltagbuilderpart import XmlTagBuilderPart
from xierpa3.builders.builderparts.htmlbuilderpart import HtmlBuilderPart
from xierpa3.builders.builderparts.xmltransformerpart import XmlTransformerPart
from xierpa3.builders.builderparts.svgbuilderpart import SvgBuilderPart
from xierpa3.builders.builderparts.canvasbuilderpart import CanvasBuilderPart
from xierpa3.constants.constants import C
from xierpa3.toolbox.transformer import TX

class HtmlBuilder(XmlTagBuilderPart, CanvasBuilderPart, SvgBuilderPart, 
        XmlTransformerPart, HtmlBuilderPart, Builder, C):
    u"""
    """
    # Used for dispatching component.build_sass, and builder.isType('html'),
    # for components that want to define builder dependent behavior. In normal
    # processing of a page, this should never happen. But it can be used to
    # select specific parts of code that should not be interpreted by other builders.
    ID = C.TYPE_HTML # Also the default extension of the output format.
    EXTENSION = ID
    ATTR_POSTFIX = ID # Postfix of dispatcher and attribute names above generic names.

    @classmethod
    def getModelsPath(cls):
        pass

    def getUrl(self):
        u"""Answer the url of the current page. To be implemented by inheriting classes
        that actually knows about urls. Default behavior is to do nothing."""
        return self.e.getFullUrl()

    def getFilePath(self, site):
        u"""
        Answers the file path, based on the URL. Add '/files' to hide Python sources from view.
        The right 2 slash-parts of the site path are taken for the output (@@@ for now)
        """
        return self.getExportPath(site) + site.name + '.' + self.getExtension()

    def theme(self, component):
        pass

    def _theme(self, component):
        pass

    def page(self, component):
        u"""
        Builds entire HTML document.
        """
        self.clear() # Clear the output stream for next theme page
        #self.docType(self.ID)
        self.html()
        self.head()
        self.title_(component.getTitle(self.getPath())) # Search for the title in the component tree
        self.ieExceptions()
        # self.supportMediaQueries() # Very slow, getting this from Google?
        # self.title_(component.getTitle()) # Search for the title the component tree
        self.setViewPort()
        self.buildFontLinks(component)
        self.buildCssLinks(component)
        self.ieExceptions()
        # Build required search engine info, if available in component.adapter
        self.buildMetaDescription(component)
        self.buildMetaKeyWords(component)
        
        self.link(rel="apple-touch-icon-precomposed", href="img/appletouchicon.png")
        self.buildJavascript(component)
        self.buildFavIconLinks(component)
        self._head()

        self.body()
        # Instead of calling the main self.block
        self.div(class_=component.class_ or C.CLASS_PAGE)
        if self.isEditor(): # If in /edit mode, make the whole page as form.
            self.editor(component) # Build top editor interface.

    def _page(self, component):
        # Instead of calling the main self._block
        if self.isEditor(): # If in /edit mode, make the whole page as form.
            self._editor(component)
        self._div(comment=C.CLASS_PAGE)
        if self.e.form['fontsize']:
            self.jsUrl('js/showfontsize.js')
        self._body()
        self._html()

    def save(self, component, path=None):
        u"""Save the file in path. If the optional <i>makeDirectory</i> attribute is 
        <b>True</b> (default is <b>True</b>) then create the directories in the path 
        if they don’t exist."""
        if path is None:
            path = self.getExportPath(component)
        self.makeDirectory(path) # Make sure that the directory part of path exists.
        for template in component.getTemplates():
            template.build(self)
            f = open(path, 'wb')
            f.write(self.getResult())
            f.close()
        return path
    
    def buildJavascript(self, component):
        if component.style and component.style.js:
            self.jsUrl(component.style.js)

    def buildFavIconLinks(self, component):
        favIcon = component.getFavIcon(self)
        if favIcon is not None:
            self.output("<link type='image/x-icon' rel='icon' href='%s'></link>" % favIcon)

    def buildMetaDescription(self, component):
        u"""Build the meta tag with description of the site for search engines, is available in the adapter."""
        data = component.adapter.getDescription(component)
        if data.text is not None:
            self.meta(name=self.META_DESCRIPTION, content=data.text)
            
    def buildMetaKeyWords(self, component):
        u"""Build the meta tag with keywords of the site for search engines, if available in the adapter."""
        data = component.adapter.getKeyWords(component)
        if data.text is not None:
            self.meta(name=self.META_KEYWORDS, content=data.text)
            
    def cssUrl(self, css):
        if not isinstance(css, (list, tuple)):
            css = [css]
        for url in css:
            self.link(href=url, rel="stylesheet", type="text/css")

    def jsUrl(self, js):
        # Alternative to jQuery: http://vanilla-js.com
        if not isinstance(js, (tuple, list)):
            js = [js]
        for url in js:
            self.script(type="text/javascript", src=url)

    def buildCssLinks(self, component):
        u"""
        Create the CSS links inside the head. /css-<SASS_STYLENAME> defines the type of CSS output from the Sass
        compiler. The CSS parameter must be one of ['nested', 'expanded', 'compact', 'compressed']
        """
        #urlName = component.root.urlName # Get the specific URL prefix for from root of this component.
        for cssUrl in component.css: # Should always be defined, default is an empty list
            #if not cssUrl.startswith('http://'):
            #    cssUrl = '/' + urlName + cssUrl
            self.link(href=cssUrl, type="text/css", charset="UTF-8", rel="stylesheet", media="screen")

    def buildFontLinks(self, component):
        for fontUrl in component.fonts: # Should always be defined, default is an empty list
            self.link(href=fontUrl, type="text/css", charset="UTF-8", rel="stylesheet", media="screen")

    def ieExceptions(self):
        self.comment("1140px Grid styles for <= IE9")
        self.newline()
        self.text("""<!--[if lte IE 9]><link rel="stylesheet" href="/cssie/ie9.css" type="text/css" media="screen" /><![endif]-->""")
        # self.text("""<link rel="stylesheet" href="cssie/ie9.css" type="text/css" media="screen,projection" />""")
        self.newline()

    def supportMediaQueries(self):
        self.comment("""Enables media queries in some unsupported browsers""")
        self.newline()
        self.script(type="text/javascript", src="http://code.google.com/p/css3-mediaqueries-js")

    def setViewPort(self):
        self.meta(name='viewport', content='width=device-width, initial-scale=1.0')

    # E D I T O R

    def isEditor(self):
        if not self.e:
            return False # Running batch mode, has no editor.
        return self.e.form[self.PARAM_EDIT]

    def editor(self, component):
        self.form(id='editor', method='post', action='/' + component.root.urlName)
        self.div(style='float:left;background-color:#D0D0D0;width:100%')
        self.input(type='hidden', name='edit', value=self.e.form[self.PARAM_EDIT]) # Keep edit open when in that mode.
        self.input(type='hidden', name='article', value=self.e.form[self.PARAM_ARTICLE]) # Keep edit open when in that mode.
        self.input(type='submit', name='new', value='New')
        self.input(type='submit', name='save', value='Save', onclick='saveArticle();')
        self._div()

    def _editor(self, component):
        # Add script to collect the editable texts from the html
        self._form()
        self.script()
        self.output("""
        function newArticle(){
            alert('New article');
        }
        function saveArticle(){
            alert(document.getElementById("article").html());
            document.getElementById("editor").submit();
        }
        function getContentEditableText(id) {
            var ce = $("<pre />").html($("#" + id).html());
            if ($.browser.webkit)
              ce.find("div").replaceWith(function() { return "\\n" + this.innerHTML; });
            if ($.browser.msie)
              ce.find("p").replaceWith(function() { return this.innerHTML + "<br>"; });
            if ($.browser.mozilla || $.browser.opera || $.browser.msie)
              ce.find("br").replaceWith("\\n");
            return ce.text();
        }
        """)
        self._script()

    # B L O C K

    def block(self, component):
        """Optional space for a component to build the opening of a block.
        This does <b>not</b> automatically build a <b>div</div> since that is not flexible enough.
        To be redefined by inheriting builder classed. Default behavior is to do nothing, except 
        showing the <b>component.selector</b> as comment/"""
        if component.selector:
            self.tabs()
            self.div(class_=component.class_)
            self.comment(component.selector)

    def _block(self, component):
        """Allow the component to build the closing of a block.
        This does <b>not</b> automatically build a <b>div</div> since that is not flexible enough.
        To be redefined by inheriting builder classed. Default behavior is to do nothing, except 
        showing the <b>component.selector</b> as comment."""
        if component.selector:
            self.tabs()
            self._div(comment=component.class_)
            self.comment('%s' % component.selector)

    def linkBlock(self, component, **kwargs):
        self.a(**kwargs)

    def _linkBlock(self, component):
        self._a()

    def text(self, componentOrText, **kwargs):
        u"""
        If in <b>self._svgMode</b> output as SVG tags. Otherwise just output if plain text string.
        If it is a components, then get it’s text string.
        """
        if componentOrText is None:
            return
        if isinstance(componentOrText, basestring):
            if self._svgMode:
                self.svgText(componentOrText, **kwargs)
            else:
                self.output(componentOrText)
        else: # Otherwise it must be of type component
            if componentOrText.id:
                self.span(id=id, contentEditable=componentOrText.editable)
            self.output(componentOrText.text)
            if componentOrText.id:
                self._span()

    def image(self, component, class_=None):
        u"""
        """
        if component.style:
            width = component.style.width_html # Take explicit HTML width/height if defined in component.
            height = component.style.height_html
        else:
            width = None
            height = None
        if height is None and width is None:
            width = '100%'
        elif height is not None:
            width = None
        alt = component.alt or TX.path2Name(component.url)
        self.img(src=component.url, width_html=width, height_html=height, alt=component.alt,
            class_=TX.flatten2Class(class_, component.getPrefixClass()))

    def element(self, **kwargs):
        u"""Elements are used for local CSS definitions. Ignored by HTML output."""
        pass
    
    # D R A W I N G
        