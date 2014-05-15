# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#    ruler.py
#
from xierpa3.components.component import Component

class Ruler(Component):

    def buildBlock(self, builder):
        # Generic builder for all components. To be redefined by inheriting class.
        builder.hr(**self.__dict__)
