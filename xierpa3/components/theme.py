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
# Default builders for the standard Theme class.
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.builders.cssbuilder import CssBuilder

class Theme(Component):

    TITLE = 'Redefine cls.TITLE in inheriting theme class.'
    CLS_BUILDER = HtmlBuilder

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
        for urlName in builder.e.form.keys():
            urlNames.add(urllib.unquote(urlName).replace(' ', ''))
        for component in self.components:
            if component.template in urlNames or component.name in urlNames:
                return component

        # Could not find a match, answer the default template.
        return self.getComponent(C.TEMPLATE_DEFAULT)

    def getTemplates(self):
        u"""Answer the list of templates of this theme."""
        return self.components
            
    def getBuilder(self, path):
        u"""Answer the builder instance that fits the extension of this url request.
        <b>CssBuilder</b> and <b>self.CLS_BUILDER</b> intstances."""
        if path.endswith('.css'):
            return CssBuilder(self)
        # Answer the instance of the default builder for this theme.
        # Can be changed by inheriting classes.
        return self.CLS_BUILDER(self) 

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

if __name__ == "__main2__":

    from xierpa3.builders.htmlbuilder import HtmlBuilder
    from xierpa3.builders.sassbuilder import SassBuilder
    from xierpa3.descriptors.style import Style
    from xierpa3.components import *
    # Define general page descriptors
    style = Style(layout='responsive') # Default behavior
    style.fontfamily = 'Verdana'
    style.fontsize = '1em'
    style.addMedia(max=500, backgroundcolor='yellow', fontfamily='Verdana', fontweight='bold')
    style.addMedia(min=500, max=700, backgroundcolor='orange', fontfamily='Georgia')
    style.addMedia(min=700, color='green', fontfamily='Verdana')
    style.addStyle('body', backgroundcolor='yellow')
    # Define page components
    sidebar = Sidebar(name='TheSidebar', components=(
        Ruler(size=20, color='red'),
        Header(Text('Sidebar header'), fontsize=24),
        Navigation(backgroundcolor='#E0E0E0', type='menu'),
        TagCloud(),
        ), id='sidebar', width='38%', float='left'
    )
    main = Group(components=(
        Header(Text('Header of the page', fontsize=50, color='red')),
        Article(Text('This is a text. ' * 40)),
        Header(Text('Another header')),
        Article(Text('This is another text. ' * 20)),
        ), id='main', width='60%', float='left'
    )
    contact = Group(components=(
        Header(Text('Contact', fontsize=50), name='Contact'))
    )
    components = (
        Page(name='index', components=(main, sidebar), style=style),
        Page(name='contact', components=(contact, sidebar), style=style)
    )
    t = Theme(components)
    hb = HtmlBuilder()
    for page in t.pages:
        page.build(hb) # Clear the builder and build the HTML for page
        hb.save('/Library/WebServer/Documents/xierpa3/%s.html' % page.name)
        print hb.getResult()
        print
        print

    sb = SassBuilder()
    t.build(sb)
    sb.save('/Library/WebServer/Documents/xierpa3/style.scss')
    print sb.getResult()

