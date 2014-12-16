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
from xierpa3.components import Theme, Page, Container, Article, FeaturedByImage, FeaturedByText,\
    Logo, Menu, MobileNavigation, Header, Footer
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.toolbox.transformer import TX
# Get articles from textile files. See http://en.wikipedia.org/wiki/Textile_(markup_language)
from xierpa3.adapters import TextileFileAdapter

# For sake of the example define two component classes here. Normally these would come 
# from a component library, where the BluePrint values function as API to adjust the 
# component instance behavior from the outside.

class SimpleSiteAdapter(TextileFileAdapter):
    def getDescription(self):
        return self.newArticle(text=u"""Simple site, showing what is possible with articles from files.""")

    def getKeyWords(self):
        return self.newArticle(text=u"""Simple site. Xierpa3. Demo. Articles.""")

class SimpleWebSite(Theme):
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Theme.C

    # This title will be combined with the title of the article of a specific page.
    TITLE = u'Simple Website'

    BODYFAMILY = '"BentonSansRE", Verdana, sans'
    HEADFAMILY = '"Bureau Grot Cond", Impact, Verdana, sans'

    BODYSIZE = Px(12)
    BODYLEADING = Em(1.4)
    FOOTERBGCOLOR = Color('#202020')

    URL_FONTS = [
        # Note that this package contains the a set of latest featured font, and may be changed in the future.
        # If using the font in this package, safest is to refer to the functional constant names below,
        # instead of making a direct reference to the family name.
        # Of course, taking your own account at //www.webtype.com is even better :)
        C.XIERPA3_DEMOFONTS, # Webtype @fontface fonts, to be used for localhost demo purposes.
    ]    

    def baseStyle(self):
        s = self.newStyle() # Answer root style without selector
        s.addStyle('body', fontfamily=self.BODYFAMILY, fontsize=self.BODYSIZE, lineheight=self.BODYLEADING)
        s.addStyle('h1, h2, h3, h4, h5, p.lead', fontfamily=self.HEADFAMILY)
        s.addStyle('h6', fontfamily=self.BODYFAMILY)
        return s
    
    def baseComponents(self):
        # Create the article adapter
        # Import articles from the doingbydesign site, sharing the article files.
        from xierpa3.sites import doingbydesign
        # Root path where to find the article Simplex wiki file for this example page.
        articleRoot = TX.module2Path(doingbydesign) + '/files/articles/'
        adapter = SimpleSiteAdapter(articleRoot)

        # Header
        logo = Logo()
        menu = Menu()
        header = Header(components=(logo,menu), mobileContainerDisplay=self.C.NONE,
            doc_mobileContainerDisplay=u'Header is not visible for mobile')
        mobileNavigation = MobileNavigation() # Is container by itself. Change??

        # Create the component instances
        #article = Article(width=Perc(68))
        featuredByImage = FeaturedByImage(count=1, width=Perc(30))
        #featuredByText = FeaturedByText(start=1, count=3, width=Perc(30))
        # Create the single page instance, containing the number of components
        #mainHome = Container(components=(article, featuredByImage, featuredByText))

        # Footer
        footer = Footer(components=(menu,), containerBackgroundColor=self.FOOTERBGCOLOR)

        # The class is also the page name in the url.
        homePage = Page(class_=self.C.TEMPLATE_INDEX, name=self.C.TEMPLATE_INDEX, adapter=adapter,
            #components=(mobileNavigation, header, mainHome, footer),
            #components=(header, mainHome, footer),
            components=featuredByImage,
            fonts=self.URL_FONTS, title=self.TITLE, css=self.C.URL_CSS)
        return [homePage]
    
    def make(self, root=None):
        u"""The instance of this class builds CSS and HTML files at the optional path **root**.
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
