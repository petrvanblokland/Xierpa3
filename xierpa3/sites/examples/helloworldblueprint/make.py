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
from xierpa3.toolbox.transformer import TX
from xierpa3.components import Theme, Page, Column 
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.attributes import Em, Margin, Perc, Color
from xierpa3.descriptors.media import Media 
from xierpa3.descriptors.blueprint import BluePrint

BODYFAMILY = 'Impact, Verdana, sans'
CAPTIONFAMILY = 'Georgia, serif' 

class HelloWorldBluePrintText(Column):
 
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Theme.C
    
    # The BluePrint defined the parameters for the component. They can be adjusted by parent
    # components who implement this component on a page, or by inheriting classes that
    # only want to redefine part of the parameters. The actual self.style is created during
    # compilation of the start (not during run-time) as cascading result of all parent BLUEPRINT
    # dictionaries.
    # Furthermore the documentation builder is using the BluePrint instance to visualize 
    # the interface of each component available.
    # 
    BLUEPRINT = BluePrint(
        # Attribute, documentation about the attribute.
        # Main div block
        bodyFamily=BODYFAMILY, doc_bodyFamily=u'Body font family of this example. For now, in this example we only use system fonts.',
        fontSize=Em(4), doc_fontSize=u'Font size of the body text, relative to the body font size.',
        lineHeight=Em(1.2), doc_lineHeight=u'Line height (leading) of body text.',
        textAlign=C.CENTER, doc_textAlign=u'Horizontal alignment of text.',
        color=Color('yellow'), doc_color=u'Color of the main column.',
        colorTablet=Color('orange'), doc_colorTablet=u'Text color of the main column for tablet.',
        colorMobile=Color('red'), doc_colorMobile=u'Text color of the main column for mobile.',
        backgroundColor=Color('red'), doc_backgroundColor=u'Background color of the main column',
        backgroundColorTablet=Color('green'), doc_backgroundColorTablet=u'Background color of the main column for tablet.',
        backgroundColorMobile=Color('#BBB'), doc_backgroundColorMobile=u'Background color of the main column for mobile.',
        paddingTop=Em(0.5), doc_paddingTop=u'Padding on top of the page',
        paddingBottom=Em(0.5), doc_paddingBottom=u'Padding at bottom of the page.',
        margin=Margin(0, C.AUTO), doc_margin=u'Page margin of the column. In this case, horizontally centered on the page.',
        width=Perc(80), doc_width=u'Width of the main column. Default is 80% os the page with.',
        maxWidth=700, doc_maxWidth=u'Maximal width of the column.',
        minWidth=300, doc_minWidth=u'Minimal width of the column.',
        # Caption
        captionFont=CAPTIONFAMILY, doc_captionFont=u'Caption font family for this example. For now, in this example we only use system fonts.',
        captionColor=Color('#888'), doc_captionColor=u'Color of the caption.',
        captionPaddingTop=Em(0.2), doc_captionPaddingTop=u'Padding top of the caption.',
    )
    
    def buildBlock(self, b):
        u"""Build the column, using the parameters from the class BluePrint instance.
        This dictionary is builds the **self.style()** by cascading all BlurPrint instances
        of the parent classes. The result is a complete specification of all the parameters 
        the direction the style and behavior of this component."""
        s = self.style
        b.div(class_=self.getClassName(), color=s.color, margin=s.margin, 
            width=s.width, maxwidth=s.maxWidth, minwidth=s.minWidth, backgroundcolor=s.backgroundColor,
            paddingtop=s.paddingTop, paddingbottom=s.paddingBottom, fontfamily=s.bodyFamily, 
            fontsize=s.fontSize, textalign=s.textAlign, lineheight=s.lineHeight,
            # Now define the @media parameters, where they belong: inside the definition of the element.
            # The media parameters are collected and sorted for output at the end of the CSS document.
            media=(
                # Example for table, show lighter background, change color of text and smaller size.
                Media(min=self.C.M_TABLET_MIN, max=self.C.M_TABLET_MAX, backgroundcolor=s.backgroundColorTablet, 
                    color=s.colorTablet, fontsize=Em(3), width=self.C.AUTO, float=self.C.NONE),
                # For mobile, even more lighter background, change color of text and smaller size.
                Media(max=self.C.M_MOBILE_MAX, backgroundcolor=s.backgroundColorMobile, 
                    color=s.colorMobile, fontsize=Em(2), width=self.C.AUTO, float=self.C.NONE)
            ))
        b.text('Hello parametric world.')
        # One of the advantages of using a real programming language to generate 
        # HTML/CSS code, is that repetitions can be written as a loop. Not necessary
        # fewer lines, but more expandable and less redundant distribution of 
        # knowledge in the code.
        data = (
            # class, minWidth, maxWidth,  text
            ('c1', self.C.M_DESKTOP_MIN, None, 'Responsive desktop mode.' ),
            ('c2', self.C.M_TABLET_MIN, self.C.M_TABLET_MAX, 'Responsive tablet mode.' ),
            ('c3', None, self.C.M_MOBILE_MAX, 'Responsive mobile mode..' ),
        )
        for class_, minWidth, maxWidth, text in data:
            b.div(class_=class_, display=self.C.NONE, fontsize=Em(0.7), color=Color(self.C.WHITE),
                media=Media(min=minWidth, max=maxWidth, display=self.C.BLOCK))
            b.text(text)
            b._div()
        b._div()
        b.div(class_=self.C.CLASS_CAPTION, color=s.captionColor, margin=Margin(0, self.C.AUTO), 
              width=Perc(100), maxwidth=700, minwidth=300,
              paddingtop=s.captionPaddingTop, fontfamily=s.captionFont, fontsize=Em(0.9), 
              textalign=s.textAlign, fontstyle=self.C.ITALIC,
              # Change background color of the line to indicate the illustrate the difference for mobile size.
              #media=Media(max=self.M_MOBILE_MAX, backgroundcolor='yellow', color='#222', fontsize=Em(1),
              #  margin=0, width=Perc(100),
        )
        b.text('Responsive page, generated by Xierpa3. Using BluePrint parameters.')
        b._div()
        
class HelloWorldBluePrint(Theme):
    u"""The **HelloWorldResponsive** class implements a basic "Hello, world!" page, running as
    batch process, saving the result as an HTML file. Double click the generated file or
    drag to a browser see the result."""
    TITLE = u'The responsive "Hello, world!" page using BluePrint styling.' # Use as title of window.

    def baseComponents(self):
        u"""Create a theme site with just one single template home page. Answer a list
        of page instances that are used as templates for this site."""
        # Create an instance (=object) of the text component to be placed on the page.
        hw = HelloWorldBluePrintText()
        # Create an instance (=object) of the page, containing the "hw" component.
        # The class is also the page name in the url.
        # Components can be a single component or a list of components.
        homePage = Page(class_=self.C.TEMPLATE_INDEX, components=hw, title=self.TITLE)
        # Answer a list of types of pages for this site.
        return [homePage]

    def make(self, root):
        u"""The instance of this class builds CSS and HTML files at the optional path **root**.
        If not defined, then the default ~/Desktop/Xierpa3Examples/[component.name] is used as export path,
        as set by Builder.DEFAULT_ROOTPATH"""
        # Create an "instance" (=object) of type "HelloWorldLayout". The type (=class) defines
        # the behavior of the object that is made by calling the class.
        if root is None:
            root = TX.asDir(self.C.PATH_EXAMPLES) # Expand user path to full directory path.
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
    # Since no rootPath is added to make(), the file export is in ~/Desktop/Xierpa3Examples/HelloWorldBluePrint/   
    site = HelloWorldBluePrint()
    path = site.make()
    webbrowser.open(path) # Open file path with browser
