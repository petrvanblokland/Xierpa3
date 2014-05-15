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
#    typo2014demo.py
#
from xierpa3.themes.blog.base import BaseBlog
from xierpa3.components import Logo, Menu, SocialMedia, Header
from xierpa3.components import MobileNavigation, Footer, Page
from xierpa3.constants.constants import C
from xierpa3.toolbox.transformer import TX
from xierpa3.adapters.fileadapter import FileAdapter
from xierpa3.sites import typo2014

# Adapter
class Typo2014Adapter(FileAdapter):
    pass

class Typo2014(BaseBlog):
    TITLE = 'Typo2014'
    SUBTITLE = 'Roots.'

    SRCLOGO = 'http://data.xierpa.com.s3.amazonaws.com/_images/examples/typo2014.png'

    # Cache the adapter, initialized automatic.
    ADAPTER = Typo2014Adapter(root=TX.module2Path(typo2014) + '/files/articles')
   
    def baseComponents(self):
        logo = Logo(logoSrc=self.SRCLOGO)
        menu = Menu()
        socialmedia = SocialMedia(twitterAccount='typo2014', facebookAccount='typo2014') 

        header = Header(components=(logo,menu, socialmedia), mobileContainerDisplay=C.NONE)
        mobileNavigation = MobileNavigation() # Is container by itself. Change??
        footer = Footer(components=(menu,))
        
        homePage = Page(name=C.TEMPLATE_INDEX,
            components=(mobileNavigation, header, footer),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, favicon=self.URL_FAVICON)

        return [homePage]
