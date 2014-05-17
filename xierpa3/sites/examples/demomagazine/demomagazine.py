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
from xierpa3.components import Logo, SocialMedia, Page
from xierpa3.themes.magazine.base import BaseMagazine
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.builders.cssbuilder import CssBuilder

class DemoMagazine(BaseMagazine):
    u"""The <b>Blog</b> class implements the standard example blog."""
    TITLE = 'Blog Petr van Blokland + Claudia Mens'
    SUBTITLE = 'Notes on design and education.'

    def baseComponents(self):
        logo = Logo()
        socialmedia = SocialMedia(twitterAccount='mymagazine', facebookAccount='mymagazine') 
        
        homePage = Page(components=(logo, socialmedia))
        return [homePage]
    
if __name__ == '__main__':
    magazine = DemoMagazine()
    # Create the main CSS builder
    cssBuilder = CssBuilder()
    # Create the main HTML builder
    htmlBuilder = HtmlBuilder()
    #bluePrintBuilder = BluePrintBuilder() 
    for template in magazine.getTemplates():
        # Build the SCSS/CSS of this theme template
        template.build(cssBuilder) 
        cssPath = template.getStylePath()
        cssBuilder.save(cssPath, makeDirectory=True) # Compile the SCSS to CSS and save the file.
        # Build the HTML of this theme template
        template.build(htmlBuilder) # Build the code for every page template in the theme
        exportPath = htmlBuilder.getTemplatePath(magazine)
        print 'Saving', exportPath
        htmlBuilder.save(exportPath, makeDirectory=True) # Save the exported template code into its file.
        
        

