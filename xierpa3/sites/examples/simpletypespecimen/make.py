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
from xierpa3.attributes import Perc, Em, Margin, Px, Color
from xierpa3.components import Theme, Page, Column
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.descriptors.media import Media
from xierpa3.descriptors.blueprint import BluePrint

class SimpleTypeSpecimenColumn(Column):

    CC = Column # Access constants through super class.
    MAXWIDTH = Px(1100)
    # Load @fontface fonts for this example from www.webtype.com
    BODYFAMILY = '"Benton Sans RE"'
    HEADFAMILY = '"Benton Modern RE"'
    SPECIMENFAMILY = HEADFAMILY
    
    BLUEPRINT = BluePrint(
        # Column stuff
        fontFamily=BODYFAMILY, doc_fontFamily=u'Column main font family', 
        width=MAXWIDTH, doc_width=u'Column width.', 
        widthMobile=Perc(100), doc_widthMobile=u'Column width for mobile.',  
        minWidth=0, doc_minWidth=u'Column minimal width.', 
        minWidthMobile=0, doc_minWidthMobile=u'Column minimal width for mobile.', 
        maxWidth=MAXWIDTH, doc_maxWidth=u'Column maximal width.',   
        maxWidthMobile=Perc(100), doc_maxWidthMobile=u'Column maximal width for mobile.', 
        margin=Margin(0, CC.AUTO, 0, CC.AUTO), doc_margin=u'Column margin.', 
        marginMobile=0, doc_marginMobile=u'Column margin for mobile.', 
        padding=0, doc_padding='Column padding.', 
        fontSize=Em(1), doc_fontSize=u'Column main font size.',
        lineheight=Em(1.4), doc_lineheight=u'Column main leading.', 
        color=Color(0), doc_color=u'Column text color, default is black.',
        backgroundColor=Color('#FFF'), doc_backgroundColor='Column background color, default is white.', 
        # Row
        rowPadding=Em(2), doc_rowPadding=u'Row padding.',
        # Speciment stuff
        specimentSizeIndicator=13, doc_specimenSizeIndicator=u'Size of the size indicator.',
        specimentSmall=18, doc_specimentSmall=u'Smallest font size of the specimen.',
        specimenLarge=37, doc_specimenLarge=u'Largest font size of the specimen.', 
        specimenWidth=Perc(100), doc_specimenWidth=u'Specimen line width.', 
        specimentLineHeight=Em(1.2), doc_specimentLineHeight=u'Specimen line height, relative to waterfall font size.',
        # Size label
        sizeLabelColor=Color('#888'), doc_sizeLabelColor='Size label color, default is mid-gray.',
        # h1
        h1FontFamily=HEADFAMILY, doc_h1FontFamily=u'h1 font family.',
        h1FontSize=Em(2), doc_h1FontSize=u'h1 font size',
        h1LineHeight=Em(1.4), doc_h1LineHeight=u'h1 leading',
        h1MarginBottom=Em(0.5), doc_h1MarginBottom=u'h1 margin bottom',  
    )    
    def buildBlock(self, b):
        u"""Build the specimen column"""
        s = self.style # Copy from inherited BluePrints with redefined user attributes.
        b.div(class_=self.CLASS_COLUMN, color=s.color, 
              margin=s.margin, width=s.width, maxwidth=s.maxWidth, minwidth=s.minWidth, 
              backgroundcolor=s.backgroundColor, 
              padding=s.padding, fontfamily=s.fontFamily, fontsize=s.fontSize, 
              lineheight=s.lineheight,
              # Remove margins on mobile, showing the column on full screen width.
              media=Media(max=self.M_MOBILE_MAX, margin=s.marginMobile, width=s.widthMobile,
                maxwidth=s.maxWidthMobile, minwidth=s.minWidthMobile),
        )
        # Add div.row to allow padding, without making the main column div
        # grow outside the parent boundaries.
        b.div(class_=self.CLASS_ROW, padding=s.rowPadding)
        b.h1(fontfamily=s.h1FontFamily, fontsize=s.h1FontSize, lineheight=s.h1LineHeight, 
            marginbottom=s.h1MarginBottom)
        b.text('WebType ' + self.SPECIMENFAMILY[1:-1])
        b._h1()
        for n in range(s.specimentSmall, s.specimenLarge):
            b.div(class_='specimen%02d' % n, width=s.specimenWidth, fontsize=Px(n), 
                lineheight=s.specimentLineHeight, fontfamily=self.SPECIMENFAMILY)
            b.span(class_='size%02d' % n, fontsize=Px(s.specimentSizeIndicator), 
                color=s.sizeLabelColor, fontfamily=self.BODYFAMILY)
            b.text('%d px' % n)
            b._span()
            b.text(u'ABCDEFGHIJKLM abcdefghijklm €$@#123')
            b._div()

        # Add reference to sponsored Webtype webfonts.
        b.hr()
        b.a(href='//webtype.com', color=s.color, fontfamily=self.BODYFAMILY, fontsize=Em(0.8),
            lineheight=Em(1.4), target='external')
        b.text('The typefaces in this example %s and %s are sponsored by &lt;Webtype&gt;' % (self.BODYFAMILY, self.HEADFAMILY))
        b._a()

        # Close the row
        b._div(comment=self.CLASS_ROW)
        b._div()
        
class SimpleTypeSpecimenSite(Theme):
    u"""The <b>TypeSpecimenSite</b> generates an HTML file with a column of random blurb text. 
    Double click the generated file or drag to a browser see the result."""
    TITLE = u'The Simple Type Specimen Page' # Use as title of window.

    URL_FONTS = (
        # Note that this package contains the a set of latest featured font, and may be changed in the future.
        # If using the font in this package, safest is to refer to the functional constant names below,
        # instead of making a direct reference to the family name.
        # Of course, taking your own account at //www.webtype.com is even better :)
        Theme.XIERPA3_DEMOFONTS,    # Webtype @fontface fonts, to be used for localhost demo purposes.
    )    
    def baseComponents(self):
        u"""Create a theme site with just one single template home page. Answer a list
        of page instances that are used as templates for this site."""
        # Create an instance (=object) of components to be placed on the page.
        column = SimpleTypeSpecimenColumn()
        # Create an instance (=object) of the page, containing the navigation components.
        homePage = Page(class_='home', components=(column,), title=self.TITLE, 
            fonts=self.URL_FONTS)
        # Answer a list of types of pages for this site. In this case just one template.
        return [homePage]
    
    def make(self):
        u"""The instance of this class builds CSS and HTML."""
        # Create an "instance" (=object) of type "HelloWorldLayout". The type (=class) defines
        # the behavior of the object that is made by calling the class.

        # C S S
        # Create the main CSS builder instance to build the SASS/CSS part of the site.
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
    