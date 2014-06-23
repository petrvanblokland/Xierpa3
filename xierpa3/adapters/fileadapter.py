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
#    fileadapter.py
#
#    xpath examples: http://msdn.microsoft.com/en-us/library/ms256086(v=vs.110).aspx
#
import os
from lxml import etree
import codecs
from xierpa3.toolbox.transformer import TX
from xierpa3.adapters.adapter import Adapter, Data

class Article(Data):
    u"""Inheriting from the <b>Data</b> class, the <b>Article</b> automatically generates
    (and caches) information from the <b>self.tree</b>."""
    # self.id: Unique id of the article, bound to (unique) file name. Key in the cache
    # self.path: Url path name of the file
    # self.name: Name of the article, derived from the <title> tag.
    # self.items: List of chapter tags, children of the <chapters> tag.
    def __init__(self, **kwargs):
        Data.__init__(self, **kwargs)
        self.name = self.findText('.//meta/title', 'Untitled') # <title>
        self.tag = self.findText('.//meta/tag') # <tag> is the shorted usage of name/title
        self.url = self.findText('.//meta/url') # <url> is the optional url, otherwise /article-name is used.
        self.items = self.findAll('.//chapters/*') # List of <chapters> children
        self.featured = self.findAll('.//featured/*') # List of <featured> articles.
        self.children = self.findAll('.//children/*') # List of <children> articles.
        self.menu = self.findAll('.//menu/*') # List of <menu> children
        self.summary = self.find('.//meta/summary') # <summary>
        self.author = self.findText('.//meta/author')
        self.category = self.findText('.//meta/category') # Category of the article
        self.level = self.findText('.//meta/level')
        self.topic = self.find('.//meta/topic') # Short description of the article
        poster = self.find('.//meta/poster') # First <poster> or <image>
        if poster is None:
            poster = self.find('.//image')
        if poster is None:
            self.poster = None
        else:
            self.poster = poster.attrib['src']
        # Collect the footnotes per chapter
        self.footnotes = []
        for item in self.items:
            self.footnotes.append(item.findall('.//footnote')) # All footnotes per chapter
            
    def __repr__(self):
        return '[Article:%s]' % self.name

    def find(self, xpath):
        return self.tree.find(xpath)
    
    def findAll(self, xpath):
        return self.tree.findall(xpath)
          
    def findText(self, xpath, default=None):
        element = self.find(xpath)
        if element is not None:
            return element.text
        return default
    
class FileAdapter(Adapter):
    u"""
    Adapter for XML file serving
    """
    def initialize(self):
        self._cache = {}
        self.readArticles()
        
    def readArticles(self):
        for id, path in self.getIdPaths():
            xml = self.readXmlFile(self.root + path)
            if xml is not None:
                # Create the article instance and cache the standard query values from the tree.
                article = Article(id=id, path=path, tree=etree.fromstring(xml))
                self.cacheArticle(article)
    
    def readXmlFile(self, fsPath): 
        if not fsPath.endswith('.xml'):
            fsPath += '.xml'           
        if os.path.exists(fsPath):
            f = codecs.open(fsPath, encoding='utf-8', mode='r+')
            xml = f.read()
            f.close()
        else:
            xml = None
        return xml
    
    def cacheArticle(self, article):
        self._cache[article.id] = article
        
    def getCachedArticle(self, id):
        u"""Answer the cached articles. If not available yet, read them through <self.getPaths()<b>."""
        if isinstance(id, list):
            pass
        return self._cache.get(id)
    
    def getCachedArticles(self):
        return self._cache
    
    def getIdPaths(self, path=None, idPaths=None):
        if path is None:
            path = '/'
        if idPaths is None:
            idPaths = []
        for name in os.listdir(self.root + path):
            filePath = path + name
            if name.startswith('.'):
                continue
            if os.path.isdir(self.root + filePath):
                self.getIdPaths(filePath+'/', idPaths)
            elif not name.endswith('.xml'):
                continue
            else:
                name = name.replace('.xml', '')
                idPaths.append((name, filePath))
        return idPaths
    
    def getChapters(self, article):
        if article.items is None:
            return []
        return article.items 
    
    def getChapterByIndex(self, article, index):
        if 0 <= index < len(article.items or []):
            return article.items[index]
        return None
    
    def getChapterTitleByIndex(self, article, index):
        chapter = self.getChapterByIndex(article, index)
        if chapter is not None:
            return chapter.find('./meta/title')
        return None
    
    #    A P I  G E T 
    
    def getPageTitle(self, id=None):
        article = self.getArticle(id)
        if article is not None:
            return Data(text=article.name)
        return None
    
    def getPages(self, count=None):
        pages = Data()
        pages.items = []
        for name, article in self.getCachedArticles().items(): # @@@ Add priority sorting and counting here
            pages.items.append(article)
        return pages
    
    getArticles = getPages
    
    def getMobilePages(self, count=None):
        return self.getPages(count)
    
    def getArticle(self, id=None):
        return self.getCachedArticle(id)
    
    def getFeaturedArticles(self, id, start, count):
        u"""Answer a list of featured articles in the article that has <i>id</i>."""
        data = Data()
        data.items = []
        article = self.getArticle(id)
        if article:
            for index, featured in enumerate(article.featured[start:start+count]):
                if index == count:
                    break
                featuredArticle = self.getArticle(featured.attrib['id'])
                if featuredArticle is not None:     
                    data.items.append(featuredArticle)
        return data
    
    def getCategories(self, component):
        categories = {}
        for article in self.getCachedArticles().values():
            category = article.category
            if not categories.has_key(category):
                categories[category] = []
            categories[category].append(article)
        return categories
    
    def getMenu(self, id):
        u"""Answer the list of menu articles in this component."""
        data = Data()
        data.menuItems = []
        article = self.getArticle(id)
        if article:
            for menu in article.menu:
                menuArticle = self.getArticle(menu.attrib['id'])
                if menuArticle is not None:
                    data.menuItems.append(menuArticle)
        return data
    
    def getLogo(self, component):
        data = Data()
        data.url = '/home'
        data.src = 'http://data.doingbydesign.com.s3.amazonaws.com/_images/logo.png'
        return data

if __name__ == '__main__':
    # Cache the adapter
    from xierpa3.sites import doingbydesign
    fa = FileAdapter(root=TX.module2Path(doingbydesign)+'/files/articles')
    if 0:
        print fa.getIdPaths()
        print fa.getPages(None).items
    if 1: 
        featured = fa.getFeaturedArticles(None, 'home', 3).items
        print featured
        print featured[0].name        
        print featured[0].poster
