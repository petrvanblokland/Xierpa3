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
from xierpa3.components import Theme, Page, Column 
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder

class HelloWorldText(Column):
    u"""The <b>HelloWorldText</b> text column component shows the fixed ”Hello world” 
    in red color."""
    def buildBlock(self, b):
        # Single style attribute, just to show how it works. 
        # In the simple example the resulting div does not have a class.
        b.div(color='red') 
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
        homePage = Page(components=(hw,), title=self.TITLE)
        # Answer a list of types of pages for this site.
        return [homePage]

    def make(self):
        u"""The instance of this class builds CSS and HTML."""
        # Create an "instance" (=object) of type "HelloWorld". The type (=class) defines
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
    path = HelloWorld().make()
    webbrowser.open(path)
