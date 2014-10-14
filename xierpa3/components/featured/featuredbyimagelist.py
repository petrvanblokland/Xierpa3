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
#    featuredbyimagelist.py
#
from featuredbase import FeaturedBase
from xierpa3.attributes import Em, Perc, Color
from xierpa3.descriptors.blueprint import BluePrint

class FeaturedByImageList(FeaturedBase):
    u"""The *FeaturedByImageList* feature component builds a vertical list if thumbnails,
    level and optional names of the selected article items."""
    # Get Constants->Config as class variable, so inheriting classes can redefine values.

    C = FeaturedBase.C

    LEVELSIZE = Em(0.9)
    LEVELCOLOR= Color('#6294D0')
    NAMECOLOR = Color('#A32C2D')

    BLUEPRINT = BluePrint(FeaturedBase.BLUEPRINT,
        showLevel=False, doc_showLevel=u'Boolean flag to show the level field of the article.',
        showName=False, doc_showName=u'Boolean flag to show the name field of the article.',
        showTopic=True, doc_showTopic=u'Boolean flag to show the topic of the article.',

        # Selection stuff
        start=0, doc_start=u'Index of first selected item to feature.',
        count=3, doc_count=u'Number of selected items to feature.',
        # Col block stuff
        colDisplay=C.BLOCK, doc_colDisplay=u'Column display type.',
        colClear=C.BOTH, doc_colClear='Column float clear.',
        colMarginBottom=Em(0.5), doc_colMarginBottom='Column margin bottom.',
        colColor=None, doc_colColor=u'Column color',
        colMarginRight=Perc(1.8), doc_colMarginLeft=u'Column margin left.',
        colMarginLeft=0,
        colFloat=C.LEFT,
        colMinHeight=1,
        # Layout stuff
        colWidth=4, doc_colWidth=u'Default amount of columns for this component.',
        # Item stuff
        itemClear=C.NONE,
        itemDisplay=C.LEFT,
        itemWidth=Perc(55),
        # Thumbnail image stuff
        thumbDisplay=C.BLOCK,
        # Level stuff, handle local fontsize and lineheight here, related to the item size
        genericLevel='Generic', doc_genericLevel=u'Show this generic level name if level attitbute is undefined in adapter data.',
        levelColor=Color(LEVELCOLOR), doc_levelColor=u'Level color.',
        levelSize=LEVELSIZE, doc_levelSize=u'Level font size.',
        levelWeight=C.BOLD, doc_levelWeight=u'Level font weight.',
        levelMarginTop=Em(0.5), doc_levelMarginTop=u'Level margin top.',
        # Optional name stuff, handle local fontsize and lineheight here, related to the item sizes
        nameColor=Color(NAMECOLOR),
        nameSize=Em(0.9),
        nameLineHeight=Em(1.2),
        nameWeight=C.BOLD,
        # Mobile stuff
        mobileDisplay=C.NONE,
        mobilePaddingTop=Em(2), mobilePaddingBottom=Em(0.5), mobilePaddingLeft=Em(0.5), mobilePaddingRight=Em(0.5),
        mobileMarginTop=Em(2), mobileMarginBottom=Em(0.5), mobileMarginLeft=Em(0.5), mobileMarginRight=Em(0.5),
        mobileFloat=C.NONE, mobileWidth=C.AUTO,
    )

    def buildFeatured(self, b, articles):
        s = self.style
        for article in articles.items:
            if not article.poster:
                continue # Only show articles that have some kind of poster image.
            b.div(class_=self.CLASS_FEATURED_ITEM, display=s.itemDisplay,
                clear=s.itemClear, marginbottom=s.itemMarginBottom, width=s.itemWidth,
            )
            b.a(href='/%s-%s' % (self.C.PARAM_ARTICLE, article.id))
            if s.showLevel:
                b.h5(color=s.levelColor, fontsize=s.levelSize, fontweight=s.levelWeight,
                    margintop=s.levelMarginTop)
                b.text(article.level or s.genericLevel)
                b.text(' level')
                b._h5()
            b.img(class_=self.C.CLASS_AUTOWIDTH, src=article.poster)
            if s.showName:
                b.h4(color=s.nameColor, fontsize=s.nameSize, fontweight=s.nameWeight,
                     lineheight=s.nameLineHeight)
                b.text(article.name)
                b._h4()
            if s.showTopic and article.topic is not None: # Elements must be defined in global style
                self.buildElement(b, article.topic)
            b._a()
            if b.e.form[self.C.PARAM_DEBUG]:
                b.text(`article`)
            b._div(comment=self.CLASS_FEATURED_ITEM)
