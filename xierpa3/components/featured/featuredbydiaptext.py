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
#    featuredbydiaptext.py
#
from featuredbytext import FeaturedByText
from xierpa3.attributes import Em, Color,Perc
from xierpa3.descriptors.blueprint import BluePrint

class FeaturedByDiapText(FeaturedByText):
    u"""As FeaturedByText, but default on a dark background."""

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = FeaturedByText.C

    LEVELSIZE = Em(0.9)
    AUTHORSIZE = Em(1.2)
    CATEGORYSIZE = Em(1.4)
    AUTHORCOLOR = Color('#828487')
    CATEGORYCOLOR = AUTHORCOLOR
    LABELCOLOR = AUTHORCOLOR
    TEXTCOLOR = Color('#FFF')
    NAMECOLOR= Color('#66696C')
    SUMMARYCOLOR= Color('#E0E0E0')
    BACKGROUNDCOLOR = Color('#323A46')
    LEVELCOLOR = Color('#6294D0')
    NAMECOLOR = Color('#E1E1E1')
    AUTHORCOLOR = Color('#B2B4B7')

    # Inherit from the super class blueprint, and then change some of the parameters.
    BLUEPRINT = BluePrint(FeaturedByText.BLUEPRINT,
        width=Perc(100), doc_colWidth=u'Relative width for the featured by text column.',
        gutter=8, doc_gutter=u'Gutter width between columns.',
        # Layout alternatives
        showPoster=True, doc_showPoster=u'Boolean flag to indicate if the poster of the article should be shown.',
        showCategory=True, doc_showCategory=u'Boolean flag to indicate if the category of this article should be shown.',

        # Selection stuff
        # Index of first and amount of selected features for this component
        start=0, doc_start=u'Index of first selected item to feature.',
        count=10, doc_count=u'Number of selected items to feature.',
        itemRandom=True, doc_itemRandom=u'Choose random from the selected items.',
        # Label stuff
        label=None, doc_label=u'Label string.',
        labelSize=Em(2.2), doc_labelSize=u'Label size.',
        labelColor=Color('#828487'), doc_labelColor=u'Label color.',
        labelMarginBottom=Em(0.5),
        labelMarginTop=Em(0.3),
        # Poster
        posterWidth='40%', doc_posterWidth=u'Width of the poster image, to allow text to flow around.',
        # Layout stuff
        color=TEXTCOLOR,
        paddingTop=Em(2),
        paddingBottom=Em(2),
        paddingLeft=Em(1),
        paddingRight=Em(1),
        backgroundColor=Color(BACKGROUNDCOLOR), doc_backgroundColor=u'Background color of the component. Default is a dark gray.',
        # Level stuff, handle local fontsize and lineheight here, related to the item size
        showLevel=True, genericLevel='Generic', # Show generic level if level is omitted in data.
        levelColor=Color(LEVELCOLOR), doc_levelColor=u'Color of the level indicator.',
        levelSize=LEVELSIZE,
        levelWeight=C.BOLD,
        levelMarginTop=Em(0.5),
        # Category stuff in h5
        categoryColor=CATEGORYCOLOR,
        categorySize=Em(1.8),
        categoryLineHeight=Em(1.2),
        categoryWeight=C.BOLD,
        # Name stuff in h2
        nameSize=Em(1.8),
        nameLineHeight=Em(1.1),
        nameWeight=None, # Default inheriting from the main weight.
        nameColor=Color(NAMECOLOR),
        nameMarginBottom=Em(0.2),
        nameMarginTop=0,
        nameDisplay=C.BLOCK,
        # Author stuff in h6
        authorSize=AUTHORSIZE,
        authorWeight=C.NORMAL,
        authorColor=Color(AUTHORCOLOR), # Inheriting from the main color as default
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
        mobilePaddingLeft=Em(0.5),
        mobilePaddingRight=Em(0.5),
        mobileMarginTop=Em(2),
        mobileMarginBottom=Em(0.5),
        mobileMarginLeft=Em(0.5),
        mobileMarginRight=Em(0.5),
        mobileFloat=C.NONE,
    )
