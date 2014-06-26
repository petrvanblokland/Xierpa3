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
#   adapter.py
#
from xierpa3.toolbox.transformer import TX
from xierpa3.toolbox.storage.status.status import Data
from xierpa3.constants.constants import C

class Data(object):
    u"""Generic data instance, answered by every adapter query."""
    def __init__(self, **kargs):
        self.items = [] # Make sure that self.items is always iterable.
        for key, item in kargs.items():
            setattr(self, key, item)
    
    def __getattr__(self, key):
        return self.__dict__.get(key)
    
    def __repr__(self):
        return '[Data] %s' % `self.__dict__`
    
class Adapter(C):
    u"""
    The Adapter classes connect the templates to content. Note that an adapter always a <b>Data</b>
    instance with attributes fields that fit the request. The caller needs to check if the requested fields
    really where filled. In case of an error the <b>data.error</b> field is holding the error message
    and the error fields are <b>None</b>. In case there is an unknown request, the output text is
    equal to the error message.
    """
    DATACLASS = Data
    
    def __init__(self, root=None):
        # Store optional root, so the adapter knows where to find stuff.
        self.root = root
        self.initialize()
    
    @classmethod
    def newData(cls, **kwargs):
        u"""To allow modification by inheriting classes, answer a new instance of Data."""
        return cls.DATACLASS(**kwargs)
    
    def __repr__(self):
        return '<Adapter: %s>' % self.__class__.__name__
       
    def initialize(self):
        u"""Optionally to be redefined by inheriting adapter classes. Default behavior is to do nothing."""
        pass
    
    def get(self, contentID=None, **kwargs):
        u"""
        This get method is the core routine to make the adapter produce content. 
        There is a dispatcher level to search for an adapter method that matches 
        the contentID.
        All adapter method need to answer a Data instance, where the requested data is embedded
        as one of the attributes <b>(data.text, data.url, data.items)</b>.
        """
        data = hook = None
        if contentID is not None:
            hook = TX.asGetMethodName(contentID)
            if hasattr(self, hook):
                data = getattr(self, hook)(**kwargs)
        if data is None:
            message = '[%s] Could not find adapter.%s()' % (self, hook)
            data = self.newData(error=message, text=message)
            print data.error
        return data

    # Set of available direct request, which inheriting adapter classes may choose
    # to redefine.
    
    def getSocialMedia(self, **kwargs):
        return self.newData(text='[Social media icons]')

    def getTagCloud(self, **kwargs):
        return self.newData(text='[Tag Cloud]')

    # A R T I C L E
    
    def getArticleIds(self, start=0, count=1, selector=None, order=None, **kwargs):
        u"""Answer the list article ids in the current sort order. To be redefined
        but inheriting adapter classes. Default behavior is the answer an list of index
        numbers from <b>start</b> to <b>start+count</b>.
        The <b>selector</b> and <b>order</b> indicate the kind of articles to be 
        selected and the order in which they should be indexed. """
        return range(start, count) # Ignore selector and order in the base method.

    def getArticle(self, id=None, index=0, selector=None, order=None, **kwargs):
        u"""Answer the article, indicate by <b>id</b>. If <b>id</b> is <b>None</b>
        or omitted, then try to find the id the sort order of article ids at <b>index</b>."""
        if id is None:
            id = self.getArticleIds(start=index, selector=selector, order=order, **kwargs)
        return self.newData(text='[' + 'Article text of ”%s”]' % id)

    def getArticles(self, ids=None, start=0, count=1, selector=None, order=None, **kwargs):
        u"""Answer the articles as indicated by the arguments. There are several types
        of selection possible. <b>self.getArticles(count=4)</b> will answer the 
        first 4 articles in the current sort order of articles. <b>self.getArticles(start=5, count=3)</b>
        will answer the articles with index 5, 6 and 7 in the current sort order of articles.
        <b>self.getArticles(ids=('aaa', 'bbb', 'ccc')</b> will answer the articles with
        the indicated id in the defined order."""
        items = []
        if ids is None:
            ids = self.getArticleIds(start=start, count=count, selector=selector, order=None, **kwargs)
        for id in ids:
            assert id is not None
            items.append(self.getArticle(id=id, **kwargs))
        return self.newData(items=items)

    def getChapter(self, index, **kwargs):
        u"""Answer the chapter with in index of the current article."""
        return self.newData(index=index, text='[Chapter %d]' % index)
 
    def getChapters(self, **kwargs):
        u"""Answer a list of featured chapters. Also answer the article itself
        as <b>data.article</b>."""
        items = []
        for index in kwargs.get('count', 1):
            items.append(self.getChapter(index=index, **kwargs))
        return self.newData(items=items, article=self.getArticle(**kwargs))
   
    # P A G E  S T U F F
        
    def getFavIcon(self, **kwargs):
        return self.newData(url=C.URL_FAVICON)
    
    def getPageTitle(self, **kwargs):
        return self.newData(text='Untitled') # To be redefined by inheriting adapter class.
    
    def getMenu(self, count=1, **kwargs):
        return self.newData(items=(
            self.newData(text='Menu 1', url='/home'),
            self.newData(text='Menu 2', url='/home'),
            self.newData(text='Menu 3', url='/home'),
        ))

    def getFooter(self, **kwargs):
        return self.newData(text='[' + 'Footer text. ' * 20 + ']')

    def getLogo(self, **kwargs):
        return self.newData(text='[Logo]', url=C.URL_LOGO)
   
    def getPages(self, count=10):
        return self.newData(items=(self.newData(name='Page', url='/page'),)*count)

    def getMobilePages(self, count=10):
        return self.newData(items=(self.newData(name='MobilePage', url='/mobilepage'),)*count)
        
    def getDescription(self):
        u"""Answer the description of the site (or page) to be used in the head.meta.description tag."""
        return self.newData(text=u'Description of the site here.')
    
    def getKeyWords(self):
        u"""Answer the keywords of the site (or page) to be used in the head.meta.keywords tag."""
        return self.newData(text='Keywords of the site here.')
    