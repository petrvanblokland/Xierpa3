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
from xierpa3.toolbox.transformer import TX 
from xierpa3.constants.constants import C

class Message(Component):
            
    def buildBlock(self, builder):
        builder.block(self)
        for component in self.getAdapterComponents(C.ADAPTER_MESSAGE):
            component.build(builder)
        builder._block(self)
