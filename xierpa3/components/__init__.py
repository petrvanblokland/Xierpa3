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
from component import Component
from text import Text
from title import Title
from header import Header
from footer import Footer
from container import Container
from column import Column
from group import Group, ItemGroup # Group of floating rows
from menu import Menu
from logo import Logo
from page import Page
from article import Article, ArticleSideBar
from sidebar import Sidebar
from navigation import Navigation, MobileNavigation
from tagcloud import TagCloud
from message import Message
from theme import Theme
from ruler import Ruler
from socialmedia import SocialMedia
from documentation import Documentation
from nothing import Nothing # Place holder component doing nothing. Can be used for debugging.
# Featured components
from featured.featuredbyimage import FeaturedByImage
from featured.featuredbytext import FeaturedByText
from featured.featuredbydiaptext import FeaturedByDiapText

# Deprecated. Used featured.Featured instead
#from featured import FeaturedByImage, FeaturedByImageList, FeaturedByDiapText, FeaturedByText, FeaturedByTextList
