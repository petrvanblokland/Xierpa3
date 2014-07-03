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
#    Demo site for the simple "hello world" example.
#    The "run.py" program creates the files:
#        ~/Xierpa3Examples/HelloWorldLayout/css/style.scss
#        ~/Xierpa3Examples/HelloWorldLayout/css/style.css
#        ~/Xierpa3Examples/HelloWorldLayout/index.html
#    from the one HelloWorldLayout theme instance by applying respectively the
#    CssBuilder and HtmlBuilder to the theme.
#    Each of the builders takes the information from the theme to build its
#    own type of file.
#
import webbrowser
from xierpa3.components import Theme, Page, Column 
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.constants.constants import C
from xierpa3.attributes import Em, Margin 

class HelloWorldText(Column):
    def buildBlock(self, b):
        u"""Build the column. Note that although the "div" suggest that it is just
        HTML building there, the method get called both with <b>b</b> as CssBuilder
        and as HtmlBuilder. Each builder will filter out the appropriate attributes and
        translates it into its own syntax. The HTML tags generated by the article
        are set in CSS by the empty statements.
        Building the styled 2 text blocks, written out with duplicated values,
        as example how this works. See other examples for approaches with more
        cascading styled hierarchy."""
        # For the showing of this example, the parameters in the column div are hard coded.
        # Normally a components should allow access to many of the attributes through the
        # class dictionary cls.BLUEPRINT, which is a BluePrint instance.
        # See the example “HelloWorldBluePrint” for how this works.
        b.div(class_=self.getClassName(), color='yellow', margin=Margin(0, C.AUTO, 0, C.AUTO), 
              width='70%', maxwidth=700, minwidth=300, backgroundcolor='#222', 
              padding=Em(0.5), fontfamily='Georgia', fontsize=Em(4), textalign=C.CENTER,
              lineheight=Em(1.4))
        b.text('Hello world.')
        b._div()
        b.div(class_='caption', color='#888', margin=Margin(0, C.AUTO, 0, C.AUTO), 
              width='70%', maxwidth=700, minwidth=300,
              paddingleft=Em(0.5), fontfamily='Georgia', fontsize=Em(0.8), textalign=C.CENTER,
              lineheight=Em(1.4), fontstyle=C.ITALIC)
        b.text('Intentionally non-responsive page example. Generated by Xierpa3.')
        b._div()
        
class HelloWorldLayout(Theme):
    u"""The <b>HelloWorldLayout</b> class implements a basic Hello World page, running as
    batch process, saving the result as an HTML file. Also it is available in the example webserver,
    e.g. through the Xierpa3App."""
    TITLE = u'The layout “Hello world” page.' # Use as title of window.

    def baseComponents(self):
        u"""Create a theme site with just one single template home page. Answer a list
        of page instances that are used as templates for this site."""
        # Create an instance (=object) of the text component to be placed on the page.
        hw = HelloWorldText()
        # Create an instance (=object) of the page, containing the "hw" component.
        # The class is also the page name in the url.
        # Components can be a single component or a list of components.
        homePage = Page(class_=self.TEMPLATE_INDEX, components=hw, title=self.TITLE)
        # Answer a list of types of pages for this site.
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
    # Since no rootPath is added to make(), the file export is in ~/Desktop/Xierpa3Examples/HelloWorldLayout/   
    path = HelloWorldLayout().make()
    webbrowser.open(path)
