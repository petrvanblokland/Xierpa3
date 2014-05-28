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
#    component.py
#
#    Component
#        Theme
#        Page
#        Logo
#        Ruler
#        Text
#        Sidebar
#        TagCloud
#        Menu
#        Message
#        (Navigation)
#            MobileNavigation
#        Featured
#        Header
#        Footer
#        Column
#            Article
#            (FeaturedBase)
#                FeaturedByImage
#                FeaturedByImageList
#                FeaturedByText
#                FeaturedByDiapText
#                FeaturedByTextList
#            Group
#                ItemGroup
#            SocialMedia
#
import weakref
import hashlib
import inspect
from xierpa3.descriptors.style import Style
from xierpa3.descriptors.blueprint import BluePrint
from xierpa3.constants.constants import C
from xierpa3.toolbox.transformer import TX
from xierpa3.attributes import Perc
from xierpa3.adapters.blurbadapter import BlurbAdapter # Blurb adapter as default in root component.

class Component(C):
    u"""
    The Component describes the abstract behavior of components on the page.
    """
    # Root default style template. To be cascaded by inheriting classes.
    BLUEPRINT = BluePrint(
        # Default behavior of images, use class autowidth to cover differences between browsers.
        imgClass=C.CLASS_AUTOWIDTH, doc_imgClass=u'Image class, set default to AUTOWIDTH.',
        imgMaxWidth=Perc(100), doc_imgMaxWidth=u'Image maximal width',
        imgMinWidth=0, doc_imgMinWidth=u'Image minimal width',                           
    )
        
    ADAPTER = None # To be inherited or defined separately into the component.
    TAGNAME = 'div' # By default every component has a root div element.
    BUILD_CSS = True # Default behavior of every component is to build in CSS.
    STYLE_DEFAULT = {} # Default style source, optionally redefined by inheriting classes.
    
    def __init__(self, components=None, style=None, id=None, parent=None, name=None,
            css=None, fonts=None, prefix=None, class_=None, type=None, contentID=None, 
            count=1, title=None, url=None, template=None, editable=False, adapter=None, 
            selector=None, **kwargs):
        # The class name of the components is used as class names in SASS/CSS
        # Initialize the self.style, as selector and id are stored there.
        self.style = style # If style is None, then use a copy of the self.BLUEPRINT style.
        self.style.add(kwargs) # Further initialize self.style from keyword arguments
        self.style.component = self # Add the weakref reference to self for the root style.
        # CSS and Fonts urls
        self.css = css # Set the css path list for this component (can be empty list or None)
        self.fonts = fonts # Set the css path list for this component (can be empty list or None)
        # The optional id is the #id in HTML must be unique in the page. Stored as self.style.id.
        # Has no default value, so not all HTML elements will have id attribute.
        self.id = id
        # Used overruling the otherwise calculated self.selector
        self.selector = selector
        # Used as class name when constructing selector (amongst other choices).
        # Take class_ or class component. Stored as self.style.class_
        self.class_ = class_
        # self.name is used to identity components. Always answers something. Does not have to be unique.
        self.name = name
        # Forced title of the browser window or generated document or table of content.
        # If kept None, then the adapter will be queried for the title.
        # This allows both the definition of static names (per page template) or the usage
        # of page titles that depend on the current url.
        # If the adapter answers None as title, then use self.TITLE
        self.title = title
        # Prefix of class and selector, stored as self.style.prefix. Shows in CSS selector as myPrefix.class
        self.prefix = prefix
        # Cache for the unique ID based on the content tree, so components can be compared.
        self._uid = None
        self.template = template # Optional template match with URL parameter
        self.adapter = adapter or self.ADAPTER # Adapter instance for content query, otherwise ask the parent of self.
        self.contentID = contentID # Optional unique id to query content from the adapter
        self.parent = parent # Weakref to parent component
        self.count = count # Count for repeating this component in output
        self.url = url # Default is not to have a URL. Page attribute define URL automatic from name.
        self.editable = editable # Is content of the component editable?
        self.type = type # Type of the website, taking TYPES[self.type] from this pool
        # Child components of self. Default is self.baseComponents
        self.initializeComponents(components)
        # Allow inheriting class to (re)define other stuff when inheriting class redefined initialize()
        # Default behavior is to do nothing here.
        self.initialize()

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.selector or self.name)

    def __getattr__(self, key):
        # Always answer None for missing attributes.
        return self.__dict__.get(key)

    @classmethod
    def getClassName(cls):
        u"""
        Answers the class name of the <i>cls</i> as capitalized name.
        """
        name = cls.__name__
        return name[0].lower() + name[1:]

    def isLast(self, component):
        u"""Allow components to test the parent if they are last."""
        return self.components and self.components[-1] is component

    def getColClass(self, col):
        u"""Answer the colClass, based on the numeric <i>col</i> value and if the component is the
        last in the parent list of child components."""
        colClass = TX.col2Class(col)
        if self.parent.isLast(self):
            colClass = (colClass, self.CLASS_LAST)
        return colClass
    
    def getFavIcon(self, builder):
        u"""Call back from the builder to answer the favIcon url. This can be redefined by inheriting classes
        if the favIcon is depending on the content and status of a page."""
        if self.style and self.style.favIcon:
            return self.style.favIcon
        return None
    
    # self.className        Answer self.style.className or otherwise class name is directly derived from the object class.
    
    def _get_className(self):
        # @@@ Clean this up, so self.className is used everywhere instead of self.getClassName() or self.class_
        return self.style.className or self.getClassName()
    
    className = property(_get_className)
    
    def getPrefixClass(self, prefix2=None):
        u"""Answers the extended class name <b>self.prefix + self.prefix2 + self.class_</b>.
        If <b>self.class_</b> is not defined, and <b>self.prefix + self.prefix2</b> are defined,
        then always add the class name of the component."""
        name = []
        prefix = self.prefix
        if prefix:
            name.append(prefix)
        if prefix2:
            name.append(prefix2)
        name.append(self.getClassName())
        return ' '.join(name)

    def initializeComponents(self, components):
        u"""
        Sets the self.components. If not components, then use the self.baseComponents().
        """
        if components is None:
            components = self.baseComponents()
        self.components = components # Create parent weakrefs in the components to self

    def initialize(self):
        # To be redefined by inheriting classes to fill adapter, default style and components.
        pass

    def readFile(self, path):
        # Generic method to read from local file system.
        f = open(path, 'rb')
        s = f.read()
        f.close()
        return s

    def getRootPath(self):
        from xierpa3 import components
        return components.__path__[0]

    def baseComponents(self):
        """To be redefined by inheriting classes to answer the default child components of the component."""
        return []

    def isEmpty(self):
        """Answer the boolean flag if this component has any attributes or child components."""
        return len(self.components) == 0 and self.style.isEmpty()

    def isEmptyCss(self):
        u"""Answer the boolean flag if this component will generate CSS content. This is different from the regular
        <b>self.isEmpty</b>, since there may be components with content that have <b>self.BUILD_CSS</b> 
        set to <b>False</b>. When <b>self.BUILD_CSS is True</b> it still should build if there is CSS 
        content that has set <b>self.BUILD_CSS</b> to <b>True</b>.
        """
        if not self.style.isEmpty():
            return False
        for component in self.components:
            if not component.isValidCss():
                return False
        if not self.BUILD_CSS: # It must be empty.
            return True
        return False

    def isValidCss(self):
        if self.isEmptyCss():
            return False
        return bool(self.selector)

    def isComponent(self, name):
        """Answer the boolean flag if this is a component where <b>name == self.name</b>."""
        return name == self.name # Compare with self._name or class names

    def getComponent(self, name):
        """Answer the component that matches name."""
        for component in self.components:
            if component.name == name:
                return component
        return None

    # self.title
    
    def getTitle(self, path=None):
        u"""Answer the title of the page. If <b>self.title</b> is not <b>None</b> then answer
        that value. Otherwise query the adapter to answer a title that may be dependent on the
        current path (=url) of the page. If the adapter result is also <b>None</b>, then
        answer <b>self.TITLE<b>, as optional defined by inheriting classes."""
        title = self._title
        if path is not None and not title:
            title = self.getAdapterData(self.ADAPTER_PAGETITLE, id=path).text
        if not title:
            title = self.TITLE
        return title
    
    def _get_title(self):
        return self.getTitle()
    
    def _set_title(self, title):
        self._title = title
        
    title = property(_get_title, _set_title)
    
    def build(self, builder):
        u"""
        Test on the type of building to be done here. Normally the plain self.buildBlock will be called, but it is possible
        to catch the call by implementing a method, dedicated for a particular kind of builder. self.buildBlock_<builder.ID>
        will then called instead.
        """
        hook = 'buildBlock_' + builder.ID
        buildBlock = getattr(self, hook)
        if buildBlock is None:
            buildBlock = self.buildBlock # Not special dispatch, use generic method instead.
        buildBlock(builder)

    def buildBlock(self, builder):
        u"""
        Generic builder for all components. Can be redefined by an inheriting class.
        """
        builder.block(self)
        for component in self.components:
            component.build(builder)
        builder._block(self)

    # X M L  R E N D E R I N G
    
    def buildElement(self, b, element):
        u"""Recursive rendering of the etree element, using the document methods in the builder
        as defined in the <b>DocumentBuilderPart</b> class. The elements are translated
        to the standard tag behavior of the builder."""
        b.docTagElement(element)
        b.text(element.text) # Plain text output of the element
        for child in element: # Recursively render all element children.
            self.buildElement(b, child)
        b._docTagElement(element)
        b.text(element.tail) # Plain text output of the element tail
         
    # A D A P T E R  S T U F F

    def getAdapterData(self, contentID=None, **kwargs):
        u"""Answer the adapter content (list of components) as indicated by the
        optional content attribute, self.contentID or the class name.
        If the result is not a list (e.g. as PHP instruction), then the caller needs
        to call a <b>adapter.forEach()</b> to generate the looping the code."""
        if contentID is None:
            contentID = self.contentID # Get the content id.
        return self.adapter.get(self, contentID, **kwargs)

    # A T T R I B U T E S

    # self.hashedID

    def _get_hashedID(self):
        u"""
        Calculate the unique ID based on the content. This ID can be compared between components to decide if they are
        identical. This is used by the CSS builder to decide of styles can be skipped then they are identical. Note that the
        value is cache, so alterations to the content of children don't reflect in the ID, once it is established.
        """
        if self._hashedID is None:
            m = hashlib.md5()
            if self.selector:
                m.update(self.selector)
            for media in self.media:
                m.update(media.hashedID)
            for style in (self.styles or []):
                m.update(style.hashedID)
            self._hashedID = m.digest()
        return self._hashedID

    hashedID = property(_get_hashedID)

    # self.name

    def _get_name(self):
        """Answer one of <b>self._name or self.id or self.class_ or self.getClassName()</b>.
        The name attribute is for text identifiation of an element. It is not guaranteed to be unique."""
        name = self._name or self.id or self.class_
        if name is None: # Still None?
            # Same as self.getClassName(), but that method answers None for some component classes.
            name = self.__class__.__name__
            name = name[0].lower() + name[1:] # First letter as lower case
        return name

    def _set_name(self, name):
        self._name = name

    name = property(_get_name, _set_name)

    # self.oge

    def _get_urlName(self):
        """Answer the url safe version of <b>self.name</b>."""
        return TX.name2UrlName(self.name)

    urlName = property(_get_urlName)

    # self.url

    def _get_url(self):
        if self._url is None:
            return TX.label2ParamId(self.name)
        return self._url

    def _set_url(self, url):
        self._url = url

    url = property(_get_url, _set_url)

    # self.style

    def newStyle(self, selector=None, d=None):
        u"""Answer a new style with <b>selection</b> and attributes defined in the optional <i>d</i> dictionary."""
        if d is None:
            d = {}
        return Style(selector, **d)

    def addStyle(self, selector=None, **kwargs):
        u"""Add the attributes to the current style."""
        return self.style.addStyle(selector, **kwargs)

    def addMedia(self, selector=None, **kwargs):
        u"""Add the media styles to the current style"""
        self.style.addMedia(selector=selector, **kwargs)

    def _get_style(self):
        u"""Answer self._style. If it doesn't exist yet, create the default style from self.copyBluePrint.
        If not defined yet, then create a new instance of <b>Style</b>, initialized by the aggregation of the cascading
        <b>self.BLUEPRINT</b> of the inherited classes."""
        if self._style is None:
            self._style = self.newStyle()
            inheritedClasses = list(inspect.getmro(self.__class__))
            inheritedClasses.reverse()
            for inheritedClass in inheritedClasses:
                if hasattr(inheritedClass, 'BLUEPRINT'):
                    self._style.addBluePrint(inheritedClass.BLUEPRINT) 
            self._style.addBluePrint(self.BLUEPRINT)
        return self._style

    def _set_style(self, style):
        assert style is None or isinstance(style, Style)
        self._style = style

    style = property(_get_style, _set_style)

    # self.css

    def _get_css(self):
        u""""Answer the list of CSS URLs for this component. If there is a parent, then answer the css of the parent,
        Otherwise answer the default list."""
        css = self.style.css
        if css is None and self.parent:
            return self.parent.css
        return ['css/style.css']

    def _set_css(self, urls):
        assert urls is None or isinstance(urls, (tuple, list))
        self.style.css = urls

    css = property(_get_css, _set_css)

    # self.fonts
    
    def _get_fonts(self):
        u"""Answer the list of web font urls for this component. If there is a parent, then answer the fonts of
        the parent. Otherwise answer the default list."""
        fonts = self.style.fonts
        if fonts is None and self.parent:
            return self.parent.fonts
        return fonts
    
    def _set_fonts(self, urls):
        if urls is None:
            urls = []
        assert isinstance(urls, (tuple, list))
        self.style.fonts = urls
        
    fonts = property(_get_fonts, _set_fonts)
    
    # self.prefix

    def _get_prefix(self):
        # Answer prefix of class
        return self.style.prefix
    def _set_prefix(self, prefix):
        self.style.prefix = prefix

    prefix = property(_get_prefix, _set_prefix)

    # self.class_     Answer the self._class. This value can be None.

    def _get_class_(self):
        return self.style.class_

    def _set_class_(self, class_):
        self.style.class_ = class_

    class_ = property(_get_class_, _set_class_)

    # self.prefixClass

    def _get_prefixClass(self):
        """Answer the <b>self.prefix</b> + <b>self.class_</b>."""
        return self.getPrefixClass()

    prefixClass = property(_get_prefixClass)

    # self.id

    def _get_id(self):
        return self.style.id

    def _set_id(self, id):
        self.style.id = id

    id = property(_get_id, _set_id)

    # self.adapter

    def _get_adapter(self):
        if self._adapter:
            return self._adapter
        if self.parent:
            return self.parent.adapter
        # The root has a default adapter to make sure there is always content.
        return BlurbAdapter()

    def _set_adapter(self, adapter):
        # Set the adapter for this component. This allows various components to have
        # their own adapter. If not defined, the component will take the adapter
        # of its parent.
        self._adapter = adapter

    adapter = property(_get_adapter, _set_adapter)

    # self.components

    def addComponent(self, component):
        if isinstance(component, basestring):
            from text import Text
            component = Text(component)
        component.parent = self
        self._components.append(component)

    def _set_components(self, components):
        if isinstance(components, basestring):
            from text import Text
            components = [Text(components)]
        elif not isinstance(components, (list, tuple)):
            components = [components]
        # Set weakref to parent (self) if we have components
        if components is not None:
            for component in components:
                component.parent = self
        self._components = components

    def _get_components(self):
        # Just answer the components definition. Filling the adapter content
        # should be filled by the inheriting component classes at building time.
        return self._components

    components = property(_get_components, _set_components)

    # self.parent    Parent component

    def _set_parent(self, parent):
        if parent is not None:
            self._parent = weakref.ref(parent)
        else:
            self._parent = None

    def _get_parent(self):
        if self._parent is not None:
            return self._parent()
        return None

    parent = property(_get_parent, _set_parent)

    # self.text     Collect all text from the component nodes

    def _get_text(self):
        text = []
        for component in self.components:
            t = component.text
            if t:
                text.append(t)
        return ' '.join(text)

    def _set_text(self, text):
        self.components = []
        self.addComponent(text) # Create Text instance if text is a string

    text = property(_get_text, _set_text)

    # self.parents    Answer the list of parent components

    def _get_parents(self):
        # Answer the list of parents.
        # If there is no parent, answer an empty list.
        parent = self.parent
        if parent is not None:
            return parent.parents + [parent]
        return []

    parents = property(_get_parents)

    # self.pages

    def _get_pages(self):
        # Answer a list with all components that have a URL.
        # Normally this is a page, but it can also be another type of component.
        # Don't drill down.
        pages = []
        for component in self.root.components:
            if component.url:
                pages.append(component)
        return pages

    pages = property(_get_pages)

    # self.root

    def _get_root(self):
        u"""
        Answers the root component of the self.parents.
        """
        parents = self.parents
        if parents:
            return parents[0]
        return self

    root = property(_get_root)

    # self.media            Get the media from self.style

    def _get_media(self):
        u"""
        Answers the collected media from self.style. If empty or self.style does not exist, answer an empty list.
        """
        style = self.style
        if style:
            return style.media
        return []

    media = property(_get_media)

    # self.selector    Construct the style selector of this component: #id, style.selector or class name.

    def _set_selector(self, selector):
        u"""
        Stores the (CSS) <i>selector</i> in self.style.
        """
        if isinstance(selector, (list, tuple)):
            selector = ' '.join(selector)
        self.style.selector = selector

    def _get_selector(self):
        """
        If <b>self.style</b> doesn’t support a selector, then <b>None</b> is answered. In this case the selector block
        opening and block close must be omitted by the caller. Just the component block will be processed. Otherwise the
        (CSS) selector is defined in order by <b>self.style.selector</b>, <b>self.getClassName()</b>.
        """
        selector = self.style.selector
        if selector is None:
            class_ = self.class_ or self.getClassName()
            if isinstance(class_, (tuple, list)):
                class_ = class_[-1]
            if class_ is not None:
                selector = self.TAGNAME + '.' + class_
        return selector

    selector = property(_get_selector, _set_selector)

if __name__ == '__main__':
    cc = [
        # selector: .component
        Component(),
        # selector: #myId
        Component(selector='#myId'),
        # selector: #myId
        Component(id='#myId'),
        # selector: div.myClass
        Component(selector='div.myClass'),
        # selector: div.myClass
        # selector: myOther
        Component(class_='myOther'),
        # selector: .component
        # prefixClass: xxx zzz ddd component
        Component(prefix='xxx zzz ddd'),
        # selector: .component
        # class_: ddd
        # prefix: zzz
        # prefixClass: zzz ddd
        Component(prefix='zzz', class_='ddd'),
    ]
    for c in cc:
        print 'Selector', c.selector, 'Id', c.id, 'Class', c.class_, 'Prefix', c.prefix, 'PrefixClass', c.prefixClass
