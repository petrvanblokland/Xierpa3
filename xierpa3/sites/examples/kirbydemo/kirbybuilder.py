# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     xierpa server
#     Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#
#     X I E R P A  3
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   phpbuilder.py
#
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.constants.constants import C
from xierpa3.toolbox.stack import Stack

class KirbyBuilder(HtmlBuilder):
    
    def theme(self, component):
        pass
    
    def _theme(self, component):
        pass
    
    def page(self, component):
        ad = component.adapter
        self.clear() # Clear the output stream for next theme page
        self.text(ad.snippet('header'))        
        self.text(ad.snippet('navigation'))
        
    def _page(self, component):
        ad = component.adapter
        self.newline()
        self.text(ad.snippet('footer'))