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
        for key, item in kargs.items():
            setattr(self, key, item)
    
    def __getattr__(self, key):
        return self.__dict__.get(key)
    
class Adapter(C):
    u"""
    The Adapter classes connect the templates to content. Note that an adapter always returns plain text/content
    elements (which can include plain HTML), not components. The conversion needs to be done by the calling
    component.
    """
    DATACLASS = Data
    
    def __init__(self, root=None):
        # Store optional root, so the adapter knows where to find stuff.
        self.root = root
        self.initialize()
    
    @classmethod
    def newData(cls, text=None, items=None, url=None, error=None):
        u"""To allow modification by inheriting classes, answer a new instance of Data."""
        return cls.DATACLASS(text=text, items=items, url=url, error=error)
    
    def __repr__(self):
        return '<Adapter: %s>' % self.__class__.__name__
       
    def initialize(self):
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
            data = self.newData(error='[%s] Could not find adapter.%s()' % (self, hook))
            print data.error
        return data

    def getPageTitle(self, **kwargs):
        return self.newData(text='Untitled') # To be redefined by inheriting adapter class.
    
    def getSocialMedia(self, **kwargs):
        return self.newData(text='Social icons')

    def getFeaturedArticleThumbs(self, **kwargs):
        return self.newData(text='Featured Article thumbs')

    def getTagCloud(self, **kwargs):
        return self.newData(text='Tag Cloud ' * kwargs.get('count', 10))

    def getChapters(self, **kwargs):
        return self.newData(items=('Chapter1', 'Chapter2', 'Chapter3'))

    def getFeaturedArticles(self, **kwargs):
        return self.newData(items=('Featured article1', 'Featured article2', 'Featured article3'))

    def getArticles(self, **kwargs):
        return self.newData(items=('Article1', 'Article2', 'Article3'))

    def getArticle(self, **kwargs):
        return self.newData(text='Article ' * 300)

    def getFooter(self, **kwargs):
        return self.newData(text='Footer ' * 20)

    def getLogo(self, **kwargs):
        return self.newData(text='Logo ' * 4)
    
    def getLogoUrl(self, **kwargs):
        return self.newData(url='http://data.xierpa.com.s3.amazonaws.com/_images/xierpa_x_green.png')
    
    def getPages(self, count=10):
        return self.newData(items=(Data(name='Page', url='/page'),)*count)

    def getMobilePages(self, count=10):
        return self.newData(items=(Data(name='MobilePage', url='/mobilepage'),)*count)
    
    def getDescription(self):
        u"""Answer the description of the site (or page) to be used in the head.meta.description tag."""
        return self.newData(text=u'Description of the site here.')
    
    def getKeyWords(self):
        u"""Answer the keywords of the site (or page) to be used in the head.meta.keywords tag."""
        return self.newData(text='Keywords of the site here.')
    