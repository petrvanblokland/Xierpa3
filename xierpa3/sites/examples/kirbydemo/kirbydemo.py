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
#    kirbydemo.py
#
#    Example theme to build a blog site.
#
import os
from xierpa3.attributes import * 
from xierpa3.components import *
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.phpbuilder import PhpBuilder
from xierpa3.builders.kirby.blueprintbuilder import BluePrintBuilder
from xierpa3.descriptors.style import Style, StyleSet
from xierpa3.constants.constants import C
from kirbyadapter import KirbyAdapter

class C(C):
    
    C100 = '100%'
        
    PAGE_ABOUT = 'about'
    PAGE_CAREERS = 'careers'
    PAGE_CONTACT = 'contact'
    PAGE_ERROR = 'error'
    PAGE_HOME = 'home'
    
    UNIT = 8
    UNIT2 = UNIT/4
    CSS_PADDING = UNIT
    SCREEN_MOBILE = 757
    SCREEN_LARGESCREEN = 1140
    M_LARGESCREEN = '100%'
    
    CSS_GRAY = '#A0A0A0'
    CSS_BODYFONT = 'Verdana'
    CSS_BODYSIZE = Em(1)
    CSS_BGCOLOR = 'white'
    CSS_BODYLEADING = Em(1.2)
    
    CLASS_GRID = 'grid'
    CLASS_ROW = 'row'
    CLASS_ERROR = 'error'
    CLASS_SLOT6789 = 'slot-6-7-8-9'
    CLASS_ARTICLETITLE = 'article-title'
    CLASS_DATE = 'date'
    CLASS_ARTICLETITLE = 'article-title'
    
    FLOAT_NONE = 'none'
    
    URL_CSS = 'css'
    URL_JAVASCRIPT = None
    URL_WEBFONTS = None
    URL_FAVICON = None
        
# Subclasses to force naming in HTML and CSS classes.
class BaseGroup(Group):
    def buildPagination(self, b):
        ad = self.adapter
        b.p()
        b.text(ad.ifPageHasPrev())
        b.a(href=ad.pagePrevUrl())
        b.text(ad.previousLabel())
        b._a()
        b.text(ad._if())
        b.text(ad.ifPageHasPrevAndNext())
        b.text(u'|')
        b.text(ad._if())
        b.text(ad.ifPageHasNext())
        b.a(href=ad.pageNextUrl())
        b.text(ad.nextLabel())
        b._a()
        b.text(ad._if())
        b._p()

    def buildArticlesPagination(self, b):
        ad = self.adapter
        b.p()
        b.text(ad.ifArticlesHasPrev())
        b.a(href=ad.articlesPrevUrl())
        b.text(ad.previousLabel())
        b._a()
        b.text(ad._if())
        b.text(ad.ifArticlesHasPrevAndNext())
        b.text(u'|')
        b.text(ad._if())
        b.text(ad.ifArticlesHasNext())
        b.a(href=ad.articlesNextUrl())
        b.text(ad.nextLabel())
        b._a()
        b.text(ad._if())
        b._p()

    def buildArticleExcerpts(self, b):
        ad = self.adapter
        b.text(ad.articles())
        b.text(ad.forEachArticle())
        b.div(class_=C.CLASS_ROW)
        b.div(class_=C.CLASS_SLOT6789)
        # Excerpts
        b.h1(class_=C.CLASS_ARTICLETITLE)
        b.a(href=ad.articleUrl())
        b.text(ad.articleTitle())
        b._a()
        b._h1()
        b.h4()
        b.p(class_=C.CLASS_DATE)
        b.text(ad.articlePublished())
        b._p()
        b._h4()
        b.p()
        b.text(ad.excerptArticle(300))
        b.a(href=ad.articleUrl())
        b.text(ad.rightArrow())
        b._a()
        b._p()
        b._div() # .slot-6-7-8-9
        b._div() # .row
        b.text(ad._forEach())
        b.text(ad.ifPaginationHasPages())
        b.div(class_=C.CLASS_ROW)
        b.div(class_=C.CLASS_SLOT6789)
        # Prev-next articles navigation
        self.buildArticlesPagination(b)        
        b.text(ad._if())
        b._div() # .slot-6-7-8-9
        b._div() # .row

class KirbyAbout(BaseGroup):
    def buildBlock(self, b):
        ad = self.adapter
        b.newline()
        b.comment(self.name)
        b.div(class_=C.CLASS_GRID)
        b.div(class_=C.CLASS_ROW)
        b.div(class_=C.CLASS_SLOT6789)
        b.br()
        b.img(src=ad.logoUrl(), width=100, alt=ad.siteTitle())
        b._div() # .slot-6-7-8-9
        b._div() # .row
        b.div(class_=C.CLASS_ROW)
        b.div(class_=C.CLASS_SLOT6789)
        b.text(ad.kirbyText())
        b._div() # .slot-6-7-8-9
        b._div() # .row
        b._div() # .grid
        b.newline()

class KirbyArticle(BaseGroup):
    def buildBlock(self, b):
        ad = self.adapter
        b.newline()
        b.comment(self.name)
        b.div(class_=C.CLASS_GRID)
        b.div(class_=C.CLASS_ROW)
        b.div(class_=C.CLASS_SLOT6789)

        # Prev-next navigation
        self.buildPagination(b)

        # Article title
        b.h1(class_=C.CLASS_ARTICLETITLE)
        b.a(href=ad.pageUrl())
        b.text(ad.pageTitle())
        b._a()
        b._h1()
        b.h4()
        b.p(class_=C.CLASS_DATE)
        b.text(ad.pagePublished())
        b._p()
        b._h4()

        # Article
        b.text(ad.kirbyText())
        b.p()
        b.text(ad.snippet('share'))
        b.br()
        b.br()
        b.text(ad.tagsLabel())
        b.text(ad.forEachPageTag())
        b.a(href=ad.articleTagUrl())
        b.text(ad.htmlTag())
        b._a()
        b.text(ad._forEach())
        b._p()

        # Prev-next navigation
        self.buildPagination(b)
        b._div() # .slot-6-7-8-9
        b._div() # .row
        b.div(class_=C.CLASS_ROW)
        b.div(class_=C.CLASS_SLOT6789)
        b.text(ad.snippet('disqus', "array('disqus_shortname' => 'USERNAME')"))
        b._div() # .slot-6-7-8-9
        b._div() # .row
        b._div() # .grid
        b.newline()
   
class KirbyArticles(BaseGroup):
    def buildBlock(self, b):
        a = self.adapter
        b.div(class_=C.CLASS_GRID)
        self.buildArticleExcerpts(b)
        b._div() # .grid
    
class KirbyError(BaseGroup):
    def buildBlock(self, b):
        a = self.adapter
        b.div(class_=C.CLASS_GRID)
        b.div(class_=C.CLASS_ROW)
        b.div(class_=(C.CLASS_SLOT6789, C.CLASS_ERROR))
        b.h2()
        b.text(a.pageTitle())
        b._h2()
        b.p()
        b.text(u"The requested page could not be found. If you're really lost, try")
        b.a(href=a.searchUrl())
        b.text(u'searching')
        b._a()
        b.text(u'for something.')
        b._p()
        b._div() # .slot-6-7-8-9
        b._div() # .row
        b._div() # .grid
 
class KirbyFeed(BaseGroup):
    def buildBlock(self, b):
        b.text(self.adapter.feed())   

class KirbyProject(BaseGroup):
    def buildBlock(self, b):       
        b.div(class_=C.CLASS_GRID)
        self.buildArticleExcerpts(b)
        b._div() # .grid
        
class KirbySearch(BaseGroup):
    def buildBlock(self, b):       
        ad = self.adapter
        b.text(ad.search())
        b.div(class_=C.CLASS_GRID)
        b.div(class_=C.CLASS_ROW)
        b.div(class_=C.CLASS_SLOT6789)
        b.form(action=ad.thisUrl())
        b.input(type='text', placeholder='What are you looking for?', name='q', id='search')
        b._form()
        b._div() # .slot-6-7-8-9
        b._div() # .row
        
        # Results
        b.text(ad.ifResults())
        b.text(ad.forEachResult())
        b.div(class_=C.CLASS_ROW)
        b.div(class_=C.CLASS_SLOT6789)
        # Article search result
        b.h1(class_=C.CLASS_ARTICLETITLE)
        b.a(href=ad.resultUrl())
        b.text(ad.resultTitle())
        b._a()
        b._h1()
        b.p()
        b.text(ad.resultDescription())
        b.text(ad.resultText(300))
        b.text('[...]')
        b.a(href=ad.resultUrl())
        b.text(ad.readMoreLabel())
        b._a()
        b._p()
        b._div() # .slot-6-7-8-9        
        b._div() # .row
        b.text(ad._forEach())

        # Pagination
        b.div(class_=C.CLASS_ROW)
        b.div(class_=C.CLASS_SLOT6789)
        b.text(ad.snippet('pagination', "array('pagination' => $results->pagination())"))
        b._div() # .slot-6-7-8-9        
        b._div() # .row
        
        # Search query
        b.text(ad.elseIfSearchQuery())
        b.div(class_=C.CLASS_ROW)
        b.div(class_=C.CLASS_SLOT6789)
        b.h3()
        b.text(u"No posts found matching «")
        b.text(ad.htmlSearchQuery())
        b.text(u"».")
        b._h3()
        b._div() # .slot-6-7-8-9        
        b._div() # .row
        b.text(ad._if())
        
        # Tags
        b.div(class_=C.CLASS_ROW)
        b.div(class_=C.CLASS_SLOT6789)
        b.h3()
        b.text('Tags')
        b._h3()
        b.p()
        b.text(ad.forEachTag())
        b.a(href=ad.tagUrl())
        b.text(ad.tagName())
        b._a()
        b.text(ad._forEach())
        b._p()
        b._div() # .slot-6-7-8-9        
        b._div() # .row
        b._div() # .grid
             
class KirbyDemo(Theme):
    u"""The <b>SimpleSite</b> class implements the standard example blog."""
    TITLE = 'Blog Petr van Blokland + Claudia Mens'
    SUBTITLE = 'Notes on design and education.'

    def initialize(self):
        self.adapter = KirbyAdapter()
     
    def getCacheFilePath(self):
        u"""Writing the kirby templates."""
        return self.PATH_KIRBY
          
    def baseStyle(self):
        s = StyleSet() # Answer root style without selector
        s.addStyle('body', fontfamily='BentonSansRE', fontsize=12, 
            backgroundcolor='#D0D0D0', leading=Em(1.4))
        s.addStyle('h1,h2,h3,h4,h5', fontfamily='MillerDisplay Regular', margintop=Em(0.5), marginbottom=Em(0.5))
        s.addStyle('h1', fontsize=Em(2))
        s.addStyle('h2', fontsize=Em(1.5))
        s.addStyle('h3', fontsize=Em(1.2))
        s.addStyle('h4', fontfamily='BentonSansRE', fontweight='bold', fontsize=Em(1))
        s.addStyle('div.page')
        s.addStyle('div.grid', padding=Padding(0, 20, 0, 0), maxwidth=C.SCREEN_LARGESCREEN,
            margin=Margin(0, 'auto'), backgroundcolor='white')
        s.addStyle('div.row', width=C.C100, maxwidth=C.SCREEN_LARGESCREEN)      
        return s
    
    def baseComponents(self):
         
        # C O M P O N E N T S
        
        about = KirbyAbout()
        article = KirbyArticle()
        articles = KirbyArticles()
        error = KirbyError()
        feed = KirbyFeed()
        project = KirbyProject()
        search = KirbySearch()
        
        # P A G E S

        aboutPage = Page(name=C.PAGE_ABOUT, id=C.PAGE_ABOUT,
            components=about, 
            css=C.URL_CSS, js=C.URL_JAVASCRIPT,
            webfonts=C.URL_WEBFONTS, favIcon=C.URL_FAVICON) 
        # @media
        aboutPage.addMedia(max=C.SCREEN_MOBILE, backgroundcolor='yellow', margin=0, 
            width=C.C100,)
        aboutPage.addMedia(min=C.SCREEN_LARGESCREEN, width=C.M_LARGESCREEN, float=C.FLOAT_NONE,
            margin=0, padding=Em(1), backgroundcolor='white')
        
        
        articlePage = Page(name=C.PAGE_ARTICLE, id=C.PAGE_ARTICLE,
            components=article, 
            css=C.URL_CSS, js=C.URL_JAVASCRIPT,
            webfonts=C.URL_WEBFONTS, favIcon=C.URL_FAVICON) 
        # @media
        articlePage.addMedia(min=C.SCREEN_LARGESCREEN, width=C.M_LARGESCREEN, float=C.FLOAT_NONE,
            margin=Margin(0,'auto'), backgroundcolor=C.CSS_GRAY)
        
        articlesPage = Page(name=C.PAGE_ARTICLES, id=C.PAGE_ARTICLES, 
            components=articles, 
            css=C.URL_CSS, js=C.URL_JAVASCRIPT,
            webfonts=C.URL_WEBFONTS, favIcon=C.URL_FAVICON) 
        # @media
        articlesPage.addMedia(min=C.SCREEN_LARGESCREEN, width=C.M_LARGESCREEN, float=C.FLOAT_NONE,
            margin=Margin(0,'auto'), backgroundcolor=C.CSS_GRAY)
        
        errorPage = Page(name=C.PAGE_ERROR, id=C.PAGE_ERROR, 
            components=error, 
            css=C.URL_CSS, js=C.URL_JAVASCRIPT,
            webfonts=C.URL_WEBFONTS, favIcon=C.URL_FAVICON) 
        # @media
        errorPage.addMedia(min=C.SCREEN_LARGESCREEN, width=C.M_LARGESCREEN, float=C.FLOAT_NONE,
            margin=Margin(0,'auto'), backgroundcolor=C.CSS_GRAY)
        
        feedPage = Page(name=C.PAGE_FEED, id=C.PAGE_FEED, 
            components=feed, 
            css=C.URL_CSS, js=C.URL_JAVASCRIPT,
            webfonts=C.URL_WEBFONTS, favIcon=C.URL_FAVICON) 
        # @media
        feedPage.addMedia(min=C.SCREEN_LARGESCREEN, width=C.M_LARGESCREEN, float=C.FLOAT_NONE,
            margin=Margin(0,'auto'), backgroundcolor=C.CSS_GRAY)
        
        projectPage = Page(name=C.PAGE_PROJECT, id=C.PAGE_PROJECT, 
            components=project, 
            css=C.URL_CSS, js=C.URL_JAVASCRIPT,
            webfonts=C.URL_WEBFONTS, favIcon=C.URL_FAVICON) 
        # @media
        projectPage.addMedia(min=C.SCREEN_LARGESCREEN, width=C.M_LARGESCREEN, float=C.FLOAT_NONE,
            margin=Margin(0,'auto'), backgroundcolor=C.CSS_GRAY)
        
        searchPage = Page(name=C.PAGE_SEARCH, id=C.PAGE_SEARCH, 
            components=search, 
            css=C.URL_CSS, js=C.URL_JAVASCRIPT,
            webfonts=C.URL_WEBFONTS, favIcon=C.URL_FAVICON) 
        # @media
        searchPage.addMedia(min=C.SCREEN_LARGESCREEN, width=C.M_LARGESCREEN, float=C.FLOAT_NONE,
            margin=Margin(0,'auto'), backgroundcolor=C.CSS_GRAY)
        
        return [aboutPage, articlePage, articlesPage, errorPage, feedPage, projectPage, searchPage]
    
if __name__ == '__main__':
    theme = KirbyDemo()

    PATH_ROOT = '/Applications/MAMP/htdocs/%s/' % theme.name.lower()
    theme.PATH_CSS  = PATH_ROOT + 'assets/css/style.css'
    theme.PATH_TEMPLATE = PATH_ROOT + 'site/templates/%s.php'
    theme.PATH_BLUEPRINT = PATH_ROOT + 'panel/defaults/blueprints/%.php'
    
    builder = CssBuilder()
    theme.build(builder) # Build the SCSS/CSS of the theme
    builder.save(theme.PATH_CSS) # Compile the SCSS to CSS and save the file.
    # Build Kirby PHP and the panel blue print for each template
    builder = KirbyBuilder()
    bluePrintBuilder = BluePrintBuilder() 
    for template in theme.getTemplates():
        template.build(builder) 
        print 'Saving', theme.PATH_TEMPLATE % template.name
        builder.save(theme.PATH_TEMPLATE % template.name)
        # Build the panel blueprint
        #template.build(bluePrintBuilder)
        #print 'Saving panel blueprint', theme.PATH_BLUEPRINT % template.name
        #bluePrintBuilder.save(theme.PATH_BLUEPRINT % template.name)
        
        

