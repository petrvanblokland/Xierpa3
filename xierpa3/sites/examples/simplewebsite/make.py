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
from xierpa3.attributes import Perc, Em, Px, Color
from xierpa3.components import Theme, Page, Container, Component, FeaturedByImage, FeaturedByText, FeaturedByDiapText
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.descriptors.blueprint import BluePrint
from xierpa3.descriptors.media import Media # Include type of Style that holds @media parameters.
from xierpa3.adapters import TextileFileAdapter
from xierpa3.toolbox.transformer import TX

# For sake of the example define two component classes here. Normally these would come 
# from a component library, where the BluePrint values function as API to adjust the 
# component instance behavior from the outside.

BODYFAMILY = '"BentonSansRE", Verdana, sans'
HEADFAMILY = '"Bureau Grot Cond", Impact, Verdana, sans'

BODYSIZE = Px(12)
BODYLEADING = Em(1.4)

class SimpleSiteAdapter(TextileFileAdapter):
    def getDescription(self):
        return self.newData(text=u"""Simple site, showing what is possible with articles from files.""")

    def getKeyWords(self):
        return self.newData(text=u"""Simple site. Xierpa3. Demo. Articles.""")

class MainColumn(Component):
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Component.C
    
    BLUEPRINT = BluePrint(
        width=Perc(65.4), doc_width=u'Main column width', 
        float=C.LEFT, 
        backgroundColor=Color('white'), doc_backgroundColor=u'Main column background color.', 
        fontSize=Em(2), doc_fontSize=u"""Font size of the body text.""",
        lineHeight=Em(1.4), doc_lineHeight=u"""Line height (leading) of the body size.""",
        # Mobile
        fontSizeMobile=Em(3), doc_fontSizeMobile=u"""Font size of the body text for mobile.""",
        lineHeightMobile=Em(1.4), doc_lineHeightMobile=u"""Line height (leading) of the body size for mobile.""",
        marginRight=Perc(0), doc_marginRight=u"""Margin right for the last column.""",

    )                
    def buildBlock(self, b):
        article = self.adapter.getArticle()
        if article is not None:
            s = self.style
            b.div(class_=self.getClassName(), fontsize=s.fontSize, lineheight=s.lineHeight,
                width=s.width, backgroundcolor=s.backgroundColor,
                media=Media(max=self.C.M_MOBILE_MAX, marginright=s.marginRight,
                  fontsize=s.fontSizeMobile, width=self.C.AUTO, float=self.C.NONE, lineheight=s.lineHeightMobile,
                )
            )
            b.h1()
            b.text(article.headline)
            b._h1()
            b.p()
            b.text(article.text)
            b._p()
            b._div(comment=self.getClassName())
          
class SideColumn(Component):
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Component.C
    
    BLUEPRINT = BluePrint(
        width=Perc(30.75), doc_width=u'Side bar width',  # @@@@ Should be 30?
        float=C.LEFT, doc_float=u'Float left inside row.',
        backgroundColor=Color('white'), doc_backgroundColor=u'Side column background color.',                  
        fontSize=Em(1), doc_fontSize=u"""Font size of the body text.""",
        lineHeight=Em(1.4), doc_lineHeight=u"""Line height (leading) of the body size.""",
        # Mobile
        fontSizeMobile=Em(1.5), doc_fontSizeMobile=u"""Font size of the body text for mobile.""",
        lineHeightMobile=Em(1.4), doc_lineHeightMobile=u"""Line height (leading) of the body size for mobile.""",
        marginRight=Perc(1.8), doc_marginRight=u"""Margin right for the column.""",
    )                
    def buildBlock(self, b):
        article = self.adapter.getArticle()
        if article is not None:
            s = self.style
            b.div(class_=self.getClassName(), fontsize=s.fontSize, lineheight=s.lineHeight,
                width=s.width, backgroundcolor=s.backgroundColor, marginright=s.marginRight,
                media=Media(max=self.C.M_MOBILE_MAX, width=self.C.AUTO, float=self.C.NONE,
                  fontsize=s.fontSizeMobile, lineheight=s.lineHeightMobile,
                )
            )
            b.h1()
            b.text(article.headline)
            b._h1()
            b.p()
            b.text(article.text)
            b._p()
            b._div(comment=self.getClassName())
        
class SimpleWebSite(Theme):
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Theme.C

    TITLE = u'The Simple Website Example Page' # Use as title of window.

    URL_FONTS = [
        # Note that this package contains the a set of latest featured font, and may be changed in the future.
        # If using the font in this package, safest is to refer to the functional constant names below,
        # instead of making a direct reference to the family name.
        # Of course, taking your own account at //www.webtype.com is even better :)
        C.XIERPA3_DEMOFONTS, # Webtype @fontface fonts, to be used for localhost demo purposes.
    ]    

    def baseStyle(self):
        s = self.newStyle() # Answer root style without selector
        s.addStyle('body', fontfamily=BODYFAMILY, fontsize=BODYSIZE, lineheight=BODYLEADING)
        s.addStyle('h1, h2, h3, h4, h5, p.lead', fontfamily=HEADFAMILY)
        s.addStyle('h6', fontfamily=BODYFAMILY)
        return s
    
    def baseComponents(self):
        # Create the article adapter
        # Import current example site, as anchor for the article files.
        from xierpa3.sites.examples import simplewebsite
        articleRoot = TX.module2Path(simplewebsite) + '/files/articles/'
        adapter = SimpleSiteAdapter(articleRoot)
        # Create the component instances
        side = SideColumn()
        main = MainColumn()
        featuredByImage = FeaturedByImage(count=1)
        featuredByText = FeaturedByText(start=1, count=1)
        featuredByDiapText = FeaturedByDiapText()
        # Create the single page instance, containing the number of components
        container = Container(components=(featuredByImage, featuredByText, featuredByDiapText, side, main))
        # The class is also the page name in the url.
        homePage = Page(class_=self.C.TEMPLATE_INDEX, name=self.C.TEMPLATE_INDEX, adapter=adapter,
            fonts=self.URL_FONTS, title=self.TITLE, css=self.C.URL_CSS, components=container)
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
    # Since no rootPath is added to make(), the file export is in ~/Desktop/Xierpa3Examples/SimpleWebSite/   
    path = SimpleWebSite().make()
    webbrowser.open(path)
