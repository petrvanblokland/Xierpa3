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
#    buroblog.py
#
#    Example theme to build a blog site.
#
#    TODO
#    Make it work (including auto install) with Amazon database + CMS functions
#    Make example templates and components
#    Make payed Udemy course how to use/implement/build
#    Blog/site/store of components with specific tasks
#
import os
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.themes.kirbyblog.kirbyblog import KirbyBlog
from xierpa3.themes.kirbyblog.kirbyadapter import KirbyAdapter
from xierpa3.themes.kirbyblog.kirbybuilder import KirbyBuilder
from xierpa3.attributes import * 
from xierpa3.components import *
from xierpa3.constants.constants import C

class BlogBuilder(KirbyBuilder):
    pass

class BlogAdapter(KirbyAdapter):
    pass

class Blog(KirbyBlog):
    u"""The <b>Blog</b> class implements the standard example blog."""
    TITLE = 'Blog Petr van Blokland + Claudia Mens'
    SUBTITLE = 'Notes on design and education.'

if __name__ == '__main__':
    adapter = BlogAdapter()
    theme = Blog(adapter=adapter)

    #builder = CssBuilder()
    #theme.build(builder) # Build the SCSS/CSS of the theme
    #builder.save(theme.getStylePath()) # Compile the SCSS to CSS and save the file.
    # Create the main builder
    builder = BlogBuilder()
    #bluePrintBuilder = BluePrintBuilder() 
    for template in theme.getTemplates():
        template.build(builder) # Build the code for every page template in the theme
        exportPath = builder.getTemplatePath(theme)
        print 'Saving', exportPath
        builder.save(exportPath, makeDirectory=True) # Save the exported template code into its file.
        # Build the panel blueprint
        #template.build(bluePrintBuilder)
        #print 'Saving panel blueprint', theme.PATH_BLUEPRINT % template.name
        #bluePrintBuilder.save(theme.PATH_BLUEPRINT % template.name)
        
        

