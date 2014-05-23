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
#    theme.py
#
import urllib
from xierpa3.components.component import Component
from xierpa3.constants.constants import C

class Theme(Component):

    TITLE = 'Redefine cls.TITLE in inheriting theme class.'

    def reset(self):
        u"""Gets called prior to every page render. Can be redefined by inheriting theme classes.
        Default behavior is to do nothing."""
        pass

    def getMatchingTemplate(self, builder):
        u"""
        Find the page template in self.components that has the best name match with currently available parameters in
        <b>self.e.form</b>. Unquote the url parameters and remove the spaces to create potential template names.
        Then match them against the available template components of <b>self</b>. 
        """
        urlNames = set()
        for urlName in builder.getParamNames():
            urlNames.add(urllib.unquote(urlName).replace(' ', ''))
        for component in self.components:
            if component.template in urlNames or component.name in urlNames:
                return component

        # Could not find a match, answer the default template.
        # If no default component exists, then answer self. 
        # This happens if there is only one page in the site.
        return self.getComponent(C.TEMPLATE_DEFAULT) or self

    def getTemplates(self):
        u"""Answer the list of templates of this theme."""
        return self.components
            
    def buildBlock(self, builder):
        u"""Build the current page of this theme."""
        builder.theme(self) # Make the builder open the site.
        for component in self.components:
            component.build(builder) # Make all components of the theme build themselves.
        builder._theme(self) # Make the builder close the site.

    def handlePost(self):
        pass

    def getClassName(self):
        return None # Selector does not show, just the style block.

