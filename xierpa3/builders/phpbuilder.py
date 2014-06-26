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
#   phpbuilder.py
#
#   Following standard
#   https://google-styleguide.googlecode.com/svn/trunk/htmlcssguide.xml
#
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.constants.constants import C
from xierpa3.toolbox.transformer import TX

class PhpBuilder(HtmlBuilder):
    u"""
    """
    # Used for dispatching component.build_sass, and builder.isType('html'),
    # for components that want to define builder dependent behavior. In normal
    # processing of a page, this should never happen. But it can be used to
    # select specific parts of code that should not be interpreted by other builders.
    ID = C.TYPE_PHP # Also the default extension of the output format.
    EXTENSION = ID
    ATTR_POSTFIX = ID # Postfix of dispatcher and attribute names above generic names.

  