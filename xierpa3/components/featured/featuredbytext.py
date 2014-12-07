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
#    featuredbytext.py
#
from featuredbase import FeaturedBase
from xierpa3.descriptors.media import Media
from xierpa3.attributes import Em, Perc, Color, Margin
from xierpa3.descriptors.blueprint import BluePrint

class FeaturedByText(FeaturedBase):
    u"""The @FeaturedByText@ feature component, shows a featured article by summary.
    Respectively the binary flags @BluePrint@ *showPoster*, *showLevel*, *showTitle* and
    *showTopic* will enable the level of the article (as defined in the article source @$level@),
    the article title (@$title@) and topic (@$topic), of set to @True@."""

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = FeaturedBase.C

    LEVELSIZE = Em(0.9)
    LEVELCOLOR = Color('#6294D0')
    AUTHORSIZE = Em(1.2)
    CATEGORYSIZE = Em(1.4)
    AUTHORCOLOR = Color('#828487')
    CATEGORYCOLOR = AUTHORCOLOR
    LABELCOLOR = AUTHORCOLOR
    NAMECOLOR= Color('#66696C')
    SUMMARYCOLOR= Color('#202020')

    BLUEPRINT = BluePrint(FeaturedBase.BLUEPRINT,
        # Alternative layout selectors
        showPoster=True, doc_showPoster=u'Boolean flag to indicate if the poster of the article should be shown.',
        showSummary=True, doc_showSummary=u'Boolean flag to indicate that summary should be shown if it exists.',
        showLevel=True, doc_showLevel=u'Boolean flag to show the intended reader level for this article.',
        showCategory=True, doc_showCategory=u'Boolean flag to indicate if the category of this article should be shown.',
        showAuthor=True, doc_showAuthor=u'Boolean flag to indicate if the author of this article should be shown.',

        # Selection stuff
        start=0, doc_start=u'Index of first selected item to feature.',
        count=3, doc_count=u'Number of selected items to feature.',
        # Label stuff '#828487'
        label=None,
        labelSize=Em(2),
        labelColor='red',
        labelMarginBottom=Em(0.5),
        labelMarginTop=Em(0.3),
        labelLineHeight=Em(1.4),
        # Poster, select by @showPoster
        posterWidth=Perc(40), doc_posterWidth=u'Width of the poster thumnail.',
        posterAlign=C.LEFT, doc_posterAlign=u'Alignment of the poster image, C.LEFT or C.RIGHT. Default is left.',
        # Layout stuff
        colWidth=8, doc_colWidth=u'Default amount of columns for this component',
        backgroundColor=None, doc_backgroundColor=u'Background color of the whole component. Default is to inherit.',
        # Level stuff, handle local fontsize and lineheight here, related to the item size
        genericLevel='Generic', # Show generic level if level is omitted in data.
        levelColor=LEVELCOLOR,
        levelSize=LEVELSIZE,
        levelLineHeight=Em(1.4),
        levelWeight=C.BOLD,
        levelMarginTop=Em(0.5),
        # Category stuff in h5
        categoryColor=CATEGORYCOLOR,
        categorySize=CATEGORYSIZE,
        categoryLineHeight=Em(1.2),
        categoryWeight=C.BOLD,
        # Name stuff in h2
        nameSize=Em(3.2),
        nameLineHeight=Em(1),
        nameWeight=None, # Default inheriting from the main weight.
        nameColor=NAMECOLOR,
        nameMarginBottom=Em(0.2),
        nameMarginTop=0,
        nameDisplay=C.BLOCK,
        # Author stuff in h6
        authorSize=AUTHORSIZE,
        authorWeight=C.NORMAL,
        authorColor=AUTHORCOLOR, doc_authorColor=u'Author name color.',
        authorDisplay=C.BLOCK,
        authorLineHeight=Em(1.4),
        # Summary stuff
        summaryColor=SUMMARYCOLOR,
        summarySize=Em(1.2),
        summaryLineHeight=Em(1.4),
        summaryMarginTop=Em(0.4),
        summaryMarginBottom=Em(0.5),
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
    def buildFeatured(self, b, articles):
        s = self.style
        b.div(class_=self.getClassName(), width=s.width, backgroundcolor=s.backgroundColor,
            display=s.display, float=s.float, padding=s.padding,
            media=Media(max=self.C.M_MOBILE_MAX, width=s.widthMobile,
                display=s.displayMobile, float=s.floatMobile),
        )
        for article in articles:
            self._buildFeaturedArticle(b, article)
        b._div()


    def _buildFeaturedArticle(self, b, article):
        u"""Build the featured article."""
        s = self.style
        if s.label:
            b.h2(fontsize=s.labelSize, color=s.labelColor, margintop=s.labelMarginTop,
                marginbottom=s.labelMarginBottom, lineheight=s.labelLineHeight,
                media=(
                    Media(min=self.C.M_TABLET_MIN, max=self.C.M_TABLET_MAX, fontsize=s.tabletLabelSize, color='red'),
                    Media(max=self.C.M_MOBILE_MAX, color='blue')
                ))
            b.text(s.label)
            b._h2()
        b.a(href='/%s-%s' % (self.C.PARAM_ARTICLE, article.id), class_=self.C.CLASS_NAME)
        b.h2(fontsize=s.nameSize, fontweight=s.nameWeight, lineheight=s.nameLineHeight,
             color=s.nameColor, marginbottom=s.nameMarginBottom, display=s.nameDisplay,
             margintop=s.nameMarginTop)
        b.text(article.name)
        b._h2()
        b._a()
        if s.showPoster and article.poster:
            b.a(href='/%s-%s' % (self.C.PARAM_ARTICLE, article.id), class_=self.C.CLASS_NAME)
            b.img(width=s.posterWidth, src=article.poster, float=s.posterAlign, padding=0,
                margin=Margin(Em(0.5), Em(0.5), 0, 0),
                media=Media(max=self.C.M_MOBILE_MAX, display=self.C.NONE)
            )
            b._a()
        if s.showLevel and (article.level or s.genericLevel):
            b.h5(class_=self.C.CLASS_LEVEL, color=s.levelColor, fontsize=s.levelSize, fontweight=s.levelWeight,
                margintop=s.levelMarginTop, lineheight=s.levelLineHeight)
            b.text(article.level or s.genericLevel)
            b.text(' level')
            b._h5()
        if s.showAuthor and article.author:
            b.a(href='/%s-%s' % (self.C.PARAM_AUTHOR, article.author), class_=self.C.CLASS_AUTHOR)
            b.h5(fontsize=s.authorSize, fontweight=s.authorWeight, color=s.authorColor,
                 lineheight=s.authorLineHeight, display=s.authorDisplay)
            b.text('By %s' % article.author)
            b._h5()
            b._a()
        if s.showCategory and article.category:
            for category in article.category:
                b.a(href='/%s-%s' % (self.C.PARAM_CATEGORY, category), class_=self.C.CLASS_CATEGORY)
                b.h5(fontsize=s.categorySize, fontweight=s.categoryWeight, lineheight=s.categoryLineHeight,
                     color=s.categoryColor, margintop=Em(1), display=self.C.BLOCK)
                b.text(category)
                b._h5()
                b._a()
        if s.showSummary and article.summary is not None: # Test on element. Summary elements tag must be defined by generic style.
            b.div(class_='featuredSummary', clear=self.C.BOTH, float=self.C.LEFT, width=Perc(100),
                color=s.summaryColor, fontsize=s.summarySize, lineheight=s.summaryLineHeight,
                margintop=s.summaryMarginTop, marginbottom=s.summaryMarginBottom)
            if isinstance(article.summary, basestring):
                b.text(article.summary)
            else:
                self.buildElement(b, article.summary)
            b._div()
        if b.e.form[self.C.PARAM_DEBUG]:
            b.text(`article`)
