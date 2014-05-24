# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#    shop.py
#
#    Example theme to build a blog site.
#
#    TODO
#    Make it work (including auto install) with Amazon database + CMS functions
#    Make example templates and components
#    Make payed Udemy course how to use/implement/build
#    Blog/site/store of components with specific tasks
#
from xierpa3.attributes import * 
from xierpa3.components import *
from xierpa3.toolbox.transformer import TX

class Shop(Theme):
    u"""The <b>SimpleBlog</b> class implements the standard example blog."""
    TITLE = '[Title of the blog]'
    SUBTITLE = '[Subtitle of the blog]'

    def XXXgetFilePath(self, site):
        u"""
        Answers the file path, based on the URL. Add '/files' to hide Python sources from view.
        """
        fileName = site.e.path.split('/')[-1:]
        if fileName:
            fileName = '/'.join(file)
        else:
            fileName = 'index'
        return TX.class2Path(site) + '/files/' + fileName
    
