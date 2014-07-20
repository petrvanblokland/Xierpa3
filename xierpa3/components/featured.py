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
from xierpa3.attributes import Em, Margin, Perc, Color, Padding
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
        articles = self.adapter.getArticles(start=s.itemStart, count=s.itemCount,
            omit=b.getCurrentArticleId())
        self.buildFeatured(b, articles)
   
class FeaturedByImage(FeaturedBase):
    u"""The @FeaturedByImage@ feature component, shows a featured article by its poster image
    on full width of the component.
    If there is no poster image defined in the article meta data, then the first image in the article
    is used here. The image is a link to the article page.
    Respectively the binary flags @BluePrint@ *showLevel*, *showTitle* and @showTopic@ 
    will enable the level of the article (as defined in the article source @$level@), 
    the article title (@$title@) and topic (@$topic), of set to @True@."""
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = FeaturedBase.C 

    BLUEPRINT = BluePrint(FeaturedBase.BLUEPRINT, 
        # Selection stuff
        itemStart=0, doc_itemStart=u'Index of first selected item to feature.',
        itemCount=3, doc_itemCount=u'Number of selected items to feature.',
        # Container component layout stuff
        width=Perc(30), doc_width=u'Overall width of the component.',
        widthMobile=Perc(100), doc_widthMobile=u'Overall width of the component for mobile.',
        backgroundColor=None, doc_backgroundColor=u'Background color of the component.',
        display=C.BLOCK, doc_display=u'Display status of the component',
        displayMobile=C.NONE, doc_displayMobile=u'Display status of the component for mobile.',
        float=C.LEFT, doc_float=u'Float status of the component.',
        floatMobile=C.NONE, doc_floatMobile=u'Float status of the component for mobile.',
        padding=0, doc_padding=u'Padding of the component content.',
        # Item/article stuff
        itemDisplay=C.BLOCK, doc_itemDisplay=u'Display type of the item/article image cell.',
        itemBackgroundColor=Color('#E0E0E0'), doc_itemBackgroundColor=u'Background color of the item/article image cell.',
        itemClear=C.NONE, doc_itemClear=u'Floating clear of item/article image cell.',
        itemMarginBottom=Em(0.5), doc_itemMarginBottom=u'Margin bottom of item/article image cell.',
        itemWidth=Perc(100), doc_itemWidth=u'Width of item/article image cell.',
        itemPadding=Padding(Em(0.35)), doc_itemPadding=u'Padding of the item/article image cell.',
        # Level
        showLevel=False, doc_showLevel=u'Boolean flag to show the level field of the article.',
        levelFormat='%s level', doc_levelFormat=u'Python string pattern as level indicator. Takes level string as parameter.',
        genericLevel=None, doc_genericLevel=u'Generic level flag, overruling the article level field.',
        levelColor=Color('#222'), doc_levelColor=u'Color of the level indicator.',
        levelSize=Em(0.8), doc_levelSize=u'Font size of the level indicator.',
        levelWeight=C.BOLD, doc_levelWeight=u'Font weight of the level indicator.',
        levelMarginTop=Em(0.2), doc_levelMarginTop=u'Margin top of the level indicator.',
        levelMarginBottom=Em(0.2), doc_levelMarginBottom=u'Margin bottom of the level indicator.',
        # Title
        showTitle=True, doc_showTitle=u'Boolean flag to show the title of the article.',
        titleColor=('#444'), doc_titleColor=u'Color of the article title.',
        titleSize=Em(1.1), doc_titleSize=u'Font size of the article title.',
        titleWeight=C.NORMAL, doc_titleWeight=u'Font weight of the article title.',
        titleLineHeight=Em(1.2), doc_titleLineHeight=u'Line height of the article title.',
        # Topic
        showTopic=True, doc_showTopic=u'Boolean flag to show the topic of the article.',
        topicColor=Color('#444'), doc_topicColor=u'Color of the article topic.',
        topicSize=Em(0.8), doc_topicSize=u'Font size of the article topic.',
        topicWeight=C.NORMAL, doc_topicWeight=u'Font weight of the article topic.',
        topicLineHeight=Em(1.2), doc_topicLineHeight=u'Line height of the article topic.',
    )
        # Col stuff ??? NOT USED
    '''
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
        '''
    def buildFeatured(self, b, articles):
        s = self.style
        b.div(class_=self.getClassName(), width=s.width, backgroundcolor=s.backgroundColor,
            display=s.display, float=s.float, padding=s.padding,
            media=Media(max=self.C.M_MOBILE_MAX, width=s.widthMobile,
                display=s.displayMobile, float=s.floatMobile),
        )
        for article in articles.items:
            if article.poster:  
                self.buildFeaturedImage(b, article)
        b._div()
        
    def buildFeaturedImage(self, b, article):
        s = self.style
        b.div(class_=self.C.CLASS_FEATUREDITEM, display=s.itemDisplay,
            backgroundcolor=s.itemBackgroundColor, padding=s.itemPadding,
            clear=s.itemClear, marginbottom=s.itemMarginBottom, margintop=s.itemMarginTop,
            width=s.itemWidth,
        )
        b.a(href='/%s-%s' % (self.C.PARAM_ARTICLE, article.id))
        b.img(class_=(self.C.CLASS_AUTOWIDTH, 'featuredImage'), src=article.poster)
        if s.showLevel or s.genericLevel:
            b.h5(class_=self.C.CLASS_LEVEL, color=s.levelColor, fontsize=s.levelSize, 
                fontweight=s.levelWeight,
                margintop=s.levelMarginTop, marginbottom=s.levelMarginBottom)
            # Format the level indicator
            b.text(s.levelFormat % (article.level or s.genericLevel))
            b._h5()
        if s.showTitle:
            b.h4(class_=self.C.CLASS_TITLE, color=s.titleColor, fontsize=s.titleSize, 
                 fontweight=s.titleWeight, lineheight=s.titleLineHeight)
            b.text(article.title)
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
  
class FeaturedByImageList(FeaturedBase):
    u"""The <b>FeaturedByImageList</b> feature component builds a vertical list if thumbnails, 
    level and optional names of the selected article items."""
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = FeaturedBase.C 

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
        showLevel=False, 
        genericLevel='Generic', doc_genericLevel=u'Show this generic level name if level attitbute is undefined in adapter data.',
        levelColor=Color('#6294D0'), doc_levelColor=u'Level color.',
        levelSize=LEVELSIZE, doc_levelSize=u'Level font size.',
        levelWeight=C.BOLD, doc_levelWeight=u'Level font weight.',
        levelMarginTop=Em(0.5), doc_levelMarginTop=u'Level margin top.',
        # Optional name stuff, handle local fontsize and lineheight here, related to the item sizes
        showName=False, 
        nameColor=Color('#A32C2D'), 
        nameSize=Em(0.9), 
        nameLineHeight=Em(1.2), 
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
            b.div(class_=self.C.CLASS_FEATURED_ITEM, display=s.itemDisplay,
                clear=s.itemClear, marginbottom=s.itemMarginBottom, width=s.itemWidth,
            )
            b.a(href='/%s-%s' % (self.C.PARAM_ARTICLE, item.id))
            if s.showLevel:
                b.h5(color=s.levelColor, fontsize=s.levelSize, fontweight=s.levelWeight,
                    margintop=s.levelMarginTop)
                b.text(item.level or s.genericLevel)
                b.text(' level')
                b._h5()
            b.img(class_=self.C.CLASS_AUTOWIDTH, src=item.poster)
            if s.showName:
                b.h4(color=s.nameColor, fontsize=s.nameSize, fontweight=s.nameWeight, 
                     lineheight=s.nameLineHeight)
                b.text(item.name)
                b._h4()
            if s.showTopic and item.topic is not None: # Elements must be defined in global style
                self.buildElement(b, item.topic)
            b._a()
            b._div(comment=self.C.CLASS_FEATURED_ITEM)

class FeaturedByText(FeaturedBase):

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = FeaturedBase.C 

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
                    Media(min=self.C.M_TABLET_MIN, max=self.C.M_TABLET_MAX, fontsize=s.tabletLabelSize, color='red'),
                    Media(max=self.C.M_MOBILE_MAX, color='blue')
                ))
            b.text(s.label)
            b._h2()
        b.a(href='/%s-%s' % (self.C.PARAM_ARTICLE, item.id), class_=self.C.CLASS_NAME)
        b.h2(fontsize=s.nameSize, fontweight=s.nameWeight, lineheight=s.nameLineHeight, 
             color=s.nameColor, marginbottom=s.nameMarginBottom, display=s.nameDisplay,
             margintop=s.nameMarginTop)
        b.text(item.name) 
        b._h2()
        b._a()
        if s.showPoster:
            b.a(href='/%s-%s' % (self.C.PARAM_ARTICLE, item.id), class_=self.C.CLASS_NAME)
            b.img(width=s.posterWidth, src=item.poster, float=self.C.LEFT, padding=0,
                margin=Margin(Em(0.5), Em(0.5), 0, 0),
                media=Media(max=self.C.M_MOBILE_MAX, display=self.C.NONE)
            )
            b._a()
        if s.showLevel:
            b.h5(class_=self.C.CLASS_LEVEL, color=s.levelColor, fontsize=s.levelSize, fontweight=s.levelWeight,
                margintop=s.levelMarginTop, lineheight=s.levelLineHeight)
            b.text(item.level or s.genericLevel)
            b.text(' level')
            b._h5()
        if item.author: # Test on text
            b.a(href='/%s-%s' % (self.C.PARAM_AUTHOR, item.author), class_=self.C.CLASS_AUTHOR)
            b.h5(fontsize=s.authorSize, fontweight=s.authorWeight, color=s.authorColor, 
                 lineheight=s.authorLineHeight, display=s.authorDisplay)
            b.text('By %s' % item.author)
            b._h5()
            b._a()
        if s.showCategory and item.category: # Text on text
            b.a(href='/%s-%s' % (self.C.PARAM_CATEGORY, item.category), class_=self.C.CLASS_CATEGORY)
            b.h5(fontsize=s.categorySize, fontweight=s.categoryWeight, lineheight=s.categoryLineHeight, 
                 color=s.categoryColor, margintop=Em(1), display=self.C.BLOCK)
            b.text(item.category)
            b._h5()
            b._a()
        if item.summary is not None: # Test on element. Summary elements tag must be defined by generic style.
            b.div(class_='featuredSummary', clear=self.C.BOTH, float=self.C.LEFT, width=Perc(100), 
                color=s.summaryColor, fontsize=s.summarySize, lineheight=s.summaryLineHeight, 
                margintop=s.summaryMarginTop, marginbottom=s.summaryMarginBottom)
            if isinstance(item.summary, basestring):
                b.text(item.summary)
            else:
                self.buildElement(b, item.summary)
            b._div()

class FeaturedByDiapText(FeaturedByText):
    u"""As FeaturedByText, but default on a dark background."""

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = FeaturedByText.C 
    
    BLUEPRINT = BluePrint(FeaturedBase.BLUEPRINT, 
        # Selection stuff
        # Index of first and amount of selected features for this component
        itemStart=0, 
        itemCount=10, 
        itemRandom=True, doc_itemRandom=u'Choose random from the selected items.',
        # Label stuff 
        label=None, doc_label=u'Label string.',
        labelSize=Em(2.2), doc_labelSize=u'Label size.',
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

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = FeaturedBase.C 

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
                b.a(href='/%s-%s' % (self.C.PARAM_CATEGORY, item.category), class_=self.C.CLASS_CATEGORYTHUMB)
                b.h5(fontsize=s.categorySize, fontweight=s.categoryWeight, lineheight=s.categoryLineHeight,
                     color=s.categoryColor, margintop=s.categoryMarginTop, display=s.categoryDisplay)
                b.text(item.category)
                b._h5()
                b._a()
            b.a(href='/%s-%s' % (self.C.PARAM_ARTICLE, item.id), class_=self.C.CLASS_NAME)
            b.h2(fontsize=s.nameSize, fontweight=s.nameWeight, lineheight=s.nameLineHeight, 
                 color=s.nameColor, marginbottom=s.nameMarginBottom, display=s.nameDisplay,
                 margintop=s.nameMarginTop)
            b.text(item.name)
            b._h2()
            b._a()
            if isinstance(item.topic, basestring):
                b.text(item.topic)
            elif item.topic is not None: # Test on element. Topic elements need to be defined in global style.
                self.buildElement(b, item.topic)

class FeaturedTitled(FeaturedBase):
    pass

