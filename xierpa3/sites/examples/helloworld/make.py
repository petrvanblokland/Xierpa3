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
#        ~/Xierpa3Examples/HelloWorld/css/style.scss
#        ~/Xierpa3Examples/HelloWorld/css/style.css
#        ~/Xierpa3Examples/HelloWorld/index.html
#    from the one HelloWorld theme instance by applying respectively the
#    CssBuilder and HtmlBuilder to the theme.
#    Each of the builders takes the information from the theme to build its
#    own type of file.
#
import webbrowser
from xierpa3.attributes import Px
from xierpa3.toolbox.transformer import TX
from xierpa3.components import Theme, Page, Column 
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder

class HelloWorldText(Column):
    u"""The <b>HelloWorldText</b> text column component shows the fixed ”Hello world” 
    in red color."""
    def buildBlock(self, b):
        # Single style attribute, just to show how it works. 
        # In the simple example the resulting div does not have a class.
        b.div(color='red', fontfamily='Verdana', fontsize=Px(24)) 
        b.text('Hello world.')
        b._div()
        
class HelloWorld(Theme):
    u"""The <b>HelloWorld</b> site class implements a basic ”Hello World page“,
    showing the smallest possible web page, while including one style attribute to be 
    generated in CSS."""
    TITLE = u'The standard “Hello world” page.' # Use as title of window.

    def baseComponents(self):
        u"""Create a theme site with just one single template home page. Answer a list
        of page instances that are used as templates for this site."""
        # Create an instance (=object) of the text component to be placed on the page.
        hw = HelloWorldText()
        # Create an instance (=object) of the page, containing the "hw" component.
        # The page class is also the page name in the url: http://localhost:8060/index
        # Components can be a single component or a list of components.
        homePage = Page(class_=self.C.TEMPLATE_INDEX, components=hw, title=self.TITLE)
        # Answer a list of types of pages for this site.
        return [homePage]

    def make(self, root):
        u"""The instance of this class builds CSS and HTML files at the optional path *root*.
        If not defined, then @Builder.C.DEFAULT_ROOTPATH@ is used, as in general builders 
        are associated where output should go to. 
        E.g. the default @HtmlBuilder.C.DEFAULT_ROOTPATH@ is defined as to the user extended 
        path of @~/Desktop/Xierpa3Examples/[component.name]@.
        And for @CssBuilder@ it is @~/Desktop/Xierpa3Examples/[component.name]/css/style.css@."""
        # C S S
        # Create the main CSS builder instance to build the CSS part of the site.
        cssBuilder = CssBuilder()
        # Compile (=build) the SCSS to CSS.
        self.build(cssBuilder) 
        # Save the file in "css/style.css".
        cssBuilder.save(self, root=root) 
    
        # H T M L
        # Create the main HTML builder instance to build the HTML part of the site.
        htmlBuilder = HtmlBuilder()
        # Compile the site instance and its components into HTML code.
        self.build(htmlBuilder) 
        # Save the resulting HTML file in "index.html"
        # Answer the file path, so we can directly open the file with a browser.
        return htmlBuilder.save(self, path=root + 'index.html')  
    
if __name__ == '__main__':
    # This construction "__name__ == '__main__'" makes this Python file only 
    # be executed when called in direct mode, such as "python make.py" in the terminal.      
    # Since no rootPath is added to make(), the file export is in builder.DEFAULT_ROOTPATH
    # which typically is the user extended path of ~/Desktop/Xierpa3Examples/HelloWorld/   
    
    # TODO: for some reason there is double output of HTML right now, using make()
    # TODO: Make(root) implements on other example classes
    
    site = HelloWorld()
    root = site.getRootDir()
    filePath = site.make(root)
    webbrowser.open('file://'+filePath)
