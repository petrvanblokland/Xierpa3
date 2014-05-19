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
#    run.py
#
#    Demo site for the simple "hello world" example.
#    The "run.py" program creates the files:
#        files/css/style.scss
#        files/css/style.css
#        files/helloWorld.html
#    from the one HelloWorld theme instance by applying respectively the
#    CssBuilder and HtmlBuilder to the theme.
#    Each of the builders takes the information from the theme to build its
#    own type of file.
#
from xierpa3.components import Theme, Page, Column 
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.builders.cssbuilder import CssBuilder

class HelloWorldText(Column):
    def buildBlock(self, b):
        b.div(color='red')
        b.text('Hello world.')
        b._div()
        
class HelloWorld(Theme):
    u"""The <b>HelloWorld</b> class implements a basic Hello World page, running as
    batch process, saving the result as an HTML file. Double click the generated file or
    drag to a browser see the result."""
    TITLE = u'The standard “Hello world” page.' # Use as title of window.

    def getRootPath(self):
        u"""Get the root path for the "files/" directory, so the builder knows where to 
        write the HTML file."""
        from xierpa3.sites.examples import helloworld
        return helloworld.__path__[0]

    def baseComponents(self):
        u"""Create a theme site with just one single template home page. Answer a list
        of page instances that are used as templates for this site."""
        # Create an instance (=object) of the text component to be placed on the page.
        hw = HelloWorldText()
        # Cerate an instance (=object) of the page, containing the "hw" component.
        homePage = Page(components=(hw,), title=self.TITLE)
        # Answer a list of types of pages for this site.
        return [homePage]
    
if __name__ == '__main__':
    # This construction make the Python file only be executed when called in direct mode,
    # such as "python run.py" in the terminal. This way it is also possible to inherit from
    # "HelloWorld" class, to make another example (see example/helloworldlayout).
    
    # Create an "instance" (=object) of type "HelloWorld". The type (=class) defines
    # the behavior of the object that is made by calling the class.
    site = HelloWorld()
    # C S S
    # Create the main CSS builder instance to build the CSS part of the site with.
    cssBuilder = CssBuilder()
    # Compile (=build) the SCSS to CSS and save the file.
    cssBuilder.save(site) 

    # H T M L
    # Create the main HTML builder instance to build the HTML part of the site with.
    htmlBuilder = HtmlBuilder()
    # Compile the HTML and save the resulting HTML file in "files/hellowork.html".
    htmlBuilder.save(site) 
