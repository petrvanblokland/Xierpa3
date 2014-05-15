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
#   cssbuilder.py
#
import os
from xierpa3.builders.sassbuilder import SassBuilder
from xierpa3.toolbox.transformer import TX

class CssBuilder(SassBuilder):
    u"""
    Used for dispatching component.build_sass, if components want to define builder dependent behavior.
    """
    ID = 'css'
    ATTR_POSTFIX = ID # Postfix of dispatcher and attribute names above generic names.

    # Compile by Sass, style is defined by /css-<styleType>
    def initialize(self):
        SassBuilder.initialize(self)
        self.css = None

    def save(self, cssPath=None, scssPath=None, styleType=None):
        u"""
        Style type is one of ['nested', 'expanded', 'compact', 'compressed'].
        Given by self.e.form['css'].
        """
        if self.e is not None: # Is there a server environment, then overwrite the style type.
            styleType = self.e.form[self.PARAM_CSS] or styleType
        if not styleType in self.SASS_STYLES:
            styleType = self.SASS_DEFAULTSTYLE
        if cssPath is None:
            cssPath = '/tmp/style.css'
        if scssPath is None:
            scssPath = cssPath.replace('.css', '.scss')
        SassBuilder.save(self, scssPath)
        os.system('sass --trace %s %s --style %s' % (scssPath, cssPath, styleType))
        f = open(cssPath, 'r')
        self.css = f.read()
        f.close()

    def getResult(self):
        if self.css is not None:
            return self.css
        return self.popResult()
