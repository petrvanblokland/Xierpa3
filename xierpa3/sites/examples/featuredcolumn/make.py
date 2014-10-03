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
from xierpa3.attributes import Em, Margin, Perc, Color, Px
from xierpa3.components import Theme, Page, Container, Featured
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder

# Load @fontface fonts for this example from www.webtype.com
BODYFAMILY = '"Hermes FB Book", Verdana, sans'
HEADFAMILY = '"Hermes FB Semibold", Impact, Verdana, sans'

class FeaturedColumn(Theme):
    u"""The *FeaturedColumn* generates overview test on the featuring components."""
    C = Theme.C

    TITLE = u'Featured column.' # Use as title of window.

    URL_FONTS = [
        # Note that this package contains the a set of latest featured font, and may be changed in the future.
        # If using the font in this package, safest is to refer to the functional constant names below,
        # instead of making a direct reference to the family name.
        # Of course, taking your own account at //www.webtype.com is even better :)
        C.XIERPA3_DEMOFONTS, # Webtype @fontface fonts, to be used for localhost demo purposes.
    ]
    def baseStyle(self):
        u"""Answer the single basis style that will be defined as overall CSS, before
        specific block definitions start."""
        s = Featured.BLUEPRINT
        root = self.newStyle() # Create root style
        root.addStyle('body', fontfamily=s.fontFamily, fontsize=s.fontSize,
            backgroundcolor=s.pageBackgroundColor, lineheight=s.lineHeight)
        s.addStyle('h1, h2, h3, h4, h5, p.lead', fontfamily=HEADFAMILY)
        s.addStyle('h6', fontfamily=s.fontFamily)
        return root
        
    def baseComponents(self):
        u"""Create a theme site with just one single template home page. Answer a list
        of page instances that are used as templates for this site."""
        # Create an instance (=object) of components to be placed on the page.
        # @itemStart        Start index of the item in the selected/sorted set of articles.
        # @itemCount        Nunmber of items (default is 3). Omit current article in the selection
        featured1 = Featured(width=Perc(100), itemCount=2)
        container = Container(components=featured1, rowMaxWidth=Perc(50))
        # Create an instance (=object) of the page, containing the featured components.
        # The class is also the page name in the url.
        homePage = Page(class_=self.C.TEMPLATE_INDEX, components=container, 
            title=self.TITLE, fonts=self.URL_FONTS)
        # Answer a list of types of pages for this site. In this case just one template.
        return [homePage]
    
    def make(self, root=None):
        u"""The instance of this class builds CSS and HTML files at the optional path <b>root</b>.
        If not defined, then the default ~/Desktop/Xierpa3Examples/[component.name] is used as export path,
        as set by Builder.DEFAULT_ROOTPATH"""
        # Create an "instance" (=object) of type "HelloWorldLayout". The type (=class) defines
        # the behavior of the object that is made by calling the class.

        # C S S
        # Create the main CSS builder instance to build the SASS/CSS part of the site.
        cssBuilder = CssBuilder()
        # Compile (=build) the SCSS to CSS and save the file in "css/style.css".
        self.build(cssBuilder) # Build from entire site theme, not just from template. Result is stream in builder.
        cssBuilder.save(self, root) 
    
        # H T M L
        # Create the main HTML builder instance to build the HTML part of the site.
        htmlBuilder = HtmlBuilder()
        # Compile the HTML and save the resulting HTML file in "helloWorld.html".
        self.build(htmlBuilder) # Build from entire site theme, not just from template. Result is stream in builder.
        # Answer the path, so we can directly open the file with a browser.
        return htmlBuilder.save(self, root)  
    
if __name__ == '__main__':
    # This construction "__name__ == '__main__'" makes this Python file only 
    # be executed when called in direct mode, such as "python make.py" in the terminal.         
    # Since no rootPath is added to make(), the file export is in ~/Desktop/Xierpa3Examples/OneColumnSite/   
    path = FeaturedColumn().make()
    webbrowser.open(path)
