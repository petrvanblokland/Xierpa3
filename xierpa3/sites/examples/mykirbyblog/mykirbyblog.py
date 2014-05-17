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
#    mykirbyblog.py
#
#    Example theme to build a kirby blog site.
#
from xierpa3.themes.kirbyblog.kirbyblog import KirbyBlog
from xierpa3.themes.kirbyblog.kirbyadapter import KirbyAdapter
from xierpa3.themes.kirbyblog.kirbybuilder import KirbyBuilder

class BlogBuilder(KirbyBuilder):
    pass

class BlogAdapter(KirbyAdapter):
    pass

class MyKirbyBlog(KirbyBlog):
    u"""The <b>Blog</b> class implements the standard example blog."""
    TITLE = 'Blog Petr van Blokland + Claudia Mens'
    SUBTITLE = 'Notes on design and education.'

if __name__ == '__main__':
    adapter = BlogAdapter()
    theme = MyKirbyBlog(adapter=adapter)

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
        
        

