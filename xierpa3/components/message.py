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
#    message.py
#
from xierpa3.components.component import Component

class Message(Component):

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Component.C 
          
    def buildBlock(self, builder):
        builder.block(self)
        for component in builder.adapter.get(self.C.ADAPTER_MESSAGE):
            component.build(builder)
        builder._block(self)
