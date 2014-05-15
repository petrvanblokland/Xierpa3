# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#    graph.py
#
from xierpa3.components.component import Component
from xierpa3.descriptors.style import Style
from xierpa3.constants.constants import C
from xierpa3.toolbox.transformer import TX 
from xierpa3.attributes import *
from xierpa3.descriptors.style import Media

class Graph(Component):

    STYLE_DEFAULT = dict(
        # Layout stuff
    )
    def buildBlock(self, b):
        s = self.style
        b.block(self)
        b.div(class_='graph', float=s.graphFloat or C.LEFT, width=s.graphWidth or C.C100)
        b._div(comment=colClass)
        b._block(self)
