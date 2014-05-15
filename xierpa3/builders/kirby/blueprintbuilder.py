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
#   blueprintbuilder.py
#
from xierpa3.builders.builder import Builder
from xierpa3.constants.constants import C
from xierpa3.toolbox.transformer import TX

class BluePrintBuilder(Builder, C):
    u"""
    """
    ID = 'blueprint'

    def page(self, component):
        pass
    
    def _page(self, component):
        pass