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

class Data(object):
    def __init__(self, **kargs):
        for key, item in kargs.items():
            setattr(self, key, item)
    
    def __getattr__(self, key):
        return self.__dict__.get(key)
    
class Adapter(object):
    u"""
    The Adapter classes connect the templates to content. Note that an adapter always returns plain text/content
    elements (which can include plain HTML), not components. The conversion needs to be done by the calling
    component.
    """
    def __init__(self, root=None):
        # Store optional root, so the adapter knows where to find stuff.
        self.root = root
        self.initialize()
        
    def initialize(self):
        pass
    
    def get(self, component, contentID, **kwargs):
        u"""
        This get method is the core routine to make the adapter produce content. 
        There are two levels of dispatching matches: search for an adapter method that matches 
        the contentID and if that cannot be found the method that matches the component class name.
        contentID of "featuredArticles" will search for adapter method "getFeaturedArticles"
        component class "MainContent" will search for adapter method "getMainContent".
        All adapter method need to answer a Data instance, where the requested data is embedded.
        """
        data = hook1 = hook2 = None
        if contentID is not None:
            hook1 = TX.asGetMethodName(contentID)
            if hasattr(self, hook1):
                data = getattr(self, hook1)(component, **kwargs)
        if data is None:
            hook2 = TX.asGetMethodName(component.__class__.__name__)
            if hook1 != hook2 and hasattr(self, hook2):
                data = getattr(self, hook2)(component, **kwargs)
        if data is None:
            data = Data(error='[Component] Could not find adapter.%s() or adapter.%s()' % (hook1, hook2))
            print data.error
        return data

    def getPageTitle(self, component, **kwargs):
        return Data(text='Untitled') # To be redefined by inheriting adapter class.
    
    def getSocialMedia(self, component, **kwargs):
        return Data(text='Social icons')

    def getFeaturedArticleThumbs(self, component, **kwargs):
        return Data(text='Featured Article thumbs')

    def getTagCloud(self, component, **kwargs):
        return Data(text='Tag Cloud ' * kwargs.get('count', 10))

    def getChapters(self, component, **kwargs):
        return Data(items=('Chapter1', 'Chapter2', 'Chapter3'))

    def getFeaturedArticles(self, component, **kwargs):
        return Data(items=('Featured article1', 'Featured article2', 'Featured article3'))

    def getArticles(self, component, **kwargs):
        return Data(items=('Article1', 'Article2', 'Article3'))

    def getArticle(self, component, **kwargs):
        return Data(text='Article ' * 300)

    def getFooter(self, component, **kwargs):
        return Data(text='Footer ' * 20)

    def getLogo(self, component, **kwargs):
        return Data(text='Logo ' * 4)
    
    def getLogoUrl(self, component, **kwargs):
        return Data(url='http://data.xierpa.com.s3.amazonaws.com/_images/xierpa_x_green.png')
    
    def getPages(self, component, count=10):
        return Data(items=(Data(name='Page', url='/page'),)*count)

    def getMobilePages(self, component, count=10):
        return Data(items=(Data(name='MobilePage', url='/mobilepage'),)*count)
    
