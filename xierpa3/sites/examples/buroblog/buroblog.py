# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    
#    Copyright (c) 2014+  Buro Petr van Blokland + Claudia Mens, www.petr.com
#    
#    X I E R P A  3
#    Usage and distribution by the MIT License.
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

class BuroBlogBuilder(KirbyBuilder):
    pass

class BuroBlogAdapter(KirbyAdapter):
    pass

class BuroBlog(KirbyBlog):
    u"""The <b>SimpleBlog</b> class implements the standard example blog."""
    TITLE = 'Blog Petr van Blokland + Claudia Mens'
    SUBTITLE = 'Notes on design and education.'

if __name__ == '__main__':
    adapter = BuroBlogAdapter()
    theme = BuroBlog(adapter=adapter)

    PATH_ROOT = '/Applications/MAMP/htdocs/%s/' % theme.name.lower()
    theme.PATH_CSS  = PATH_ROOT + 'assets/css/style.css'
    theme.PATH_TEMPLATE = PATH_ROOT + 'site/templates/%s.php'
    theme.PATH_BLUEPRINT = PATH_ROOT + 'panel/defaults/blueprints/%.php'
    
    builder = CssBuilder()
    theme.build(builder) # Build the SCSS/CSS of the theme
    builder.save(theme.PATH_CSS) # Compile the SCSS to CSS and save the file.
    # Build PHP
    builder = BuroBlogBuilder()
    #bluePrintBuilder = BluePrintBuilder() 
    for template in theme.getTemplates():
        template.build(builder) 
        exportPath = theme.PATH_TEMPLATE % template.name
        print 'Saving', exportPath
        builder.save(exportPath)
        # Build the panel blueprint
        #template.build(bluePrintBuilder)
        #print 'Saving panel blueprint', theme.PATH_BLUEPRINT % template.name
        #bluePrintBuilder.save(theme.PATH_BLUEPRINT % template.name)
        
        

