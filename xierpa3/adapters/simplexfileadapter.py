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
import codecs
from xierpa3.toolbox.transformer import TX
from xierpa3.adapters.adapter import Adapter
from xierpa3.toolbox.storage.data import Data
from xierpa3.toolbox.parsers.simplex import Simplex # Simplex Wiki parser

class SimplexFileAdapter(Adapter):
    u"""Adapter for Simples wiki file serving"""
    def initialize(self):
        self._cache = {}
        self.readArticles()
        
    def readArticles(self):
        simplex = Simplex()
        for id, path in self.getIdPaths(): # id, path 
            wiki = self.readWikiFile(self.root + path)
            if wiki is not None:
                # Create the Data instance and cache the standard query values from the tree.
                data = simplex.compile(wiki)
                data.id = id
                self.cacheArticle(data)
    
    def readWikiFile(self, fsPath): 
        extension = '.'+self.C.EXTENSION_TXT
        if not fsPath.endswith(extension):
            fsPath += extension           
        if os.path.exists(fsPath):
            f = codecs.open(fsPath, encoding='utf-8', mode='r+')
            wiki = f.read()
            f.close()
        else:
            wiki = None
        return wiki
    
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
            path = ''
        if idPaths is None:
            idPaths = []
        extension = '.'+self.C.EXTENSION_TXT
        for name in os.listdir(self.root + path):
            filePath = path + name
            if name.startswith('.'):
                continue
            if os.path.isdir(self.root + filePath):
                self.getIdPaths(filePath+'/', idPaths)
            elif not name.endswith(extension):
                continue
            else:
                name = name.replace(extension, '')
                idPaths.append((name, filePath))
        return idPaths
    
    def getChapters(self, article):
        if article.items is None:
            return []
        return article.items 
    
    def getChapterByIndex(self, index, article):
        u"""Find the chapter by <b>index</b> in the ArticleData instance <b>article</b>.
        Answer <b>None</b> if the chapter index is not valid."""
        if 0 <= index < len(article.items or []):
            return article.items[index]
        return None
    
    def getChapterTitleByIndex(self, index, article):
        u"""Find the title of the chapter by <b>index</b> in the ArticleData instance <b>article</b>.
        Answer <b>None</b> if the index is not valid or the title cannot be found."""
        chapter = self.getChapterByIndex(index, article)
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
        data.src = '//data.doingbydesign.com.s3.amazonaws.com/_images/logo.png'
        return data

if __name__ == '__main__':
    # Cache the adapter
    from xierpa3.sites.examples import simplexarticles
    fa = SimplexFileAdapter(root=TX.module2Path(simplexarticles)+'/files/articles')
    if 0:
        print fa.getIdPaths()
        print fa.getPages(None).items
    if 1: 
        featured = fa.getFeaturedArticles(None, 'home', 3).items
        print featured
        print featured[0].name        
        print featured[0].poster
