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
#    featuredbase.py
#
from xierpa3.components.column import Column

class FeaturedBase(Column):
    u"""Abstract class that combines functionality for inheriting Featured classes."""
    
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Column.C 

    CLASS_FEATURED_ITEM = 'featuredItem'
    CLASS_FEATURED_ITEM_IMG = 'featuredItemImg'
      
    def buildColumn(self, b):
        u"""Get the featured article and build the feature, depending on the type of inheriting class.
        The selectors @start@ and @count@ define which and how many articles are selected."""
        s = self.style
        # articles.items list contains the selected articles in the right order.
        # Omit the current article in the selection.
        articles = self.adapter.getArticles(start=s.start, count=s.count, omit=b.getCurrentArticleId())
        self.buildFeatured(b, articles)
   
