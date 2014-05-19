# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
# 	xierpa server
# 	(c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#
# 	X I E R P A  3
# 	No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   phpbuilder.py
#
from xierpa3.builders.htmlbuilder import HtmlBuilder

class KirbyBuilder(HtmlBuilder):

    PATH_ROOT = '/Applications/MAMP/htdocs/%s/'
       
    def theme(self, component):
        pass
    
    def _theme(self, component):
        pass
    
    def page(self, component):
        adapter = component.adapter
        self.clear() # Clear the output stream for next theme page
        
    def _page(self, component):
        pass
        
    def getRootPath(self, component): 
        return self.PATH_ROOT % component.root.name.lower()
    
    def getStylePath(self, component):
        u"""Answer the local path to the CSS file."""
        return self.getRootPath(component) + 'assets/css/style.css'
        
    def getTemplatePath(self, component):
        return self.getRootPath(component) + 'site/templates/%s.php' % component.name
    
    def getCmsPath(self):
        return self.getRootPath() + 'panel/defaults/blueprints/%.php'

    #   B L O C K
    
    def snippet(self, component, name):
        u"""Allows inheriting (PHP) classes to save the block code to another snippet file,
        by redefining this method. Default behavior is to do nothing"""
        self.tabs()
        self.text(component.adapter.getSnippet(name))
        self.pushResult(name=name) # Divert the output, so we can save the block content in the snippet file.
        
    def _snippet(self, component):
        u"""Store the snippet block content in the snippet file."""
        name, block = self.popNameResult()
        print name, block
