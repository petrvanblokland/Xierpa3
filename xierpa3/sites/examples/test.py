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
import os
from xierpa3.attributes import *
from xierpa3.components import *
from xierpa3.adapters.blurbadapter import BlurbAdapter
from xierpa3.descriptors.style import Style, StyleSet

class Test(Theme):
    # TODO
    #
    #
    TITLE = 'Title of the test site'

    def initialize(self):
        self.adapter = BlurbAdapter()

    def baseStyle(self):
        s = StyleSet() # Style set as root with invisible selectors
        m = s.addStyle('body', fontfamily='Verdana', fontsize=100, backgroundcolor='black')
        # m.addMedia(max=700, fontsize=48, backgroundcolor='yellow')
        return s

    def baseComponents(self):
        group = Group(components=Text('This is a text'), prefix='aaaa', width='60%',
            float='left', backgroundcolor='gray', margin=Margin(20))
        group.addMedia(max=700, float='none', width='40%', margin=Margin(0, 'auto'))

        # Home page: Main = Grid of thumbnails + Sidebar
        homePage = Page(name='index', components=group, color='yellow')
        homePage.addMedia(max=700, color='red', backgroundcolor='yellow')
        return [homePage]


