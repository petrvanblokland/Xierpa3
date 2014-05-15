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
#    article.py
#
from xierpa3.components.column import Column
from xierpa3.constants.constants import C
from xierpa3.toolbox.transformer import TX
from xierpa3.attributes import *
from xierpa3.descriptors.style import Media

CHAPTERCOLOR = '#202020'
CHAPTERTITLECOLOR0 = '#1F1F1F'
AUTHORCOLOR = '#828487'
CATEGORYCOLOR = '#828487'
LABELCOLOR = '#828487'
LEADCOLOR = '#828487'
NAMECOLOR= '#66696C'
TITLECOLOR= '#66696C'
SUMMARYCOLOR= '#202020'
H2COLOR = '#828487'

class ArticleColumn(Column):
    def getChapterIndex(self, b, article):
        return min(max(0, TX.asInt(b.e.form[C.PARAM_CHAPTER]) or 0), len(article.items or [])-1)
     
class Article(ArticleColumn):
    
    STYLE_DEFAULT = dict(
        # Layout stuff
        colWidth=8, # Default amount of columns for this component   
        # Post
        showPoster=False,                     
        # Title stuff on the first chapter page of the article
        titleSize=Em(3.2), titleLineHeight=Em(1.2), titleColor=TITLECOLOR,
        # Name stuff on the second+ chapter page of the article
        nameSize=Em(2), nameLineHeight=Em(1.2), nameColor=NAMECOLOR,
        # Author stuff
        authorSize=Em(1), authorColor=AUTHORCOLOR,
        # Category stuff
        categorySize=Em(0.8), categoryLineHeight=Em(1.2),
        categoryColor=NAMECOLOR, categoryWeight=None, # Default to inherit from the default weight.
        # Chapter stuff
        chapterColor=CHAPTERCOLOR, chapterSize=Em(1.2), chapterLineHeight=Em(1.4),  
        # Chapter lead stuff
        leadSize=Em(1.8), leadLineHeight=Em(1.2), leadMarginBottom=Em(0.3),
        leadColor=LEADCOLOR,
        # Chapter first page
        chapterTitleSize0=Em(1.5), chapterTitleColor0=CHAPTERTITLECOLOR0, 
        chapterTitleMarginTop0=Em(1), chapterTitleMarginBottom0=Em(0.5),
        # Chapter other pages
        chapterTitleSize1=Em(2.5), chapterTitleColor1=None,
        chapterTitleMarginTop1=Em(1), chapterTitleMarginBottom1=Em(0.5),
        # H1
        # H2
        h2Size=Em(2), h2LineHeight=Em(1.4), h2PaddingTop=Em(1), h2PaddingBottom=0,
        h2Color=H2COLOR, 
        # H3
        h3Size=Em(2), h3LineHeight=Em(1.4), h3PaddingTop=Em(1), h3PaddingBottom=0,
        # Chapter p stuff
        articleSize=Em(1.2), articleLineHeight=Em(1.6), articleIndent=Em(2),
        # First p
        firstIndent=0,
        # Bullet list
        bulletType='disc', bulletPaddingLeft=Em(2), bulletPosition='inside',
        bulletMarginBottom=0, bulletMarginTop=Em(1),
        bulletItemMarginBottom=Em(1),
        # Ordered list
        numberedListType='decimal', numberedListPosition='inside',
        numberedListPaddingLeft=Em(2),
        numberedListMarginBottom=0, numberedListMarginTop=Em(1),
        numberedListItemMarginBottom=Em(1),
        # Image & caption
        imageMarginTop=Em(1), imageMarginBottom=Em(0.8), 
        imagePaddingTop=None, imagePaddingBottom=None, imagePaddingLeft=None, 
        imagePaddingRight=None, imageBackgroundColor=None,
        captionFontStyle=C.ITALIC, captionFontSize=Em(0.9), captionMarginTop=Em(0.5),
        # Code
        codeFontFamily='Courier', codeFontSize=Em(1.2), codePaddingLeft=Em(1),
        codePaddingTop=Em(0.5), codePaddingBottom=Em(0.5),
        codeMarginTop=Em(0.5), codeMarginBottom=Em(0.5),
        codeBackgroundColor=C.WHITE,
    )
    def buildColumn(self, b):
        article = self.getAdapterData(C.ADAPTER_ARTICLE, id=b.getCurrentArticleId())
        self.buildArticle(b, article)

    def buildArticle(self, b, article):
        u"""Build the article. If there is a "/chapter-2" url parameter defined and it is in
        the range of available chapters, then show that chapter. Other values are cropped to
        min and max index of the chapter list."""
        #b.element(tag='img', class_=C.CLASS_AUTOWIDTH, margintop=Em(1), marginbottom=Em(1))
        if b.isType(('css', 'sass')): # @@@ Clean up, using model article?
            self.buildArticleTop(b, article, 0) # Separate CSS for first chapter and the rest.
            self.buildArticleTop(b, article, 1)
            self.buildArticleStyle(b) # Build the CSS style template of an article here
        elif article.items:
            chapterIndex = self.getChapterIndex(b, article)
            self.buildArticleTop(b, article, chapterIndex)
            chapter = self.adapter.getChapterByIndex(article, chapterIndex)
            if chapter is not None:
                self.buildElement(b, chapter) # Render the indexed chapter element as builder calls.
        
    def buildArticleTop(self, b, article, chapterIndex):
        u"""Build the top of the article: type, title, author, etc. on the first page, if index is <b>0</b>.
        For all other pages build a smaller version of the top."""
        s = self.style
        class_ = C.CLASS_ARTICLETOP
        b.div(class_=class_, float=C.LEFT, width=C.C100, paddingtop=Em(0.5))
        # Poster image
        if chapterIndex == 0 and s.showPoster:
            b.img(class_=C.CLASS_AUTOWIDTH, src=article.poster)
        # Article category
        if chapterIndex == 0 and article.category: # Text on text
            b.a(href='/%s-%s' % (C.PARAM_CATEGORY, article.category))
            b.h5(fontsize=s.categorySize, lineheight=s.categoryLineHeight, color=s.categoryColor, 
                fontweight=s.categoryWeight, margintop=Em(1), display=C.BLOCK)
            b.text(article.category)
            b._h5()
            b._a()
        # Article title or name (on respectively the first chapter page or the rest of the pages.
        if chapterIndex == 0: # Show large title on the chapter first page of the article
            b.h2(class_='articleTitle0', fontsize=s.titleSize, lineheight=s.titleLineHeight, 
                color=s.titleColor, marginbottom=Em(0.2), display=C.BLOCK)
            b.text(article.name)
            b._h2()
        else: # Show smaller title on the rest of the pages
            b.h2(class_='articleTitle1', fontsize=s.nameSize, lineheight=s.nameLineHeight, 
                color=s.nameColor, marginbottom=Em(0.2), display=C.BLOCK)
            b.text(article.name)
            b._h2()
        # Author
        if chapterIndex == 0 and article.author: # Test if there is an author defined.
            b.a(href='/%s-%s' % (C.PARAM_AUTHOR, article.author))
            b.h5(fontsize=s.authorSize, fontweight=s.authorWeight, authorcolor=s.authorColor,
                display=C.BLOCK)
            b.text('By %s' % article.author)
            b._h5()
            b._a()
        # Chapter title
        chapterTitle = self.adapter.getChapterTitleByIndex(article, chapterIndex)
        if chapterIndex == 0: # Show large title on the chapter first page of the article
            b.h3(class_='chapterTitle0', fontsize=s.chapterTitleSize0, color=s.chapterTitleColor0,
                 margintop=s.chapterTitleMarginTop0, marginbottom=s.chapterTitleMarginBottom0)
            if chapterTitle is not None: 
                b.text(chapterTitle.text)
                #self.buildElement(b, chapterTitle)
            b._h3()
        else: # Other chapter pages
            b.h3(class_='chapterTitle1', fontsize=s.chapterTitleSize1, color=s.chapterTitleColor1,
                 margintop=s.chapterTitleMarginTop1, marginbottom=s.chapterTitleMarginBottom1)
            if chapterTitle is not None: 
                b.text(chapterTitle.text)
                #self.buildElement(b, chapterTitle)
            b._h3()
        b._div(comment=class_)
                
    def buildArticleStyle(self, b):
        s = self.style
        # SVG demo
        b.div(class_=C.CLASS_CHAPTER, color=s.chapterColor)
        # Should move from here. Make sure that svgExamples get SCSS builder calls.
        b.div(class_='svgDemo', margintop=Em(0.5), marginbottom=Em(0.5))
        b._div()
        # h1
        b.h1(fontsize=s.h1Size, lineheight=s.h1LineHeight, fontweight=s.h1FontSize,
             fontstyle=s.h1FontStyle, fontfamily=s.h1FontFamily, color=s.h1Color,
             paddingtop=s.h1PaddingTop, paddingbottom=s.h1PaddingBottom,
        )
        b._h1()
        # <h2>
        b.h2(fontsize=s.h2Size, lineheight=s.h2LineHeight, 
             fontweight=s.h2FontSize,
             fontstyle=s.h2FontStyle, fontfamily=s.h2FontFamily, color=s.h2Color,
             paddingtop=s.h2PaddingTop, paddingbottom=s.h2PaddingBottom,
        )
        b._h2()
        # <h3>
        b.h3(fontsize=s.h3Size, lineheight=s.h3LineHeight, fontweight=s.h3FontSize,
             fontstyle=s.h3FontStyle, fontfamily=s.h3FontFamily, color=s.h3Color,
             paddingtop=s.h3PaddingTop, paddingbottom=s.h3PaddingBottom,
        )
        b._h3()
        # <h4>
        b.h4(fontsize=s.h4Size, lineheight=s.h4LineHeight, fontweight=s.h4FontSize,
             fontstyle=s.h4FontStyle, fontfamily=s.h4FontFamily, color=s.h4Color,
             paddingtop=s.h4PaddingTop, paddingbottom=s.h4PaddingBottom,
        )
        b._h4()
        # <p>
        b.p(fontsize=s.articleSize, lineheight=s.articleLineHeight, textindent=s.articleIndent)
        self.buildPStyle(b)
        b._p()
        # <p class="... first">
        b.p(class_=C.CLASS_FIRST, textindent=s.firstIndent)
        b._p()
        # <p class="... last">
        b.p(class_=C.CLASS_LAST)
        b._p()
        # <lead>
        b.p(class_=C.CLASS_LEAD, fontsize=s.leadSize, lineheight=s.leadLineHeight, 
            color=s.leadColor, marginbottom=s.leadMarginBottom, 
            textindent=s.firstIndent)
        self.buildPStyle(b)
        b._p()
        # <blockquote>
        b.blockquote(borderleft=s.blockQuoteBorderLeft or Border('solid', '4px', '#CCC'), 
            margin=s.blockQuoteMargin or Margin(Em(1.5), 10), 
            lineheight=s.blockQuoteLineHeight or Em(1.4), fontstyle=s.blockQuoteStyle or C.ITALIC,
            padding=s.blockQuotePadding or Padding(Em(0.5), 10), 
            color=s.blockQuoteColor or '#828487')
        b._blockquote()
        # <em>
        b.em(fontstyle=s.emFontStyle, fontweight=s.emFontWeight,
            color=s.emColor, fontfamily=s.emFontFamily)
        b._em()
        # <pre>
        b.pre(fontstyle=s.codeFontStyle, fontweight=s.codeFontWeight, fontsize=s.codeFontSize,
            color=s.codeColor, fontfamily=s.codeFontFamily, paddingtop=s.codeMarginTop,
            paddingbottom=s.codePaddingBottom, paddingleft=s.codePaddingLeft,
            paddingright=s.codePaddingRight, backgroundcolor=s.codeBackgroundColor,
            margintop=s.codeMarginTop, marginbottom=s.codeMarginBottom,
        )
        b._pre()
        # <div class="imageBlock"><img/><div class="caption">...</div></div>
        b.div(class_=C.CLASS_IMAGEBLOCK, backgroundcolor=s.imageBackgroundColor, 
            margintop=s.imageMarginTop, marginbottom=s.imageMarginBottom,
            paddingtop=s.imagePaddingTop, paddingbottom=s.imagePaddingBottom,
            paddingleft=s.imagePaddingLeft, paddingright=s.imagePaddingRight,)
        b.img()
        b.div(class_=C.CLASS_CAPTION, fontfamily=s.captionFontFamily, fontsize=s.captionFontSize,
            color=s.captionColor, fontstyle=s.captionFontStyle, 
            margintop=s.captionMarginTop)
        b._div() # .caption
        b._div() # .imageBlock
        # <ul><li>...</li></ul>
        b.ul(liststyletype=s.bulletType, liststyleimage=s.bulletImage, 
            liststyleposition=s.bulletPosition, paddingleft=s.bulletPaddingLeft,
            marginbottom=s.bulletMarginBottom, margintop=s.bulletMarginTop)
        self.buildLiStyle(b)
        b._ul()
        # <ol><li>...</li></ol>
        b.ol(liststyletype=s.numberedListType,  
            liststyleposition=s.numberedListPosition, paddingleft=s.numberedListPaddingLeft,
            marginbottom=s.numberedListMarginBottom, margintop=s.numberedListMarginTop)
        self.buildLiStyle(b)
        b._ol()
        
        b._div() # Article chapter
             
    def buildLiStyle(self, b):
        # <li>
        s = self.style
        b.li(marginbottom=s.bulletItemMarginBottom)
        b._li()
               
    def buildPStyle(self, b):
        # <footnote>
        s = self.style
        b.sup(class_=C.CLASS_FOOTNOTE, top=s.footnoteTop or Em(-0.5), 
            fontsize=s.footnoteFontSize or Em(0.8), position=s.footnotePosition or C.RELATIVE,
            verticalalign=s.footnoteVerticalAlign or C.BASELINE)
        b._sup()
        b.em(fontweight=s.emWeight or C.BOLD)
        b._em()
    
class ArticleSideBar(ArticleColumn):
    STYLE_DEFAULT = dict(
        # Layout stuff
        colWidth=4, # Default amount of columns for this component   
        # Chapter navigation
        showChapterNavigation=True, chapterLabel='Chapters',
        chapterNameSize=Em(1.2),
        showChapterSummaryOnMax=10, # Not show summary if more than 10 chapters
        # Footnotes
        showFootNotes=True, footnoteLabel='Footnotes', 
    )
    def buildColumn(self, b):
        article = self.getAdapterData(C.ADAPTER_ARTICLE, id=b.e.form[C.PARAM_ARTICLE])
        self.buildArticleSideBar(b, article)

    def buildArticleSideBar(self, b, article):
        u"""Build nice stuff here from the article. @@@ Add to style that calling site can change
        the order."""
        s = self.style
        if b.isType(('css', 'sass')): # @@@ Clean up, using model for article side bar?
            self.buildArticleSideBarStyle(b) # Build the CSS style template of an article here
        else:
            if s.showChapterNavigation:
                self.buildMobileChapterNavigation(b, article)
                self.buildChapterNavigation(b, article)
            if s.showFootNotes:
                self.buildFootNotes(b, article)
     
    def buildArticleSideBarStyle(self, b): 
        u"""Build the styles for the articles side bar.  # @@@ Clean up, using model for article side bar?"""
        s = self.style
        # <div class="footnotes">
        b.div(class_=C.CLASS_FOOTNOTES, marginbottom=Em(0.5))
        b.h4(fontsize=Em(1.1))
        b._h4()
        b._div(comment=C.CLASS_FOOTNOTES)  
        
        # <div class="mobileChapterNavigation">
        b.div(class_=C.CLASS_MOBILECHAPTERNAVIGATION, marginbottom=Em(0.5), display=C.NONE,
            media=Media(max=C.M_MOBILE, display=C.BLOCK)
        )
        b.ul()
        b.li(backgroundcolor=s.mobileChapterButtonColor or '#444444')
        # <a>Chapter name</a>
        b.a(fontsize=s.summaryNameSize, color=s.mobileChapterButtonColor or 'white')
        b.h2(fontsize=Em(2), lineheight=Em(1.2),
             marginbottom=Em(0.2), margintop=Em(0.2), padding=Em(0.5))
        b._h2()
        b._a()
        b._li()
        b._ul()
        b._div(comment=C.CLASS_MOBILECHAPTERNAVIGATION) # Article mobile chapter navigation
        
        # <div class="chapterNavigation">
        b.div(class_=C.CLASS_CHAPTERNAVIGATION, marginbottom=Em(0.5), display=s.mobileContainerDisplay,
            media=Media(max=C.M_MOBILE, display=C.NONE)
        )
        b.h4(fontsize=Em(1.1))
        b._h4()
        b.ul()
        b.li()
        # <a>Chapter name</a>
        b.a(fontsize=s.summaryNameSize, color=s.summaryNameColor)
        b.h2(fontsize=s.chapterNameSize, color=s.chapterNameColor, lineheight=Em(1.2),
             marginbottom=Em(0.2), margintop=Em(0.4))
        b._h2()
        b._a()
        b._li()
        b._ul()  
        b._div(comment=C.CLASS_CHAPTERNAVIGATION) # Article chapter navigation
    
    def buildMobileChapterNavigation(self, b, article):
        s = self.style
        chapters = article.items
        if chapters and len(chapters) > 1:
            b.div(class_=C.CLASS_MOBILECHAPTERNAVIGATION)
            b.ul()
            for index, chapter in enumerate(chapters):
                b.li() 
                b.a(class_=C.CLASS_NAME, 
                    href='/%s-%s/%s-%s' % (C.PARAM_ARTICLE, article.id, C.PARAM_CHAPTER, index), 
                )
                chapterTitle = chapter.find('./meta/title') # @@@ Add this as adapter query
                if chapterTitle is None: # No title, add a default chapter title (not in the right style)
                    b.text('Chapter %d' % index)
                else:
                    self.buildElement(b, chapterTitle)
                b._a()
                b._li()
            b._ul()
            b._div()
            
    def buildChapterNavigation(self, b, article):
        u"""If there is more than one chapter in the article, automatically create a chapter
        navigation in the sidebar. The title and the summary are links to a page of the same
        article, for the defined chapter index."""
        s = self.style
        chapters = article.items
        if chapters and len(chapters) > 1:
            b.div(class_=C.CLASS_CHAPTERNAVIGATION)
            b.h4()
            b.text(s.chapterLabel)
            b._h4()
            b.ul()
            for index, chapter in enumerate(chapters):
                b.li(margintop=Em(0.5))
                b.a(class_=C.CLASS_NAME, 
                    href='/%s-%s/%s-%s' % (C.PARAM_ARTICLE, article.id, C.PARAM_CHAPTER, index), 
                )
                chapterTitle = chapter.find('./meta/title') # @@@ Add this as adapter query
                if chapterTitle is None: # No title, add a default chapter title (not in the right style)
                    b.text('Chapter %d' % index)
                else:
                    self.buildElement(b, chapterTitle)
                if len(chapters) < s.showChapterSummaryOnMax:
                    summary = chapter.find('./meta/summary') # @@@ Add this as adapter query
                    if summary is not None:
                        self.buildElement(b, summary)
                b._a()
                b._li()
            b._ul()
            b._div() # .chapterNavigation
            
    def buildFootNotes(self, b, article):
        u"""Build the list of footnotes with links to the position in the article where they are defined."""
        s = self.style
        chapterIndex = self.getChapterIndex(b, article)
        footnotes = article.footnotes[chapterIndex] # Get footnotes of this chapter
        if footnotes:
            b.div(class_=C.CLASS_FOOTNOTES) 
            b.h4()
            b.text(s.footnoteLabel)
            b._h4()
            b.ol() # Not displaying the index number here, how to solve with style?
            for index, footnote in enumerate(footnotes):
                b.li(fontsize=Em(0.9), color='red')
                b.a(href='#fnref:footnoteRef%d' % (index+1), name='fnref:footnote%d' % (index+1))
                # Hard copy the index number, as <ol> doesn't show now.
                b.text('%d | %s %s' % (index+1, footnote.text, s.footnoteArrow or u'↩')) # Process element, instead of plain text.
                b._a()
                b._li()
            b._ol()
            b._div() # .footnotes

