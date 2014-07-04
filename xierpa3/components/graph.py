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
#    graph.py
#
from xierpa3.components.component import Component
from xierpa3.toolbox.transformer import TX 
from xierpa3.descriptors.blueprint import BluePrint
from xierpa3.attributes import Perc

class Graph(Component):

    BLUEPRINT = BluePrint(
        # Layout stuff
    )
    def buildBlock(self, b):
        colClass = TX.col2Class('graph')
        s = self.style
        b.block(self)
        b.div(class_=colClass, float=s.graphFloat or self.LEFT, width=s.graphWidth or Perc(100))
        b._div(comment=colClass)
        b._block(self)
