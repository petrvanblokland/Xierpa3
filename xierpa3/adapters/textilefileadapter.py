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
#
import re
import os
import codecs
import textile
from operator import attrgetter
from xierpa3.adapters.adapter import Adapter
from xierpa3.toolbox.transformer import TX

class TextileFileAdapter(Adapter):
    
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Adapter.C 
    
    # Match line pattern "$fielName value"
    FIELDVALUE = re.compile('\$([\w]*) (.*)')
    # Match comma separated list
    COMMASPLIT = re.compile('[,]*[\s]*([^,]*)')
    # Set of field names that have to become a list is in C.ADAPTER_COMMAFIELDS
    
    u"""Adapter for Textile wiki file serving. """
    def initialize(self):
        self._cache = {}
        self._sorted = []
        self.readArticles()
        # Build the cache meta field references for articles.
        self.cacheArticleFieldReferences()
     
    def readArticles(self):
        u"""Read all articles available in the root tree path."""
        for id, path in self.getIdPaths(): # id, path
            self.updateArticle(id, self.root + path)
        
    def updateArticle(self, id, path):
        u"""Update the article from *id* and *path*. Set the modification time, so we know
        when the file is updated."""
        data = None
        wiki = self.readWikiFile(path)
        if wiki is not None:
            data = self.compileArticle(wiki)
            data.id = id
            data.source = wiki
            data.ranking = TX.asInt(data.ranking) or 0 # Make sure we can sort on the ranking field.
            data.path = path # Keep the source path is case POST needs to save to the file.
            data.modificationTime = os.path.getmtime(path) # @@@ TODO: Should be DateTime instance.
            self.cacheArticle(data)
        return data
        
    @classmethod  
    def readWikiFile(cls, fsPath): 
        u"""Read the raw wiki (Textile syntax) file and answer the unicode string."""
        extension = '.'+cls.C.EXTENSION_TXT
        if not fsPath.endswith(extension):
            fsPath += extension           
        if os.path.exists(fsPath):
            f = codecs.open(fsPath, encoding='utf-8', mode='r+')
            wiki = f.read()
            f.close()
        else:
            wiki = None
        return wiki
    
    def _splitFieldValue(self, line):
        u"""Split the string *s* into field name (starting with $ and ending with space)
        and string value. If the field is one of @self.COMMAFIELDS@, then the value
        must be a comma separated list. Split the string into a list of values."""
        found = self.FIELDVALUE.findall(line)
        if found:
            fieldName, value = found[0]
            if fieldName in self.C.ADAPTER_COMMAFIELDS:
                value = self.COMMASPLIT.findall(value)[:-1] # Split and remove last empty part
            return fieldName, value
        return None, None # No field name match on this line.

    def compileArticle(self, wiki):
        u"""Compile the wiki text into a Data instance, but parsing the field definition, split
        on chapters and translate the chapter content through textile to html.
        See specification on :http://redcloth.org/hobix.com/textile/ """
        data = self.newData()
        text = []
        # Filter the field definitions
        wiki = wiki.replace('\r', '\n')
        for line in wiki.split('\n'):
            if line.startswith('$'):
                fieldName, value = self._splitFieldValue(line)
                if fieldName is not None:
                    data[fieldName] = value
            else:
                text.append(line) # Keep normal text lines.
        # Split the chapters into items
        data.items = []
        for chapter in ('\n'.join(text)).split('=C='):
            data.items.append(textile.textile(chapter))
        return data
    
    def cacheArticleFieldReferences(self):
        u"""(Re)build the dictionary of field relations. This should be done, anytime a new article 
        is cached or modified. Better to build from scratch if the source changes, than to keep track
        of changes."""
        self._urls = {}
        self._categories = {}
        self._levels = {}
        for id, article in self._cache.items():
            for url in (article.urls or []):
                if not self._urls.has_key(url):
                    self._urls[url] = []
                self._urls[url].append(article)
            for category in (article.categories or []):
                if not self._categories.has_key(category):
                    self._categories[category] = []
                self._categories[category].append(article)
            for level in (article.levels or []):
                if not self._levels.has_key(level):
                    self._levels[level] = []
                self._levels[level].append(article)

    def cacheArticle(self, article):
        u"""Cache the article by @article.id@. And keep the article sorted in the @self._sorted@
        list of all articles."""
        self._cache[article.id] = article
        self.sortArticles()
        
    def sortArticles(self):
        u"""Keep the article sorted in the @self._sorted@ list of all articles."""
        self._sorted = self._cache.values()
        self._sorted.sort(key = attrgetter('ranking'), reverse = True)
           
    def getCachedArticle(self, **kwargs):
        u"""Answer the cached articles. If not available yet, read them through <self.getPaths()<b>."""
        id = kwargs.get('id')
        if isinstance(id, list):
            pass
        data = self._cache.get(id)
        if data is not None and data.modificationTime != os.path.getmtime(data.path):
            # File content is modified after caching the article. Update it from file.
            data = self.updateArticle(data.id, data.path)
            self.cacheArticleFieldReferences() # Article may have changed fields. Build all caching of fields again.
        # If article not found, try to match on url.
        if data is None:
            data = self.getArticleByUrl(kwargs.get('url'))
        return data
     
    def getArticleByUrl(self, url):
        u"""Answer the article that is matching *url* by one of the values in the @$url@ field.
        Answer @None@ if not matching article could be found."""
        data = None
        fields = self.getFields()
        articles = fields.urls.get(url)
        if articles:
            data = articles[0] # If found multiple matches, just take the first one.
        return data
    
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
    
    def getPageTitle(self, **kwargs):
        article = self.getArticle(**kwargs)
        if article is not None:
            return self.newData(text=article.name)
        return None
    
    def getPages(self, start=0, count=1, omit=None, **kwargs):
        u"""Answer the sorted list of *count* pages/articles, starting on *start* index, 
        selected from all articles. Sorting is based om the @article.ranking@ field.
        If *omit* is a list of article ids (or a single id), then skip these articles 
        from the selection."""
        if omit is None: # Nothing to omit, just slice the pre-sorted article list.
            items = self._sorted[start:start+count]
        else: # Otherwise create the list by omitting what is in the attributes.
            if not isinstance(omit, (list, tuple)):
                omit = [omit] # Make sure it is a list.
            items = []
            for item in self._sorted[start:]:
                if not item.id in omit:
                    items.append(item)
                    if len(items) >= count:
                        break
        return self.newData(items=items)
    
    getArticles = getPages
    
    def getMobilePages(self, count=None, **kwargs):
        return self.getPages(count)
    
    def getArticle(self, **kwargs):
        u"""Answer the matching article, based on the available keywords in *kwargs*."""
        return self.getCachedArticle(**kwargs)
    
    def getFeaturedArticles(self, id, start, count):
        u"""Answer a list of featured articles in the article that has @id@ as identifier."""
        data = self.newData()
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
    
    def getFields(self):
        u"""Answer a @Data@ instance with dictionaries of all field names, related to lists of articles.
        Included @data.urls@, @data.categories@ and @data.levels@."""
        data = self.newData()
        data.urls = self._urls
        data.categories = self._categories
        data.levels = self._levels        
        return data
    
    def getMenu(self, **kwargs):
        u"""Answer the @data.items@ of the main menu, indicated by *id*. Normally this will be the @home@
        page of the site, containing the main menu options in @$menu@. The @data.items@ are article data instances."""
        data = self.newData()
        data.items = []
        article = self.getArticle(**kwargs)
        if article.menu: 
            for menuId in article.menu: # All article id references in the menu list
                menuArticle = self.getArticle(id=menuId)
                if menuArticle is not None and menuArticle.tag:
                    data.items.append(menuArticle)
        return data
    
    def getLogo(self, **kwargs):
        data = self.newData()
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
