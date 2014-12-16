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
    u"""The **Page** component builds the content of a single page, dependent on
    the parameters in the url."""
    
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Component.C
    
    BLUEPRINT = BluePrint(
        name='Untitled', doc_name=u'Name of the page.',
        class_=C.CLASS_PAGE, doc_pageClass=u'Class of the page. Default is the result of **self.getClassName()** or C.CLASS_PAGE', 
    )
    def reset(self):
        u"""Gets called prior to every page build. Can be redefined by inheriting theme classes.
        Default behavior is to do nothing."""
        pass

    def buildBlock(self, b):
        u"""
        Make the builder <i>b</i> open the page and open the block. Then call the builder 
        for all enclosed components. Make the builder <i>b</i> close the block and close the page.
        """
        b.page(self)
        for component in self.components:
            component.build(b) # Dispatch the type of building to be done here.
        # Allow the components to build the JavaScript they need.
        for component in self.components:
            component.buildJS(b)
        b._page(self)
