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
from xierpa3.attributes import Perc, Color, Em, Px
from xierpa3.components import Theme, Page, Container
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.descriptors.blueprint import BluePrint
from xierpa3.descriptors.media import Media # Include type of Style that holds @media parameters.

# Sample string, we don't use data adapaters yet in this example.
LORUMIPSUM = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque vel metus ullamcorper, 
    porttitor ligula id, sollicitudin ante. Sed molestie cursus tortor, ut blandit felis tincidunt at. Suspendisse 
    scelerisque malesuada massa, eu rhoncus nulla interdum ut. Morbi ullamcorper, leo pulvinar pharetra tincidunt, 
    dolor quam ullamcorper lectus, in dignissim magna odio ut eros. Nulla vel enim a leo hendrerit auctor luctus 
    nec urna. Donec ligula nunc, consequat ut aliquet in, auctor id nisl. Pellentesque malesuada tincidunt tortor, 
    varius sollicitudin lorem dictum vitae. Duis vel neque non leo commodo faucibus. In dictum in mauris eget 
    fermentum. Nunc feugiat vitae dolor mollis interdum. Suspendisse potenti. In hac habitasse platea dictumst. 
    Donec ac massa vel velit cursus posuere in a urna. Vestibulum porttitor lacus neque, eu scelerisque enim 
    scelerisque vitae."""

BODYFAMILY = '"Hermes FB Book"'
HEADFAMILY = '"Hermes FB Semibold"'

# Define the two component here. Normally these would come from a component library,
# where the BluePrint values function as API to adjust the component instance behavior
# from the outside.
  
class MainColumn(Container):
    CC = Container
    
    BLUEPRINT = BluePrint(
        width=Perc(70), doc_width=u'Main column width', float=CC.LEFT, 
        backgroundColor='yellow', doc_backgroundColor=u'Main column background color.', 
    )                
    def buildBlock(self, b):
        s = self.style
        b.div(class_=self.getClassName(),
            width=s.width, backgroundcolor=s.backgroundColor, padding=Em(1), lineheight=Em(1.3),
            media=Media(max=self.M_MOBILE_MAX, backgroundcolor=s.backgroundColorMobile, 
              fontsize=Em(2), width=Perc(100), margin=0, lineheight=Em(1.3),
            )
        )
        b.text(LORUMIPSUM)
        b._div()
  
class SideColumn(Container):
    CC = Container
    
    BLUEPRINT = BluePrint(
        width=Perc(20), doc_width=u'Side bar width', float=CC.LEFT, # @@@@ Should be 30
        backgroundColor='orange', doc_backgroundColor=u'Side column background color.',                  
        backgroundColorMobile=Color('#888'), doc_backgroundColorMobile=u'Side bar backtround color for mobile.',  
    )                
    def buildBlock(self, b):
        s = self.style
        b.div(class_=self.getClassName(), 
            width=s.width, backgroundcolor=s.backgroundColor, padding=Em(1), lineheight=Em(1.3),
            media=Media(max=self.M_MOBILE_MAX, backgroundcolor=s.backgroundColorMobile, 
              fontsize=Em(2), width=Perc(100), margin=0, lineheight=Em(1.3),
            )
        )
        b.text(LORUMIPSUM)
        b._div()
        
class SimpleWebSite(Theme):
    TITLE = u'The Simple Website Example Page' # Use as title of window.

    CLASS_MAINCOLUMN = 'mainColumn'
    CLASS_SIDECOLUMN = 'sideColumn'

    BODYFAMILY = '"Hermes FB Book"'
    HEADFAMILY = '"Hermes FB Semibold"'
    BODYSIZE = Px(12)
    BODYLEADING = Em(1.4)
    
    CC = Theme # Inherit the constants from the parent class.

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
        side = SideColumn()
        main = MainColumn()
        # Create the single page instance, containing the 2 components
        # The class is also the page name in the url.
        homePage = Page(class_=self.TEMPLATE_INDEX, name=self.TEMPLATE_INDEX, fonts=self.URL_FONTS,
            title=self.TITLE, css=self.URL_CSS, components=(side, main))
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
    SimpleWebSite().make()
    