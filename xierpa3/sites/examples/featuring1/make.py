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
from xierpa3.attributes import Em, Px
from xierpa3.adapters import FileAdapter
from xierpa3.components import Theme, Page, Container, FeaturedByDiapText, FeaturedByTextList
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.descriptors.blueprint import BluePrint
from xierpa3.descriptors.media import Media # Include type of Style that holds @media parameters.

# Define the two component here. Normally these would come from a component library,
# where the BluePrint values function as API to adjust the component instance behavior
# from the outside.
          
class Featuring1(Theme):
    TITLE = u'The Simple Website Example Page' # Use as title of window.

    BODYSIZE = Px(12)
    BODYLEADING = Em(1.4)
    BODYFAMILY = '"Hermes FB Book"'
    HEADFAMILY = '"Hermes FB Semibold"'
    
    CC = Theme # Inherit the constants from the parent class.

    ADAPTERCLASS = FileAdapter # Preferred adapter class for this site.
    
    URL_FONTS = [
        # Note that this package contains the a set of latest featured font, and may be changed in the future.
        # If using the font in this package, safest is to refer to the functional constant names below,
        # instead of making a direct reference to the family name.
        # Of course, taking your own account at //www.webtype.com is even better :)
        Theme.XIERPA3_DEMOFONTS, # Webtype @fontface fonts, to be used for localhost demo purposes.
    ]    

    def baseStyle(self):
        s = self.newStyle() # Answer root style without selector
        s.addStyle('body', fontfamily=self.BODYFAMILY, fontsize=self.BODYSIZE, lineheight=self.BODYLEADING)
        s.addStyle('h1, h2, h3, h4, h5, p.lead', fontfamily=self.HEADFAMILY)
        s.addStyle('h6', fontfamily=self.BODYFAMILY)
        s.addStyle('div', float=self.LEFT, width=self.C100)
        return s
    
    def baseComponents(self):
        # Create the component instances
        featured1 = FeaturedByDiapText()
        featured2 = FeaturedByTextList()
        container = Container(components=(featured1, featured2)) # Create the single page instance, containing the 2 components
        # The class is also the page name in the url.
        homePage = Page(class_=self.TEMPLATE_INDEX, name=self.TEMPLATE_INDEX, fonts=self.URL_FONTS,
            title=self.TITLE, css=self.URL_CSS, components=container)
        return [homePage]
    
    def make(self):
        cssBuilder = CssBuilder()
        self.build(cssBuilder)
        cssBuilder.save(self) 
        htmlBuilder = HtmlBuilder()
        self.build(htmlBuilder)
        return htmlBuilder.save(self)  
    
if __name__ == '__main__':
    # This construction "__name__ == '__main__'" makes this Python file only 
    # be executed when called in direct mode, such as "python make.py" in the terminal.         
    Featuring1().make()
    