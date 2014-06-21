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
#    typo2014demo2.py
#
from xierpa3.sites import typo2014
from xierpa3.themes.blog.base import BaseBlog
from xierpa3.adapters.fileadapter import FileAdapter
from xierpa3.components import Logo, Menu, SocialMedia, Header, MobileNavigation, Footer, Page
from xierpa3.constants.constants import C
from xierpa3.toolbox.transformer import TX

# Adapter

class Typo2014Adapter(FileAdapter):
    pass

# Cache the adapter, initialized automatic.
#ADAPTER = Typo2014Adapter(root=TX.module2Path(typo2014) + '/files/articles')
    
class Typo2014(BaseBlog):
    u"""The <b>Blog</b> class implements the standard example show with content based on files."""
    TITLE = 'Typo 2014'
    SUBTITLE = 'Roots'

    SRCLOGO = 'http://data.xierpa.com.s3.amazonaws.com/_images/examples/typo2014.png'
   
    def baseComponents(self):
        logo = Logo(logoName='Type 2014', hoverColor='#888') # logoSrc=self.SRCLOGO
        menu = Menu()
        socialmedia = SocialMedia(twitterAccount='typo2014', facebookAccount='typo2014') 

        title = self.TITLE + ': ' + self.SUBTITLE
        header = Header(components=(logo,menu, socialmedia), mobileContainerDisplay=self.NONE)
        mobileNavigation = MobileNavigation(title=title) # Is container by itself. Change??
        footer = Footer(components=(menu,))
        
        homePage = Page(name=self.TEMPLATE_INDEX,
            components=(mobileNavigation, header, footer),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, favicon=self.URL_FAVICON)

        return [homePage]
