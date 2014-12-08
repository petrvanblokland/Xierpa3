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
#    posterhead.py
#
from xierpa3.components.column import Column
from xierpa3.descriptors.media import Media
from xierpa3.attributes import Em, Perc, Color, Shadow
from xierpa3.descriptors.blueprint import BluePrint

class PosterHead(Column):
    u"""The @PosterHead@ component, shows a featured article by its poster image
    on full width of the component, and adding the title and the text a overlay with shadow.
    If there is no poster image defined in the article meta data, then the first image in the article
    is used here. The poster image is a link to the article page.
    Respectively the binary flags @BluePrint@ *showLevel*, *showTitle* and *showTopic* 
    will enable the level of the article (as defined in the article source @$level@), 
    the article title (@$title@) and topic (@$topic), of set to @True@."""
    # Get Constants->Config as class variable, so inheriting classes can redefine values.

    C = Column.C

    BLUEPRINT = BluePrint(Column.BLUEPRINT,
        # Container component layout stuff
        width=Perc(100), doc_width=u'Overall width of the component.',
    )
    def buildColumn(self, b):
        if b.isType(('css', 'sass')):
            self.buildPosterStyle(b)
        else:
            self.buildPoster(b)

    def buildPosterStyle(self, b):
        s = self.style
        b.div(class_=self.getClassName(), width=s.width, backgroundcolor=s.backgroundColor,
            display=s.display, float=s.float, padding=s.padding,
            media=Media(max=self.C.M_MOBILE_MAX, width=s.widthMobile,
                display=s.displayMobile, float=s.floatMobile),
        )
        b.div(class_=self.C.CLASS_FEATUREDITEM, display=s.itemDisplay,
            backgroundcolor=s.itemBackgroundColor, padding=Em(2),
            clear=s.itemClear, marginbottom=s.itemMarginBottom, margintop=s.itemMarginTop,
        )
        b.h1(color=Color('white'), fontsize=Em(4), fontweight=self.C.BOLD, textshadow=Shadow())
        b._h1()
        b.h2(color=Color('yellow'), fontsize=Em(2), fontweight=self.C.BOLD, textshadow=Shadow())
        b._h2()
        b._div(comment=self.C.CLASS_FEATUREDITEM)
        b._div()

    def buildPoster(self, b):
        s = self.style
        article = self.adapter.getArticle(id=b.getCurrentArticleId())
        if article.poster:
            b.div(class_=self.getClassName())
            b.div(class_=self.C.CLASS_FEATUREDITEM, style='background:url(%s);background-repeat:no-repeat;background-size:cover;' % article.poster)
            b.h1()
            b.text(article.title)
            b._h1()
            if article.subtitle or article.topic:
                b.h2()
                b.text(article.subtitle or article.topic)
                b._h2()
            b._div(comment=self.C.CLASS_FEATUREDITEM)
            b._div()
