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
from xierpa3.components import Theme, Page, Column 
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.attributes import Em, Margin, Perc
from xierpa3.descriptors.media import Media 
from xierpa3.descriptors.blueprint import BluePrint

class HelloWorldBluePrintText(Column):
 
    # Parent is also inheriting from the constants/config class to allow inheriting redefinition of values.
    CC = Column 
    
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
        bodyFont='Impact', doc_bodyFont=u'Body font of this example. For now, in this examply we only use system fonts.',
        fontSize=Em(4), doc_fontSize=u'Font size of the body text, relative to the body font size.',
        lineHeight=Em(1.2), doc_lineHeight=u'Line height (leading) of body text.',
        textAlign=CC.CENTER, doc_textAlign=u'Horizontal alignment of text.',
        color='yellow', doc_color=u'The “doc_” attributes are used for documentation about the interface of this component.',
        colorTablet='orange', doc_colorTablet=u'Text color of the main column.',
        backgroundColor='red', doc_backgroundColor=u'Background color of the main column',
        backgroundColorTablet='green', doc_backgroundColorTablet=u'Background color of the main column for tablet.',
        paddingTop=Em(0.5), doc_paddingTop=u'Padding on top of the page',
        paddingBottom=Em(0.5), doc_paddingBottom=u'Padding at bottom of the page.',
        margin=Margin(0, CC.AUTO), doc_margin=u'Page margin of the column. In this case, horizontally centered on the page.',
        width=Perc(80), doc_width=u'Width of the main column. Default is 80% os the page with.',
        maxWidth=700, doc_maxWidth=u'Maximal width of the column.',
        minWidth=300, doc_minWidth=u'Minimal width of the column.',
        # Caption
        captionFont='Georgia', doc_captionFont=u'Caption font for this example. For now, in this examply we only use system fonts.',
        captionColor='#888', doc_captionColor=u'Color of the caption.',
        captionPaddingTop=Em(0.2), doc_captionPaddingTop=u'Padding top of the caption.',
        # 
    )
    
    def buildBlock(self, b):
        u"""Build the column, using the parameters from the class BluePrint instance.
        This dictionary is builds the <b>self.style()</b> by cascading all BlurPrint instances
        of the parent classes. The result is a complete specification of all the parameters 
        the direction the style and behavior of this component."""
        s = self.style
        b.div(class_=self.getClassName(), color=s.color, margin=s.margin, 
            width=s.width, maxwidth=s.maxWidth, minwidth=s.minWidth, backgroundcolor=s.backgroundColor,
            paddingtop=s.paddingTop, paddingbottom=s.paddingBottom, fontfamily=s.bodyFont, 
            fontsize=s.fontSize, textalign=s.textAlign, lineheight=s.lineHeight,
            # Now define the @media parameters, where they belong: inside the definition of the element.
            # The media parameters are collected and sorted for output at the end of the CSS document.
            media=(
                # Example for table, show lighter background, change color of text and smaller size.
                Media(min=self.M_TABLET_MIN, max=self.M_TABLET_MAX, backgroundcolor=s.backgroundColorTablet, 
                    color=s.colorTablet, fontsize=Em(3), width=self.C100),
                # For mobile, even more lighter background, change color of text and smaller size.
                Media(max=self.M_MOBILE_MAX, backgroundcolor='#BBB', color='red', fontsize=Em(2), 
                    width=self.C100)
            ))
        b.text('Hello parametric world.')
        # One of the advantages of using a real programming language to generate 
        # HTML/CSS code, is that repetitions can be written as a loop. Not necessary
        # fewer lines, but more expandable and less redundant distribution of 
        # knowledge in the code.
        data = (
            # class, minWidth, maxWidth,  text
            ('c1', self.M_DESKTOP_MIN, None, 'Responsive desktop mode.' ),
            ('c2', self.M_TABLET_MIN, self.M_TABLET_MAX, 'Responsive tablet mode.' ),
            ('c3', None, self.M_MOBILE_MAX, 'Responsive mobile mode..' ),
        )
        for class_, minWidth, maxWidth, text in data:
            b.div(class_=class_, display=self.NONE, fontsize=Em(0.7), color=self.WHITE,
                media=Media(min=minWidth, max=maxWidth, display=self.BLOCK))
            b.text(text)
            b._div()
        b._div()
        b.div(class_=self.CLASS_CAPTION, color=s.captionColor, margin=Margin(0, self.AUTO), 
              width=self.C100, maxwidth=700, minwidth=300,
              paddingtop=s.captionPaddingTop, fontfamily=s.captionFont, fontsize=Em(0.9), 
              textalign=s.textAlign, fontstyle=self.ITALIC,
              # Change background color of the line to indicate the illustrate the difference for mobile size.
              #media=Media(max=self.M_MOBILE_MAX, backgroundcolor='yellow', color='#222', fontsize=Em(1),
              #  margin=0, width=self.C100),
        )
        b.text('Generated by Xierpa3.')
        b._div()
        
class HelloWorldBluePrint(Theme):
    u"""The <b>HelloWorldResponsive</b> class implements a basic Hello World page, running as
    batch process, saving the result as an HTML file. Double click the generated file or
    drag to a browser see the result."""
    TITLE = u'The responsive “Hello world” page.' # Use as title of window.

    def baseComponents(self):
        u"""Create a theme site with just one single template home page. Answer a list
        of page instances that are used as templates for this site."""
        # Create an instance (=object) of the text component to be placed on the page.
        hw = HelloWorldBluePrintText()
        # Create an instance (=object) of the page, containing the "hw" component.
        # The class is also the page name in the url.
        homePage = Page(class_=self.TEMPLATE_INDEX, components=(hw,), title=self.TITLE)
        # Answer a list of types of pages for this site.
        return [homePage]

    def make(self):
        u"""The instance of this class builds CSS and HTML."""
        # Create an "instance" (=object) of type "HelloWorldLayout". The type (=class) defines
        # the behavior of the object that is made by calling the class.

        # C S S
        # Create the main CSS builder instance to build the SASS/CSS part of the site.
        cssBuilder = CssBuilder()
        # Compile (=build) the SCSS to CSS and save the file in "css/style.css".
        self.build(cssBuilder) # Build from entire site theme, not just from template. Result is stream in builder.
        cssBuilder.save(self) 
    
        # H T M L
        # Create the main HTML builder instance to build the HTML part of the site.
        htmlBuilder = HtmlBuilder()
        # Compile the HTML and save the resulting HTML file in "helloWorld.html".
        self.build(htmlBuilder) # Build from entire site theme, not just from template. Result is stream in builder.
        # Answer the path, so we can open the file with a browser.
        return htmlBuilder.save(self)  
    
if __name__ == '__main__':
    # This construction "__name__ == '__main__'" makes this Python file only 
    # be executed when called in direct mode, such as "python make.py" in the terminal.         
    path = HelloWorldBluePrint().make()
    webbrowser.open(path)
