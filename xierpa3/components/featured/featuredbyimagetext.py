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
#    featuredbyimage.py
#
from random import choice
from featuredbase import FeaturedBase
from xierpa3.descriptors.media import Media
from xierpa3.attributes import Em, Perc, Color, Padding
from xierpa3.descriptors.blueprint import BluePrint

class FeaturedByImageText(FeaturedBase):
    u"""The @FeaturedByImageText@ feature component, shows a featured article by its poster image
    with the text column on the side..
    If there is no poster image defined in the article meta data, then the first image in the article
    is used here. The image is a link to the article page.
    Respectively the binary flags @BluePrint@ *showLevel*, *showTitle* and *showTopic* 
    will enable the level of the article (as defined in the article source @$level@), 
    the article title (@$title@) and topic (@$topic), of set to @True@."""
    # Get Constants->Config as class variable, so inheriting classes can redefine values.

    C = FeaturedBase.C 

    LEVELSIZE = Em(0.9)
    AUTHORSIZE = Em(1.2)
    CATEGORYSIZE = Em(1.4)
    AUTHORCOLOR = Color('#828487')
    CATEGORYCOLOR = AUTHORCOLOR
    LABELCOLOR = AUTHORCOLOR
    NAMECOLOR= Color('#66696C')
    SUMMARYCOLOR= Color('#202020')

    BLUEPRINT = BluePrint(FeaturedBase.BLUEPRINT,
        # Layout selection parameters.
        showPoster=True, doc_showPoster=u'Boolean flag to indicate if the poster of the article should be shown.',
        showLevel=False, doc_showLevel=u'Boolean flag to show the level field of the article.',
        showTitle=True, doc_showTitle=u'Boolean flag to show the title of the article.',
        showHeadline=True, doc_showHeadline=u'Boolean flag to show the headline of the article.',
        showTopic=True, doc_showTopic=u'Boolean flag to show the topic of the article.',

        # Selection stuff
        start=0, doc_start=u'Index of first selected item to feature.',
        count=3, doc_count=u'Number of selected items to feature.',
        # Container component layout stuff
        width=Perc(30), doc_width=u'Overall width of the component.',
        widthMobile=Perc(100), doc_widthMobile=u'Overall width of the component for mobile.',
        backgroundColor=None, doc_backgroundColor=u'Background color of the component.',
        display=C.BLOCK, doc_display=u'Display status of the component',
        displayMobile=C.BLOCK, doc_displayMobile=u'Display status of the component for mobile.',
        float=C.LEFT, doc_float=u'Float status of the component.',
        floatMobile=C.LEFT, doc_floatMobile=u'Float status of the component for mobile.',
        padding=0, doc_padding=u'Padding of the component content.',
        # Item/article stuff
        itemDisplay=C.BLOCK, doc_itemDisplay=u'Display type of the item/article image cell.',
        itemBackgroundColor=Color('#E0E0E0'), doc_itemBackgroundColor=u'Background color of the item/article image cell.',
        itemClear=C.NONE, doc_itemClear=u'Floating clear of item/article image cell.',
        itemMarginBottom=Em(0.5), doc_itemMarginBottom=u'Margin bottom of item/article image cell.',
        itemPadding=Padding(Em(0.5)), doc_itemPadding=u'Padding of the item/article image cell.',
        # Level
        levelFormat='%s level', doc_levelFormat=u'Python string pattern as level indicator. Takes level string as parameter.',
        genericLevel=None, doc_genericLevel=u'Generic level flag, overruling the article level field.',
        levelColor=Color('#222'), doc_levelColor=u'Color of the level indicator.',
        levelSize=Em(0.8), doc_levelSize=u'Font size of the level indicator.',
        levelWeight=C.BOLD, doc_levelWeight=u'Font weight of the level indicator.',
        levelMarginTop=Em(0.2), doc_levelMarginTop=u'Margin top of the level indicator.',
        levelMarginBottom=Em(0.2), doc_levelMarginBottom=u'Margin bottom of the level indicator.',
        # Title
        titleFontFamily=None, doc_titleFontFamily=u'Font family of the article title.',
        titleColor=('#444'), doc_titleColor=u'Color of the article title.',
        titleSize=Em(1.1), doc_titleSize=u'Font size of the article title.',
        titleWeight=C.NORMAL, doc_titleWeight=u'Font weight of the article title.',
        titleLineHeight=Em(1.2), doc_titleLineHeight=u'Line height of the article title.',
        # Headline
        headlinePaddingTop=Em(0.1), doc_headlinePaddingTop=u'Padding between image and headline.',
        headlineFontFamily=None, doc_headlineFontFamily=u'Font family of the article headline.',
        headlineColor=('#444'), doc_headlineColor=u'Color of the article headline.',
        headlineSize=Em(1.8), doc_headlineSize=u'Font size of the article headline.',
        headlineWeight=C.NORMAL, doc_headlineWeight=u'Font weight of the article headline.',
        headlineLineHeight=Em(1.2), doc_headlineLineHeight=u'Line height of the article headline.',
        # Topic
        topicColor=Color('#444'), doc_topicColor=u'Color of the article topic.',
        topicSize=Em(0.8), doc_topicSize=u'Font size of the article topic.',
        topicWeight=C.NORMAL, doc_topicWeight=u'Font weight of the article topic.',
        topicLineHeight=Em(1.2), doc_topicLineHeight=u'Line height of the article topic.',
    )
    def buildFeatured(self, b, articles):
        s = self.style
        b.div(class_=self.getClassName(), width=s.width, backgroundcolor=s.backgroundColor,
            display=s.display, float=s.float, padding=s.padding,
            media=Media(max=self.C.M_MOBILE_MAX, width=s.widthMobile,
                display=s.displayMobile, float=s.floatMobile),
        )
        for article in articles.items:
            if s.showPoster and article.poster:
                self.buildFeaturedImage(b, article)
        b._div()
        
    def buildFeaturedImage(self, b, article):
        s = self.style
        b.div(class_=self.C.CLASS_FEATUREDITEM, display=s.itemDisplay,
            backgroundcolor=s.itemBackgroundColor, padding=s.itemPadding,
            clear=s.itemClear, marginbottom=s.itemMarginBottom, margintop=s.itemMarginTop,
        )
        b.a(href='/%s-%s' % (self.C.PARAM_ARTICLE, article.id))
        b.img(class_=(self.C.CLASS_AUTOWIDTH, 'featuredImage'), src=article.poster)
        if s.showLevel or s.genericLevel:
            # Format the level indicator
            b.h5(class_=self.C.CLASS_LEVEL, color=s.levelColor, fontsize=s.levelSize,
                fontweight=s.levelWeight,
                margintop=s.levelMarginTop, marginbottom=s.levelMarginBottom)
            b.text(s.levelFormat % (article.level or s.genericLevel))
            b._h5()
        if s.showTitle and article.title:
            # Format the article title
            b.h4(class_=self.C.CLASS_TITLE, fontfamily=s.titleFontFamily, color=s.titleColor,
                 fontsize=s.titleSize, fontweight=s.titleWeight, lineheight=s.titleLineHeight)
            b.text(article.title)
            b._h4()
        if s.showHeadline and article.headline:
            # Format the article headline
            b.h4(class_=self.C.CLASS_HEADLINE, fontfamily=s.headlineFontFamily, color=s.headlineColor,
                 fontsize=s.headlineSize, fontweight=s.headlineWeight, lineheight=s.headlineLineHeight,
                 paddingtop=s.headlinePaddingTop)
            b.text(article.headline)
            b._h4()
        if s.showTopic and article.topic is not None: # Elements must be defined in global style
            b.h5(class_=self.C.CLASS_TOPIC, color=s.topicColor, fontsize=s.topicSize,
                 fontweight=s.topicWeight, lineheight=s.topicLineHeight)
            if isinstance(article.topic, basestring):
                b.text(article.topic)
            else:
                self.buildElement(b, article.topic)
            b._h5()
        b._a()
        b._div(comment=self.C.CLASS_FEATUREDITEM)
