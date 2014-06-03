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
from xierpa3.attributes import Em, Perc
from xierpa3.components import Theme, Page, Container, Header, MobileNavigation, Footer, Text
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.descriptors.blueprint import BluePrint
        
class SimpleWebSite(Theme):
    u"""The <b>TypeSpecimenSite</b> generates an HTML file with a column of random blurb text. 
    Double click the generated file or drag to a browser see the result."""
    TITLE = u'The Simple Website Example Page' # Use as title of window.

    CLASS_SIDEBAR = 'sideBar'
    CLASS_MAINCOLUMN = 'mainColumn'
    
    CC = Theme
    BLUEPRINT = BluePrint(
        # Sidebar
        sideBarWidth=Perc(20), doc_sideBarWidth=u'Side bar width', 
        sideBarBackgroundColor='orange', doc_sideBarBackgroundColor=u'Side bar backtround color.',                  
        # Main
        mainWidth=Perc(75), doc_mainWidth=u'Main column width',
        mainBackgroundColor='yellow', doc_mainBackgroundColor=u'Main column background color.', 
    )
    def baseComponents(self):
        u"""Create a theme site with just one single template home page. Answer a list
        of page instances that are used as templates for this site."""
        s = self.style
        # Create an instance (=object) of components to be placed on the page.
        header = Header(components=[], mobileContainerDisplay=self.NONE)
        mobileNavigation = MobileNavigation() # Is container by itself. Change??
        footer = Footer(components=[])
        #@@@ Bug here, CSS background color gets in output preceding this div class.
        sideBar = Container(class_=self.CLASS_SIDEBAR, components=(Text('sidebar'),), 
            width=s.sideBarWidth,
            backgroundcolor=s.sideBarBackgroundColor, float=self.LEFT)
        mainContent = Container(class_=self.CLASS_MAINCOLUMN, components=(Text('main content'),), 
            width=s.mainWidth, backgroundcolor=s.mainBackgroundColor, float=self.LEFT)

        # Create an instance (=object) of the page, containing the navigation components.
        homePage = Page(class_='index', name=self.TEMPLATE_INDEX, 
            title=self.TITLE,
            #components=(mobileNavigation, header, sideBar, mainContent, footer),
            #components=(sideBar, mainContent,),
            components=(mainContent,),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, 
            favicon=self.URL_FAVICON)
    
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
    path = SimpleWebSite().make()
    