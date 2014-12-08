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
from xierpa3.toolbox.storage.article import Article
from xierpa3.constants.constants import Constants
    
class Adapter(object):
    u"""
    The Adapter classes connect the templates to content. Note that an adapter always a <b>Data</b>
    instance with attributes fields that fit the request. The caller needs to check if the requested fields
    really where filled. In case of an error the *article.error* field is holding the error message
    and the error fields are <b>None</b>. In case there is an unknown request, the output text is
    equal to the error message.
    """
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Constants

    ARTICLECLASS = Article
    
    def __init__(self, root=None):
        # Store optional root, so the adapter knows where to find stuff.
        self.root = root
        self.initialize()

    @classmethod
    def newArticle(cls, **kwargs):
        u"""To allow modification by inheriting classes, answer a new instance of Data."""
        return cls.ARTICLECLASS(**kwargs)
    
    def __repr__(self):
        return '<Adapter: %s>' % self.__class__.__name__

    def __len__(self):
        return len(self.children)

    def initialize(self):
        u"""Optionally to be redefined by inheriting adapter classes. Default behavior is to do nothing."""
        pass
    
    def get(self, contentID=None, **kwargs):
        u"""
        This get method is the core routine to make the adapter produce content. 
        There is a dispatcher level to search for an adapter method that matches 
        the contentID.
        All adapter method need to answer a Data instance, where the requested data is embedded
        as one of the attributes @(article.text, article.url, article.chapters)@.
        """
        article = hook = None
        if contentID is not None:
            hook = TX.asGetMethodName(contentID)
            if hasattr(self, hook):
                article = getattr(self, hook)(**kwargs)
        if article is None:
            message = '[%s] Could not find adapter.%s()' % (self, hook)
            article = self.newArticle(error=message, text=message)
            print article.error
        return article

    # Set of available direct request, which inheriting adapter classes may choose
    # to redefine.
    
    def getSocialMedia(self, **kwargs):
        return self.newArticle(text='[Social media icons]')

    def getTagCloud(self, **kwargs):
        return self.newArticle(text='[Tag Cloud]')

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
        return self.newArticle(text='[' + 'Article text of ”%s”]' % id)

    def getArticles(self, ids=None, start=0, count=1, selector=None, order=None, **kwargs):
        u"""Answer the articles as indicated by the arguments. There are several types
        of selection possible. <b>self.getArticles(count=4)</b> will answer the 
        first 4 articles in the current sort order of articles. <b>self.getArticles(start=5, count=3)</b>
        will answer the articles with index 5, 6 and 7 in the current sort order of articles.
        <b>self.getArticles(ids=('aaa', 'bbb', 'ccc'))</b> will answer the articles with
        the indicated id in the defined order."""
        articles = []
        if ids is None:
            ids = self.getArticleIds(start=start, count=count, selector=selector, order=None, **kwargs)
        for id in ids:
            kwargs['id'] = id # Cannot be direct argument?
            articles.append(self.getArticle(**kwargs))
        return articles

    def getChapter(self, index=0, **kwargs):
        u"""Answer the chapter with in index of the current article."""
        return self.newArticle(chapter=index, text='[Chapter %d]' % index)
 
    def getChapters(self, **kwargs):
        u"""Answer a list of the selected article chapters."""
        article = self.getArticle(**kwargs)
        if article is not None:
            return article.chapters
        return  []

    # P A G E  S T U F F
        
    def getFavIcon(self, **kwargs):
        return self.newArticle(url=self.C.URL_FAVICON)
    
    def getPageTitle(self, **kwargs):
        return self.newArticle(text='Untitled') # To be redefined by inheriting adapter class.

    def getFooter(self, **kwargs):
        return self.newArticle(text='[' + 'Footer text. ' * 20 + ']')

    def getLogo(self, **kwargs):
        return self.newArticle(text='[Logo]', url=self.C.URL_LOGO)
   
    def getPages(self, count=10):
        pages = []
        for i in range(count):
            pages.append(self.newArticle(name='Page', url='/page'),)

    def getMobilePages(self, count=10):
        pages = []
        for i in range(count):
            pages.append(self.newArticle(name='MobilePage', url='/mobilepage'),)
        
    def getDescription(self):
        u"""Answer the description of the site (or page) to be used in the head.meta.description tag."""
        return self.newArticle(text=u'Description of the site here.')
    
    def getKeyWords(self):
        u"""Answer the keywords of the site (or page) to be used in the head.meta.keywords tag."""
        return self.newArticle(text='Keywords of the site here.')
