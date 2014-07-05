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
#    navigation.py
#
from xierpa3.components.component import Component
from xierpa3.descriptors.blueprint import BluePrint

class TagCloud(Component):

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Component.C 
  
    BLUEPRINT = BluePrint( 
    )
    def initialize(self):
        # Generic builder for all components. To be redefined by inheriting class.
        components = self.components # Replace by linked components
        self.components = []
        #for component in components:
        #    link = Link(component, fontsize=component.style.emphasis)
        #    self.addComponents(link)
    
    
