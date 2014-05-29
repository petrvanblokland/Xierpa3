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
from xierpa3.descriptors.blueprint import BluePrint

class Page(Component):
    u"""The <b>Page</b> component builds the content of a single page, dependent on
    the parameters in the url."""
    
    CC = Component # Access constants through parent class.
    
    BLUEPRINT = BluePrint(
        name='Untitled', doc_name=u'Name of the page.',
        class_=CC.CLASS_PAGE, doc_pageClass=u'Class of the page. Defailt = CLASS_PAGE', 
    )
    def reset(self):
        u"""Gets called prior to every page build. Can be redefined by inheriting theme classes.
        Default behavior is to do nothing."""
        pass

    def block(self, b):
        s = self.style
        b.div(class_=s.class_ or s.name or self.class_ or self.name)
        b.comment(self.name)
        
    def _block(self, b):
        s = self.style
        b._div(comment=s.class_ or s.name or self.class_ or self.name) # End comment is automatic.
        
    def buildBlock(self, b):
        u"""
        Make the <i>builder</i> open the page and open the block. Then call the builder for all enclosed components. Make
        the <i>builder</i> close the block and close the page.
        """
        b.page(self)
        for component in self.components:
            component.build(b) # Dispatch the type of building to be done here.
        b._page(self)
