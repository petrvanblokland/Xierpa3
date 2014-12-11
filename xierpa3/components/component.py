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
import os
import weakref
import hashlib
import inspect
import textile
from xierpa3.adapters import BlurbAdapter
from xierpa3.descriptors.style import Style
from xierpa3.descriptors.blueprint import BluePrint
from xierpa3.constants.constants import Constants
from xierpa3.toolbox.transformer import TX
from xierpa3.attributes import Perc, Color

class Component(object):
    u"""
    The Component describes the abstract behavior of components on the page.
    """
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Constants
    # Root default style template. To be cascaded by inheriting classes.
    BLUEPRINT = BluePrint(
        # Default behavior of images, use class autowidth to cover differences between browsers.
        imgClass=C.CLASS_AUTOWIDTH, doc_imgClass=u'Image class, set default to AUTOWIDTH.',
        imgMaxWidth=Perc(100), doc_imgMaxWidth=u'Image maximal width',
        imgMinWidth=0, doc_imgMinWidth=u'Image minimal width',
    )
    TAGNAME = 'div' # By default every component has a root div element.
    BUILD_CSS = True # Default behavior of every component is to build in CSS.
    STYLE_DEFAULT = {} # Default style source, optionally redefined by inheriting classes.

    ADAPTER = BlurbAdapter() # Unless defined otherwise by inheriting classes.

    def __init__(self, components=None, style=None, id=None, parent=None, name=None,
            css=None, fonts=None, prefix=None, class_=None, type=None, contentID=None,
            repeat=1, title=None, url=None, template=None, editable=False,
            adapter=None, selector=None, **kwargs):
        # The class name of the components is used as class names in SASS/CSS
        # Initialize the self.style, as selector and id are stored there.
        self.style = style # If style is None, then use a copy of the self.BLUEPRINT style.
        self.style.add(kwargs) # Overwrite further initialize self.style from rest of arguments
        self.style.title = title # Page or other component title
        self.style.component = self # Add the weakref reference to self for the root style.
        # Adapter for reading content/data
        self.adapter = adapter # If None, then "parent.adapter or self.ADAPTER" is used
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
        # If kept None, then the self.adapter will be queried for the title.
        # This allows both the definition of static names (per page template) or the usage
        # of page titles that depend on the current url.
        # If the self.adapter answers None as title, then use self.TITLE
        self.title = title
        # Prefix of class and selector, stored as self.style.prefix. Shows in CSS selector as myPrefix.class
        self.prefix = prefix
        # Cache for the unique ID based on the content tree, so components can be compared.
        self._uid = None
        self.template = template # Optional template match with URL parameter
        self.contentID = contentID # Optional unique id to query content from the self.adapter
        self.parent = parent # Weakref to parent component
        self.repeat = repeat # TODO: Make this work. Repeat count for repeating this component in output
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

    def _getInheritedClasses(self):
        u"""Private method. Answer the list of inherited parent classes by this component."""
        return list(inspect.getmro(self.__class__))

    def _getInheritedClassNames(self):
        u"""Private method. Answer the list of inherited class names by this component."""
        names = []
        for cls in self._getInheritedClasses():
            names.append(cls.__name__)
        return names

    @classmethod
    def getRootDir(cls):
        u"""Answer the default root directory path, e.g. to store example files and cached SASS/CSS."""
        return TX.asDir(cls.C.PATH_EXAMPLES + cls.getPythonClassName().lower() + '/') # Expand user path to full directory path.

    @classmethod
    def getClassName(cls):
        u"""Answers the class name of the *cls* as capitalized name."""
        name = cls.__name__
        return name[0].lower() + name[1:]

    @classmethod
    def getPythonClassName(cls):
        u"""Answer the Python class name of @self@."""
        return cls.__name__

    def isLast(self, component):
        u"""Allow components to test the parent if they are last."""
        return self.components and self.components[-1] is component

    def getColClass(self, col):
        u"""Answer the colClass, based on the numeric *col* value and if the component is the
        last in the parent list of child components."""
        colClass = TX.col2Class(col)
        if self.parent is None or self.parent.isLast(self):
            colClass = (colClass, self.C.CLASS_LAST)
        return colClass

    def getTitle(self, path):
        u"""Answer the page title as defined in the style or answered by @self.adapter@.
        The adapter can use the @path@ argument to fine-tune the title."""
        pageTitle = self.style.title
        articleTitle = self.adapter.getPageTitle(path=path)
        if pageTitle and articleTitle:
            return '%s | %s' % (pageTitle, articleTitle)
        return pageTitle or articleTitle

    def getFavIcon(self, builder):
        u"""Call back from the builder to answer the favIcon url. This method can be redefined 
        by inheriting classes if the favIcon is depending on the content and status of a page.
        Defautl is to answer style value @self.style.favIcon@."""
        if self.style and self.style.favIcon:
            return self.style.favIcon
        return None

    # self.className        Answer self.style.className or otherwise class name is directly derived from the object class.

    def _get_className(self):
        u"""Get method of property @self.className@. Use the property instead of this method."""
        # @@@ Clean this up, so self.className is used everywhere instead of self.getClassName() or self.class_
        return self.style.className or self.getClassName()

    className = property(_get_className)

    def getPrefixClass(self, prefix2=None):
        u"""Answers the extended class name @self.prefix + self.prefix2 + self.class_@.
        If @self.class_@ is not defined, and @self.prefix + self.prefix2@ are defined,
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
        Sets the self.components. If components is None, then use the result of @self.baseComponents()@.
        If *components* is a single component, then make it into a list.
        """
        if components is None:
            components = self.baseComponents()
        elif not isinstance(components, (list, tuple)):
            components = [components]
        self.components = components # Create parent weakrefs in the components to self

    def initialize(self):
        u"""Called by every component when the constructor finished. This allows inheriting
        component classes to adjust default settings. Inheriting classes need to redefine the
        method. Default behavior is to do nothing."""
        pass

    def readFile(self, path):
        u"""Generic method to read from local file system. Answer None if the file does not exist."""
        if os.path.exists(path):
            f = open(path, 'rb')
            s = f.read()
            f.close()
            return s
        return None

    def getRootPath(self):
        u"""Answer the file path of @from xierpa3 import components@."""
        from xierpa3 import components
        return components.__path__[0]

    def baseComponents(self):
        """To be redefined by inheriting classes to answer the default child
        components of the component."""
        return []

    def isEmpty(self):
        """Answer the boolean flag if this component has any attributes or child
        components."""
        return len(self.components) == 0 and self.style.isEmpty()

    def isEmptyCss(self):
        u"""Answer the boolean flag if this component will generate CSS content. This is different from the regular
        @self.isEmpty@, since there may be components with content that have @self.BUILD_CSS@
        set to @False@. When @self.BUILD_CSS is True@ it still should build if there is CSS
        content that has set @self.BUILD_CSS@ to @True@.
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
        u"""Answer the boolean flag of there is valid CSS for this component. If not
        @self.isEmptyCss()@ then answer @False@. Otherwise answer of there is a
        @self.selector@ in the component."""
        if self.isEmptyCss():
            return False
        return bool(self.selector)

    def isComponent(self, name):
        """Answer the boolean flag if this is a component where @name == self.name@."""
        return name == self.name or (name in self.class_ or []) # Compare with self._name or class names

    def getComponent(self, name):
        """Answer the child component that matches *name.*"""
        for component in self.components:
            if component.isComponent(name):
                return component
        return None

    def build(self, b):
        u"""
        Test on the type of building to be done here by builder *b*.
        Normally the plain @self.buildBlock@ will be called, but it is possible
        to catch the call by implementing a method, dedicated for a particular
        kind of builder. @self.buildBlock_[builder.ID]@ will then called instead.
        E.g. @self.buildBlock_css(b)@ will force the CSS builder to call that
        method instead of the regular @self.buildBlock(b)@. Note that this only should be
        exceptional situation where there is no way to make the builder call abstract.
        Normally components should not be aware which builder they are talking to.
        """
        hook = 'buildBlock_' + b.ID
        if hasattr(self, hook):
            buildBlock = getattr(self, hook)
        else:
            buildBlock = self.buildBlock # Not special dispatch, use generic method instead.
        buildBlock(b)

    def buildBlock(self, b):
        u"""
        Generic builder *b* for all child components of @self@.
        Can be redefined by an inheriting class.
        """
        b.block(self)
        for component in self.components:
            component.build(b)
        b._block(self)

    def buildAjaxDict(self, site=None, d=None):
        u"""Answer the ajax result dictionary that gets sent back as json."""
        if d is None:
            d = {}
        if site is None:
            site = self
        for component in self.components:
            component.buildAjaxDict(site, d)
        return d

    def buildJS(self, b):
        u"""
        Will be called for every component in the tree, so each is allows to build its own
        Javascript at the end of a document. Default behavior is to ignore this for other
        than the HtmlBuilder and the just call the child components. Inheriting component
        classes that want to export Javascript need to redefined this method."""
        if b.isType('html'): 
            for component in self.component:
            component.builsJS(b)

    # D O C U M E N T A T I O N

    def buildDocumentation(self, b):
        u"""Builder of the documentation of self. It is the main method generating this
        documentation page."""
        b.page(self)
        b.div(class_=self.C.CLASS_DOCUMENTATION, width=Perc(100))
        self.buildDocumentationBlock(b)
        b._div(comment=self.C.CLASS_DOCUMENTATION)
        b._page(self)

    def buildDocumentationBlock(self, b, processed=None):
        u"""Recursive call to build the documentation of @self@ and its child
        components, using builder *b*. It is the method generating the
        documentation for this component.
        The information extracted includes the level of inheritance of the component,
        the general description, as defined in the class doc string, a list of child
        components, a table with the available cascaded method and the component style,
        which cascades from the parent class @BLUEPRINT@ definitions."""
        if processed is None:
            processed = set()
        if self in processed:
            return

        processed.add(self)

        name = self.getPythonClassName()
        b.h1(color='red', fontfamily='Verdana', fontsize=14)
        b.text('Component %s' % name)
        b._h1()
    
        # Doc string as class descriptor, if is exists.
        if self.__doc__:
            b.text(textile.textile(self.__doc__))
        b.p()
        if self.components:
            componentList = []
            for component in self.components:
                componentList.append(component.name)
            if len(componentList) > 1:
                componentLabel = 'components'
            else:
                componentLabel = 'component'
            b.text('This <b>%s</b> instance contains %d child %s: <b>%s</b>.' % (name, len(componentList), componentLabel, ', '.join(componentList)))
        else:
            b.text('<b>%s</b> has no child components.' % name)
        b._p()
        # Inheritance
        b.p()
        b.text(u'<b>%s</b> → %s' % (name, u' → '.join(self._getInheritedClassNames()[1:])))
        b._p()
        # Show the component style
        b.h2()
        b.text('Style from cascaded BluePrints')
        b._h2()
        b.table(width=Perc(100))
        b.tr()
        for class_, label, width in (('name', 'Name', Perc(25)), ('value', 'Value', Perc(25)), ('description', 'Description', Perc(50))):
            b.th(class_=class_, width_html=width)
            b.text(label)
            b._th()
        b._tr()
        for key, value in sorted(self.style.items()):
            b.tr()
            b.td(class_='name')
            b.text(key)
            b._td()
            b.td(class_='value', textalign=self.C.RIGHT)
            if value is None:
                b.span(style='color:#888;')
                b.text('(Inherited)')
                b._span()
            elif isinstance(value, Color):
                b.text('%s' % value)
                b.span(style='background-color:%s;' % value)
                b.text('&nbsp;'*4)
                b._span()
            elif isinstance(value, (tuple, list)):
                b.text(`value`)
            elif not isinstance(value, basestring):
                b.text('%s' % value)
            elif value.startswith('//'):
                b.img(src=value, width=50) # Show the image
            elif len(value) > 50:
                b.text(value[:50] + '...')
            else:
                b.text(value)
            b._td()
            b.td(class_='description')
            doc = self.style.getDoc(key)
            if doc is not None:
                b.text(textile.textile(doc))
            b._td()
            b._tr()
        b._table()
        # Attributes of this component
        b.h2()
        b.text('Attributes')
        b._h2()
        b.table(width=Perc(100))
        b.tr()
        b.th()
        b.text('Name')
        b._th()
        b.th()
        b.text('Attributes')
        b._th()
        b.th()
        b.text('Description')
        b._th()
        b._tr()
        for name, value in self.__dict__.items():
            if name.startswith('_'):
                continue
            b.tr()
            b.td(class_='name')
            b.text(name)
            b._td()
            b.td(class_='value')
            b.text(`value`)
            b._td()
            b.td(class_='description')
            b.text('...')
            b._td()
            b._tr()
        b._table()
        # Methods of this component
        b.h2()
        b.text('Methods')
        b._h2()
        b.table(width=Perc(100))
        b.tr()
        b.th(class_='name')
        b.text('Name')
        b._th()
        b.th(clas_='value')
        b.text('Arguments')
        b._th()
        b.th(class_='description')
        b.text('Description')
        b._th()
        b._tr()
        for name, method in inspect.getmembers(self.__class__, predicate=inspect.ismethod):
            if name.startswith('__'):
                continue
            b.tr()
            b.td(class_='name')
            b.text(name)
            b._td()
            b.td(class_='value')
            args, varargs, keywords, defaults = inspect.getargspec(method)
            for index, arg in enumerate(args):
                if arg == 'self':
                    continue
                b.text(arg)
                if defaults is not None and index < len(defaults):
                    b.text('=%s' % defaults[index])
                b.br()
            #b.text(varargs)
            if keywords:
                b.text('**%s' % keywords)
                b.br()
            #b.text(`defaults`)
            b._td()
            b.td(class_='description')
            if method.__doc__:
                b.text(textile.textile(method.__doc__))
            b._td()
            b._tr()
        b._table()
        # Show recursively the rest of the components
        for component in self.components:
            component.buildDocumentationBlock(b, processed)
        
    # X M L  R E N D E R I N G

    def buildElement(self, b, element):
        u"""Recursive rendering of the etree element, using the document methods in the builder
        as defined in the @DocumentBuilderPart@ class. The elements are translated
        to the standard tag behavior of the builder."""
        b.docTagElement(element)
        b.text(element.text) # Plain text output of the element
        for child in element: # Recursively render all element children.
            self.buildElement(b, child)
        b._docTagElement(element)
        b.text(element.tail) # Plain text output of the element tail

    # A T T R I B U T E S

    # self.hashedID

    def _get_hashedID(self):
        u"""Get-only property @self.hashedID@. 
        Answer the calculated unique ID based on the content. This ID can be compared between components to decide if they are
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
        """Set/Get property @self.name@.
        Answer one of @self._name or self.id or self.class_ or self.getClassName()@.
        The name attribute is for text identification of an element. It is not guaranteed to be unique."""
        name = self._name or self.id or self.class_
        if name is None: # Still None?
            # Same as self.getClassName(), but that method answers None for some component classes.
            name = self.__class__.__name__
            name = name[0].lower() + name[1:] # First letter as lower case
        return name

    def _set_name(self, name):
        """Set/Get property @self.name@.
        Set @self._name@ to *name*."""
        self._name = name

    name = property(_get_name, _set_name)

    # self.oge

    def _get_urlName(self):
        """Get-only property @self.urlName@.
        Answer the url safe version of @self.name@."""
        return TX.name2UrlName(self.name)

    urlName = property(_get_urlName)

    # self.url

    def _get_url(self):
        u"""Set/Get property @self.url@.
        Answer the url of this component. Otherwise answer @None@."""
        if self._url is None:
            return TX.label2ParamId(self.name)
        return self._url

    def _set_url(self, url):
        u"""Set/Get property @self.url@.
        Set the @self._url@ to *url*."""
        self._url = url

    url = property(_get_url, _set_url)

    # self.style

    def newStyle(self, selector=None, d=None):
        u"""Answer a new style with @selection@ and attributes defined in the optional *d* dictionary.
        using *selector*."""
        if d is None:
            d = {}
        return Style(selector, **d)

    def baseStyle(self):
        u"""Answer the base style for this component, before the BluePrint parameters
        are copied into it. This can be cone by inheriting classes defining htis method.
        Default behavior is just to answer the result of @self.newStyleI()@."""
        return self.newStyle()

    def addStyle(self, selector=None, **kwargs):
        u"""Add the *selector* and style attributes @**kwargs@ to @self.style@."""
        return self.style.addStyle(selector, **kwargs)

    def addMedia(self, selector=None, **kwargs):
        u"""Add the *selector* media style, defined in @**kwargs@ to @self.style@."""
        self.style.addMedia(selector=selector, **kwargs)

    def _get_style(self):
        u"""Set/Get property @self.style@.
        If it doesn't exist yet, create the default style from self.copyBluePrint.
        If not defined yet, then create a new instance of @Style@, initialized by the aggregation of the cascading
        @self.BLUEPRINT@ of the inherited classes."""
        if self._style is None:
            self._style = self.baseStyle() # Allow theme to define the base style.
            # Get the list of classes that self is inheriting from.
            inheritedClasses = self._getInheritedClasses()
            inheritedClasses.reverse()
            for inheritedClass in inheritedClasses:
                if hasattr(inheritedClass, 'BLUEPRINT'):
                    self._style.addBluePrint(inheritedClass.BLUEPRINT)
            self._style.addBluePrint(self.BLUEPRINT)
        return self._style

    def _set_style(self, style):
        u"""Set/Get property @self.style@.
        Set the @self._style@ to *style*."""
        assert style is None or isinstance(style, Style)
        self._style = style

    style = property(_get_style, _set_style)

    # self.css

    def _get_css(self):
        u"""Set/Get property @self.css@.
        Answer the list of CSS URLs for this component. If there is a parent, then answer the css of the parent,
        Otherwise answer the default list."""
        css = self.style.css
        if css is None and self.parent:
            return self.parent.css
        return ['css/style.css']

    def _set_css(self, urls):
        u"""Set/Get property @self.css@.
        Set the list of CSS URLs for this component to *urls*. 
        If there is a parent, then answer the css of the parent, Otherwise answer the default list."""
        assert urls is None or isinstance(urls, (tuple, list))
        self.style.css = urls

    css = property(_get_css, _set_css)

    # self.fonts

    def _get_fonts(self):
        u"""Set/Get property @self.font@.
        Answer the list of web font urls for this component. If there is a parent, then answer the fonts of
        the parent. Otherwise answer the default list."""
        fonts = self.style.fonts
        if fonts is None and self.parent:
            return self.parent.fonts
        return fonts

    def _set_fonts(self, urls):
        u"""Set/Get property @self.font@.
        Set the list of web font urls for this component to *urls*."""
        if urls is None:
            urls = []
        assert isinstance(urls, (tuple, list))
        self.style.fonts = urls

    fonts = property(_get_fonts, _set_fonts)

    # self.prefix

    def _get_prefix(self):
        u"""Set/Get property @self.prefix@.
        Answer the prefix of class."""
        return self.style.prefix

    def _set_prefix(self, prefix):
        u"""Set/Get property @self.prefix@.
        Set the prefix of class to *prefix*."""
        self.style.prefix = prefix

    prefix = property(_get_prefix, _set_prefix)

    # self.class_     Answer the self._class. This value can be None.

    def _get_class_(self):
        u"""Set/Get property @self.class_@.
        Answer the class name of @self@. Use the property instead of this method."""
        return self.style.class_

    def _set_class_(self, class_):
        u"""Set/Get property @self.class_@.
        Set the class name of @self@ to *class_*. Use the property instead of this method."""
        self.style.class_ = class_

    class_ = property(_get_class_, _set_class_)

    # self.prefixClass

    def _get_prefixClass(self):
        u"""Get-only property @self.prefixClass@ 
        Answer the result of @self.getPrefixClass()@. Use the property instead of this method."""
        return self.getPrefixClass()

    prefixClass = property(_get_prefixClass)

    # self.id

    def _get_id(self):
        u"""Set/Get property @self.id@.
        Answer the id of @self@. Use the property instead of this method."""
        return self.style.id

    def _set_id(self, id):
        u"""Set/Get property @self.id@.
        Set the id of @self@ to *id*. Use the property instead of this method."""
        self.style.id = id

    id = property(_get_id, _set_id)

    # self.adapter

    def _get_adapter(self):
        u"""Property @self.adapter@ Answer the adapter of @self@. Although it may
        be change during the course of development (and also force otherwise), a component
        keeps the instance of the adapter. The reason is that we want caching to be done by
        the adapter. Builders are only created temporary, so they should not hold the adapter.
        Use the property instead of this method."""
        if self._adapter is not None:
            return self._adapter
        if self.parent is not None:
            return self.parent.adapter
        return self.ADAPTER # Use default adapter of this component

    def _set_adapter(self, adapter):
        u"""Set the adapter for this component. This allows various components to have
        their own adapter. If not defined, the component will take the adapter
        of its parent. If the parent adapter is @None@, then don’t overwrite
        the adapter of the builder during runtime. Use the property instead of this method."""
        self._adapter = adapter

    adapter = property(_get_adapter, _set_adapter)

    # self.components

    def addComponent(self, component):
        u"""Add *component* to the @self.component@ list of children."""
        if isinstance(component, basestring):
            from text import Text
            component = Text(component)
        component.parent = self
        self._components.append(component)

    def _set_components(self, components):
        u"""Get/Set property @self.components@.
        Set the @self._components@ to *components*. If *components* is not a tuple
        or a list, then convert the single component into a list first. Set the 
        @component.parent@ to self for every component in the list.
        Use the property instead of this method."""
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
        u"""Get/Set property @self.components@.
        Answer @self._components@. Use the property instead of this method."""
        return self._components

    components = property(_get_components, _set_components)

    # self.parent    Parent component

    def _set_parent(self, parent):
        u"""Get/Set property @self.parent@.
        Set @self._parent to the weakref of *parent*. Use the property instead of this method."""
        if parent is not None:
            self._parent = weakref.ref(parent)
        else:
            self._parent = None

    def _get_parent(self):
        u"""Get/Set property @self.parent@.
        Answer the converted weakref of @self._parent@ if it exists and if it is a valid reference.
        Answer @None@ otherwise. Use the property instead of this method."""
        if self._parent is not None:
            return self._parent()
        return None

    parent = property(_get_parent, _set_parent)

    # self.text     Collect all text from the component nodes

    def _get_text(self):
        u"""Get/Set property @self.text@.
        Answer the plain text of the @self@ and recursively called from all child components.
        Use the property instead of this method."""
        text = []
        for component in self.components:
            t = component.text
            if t:
                text.append(t)
        return ' '.join(text)

    def _set_text(self, text):
        u"""Get/Set property @self.text@.
        Reset @self.components@ to a list with a @Text(text) instance inside.
        Use the property instead of this method."""
        self.components = []
        self.addComponent(text) # Create Text instance if text is a string

    text = property(_get_text, _set_text)

    # self.parents    Answer the list of parent components

    def _get_parents(self):
        u"""Get-only property @self.parents@.
        Answer the list of parents. If there is no parent, answer an empty list.
        Use the property instead of this method."""
        parent = self.parent
        if parent is not None:
            return parent.parents + [parent]
        return []

    parents = property(_get_parents)

    # self.pages

    def _get_pages(self):
        u"""Get-only property @self.pages@.
        Answer a list with all components that have a URL.
        Normally this is a page, but it can also be another type of component.
        Don't drill down. Use the property instead of this method."""
        pages = []
        for component in self.root.components:
            if component.url:
                pages.append(component)
        return pages

    pages = property(_get_pages)

    # self.root

    def _get_root(self):
        u"""Get-only property @self.root@.
        Answers the root component of the @self.parents@. Use the property instead of this method.
        """
        parents = self.parents
        if parents:
            return parents[0]
        return self

    root = property(_get_root)

    # self.media            Get the media from self.style

    def _get_media(self):
        u"""Get-only property @self.media@.
        Answers the collected media from @self.style@. 
        If empty or @self.style@ does not exist, answer an empty list.
        Use the property instead of this method."""
        style = self.style
        if style:
            return style.media
        return []

    media = property(_get_media)

    # self.selector    Construct the style selector of this component: #id, style.selector or class name.

    def _set_selector(self, selector):
        u"""Get/Set property @self.selector@.
        Stores the (CSS) *selector* in @self.style. Use the property instead of this method.@
        """
        if isinstance(selector, (list, tuple)):
            selector = ' '.join(selector)
        self.style.selector = selector

    def _get_selector(self):
        u"""Get/Set property @self.selector@.
        If @self.style@ doesn’t support a selector, then @None@ is answered. In this case the selector block
        opening and block close must be omitted by the caller. Just the component block will be processed. Otherwise the
        (CSS) selector is defined in order by @self.style.selector@, @self.getClassName()@.
        Use the property instead of this method.
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
