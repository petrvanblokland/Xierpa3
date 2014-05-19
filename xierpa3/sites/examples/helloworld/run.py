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
#    demomagazine.py
#
#    Example theme to build a kirby blog site.
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
    u"""The <b>HelloWorld</b> class implements a basic Hello World page."""
    TITLE = u'The standard “Hello world” page.'
    SUBTITLE = u'Any subtitle goes here.'

    def getRootPath(self):
        from xierpa3.sites.examples import helloworld
        return helloworld.__path__[0]

    def baseComponents(self):
        u"""Create a theme site with just one single template home page."""
        hw = HelloWorldText()
        homePage = Page(components=(hw,))
        return [homePage]
    
if __name__ == '__main__':
    site = HelloWorld()
    # C S S
    # Create the main CSS builder and build the CSS part of the site with it.
    cssBuilder = CssBuilder()
    # Compile the SCSS to CSS and save the file.
    cssBuilder.save(site) 

    # H T M L
    # Create the main HTML builder
    htmlBuilder = HtmlBuilder()
    # Compile the HTML and save in separate files.
    htmlBuilder.save(site) 
