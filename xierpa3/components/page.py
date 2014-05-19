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
#    page.py
#
from xierpa3.components.component import Component

class Page(Component):

    def reset(self):
        u"""Gets called prior to every page render. Can be redefined by inheriting theme classes.
        Default behavior is to do nothing."""
        pass

    def block(self, b):
        b.div(class_=self.class_ or self.name) # @@@@ Page?
        b.comment(self.name)
        
    def _block(self, b):
        b._div(comment=self.name) # End comment is automatic.
        
    def buildBlock(self, b):
        u"""
        Make the <i>builder</i> open the page and open the block. Then call the builder for all enclosed components. Make
        the <i>builder</i> close the block and close the page.
        """
        b.page(self)
        for component in self.components:
            component.build(b) # Dispatch the type of building to be done here.
        b._page(self)
