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
from xierpa3.attributes import Em, Margin, Px 
from xierpa3.components import Theme, Page, Column
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.descriptors.style import Media

class SimpleTypeSpecimenColumn(Column):

    CSS_BODYFONT = '"BentonSansRE"'
    CSS_HEADFONT = '"BentonSansCond Medium"'
    
    SIZE_SMALL = 9
    SIZE_LARGE = 60
    
    def buildBlock(self, b):
        u"""Build the specimen column"""
        b.div(class_=self.CLASS_COLUMN, color=self.BLACK, 
              margin=Margin(0, self.AUTO, 0, self.AUTO), width=1100, 
              maxwidth=1100, minwidth=0, backgroundcolor=self.WHITE, 
              padding=0, fontfamily=self.CSS_BODYFONT, fontsize=Em(1), 
              lineheight=Em(1.4),
              # Remove margins on mobile, showing the column on full screen width.
              media=Media(max=self.M_MOBILE_MAX, margin=0, width=self.C100,
                maxwidth=self.C100, minwidth=0),
        )
        # Add div.row to allow padding, without making the main column div
        # grow outside the parent boudaries.
        b.div(class_=self.CLASS_ROW, padding=Em(2))
        for n in range(self.SIZE_SMALL, self.SIZE_LARGE):
            b.div(class_='specimen%02d' % n, width=self.C100, fontsize=Px(n), lineheight=Em(1.1))
            b.span(class_='size%02d' % n, fontsize=Px(self.SIZE_SMALL))
            b.text('%d px' % n)
            b._span()
            b.text(u'ABCDEFGH abcdefgh €$@#123')
            b._div()
        b._div(comment=self.CLASS_ROW)
        b._div()
        
class SimpleTypeSpecimenSite(Theme):
    u"""The <b>TypeSpecimenSite</b> generates an HTML file with a column of random blurb text. 
    Double click the generated file or drag to a browser see the result."""
    TITLE = u'The Single Column Example Page.' # Use as title of window.

    URL_FONTS = (
        # Topaz (Benton Sans RE)
        'http://cloud.webtype.com/css/7aa22aa1-1709-4b55-b95c-3413d3e5280a.css',
    )    
    def baseComponents(self):
        u"""Create a theme site with just one single template home page. Answer a list
        of page instances that are used as templates for this site."""
        # Create an instance (=object) of components to be placed on the page.
        column = SimpleTypeSpecimenColumn()
        # Create an instance (=object) of the page, containing the navigation components.
        homePage = Page(class_='home', components=(column,), title=self.TITLE, fonts=self.URL_FONTS)
        # Answer a list of types of pages for this site. In this case just one template.
        return [homePage]
    
    def make(self):
        u"""Make the instance of this class to build CSS and HTML."""
        # Create an "instance" (=object) of type "HelloWorldLayout". The type (=class) defines
        # the behavior of the object that is made by calling the class.

        # C S S
        # Create the main CSS builder instance to build the CSS part of the site.
        cssBuilder = CssBuilder()
        # Compile (=build) the SCSS to CSS and save the file in "css/style.css".
        cssBuilder.save(self) 
    
        # H T M L
        # Create the main HTML builder instance to build the HTML part of the site.
        htmlBuilder = HtmlBuilder()
        # Compile the HTML and save the resulting HTML file in "helloWorld.html".
        # Answer the path, so we can open the file with a browser.
        return htmlBuilder.save(self)  
    
if __name__ == '__main__':
    # This construction "__name__ == '__main__'" makes this Python file only 
    # be executed when called in direct mode, such as "python make.py" in the terminal.         
    path = SimpleTypeSpecimenSite().make()
    