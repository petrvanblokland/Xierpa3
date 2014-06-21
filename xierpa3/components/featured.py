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
#    featured.py
#
from random import choice
from xierpa3.components.column import Column
from xierpa3.components.container import Container
from xierpa3.descriptors.media import Media
from xierpa3.attributes import Em, Margin, Perc, Color
from xierpa3.constants.constants import C
from xierpa3.descriptors.blueprint import BluePrint

LEVELSIZE = Em(0.9)
AUTHORSIZE = Em(1.2)
CATEGORYSIZE = Em(1.4)
AUTHORCOLOR = Color('#828487')
CATEGORYCOLOR = AUTHORCOLOR
LABELCOLOR = AUTHORCOLOR
NAMECOLOR= Color('#66696C')
SUMMARYCOLOR= Color('#202020')

class Featured(Container):
    pass

class FeaturedBase(Column):

    CLASS_FEATURED_ITEM = 'featuredItem'
    CLASS_FEATURED_ITEM_IMG = 'featuredItemImg'
      
    def buildColumn(self, b):
        s = self.style
        data = b.adapter.get(self.ADAPTER_FEATUREDARTICLES, id=b.getCurrentArticleId() or self.ID_HOME, 
            start=s.itemStart, count=s.itemCount)
        self.buildFeatured(b, data)
   
class FeaturedByImage(FeaturedBase):
    u"""The <b>FeaturedByImage</b> feature component, shows a featured article by its poster image.
    If there is no poster image defined in the article meta data, then the first image in the article
    is used here. The image is a link to the article page."""
    BLUEPRINT = BluePrint(FeaturedBase.BLUEPRINT, 
        # Selection stuff
        itemStart=0, doc_itemStart=u'Index of first selected item to feature.',
        itemCount=24, doc_itemCount=u'Number of selected items to feature.',
        # Col layout stuff
        colWidth=8, doc_colWidth=u'Default amount of columns for this component.',
        colMarginRight=Perc(1.8), doc_colMarginRight=u'Div.col margin right.',
        colMarginLeft=0, doc_colMarginLeft=u'Div.col margin left.',
        colFloat=C.LEFT, doc_colFloat=u'Div.col float',
        colMinHeight=1, doc_colMinHeight=u'Div.col minimal height.',
        colDisplay=C.BLOCK, doc_colDisplay=u'Div.col display type.',
        # Mobile stuff
        mobileDisplay=C.NONE,
        mobilePaddingTop=Em(2), 
        mobilePaddingBottom=Em(0.5), 
        mobilePaddingLeft=Em(0.5), 
        mobilePaddingRight=Em(0.5),
        mobileMarginTop=Em(2), 
        mobileMarginBottom=Em(0.5), 
        mobileMarginLeft=Em(0.5), 
        mobileMarginRight=Em(0.5),
        mobileFloat=C.NONE, 
        mobileWidth=C.AUTO,
    )
    def buildFeatured(self, b, data):
        s = self.style
        if s.itemStart < len(data.items):
            item = data.items[s.itemStart]
            b.div(class_=self.CLASS_FEATURED_ITEM, display=s.itemDisplay,
                clear=s.itemClear, marginbottom=s.itemMarginBottom, width=s.itemWidth,
            )
            b.a(href='/%s-%s' % (self.PARAM_ARTICLE, item.id))
            b.img(class_=(self.CLASS_AUTOWIDTH, 'featuredImage'), src=item.poster)
            if s.showLevel:
                b.h5(color=s.levelColor, fontsize=s.levelSize, fontweight=s.levelWeight,
                    margintop=s.levelMarginTop)
                b.text(item.level or s.genericLevel)
                b.text(' level')
                b._h5()
            if s.showName:
                b.h4(color=s.nameColor, fontsize=s.nameSize, fontweight=s.nameWeight, 
                     lineheight=s.nameLineHeight)
                b.text(item.name)
                b._h4()
            if s.showTopic and item.topic is not None: # Elements must be defined in global style
                self.buildElement(b, item.topic)
            b._a()
            b._div(comment=self.CLASS_FEATURED_ITEM)
  
class FeaturedByImageList(FeaturedBase):
    u"""The <b>FeaturedByImageList</b> feature component builds a vertical list if thumbnails, 
    level and optional names of the selected article items."""
    BLUEPRINT = BluePrint(FeaturedBase.BLUEPRINT, 
        # Selection stuff
        itemStart=0, doc_itemStart=u'Index of first selected item to feature.', 
        itemCount=3, doc_itemCount=u'Number of selected items to feature.',
        # Col block stuff
        colDisplay=C.BLOCK, doc_colDisplay=u'Column display type.',
        colClear=C.BOTH, doc_colClear='Column float clear.',
        colMarginBottom=Em(0.5), doc_colMarginBottom='Column margin bottom.',
        colColor=None, doc_colColor=u'Column color',
        colMarginRight=Perc(1.8), 
        colMarginLeft=0, 
        colFloat=C.LEFT, 
        colMinHeight=1,  
        # Layout stuff
        colWidth=4, doc_colWidth=u'Default amount of columns for this component.',
        # Item stuff
        itemClear=C.NONE, itemDisplay=C.LEFT, itemWidth=Perc(55),
        # Thumbnail image stuff
        thumbDisplay=C.BLOCK,
        # Level stuff, handle local fontsize and lineheight here, related to the item size
        showLevel=True, 
        genericLevel='Generic', doc_genericLevel=u'Show this generic level name if level attitbute is undefined in adapter data.',
        levelColor=Color('#6294D0'), doc_levelColor=u'Level color.',
        levelSize=LEVELSIZE, doc_levelSize=u'Level font size.',
        levelWeight=C.BOLD, doc_levelWeight=u'Level font weight.',
        levelMarginTop=Em(0.5), doc_levelMarginTop=u'Level margin top.',
        # Optional name stuff, handle local fontsize and lineheight here, related to the item sizes
        showName=False, 
        nameColor=Color('#A32C2D'), 
        nameSize=Em(0.9), 
        nameLineHeight=Em(1.4), 
        nameWeight=C.BOLD,
        # Optional topic
        showTopic=False,
        # Mobile stuff
        mobileDisplay=C.NONE,
        mobilePaddingTop=Em(2), mobilePaddingBottom=Em(0.5), mobilePaddingLeft=Em(0.5), mobilePaddingRight=Em(0.5),
        mobileMarginTop=Em(2), mobileMarginBottom=Em(0.5), mobileMarginLeft=Em(0.5), mobileMarginRight=Em(0.5),
        mobileFloat=C.NONE, mobileWidth=C.AUTO,
    )
    
    def buildFeatured(self, b, data):
        s = self.style
        for item in data.items:
            b.div(class_=self.CLASS_FEATURED_ITEM, display=s.itemDisplay,
                clear=s.itemClear, marginbottom=s.itemMarginBottom, width=s.itemWidth,
            )
            b.a(href='/%s-%s' % (self.PARAM_ARTICLE, item.id))
            if s.showLevel:
                b.h5(color=s.levelColor, fontsize=s.levelSize, fontweight=s.levelWeight,
                    margintop=s.levelMarginTop)
                b.text(item.level or s.genericLevel)
                b.text(' level')
                b._h5()
            b.img(class_=self.CLASS_AUTOWIDTH, src=item.poster)
            if s.showName:
                b.h4(color=s.nameColor, fontsize=s.nameSize, fontweight=s.nameWeight, 
                     lineheight=s.nameLineHeight)
                b.text(item.name)
                b._h4()
            if s.showTopic and item.topic is not None: # Elements must be defined in global style
                self.buildElement(b, item.topic)
            b._a()
            b._div(comment=self.CLASS_FEATURED_ITEM)

class FeaturedByText(FeaturedBase):

    BLUEPRINT = BluePrint(FeaturedBase.BLUEPRINT, 
        # Selection stuff
        # Index of first and amount of selected features for this component
        itemStart=0, itemCount=1, itemRandom=True,
        # Label stuff '#828487'
        label=None, labelSize=Em(2), labelColor='red', labelMarginBottom=Em(0.5),
        labelMarginTop=Em(0.3), labelLineHeight=Em(1.4),
        # Poster
        showPoster=True, posterWidth='40%',
        # Layout stuff
        colWidth=8, # Default amount of columns for this component
        # Level stuff, handle local fontsize and lineheight here, related to the item size
        showLevel=True, genericLevel='Generic', # Show generic level if level is omitted in data.
        levelColor='#6294D0', levelSize=LEVELSIZE, levelLineHeight=Em(1.4),
        levelWeight=C.BOLD, levelMarginTop=Em(0.5),
        # Category stuff in h5
        showCategory=False, categoryColor=CATEGORYCOLOR, categorySize=CATEGORYSIZE, 
        categoryLineHeight=Em(1.2), categoryWeight=C.BOLD,
        # Name stuff in h2
        nameSize=Em(3.2), nameLineHeight=Em(1), nameWeight=None, # Default inheriting from the main weight.
        nameColor=NAMECOLOR, nameMarginBottom=Em(0.2), nameMarginTop=0,
        nameDisplay=C.BLOCK,
        # Author stuff in h6
        authorSize=AUTHORSIZE, 
        authorWeight=C.NORMAL, 
        authorColor=AUTHORCOLOR, doc_authorColor=u'Author name color.',
        authorDisplay=C.BLOCK, authorLineHeight=Em(1.4),
        # Summary stuff
        summaryColor=SUMMARYCOLOR, summarySize=Em(1.2), summaryLineHeight=Em(1.4),
        summaryMarginTop=Em(0.4), summaryMarginBottom=Em(0.5),
        # Mobile stuff
        mobileDisplay=C.NONE,
        mobilePaddingTop=Em(2), mobilePaddingBottom=Em(0.5), mobilePaddingLeft=Em(0.5), mobilePaddingRight=Em(0.5),
        mobileMarginTop=Em(2), mobileMarginBottom=Em(0.5), mobileMarginLeft=Em(0.5), mobileMarginRight=Em(0.5),
        mobileFloat=C.NONE, mobileWidth=C.AUTO,
    )
    
    def buildFeatured(self, b, data):
        u"""Build the featured item. If <b>self.style.itemRandom</b> is <b>True</b>, then select a random item from the list.
        If there is no <b>data.item</b> available, then ignore this method."""
        if not data.items:
            return
        s = self.style
        if s.itemRandom:
            item = choice(data.items)
        else:
            item = data.items[0]
        if s.label:
            b.h2(fontsize=s.labelSize, color=s.labelColor, margintop=s.labelMarginTop,
                marginbottom=s.labelMarginBottom, lineheight=s.labelLineHeight,
                media=(
                    Media(min=self.M_TABLET_MIN, max=self.M_TABLET_MAX, fontsize=s.tabletLabelSize, color='red'),
                    Media(max=self.M_MOBILE_MAX, color='blue')
                ))
            b.text(s.label)
            b._h2()
        b.a(href='/%s-%s' % (self.PARAM_ARTICLE, item.id), class_=self.CLASS_NAME)
        b.h2(fontsize=s.nameSize, fontweight=s.nameWeight, lineheight=s.nameLineHeight, 
             color=s.nameColor, marginbottom=s.nameMarginBottom, display=s.nameDisplay,
             margintop=s.nameMarginTop)
        b.text(item.name) 
        b._h2()
        b._a()
        if s.showPoster:
            b.a(href='/%s-%s' % (self.PARAM_ARTICLE, item.id), class_=self.CLASS_NAME)
            b.img(width=s.posterWidth, src=item.poster, float=self.LEFT, padding=0,
                margin=Margin(Em(0.5), Em(0.5), 0, 0),
                media=Media(max=self.M_MOBILE_MAX, display=self.NONE)
            )
            b._a()
        if s.showLevel:
            b.h5(class_=self.CLASS_LEVEL, color=s.levelColor, fontsize=s.levelSize, fontweight=s.levelWeight,
                margintop=s.levelMarginTop, lineheight=s.levelLineHeight)
            b.text(item.level or s.genericLevel)
            b.text(' level')
            b._h5()
        if item.author: # Test on text
            b.a(href='/%s-%s' % (self.PARAM_AUTHOR, item.author), class_=self.CLASS_AUTHOR)
            b.h5(fontsize=s.authorSize, fontweight=s.authorWeight, color=s.authorColor, 
                 lineheight=s.authorLineHeight, display=s.authorDisplay)
            b.text('By %s' % item.author)
            b._h5()
            b._a()
        if s.showCategory and item.category: # Text on text
            b.a(href='/%s-%s' % (self.PARAM_CATEGORY, item.category), class_=self.CLASS_CATEGORY)
            b.h5(fontsize=s.categorySize, fontweight=s.categoryWeight, lineheight=s.categoryLineHeight, 
                 color=s.categoryColor, margintop=Em(1), display=self.BLOCK)
            b.text(item.category)
            b._h5()
            b._a()
        if item.summary is not None: # Test on element. Summary elements tag must be defined by generic style.
            b.div(class_='featuredSummary', clear=self.BOTH, float=self.LEFT, width=self.C100, color=s.summaryColor,
                fontsize=s.summarySize, lineheight=s.summaryLineHeight, 
                margintop=s.summaryMarginTop, marginbottom=s.summaryMarginBottom)
            self.buildElement(b, item.summary)
            b._div()

class FeaturedByDiapText(FeaturedByText):
    u"""As FeaturedByText, but default on a dark background."""
    
    BLUEPRINT = BluePrint(FeaturedBase.BLUEPRINT, 
        # Selection stuff
        # Index of first and amount of selected features for this component
        itemStart=0, itemCount=10, 
        itemRandom=True, doc_itemRandom=u'Choose random from the selected items.',
        # Label stuff 
        label=None, labelSize=Em(2.2), 
        labelColor=Color('#828487'), doc_labelColor=u'Label color.',
        labelMarginBottom=Em(0.5),
        labelMarginTop=Em(0.3),
        # Poster
        showPoster=True, posterWidth='40%',
        # Layout stuff
        colWidth=8, # Default amount of columns for this component
        # Level stuff, handle local fontsize and lineheight here, related to the item size
        showLevel=True, genericLevel='Generic', # Show generic level if level is omitted in data.
        levelColor=Color('#6294D0'), 
        levelSize=LEVELSIZE, 
        levelWeight=C.BOLD, 
        levelMarginTop=Em(0.5),
        # Category stuff in h5
        showCategory=False, 
        categoryColor=CATEGORYCOLOR, 
        categorySize=Em(1.8), 
        categoryLineHeight=Em(1.2), 
        categoryWeight=C.BOLD,
        # Name stuff in h2
        nameSize=Em(1.8), 
        nameLineHeight=Em(1.1), 
        nameWeight=None, # Default inheriting from the main weight.
        nameColor=Color('#E1E1E1'), 
        nameMarginBottom=Em(0.2), 
        nameMarginTop=0,
        nameDisplay=C.BLOCK,
        # Author stuff in h6
        authorSize=AUTHORSIZE, 
        authorWeight=C.NORMAL, 
        authorColor=Color('#B2B4B7'), # Inheriting from the main color as default
        authorDisplay=C.BLOCK, 
        authorLineHeight=Em(1.4),
        # Summary stuff
        summaryColor=C.WHITE, 
        summaryMarginTop=Em(0.4), 
        summaryMarginBottom=Em(0.5),
        # Tablet stuff
        tabletLabelSize=Em(1.5),
        # Mobile stuff
        mobileDisplay=C.NONE,
        mobilePaddingTop=Em(2), 
        mobilePaddingBottom=Em(0.5), 
        mobilePaddingLeft=Em(0.5), mobilePaddingRight=Em(0.5),
        mobileMarginTop=Em(2), 
        mobileMarginBottom=Em(0.5), 
        mobileMarginLeft=Em(0.5), mobileMarginRight=Em(0.5),
        mobileFloat=C.NONE, 
    )
       
class FeaturedByTextList(FeaturedBase):

    BLUEPRINT = BluePrint( 
        # Selection stuff
        itemStart=0, 
        itemCount=6, # Index of first and last selected feature for this component
        # Layout stuff
        colWidth=4, # Default amount of columns for this component
        # Category stuff in h5
        categoryColor=Color('#828487'), categorySize=Em(0.9), categoryLineHeight=Em(1.2), 
        categoryWeight=C.NORMAL, categoryMarginTop=Em(1), categoryDisplay=C.BLOCK,
        # Name stuff in h2
        nameColor=Color('#4080D0'), nameSize=Em(1.4), nameWeight=C.NORMAL, nameDisplay=C.BLOCK, 
        nameMarginBottom=Em(0.2), nameMarginTop=Em(0.2), nameLineHeight=Em(1.2),
        # Topic stuff
        topicColor=Color('#202020'),
        # Mobile stuff
        mobileDisplay=C.NONE,
        mobilePaddingTop=Em(2), mobilePaddingBottom=Em(0.5), mobilePaddingLeft=Em(0.5), mobilePaddingRight=Em(0.5),
        mobileMarginTop=Em(2), mobileMarginBottom=Em(0.5), mobileMarginLeft=Em(0.5), mobileMarginRight=Em(0.5),
        mobileFloat=C.NONE, 
    )

    def buildFeatured(self, b, data):
        s = self.style
        for item in data.items:
            if item.category:
                b.a(href='/%s-%s' % (self.PARAM_CATEGORY, item.category), class_=self.CLASS_CATEGORYTHUMB)
                b.h5(fontsize=s.categorySize, fontweight=s.categoryWeight, lineheight=s.categoryLineHeight,
                     color=s.categoryColor, margintop=s.categoryMarginTop, display=s.categoryDisplay)
                b.text(item.category)
                b._h5()
                b._a()
            b.a(href='/%s-%s' % (self.PARAM_ARTICLE, item.id), class_=self.CLASS_NAME)
            b.h2(fontsize=s.nameSize, fontweight=s.nameWeight, lineheight=s.nameLineHeight, 
                 color=s.nameColor, marginbottom=s.nameMarginBottom, display=s.nameDisplay,
                 margintop=s.nameMarginTop)
            b.text(item.name)
            b._h2()
            b._a()
            if item.topic is not None: # Test on element. Topic elements need to be defined in global style.
                self.buildElement(b, item.topic)

class FeaturedTitled(FeaturedBase):
    pass

