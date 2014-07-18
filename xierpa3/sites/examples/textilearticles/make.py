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
#    make.py
#
import webbrowser
from xierpa3.attributes import Em, Px, Color, Perc
from xierpa3.toolbox.transformer import TX
from xierpa3.adapters import TextileFileAdapter 
from xierpa3.components import Theme, Page, Container, Article, ArticleSideBar, Menu
from xierpa3.components import FeaturedByImage
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder

class ArticleAdapter(TextileFileAdapter):
    u"""Inherit from the *FileAdapter* to read the example XML article file."""
    
class TextileArticles(Theme):
    u"""Show article pages for the amount of articles in @files/articles@, with a top navigation,
    article column and article side bar. The menu items are define in the @home.txt@ article source."""
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Theme.C

    TITLE = u'The Textile Example Page' # Use as title of window.

    BODYSIZE = Px(16)
    BODYLEADING = Em(1.4)
    BODYCOLOR = '#333333'
    
    LINKCOLOR = '#4890BE'
   
    H1SIZE = Em(2.8)
    H1LINEHEIGHT = Em(1)
    H1MARGINTOP = Em(0.5)
    H1MARGINBOTTOM = Em(0.5)
    H1COLOR = '#666666'
    
    H2SIZE = Em(2)
    H2LINEHEIGHT = Em(1.1)
    H2MARGINTOP = Em(0.5)
    H2MARGINBOTTOM = Em(0.5)
    H2COLOR = '#333333'
 
    BODYFAMILY = '"Hermes FB Book", Verdana, sans'
    HEADFAMILY = '"Hermes FB Semibold", Impact, sans'
    CODEFAMILY = 'Courier, monospace'
    
    CC = Theme # Inherit the constants from the parent class.
    
    URL_FONTS = [
        # Note that this package contains the a set of latest featured font, and may be changed in the future.
        # If using the font in this package, safest is to refer to the functional constant names below,
        # instead of making a direct reference to the family name.
        # Of course, taking your own account at //www.webtype.com is even better :)
        C.XIERPA3_DEMOFONTS, # Webtype @fontface fonts, to be used for localhost demo purposes.
    ]    

    def baseStyle(self):
        s = self.newStyle() # Answer root style without selector
        s.addStyle('body', fontfamily=self.BODYFAMILY, fontsize=self.BODYSIZE, color=self.BODYCOLOR, 
            lineheight=self.BODYLEADING)
        s.addStyle('a', color=self.LINKCOLOR)
        s.addStyle('h1, h2, h3, h4, h5, p.lead', fontfamily=self.HEADFAMILY, color=self.BODYCOLOR)
        s.addStyle('h1', fontsize=self.H1SIZE, lineheight=self.H1LINEHEIGHT, color=self.H1COLOR, margintop=self.H1MARGINTOP, marginbottom=self.H1MARGINBOTTOM)
        s.addStyle('h2', fontsize=self.H2SIZE, lineheight=self.H2LINEHEIGHT, color=self.H2COLOR, margintop=self.H2MARGINTOP, marginbottom=self.H2MARGINBOTTOM)
        s.addStyle('h6', fontfamily=self.BODYFAMILY)
        s.addStyle('code', fontfamily=self.CODEFAMILY, fontsize=Em(1.1), 
            color=Color('#333'), paddingleft=Em(0.25),
            paddingright=Em(0.25))
        s.addStyle('pre', margintop=0, marginbottom=Em(1.5))
        s.addStyle('.error', color='red', backgroundcolor=Color('red'))
        return s
    
    def baseComponents(self):
        u"""Create the component instances"""
        # Import current example site, as anchor for the article files.
        from xierpa3.sites.examples import textilearticles
        # Root path where to find the article Simples wiki file for this example page.
        articleRoot = TX.module2Path(textilearticles) + '/files/articles/' 
        adapter = ArticleAdapter(articleRoot) # Preferred adapter class for articles in this site.
        # Create navigation instance, to choose between the available articles.
        menu = Menu(adapter=adapter)
        menuContainer = Container(components=menu)
        # Create the article component to contain articles answered by the adapter.
        #article = SimplexArticle(adapter=adapter) 
        article = Article(width=Perc(70), adapter=adapter, showPoster=True, splitChapters=False) 
        articleSideBar = ArticleSideBar(width=Perc(22), adapter=adapter)
        featuredArticles = FeaturedByImage(width=Perc(22), adapter=adapter)
        # Make main page container for the article column
        container = Container(components=(article, articleSideBar, featuredArticles)) 
        # The class is also the page name in the url.
        homePage = Page(class_=self.C.TEMPLATE_INDEX, name=self.C.TEMPLATE_INDEX, 
            fonts=self.URL_FONTS, title=self.TITLE, css=self.C.URL_CSS, 
            components=(menuContainer, container))
        return [homePage]
    
    def make(self, root=None):
        u"""The instance of this class builds CSS and HTML files at the optional path <b>root</b>.
        If not defined, then the default ~/Desktop/Xierpa3Examples/[component.name] is used as export path,
        as set by Builder.DEFAULT_ROOTPATH"""
        
        cssBuilder = CssBuilder()
        self.build(cssBuilder)
        cssBuilder.save(self, root) 
        htmlBuilder = HtmlBuilder()
        self.build(htmlBuilder)
        return htmlBuilder.save(self, root)  
    
if __name__ == '__main__':
    # This construction "__name__ == '__main__'" makes this Python file only 
    # be executed when called in direct mode, such as "python make.py" in the terminal.         
    # Since no rootPath is added to make(), the file export is in ~/Desktop/Xierpa3Examples/Featuring1/   
    path = TextileArticles().make()
    webbrowser.open(path)
