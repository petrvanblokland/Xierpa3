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
#    textilefileadapter.py
#
#    https://github.com/textile/python-textile
#    http://redcloth.org/hobix.com/textile/
#
#    Based on textile wiki format, with the following additions:
#    =C= is separator between chapters, will be processed separately by textile.
#    $fileName Field Content lines are pre-processed to fiil the fields of the Data instance.
#
#    TODO: See how we can add soft-hyphens here.
#
#    Textile syntax
#
#    Single return creates break --> <br/>
#    Double white line creates paragraph. --> <p>...</p>
#    Plain HTML will be copied
#    "Observe" smart quotes
#    -- --> emdash
#    - --> endash
#    ... --> ellipsis
#    space x space --> multiplication sign
#    (TM) (C) (R) --> ™ © ®
#    * Bullet list
#    #  Numbered list
#    h1. This is a header h1
#    h2. This is a header h2
#    h3. This is a header h3
#    bq. to blockquote
#    Reference to footnote[1]
#    fn1. Definition of footnote.
#    _word_ --> <em>word</em>
#    *word* --> <strong>word</strong>
#    **word** --> <b>word</b>
#    __word__ --> <i>word</i>
#    ??word?? --> <cite>word</cite>
#    @r.to_html@ --> <code>r.to_html</code>
#    -word- --> <del>word</del> (Deletion, strike through)
#    +word+ --> <ins>word</ins> (Insertion)
#    ^word^ --> <sup>word</sup>
#    ~word~ --> <sub>word</sub>
#    %span% --> <span>word</span>
#    %{color:red}word% --> <span style="color:red;">word</span>
#    p(example). Example --> <p class="example">Example</p>
#    p(#example). Example --> <p id="example">Example</p>
#    p(example1#big-red2). Red here --> <p class="example1" id="big-red2">Red here</p>
#    p{color:blue;margin:30px}. Spacey blue --> <p style="color:blue; margin:30px;">Spacey blue</p>
#    p[fr]. rouge --> <p lang="fr">rouge</p>
#    I seriously *{color:red}blushed*
#        when I _(big)sprouted_ that
#        corn stalk from my
#        %[es]cabeza%.
#    -->
#    <p>I seriously <strong style="color:red;">blushed</strong>
#    when I <em class="big">sprouted</em> that
#    corn stalk from my
#    <span lang="es">cabeza</span>.</p>
#    p<. align left --> <p style="text-align:left;">align left</p>
#    p>. align right --> <p style="text-align:right;">align right</p>
#    p=. centered --> <p style="text-align:center;">centered</p>
#    p<>. justified --> <p style="text-align:justify;">justified</p>
#    p(. left ident 1em --> <p style="padding-left:1em;">left ident 1em</p>
#    p((. left ident 2em --> <p style="padding-left:2em;">left ident 2em</p>
#    p))). right ident 3em --> <p style="padding-right:3em;">right ident 3em</p>
#    h2()>. Bingo. --> <h2 style="padding-left:1em; padding-right:1em; text-align:right;">Bingo.</h2>
#    h3()>[no]{color:red}. Bingo --> <h3 style="color:red; padding-left:1em; padding-right:1em; text-align:right;" lang="no">Bingo</h3>
#    I searched "Google":http://google.com. --> <p>I searched <a href="http://google.com">Google</a>.</p>
#    !http://redcloth.org/hobix.com/textile/sample.jpg! --> <img src="..."/>
#    !openwindow1.gif(Bunny.)! --> <img src="..." title="Bunny." alt="Bunny." />
#    !openwindow1.gif!:http://hobix.com/ --> <a href="..."><img src="openwindow1.gif" alt="" />
#    !>obake.gif! --> <p style="float:right"><img src="obake.gif" alt="" /></p>
#    We use CSS(Cascading Style Sheets). --> <p>We use <acronym title="Cascading Style Sheets">CSS</acronym>.</p>
#    Table:
#    | name | age | sex |
#    | joan | 24 | f |
#    | archie | 29 | m |
#    | bella | 45 | f |
#
#    |_. name |_. age |_. sex |    --> Header cells
#    | joan | 24 | f |
#    | archie | 29 | m |
#    | bella | 45 | f |
#
#    Cell alignment
#    |_. attribute list |
#    |<. align left |
#    |>. align right|
#    |=. center |
#    |<>. justify |
#    |^. valign top |
#    |~. bottom |
#    
#    Cell attributes
#    |\2. spans two cols |
#    | col 1 | col 2 |
#
#    Table attributes
#    table{border:1px solid black}.
#    |This|is|a|row|
#    |This|is|a|row|
#
#    Attributes of rows
#    |This|is|a|row|
#    {background:#ddd}. |This|is|grey|row|

import os
import codecs
import textile
from xierpa3.adapters.adapter import Adapter
from xierpa3.toolbox.storage.data import Data

class TextileFileAdapter(Adapter):
    u"""Adapter for Textile wiki file serving"""
    def initialize(self):
        self._cache = {}
        self.readArticles()
        
    def readArticles(self):
        for id, path in self.getIdPaths(): # id, path
            rootPath = self.root + path 
            wiki = self.readWikiFile(rootPath)
            if wiki is not None:
                data = self.compileArticle(wiki)
                data.id = id
                data.path = rootPath # Keep the source is case the file needs editing.
                self.cacheArticle(data)
                
    def compileArticle(self, wiki):
        u"""Compile the wiki text into a Data instance, but parsing the field definition, split
        on chapters and translate the chapter content through textile to html."""
        data = self.newData()
        text = []
        # Filter the field definitions
        wiki = wiki.replace('\r', '\n')
        for line in wiki.split('\n'):
            if line.startswith('$'):
                parts = line.split(' ')
                if len(parts) >= 2:
                    # Get field name and restore rest of the line.
                    # Field names are case sensitive.
                    data[parts[0][1:]] = ' '.join(parts[1:])
                else:
                    data.error = 'Error in field syntax: "%s"' % line
            else:
                text.append(line) # Keep normal text lines.
        data.items = []
        for chapter in ('\n'.join(text)).split('=C='):
            data.items.append(textile.textile(chapter))
        return data
    
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
    test = """
h2. markItUp! Universal markup editor

!../markitup/preview/picture.png(markItUp! Logo)!

*markItUp!* is a javascript over "jQuery(jQuery Website)":http://www.jquery.com plug-in which allow you to turn any textarea in a markup editor.

*markItUp!* is a lightweight fully customizable engine made to easily fit all developers needs in their CMS, blogs, forums or websites.

_Html, Textile, Wiki Syntax, Markdown, BBcode_ or even your own Markup system can be easily implemented.

* integrate it easily
* customize buttons and macros to fit all your need
* customize keyboard shortcuts
* customize toolbar and css look and feel
** skins
** icons
** dropdown menus
** separators
* use the engine from anywhere in the page
* implement any markup language even your own
* implement your own javascript macros even the most advanced
* allow multi-line edition
* preview ajax result dynamically in any markup parser
* offers userfriendly experience and effectiveness
    """
    print textile.textile(test)
