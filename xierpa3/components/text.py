# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#    text.py
#
from xierpa3.components.component import Component

class Text(Component):
    def __init__(self, text=None, style=None, id=None, parent=None, 
            class_=None, type=None, contentID=None, editable=False, **kwargs):
        Component.__init__(self, style=style, id=id, parent=parent,
            class_=class_, type=type, contentID=None, editable=editable, **kwargs)
        if isinstance(text, dict):
            # In case text is a dict, add the attributes to style. 
            for key, value in text.items():
                if key != 'text':
                    self.style[key] = value
            text = text.get('text') or ''
        elif not text:
            text = '[Default text]'
        assert isinstance(text, basestring)
        self.text = text

    def buildBlock(self, builder):
        # Text builder does not have separate open and close block. 
        if self.text is not None:
            builder.text(self)
        elif self.contentID is not None:
            # In case of adapter content, use these.
            for component in self.readAdapterContent():
                component.build(builder)
        
    # self.text     Collect all text from the component nodes
    
    def _get_text(self):
        return self._text
    
    def _set_text(self, text):
        self._text = text
        
    text = property(_get_text, _set_text)
    
