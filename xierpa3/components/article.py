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
from xierpa3.toolbox.transformer import TX
from xierpa3.attributes import Perc, Em, Border, Margin, Padding, Color
from xierpa3.descriptors.media import Media
from xierpa3.descriptors.blueprint import BluePrint

class ArticleColumn(Column):
    u"""Generic column for articles."""
    def getChapterIndex(self, b, article):
        return min(max(0, TX.asInt(b.e.form[self.C.PARAM_CHAPTER]) or 0), len(article.items or [])-1)
     
class Article(ArticleColumn):
    u"""The Article component is the main medium to display article content."""
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = ArticleColumn.C
    
    CHAPTERCOLOR = Color('#202020')
    SUMMARYCOLOR= CHAPTERCOLOR
    CHAPTERTITLECOLOR0 = Color('#1F1F1F')
    CHAPTERTITLECOLOR1 = CHAPTERTITLECOLOR0
    H2COLOR = Color('#828487')
    AUTHORCOLOR = H2COLOR
    CATEGORYCOLOR = H2COLOR
    LABELCOLOR = H2COLOR
    LEADCOLOR = H2COLOR
    NAMECOLOR= Color('#66696C')
    TITLECOLOR= NAMECOLOR

    # Define the basic blue print style for this type of component.
    BLUEPRINT = BluePrint( 
        # Layout stuff
        colWidth=8, doc_colWidth=u'Default amount of columns for this component.', 
        # Post
        showPoster=False, doc_showPoster=u'Boolean flag if the poster image should be shown at start of the article.',                    
        # Title stuff on the first chapter page of the article
        titleSize=Em(3.2), doc_titleSize=u'Title font size on the first chapter page of an article.',
        titleLineHeight=Em(1.2), doc_titleLineHeight=u'Title leading on the first chapter page of an article.',
        titleColor=TITLECOLOR, doc_titleColor=u'Title color on the first chapter page of an article.',
        # Name stuff on the second+ chapter page of the article
        nameSize=Em(2), doc_nameSize=u'Name font size on the second+ page of an article.',
        nameLineHeight=Em(1.2), doc_nameLineHeight=u'Name leading on the second+ page of an article.',
        nameColor=NAMECOLOR, doc_nameColor=u'Name color on the second+ page of an article.',
        # Author stuff
        authorSize=Em(1), doc_autorSize=u'Author font size near article title.',
        authorColor=AUTHORCOLOR, doc_authorColor=u'Author color near article title.',
        # Category stuff
        categorySize=Em(0.8), doc_categorySize=u'Article category font size.',
        categoryLineHeight=Em(1.2), doc_categoryLineHeight=u'Article category leading.',
        categoryColor=NAMECOLOR, doc_categoryColor=u'Article category color.',
        categoryWeight=None, doc_categoryWeight=u'Article category weight.', # Default to inherit from the default weight.
        # Chapter stuff
        chapterColor=CHAPTERCOLOR, doc_chapterColor=u'Chapter color.',
        chapterSize=Em(1.2), doc_chapterSize=u'Chapter font size.',
        chapterLineHeight=Em(1.4), doc_chapterLineHeight=u'Chapter leading.',  
        # Chapter lead stuff
        leadSize=Em(1.8), doc_leadSize=u'Chapter lead font size.',
        leadLineHeight=Em(1.2), doc_leadLineHeight=u'Chapter lead leading.',
        leadMarginBottom=Em(0.3), doc_leadMarginBottom=u'Chapter lead bottom margin.',
        leadColor=LEADCOLOR, doc_leadColor=u'Chapter lead color.',
        # Chapter first page
        chapterTitleSize0=Em(1.5), doc_chapterTitleSize0=u'Chapter title font size on first page.',
        chapterTitleColor0=CHAPTERTITLECOLOR0, doc_chapterTitleColor0=u'Chapter title color on first page.', 
        chapterTitleMarginTop0=Em(1), doc_chapterTitleMarginTop0=u'Chapter title margin top on first page.',
        chapterTitleMarginBottom0=Em(0.5), doc_chapterTitleMarginBottom0=u'Chapter title margin bottom on first page.',
        # Chapter other pages
        chapterTitleSize1=Em(2.5), doc_chapterTitleSize1=u'Chapter title font size on second+ page.',
        chapterTitleColor1=CHAPTERTITLECOLOR1, doc_chapterTitleColor1=u'Chapter title color on second+ page.', 
        chapterTitleMarginTop1=Em(1), doc_chapterTitleMarginTop1=u'Chapter title margin top on second+ page.',
        chapterTitleMarginBottom1=Em(0.5), doc_chapterTitleMarginBottom1=u'Chapter title margin bottom on second+ page.',
        # H1
        # H2
        h2Size=Em(2), doc_h2Size=u'Article h2 font size.',
        h2LineHeight=Em(1.4), doc_h2LineHeight=u'Article h2 leading.',
        h2PaddingTop=Em(1), doc_h2PaddingTop=u'Article h2 padding top.',
        h2PaddingBottom=0, doc_h2PaddingBottom=u'Article h2 padding bottom.',
        h2Color=H2COLOR, doc_h2Color=u'Article h2 color in article.',
        # H3
        h3Size=Em(2), doc_h3Size=u'Article h3 font size.', 
        h3LineHeight=Em(1.4), doc_h3LineHeight=u'Article h3 leading.',
        h3PaddingTop=Em(1), doc_h3PaddingTop=u'Article h3 padding bottom.',
        h3PaddingBottom=0, doc_h3PaddingBottom=u'Article h3 color.',
        # Chapter p stuff
        articleSize=Em(1.1), doc_articleSize=u'Article p font size.',
        articleLineHeight=Em(1.6), doc_articleLineHeight=u'Article p leading.',
        articleIndent=Em(2), doc_articleInden=u'Article p indent.',
        articleFirstIndent=0, doc_firstIndent=u'Article p first indent.',
        # Bullet list
        bulletType='disc', doc_bulletType=u'Article bullet type',
        bulletPosition='inside', doc_bulletPosition=u'Article bullet position.',
        bulletPaddingLeft=Em(2), doc_bulletPaddingLeft=u'Article bullet padding left.',
        bulletMarginTop=Em(1), doc_bulletMarginTop=u'Article bullet margin top.',
        bulletMarginBottom=0, doc_bulletMarginBottom=u'Article bullet margin bottom.',
        bulletItemMarginBottom=Em(1), doc_bulletItemMarginBottom=u'Article bullet item margin bottom.',
        # Ordered list
        numberedListType='decimal', doc_numberedListType=u'Article numbered list type', 
        numberedListPosition='inside', doc_numberedListPosition=u'Article numbered list position.',
        numberedListPaddingLeft=Em(2), doc_numberedListPaddingLeft=u'Article numbered list padding left.',
        numberedListMarginBottom=0, 
        numberedListMarginTop=Em(1),
        numberedListItemMarginBottom=Em(1),
        # Image & caption
        imgMarginTop=Em(1), 
        imgMarginBottom=Em(0.8), 
        imgPaddingTop=None, 
        imgPaddingBottom=None, 
        imgPaddingLeft=None, 
        imgPaddingRight=None, 
        imgBackgroundColor=None,
        captionFontStyle=C.ITALIC, 
        captionFontSize=Em(0.9), 
        captionMarginTop=Em(0.5),
        # Code
        codeFontFamily='Courier', 
        codeFontSize=Em(1.1), 
        codePaddingLeft=Em(1),
        codePaddingTop=Em(0.5), 
        codePaddingBottom=0,
        codeMarginTop=Em(0.5), 
        codeMarginBottom=Em(0.5),
        codeBackgroundColor=Color(C.WHITE),
    )
    def buildColumn(self, b):
        article = self.adapter.getArticle(id=b.getCurrentArticleId())
        self.buildArticle(b, article)

    def buildArticle(self, b, article):
        u"""Build the article. If there is a "/chapter-2" url parameter defined and it is in
        the range of available chapters, then show that chapter. Other values are cropped to
        min and max index of the chapter list."""
        #b.element(tag='img', class_=self.CLASS_AUTOWIDTH, margintop=Em(1), marginbottom=Em(1))
        if b.isType(('css', 'sass')): # @@@ Clean up, using model article?
            self.buildArticleTop(b, article, 0) # Separate CSS for first chapter and the rest.
            self.buildArticleTop(b, article, 1)
            self.buildArticleStyle(b) # Build the CSS style template of an article here
        elif article.items:
            chapterIndex = self.getChapterIndex(b, article)
            self.buildArticleTop(b, article, chapterIndex)
            # @@@@
            #chapter = b.adapter.getChapterByIndex(chapterIndex, component=article)
            #if chapter is not None:
            #    self.buildElement(b, chapter) # Render the indexed chapter element as builder calls.
        elif article.text:
            b.text(article.text)
        else:
            b.text('Cannot find article')
            
    def buildArticleTop(self, b, article, chapterIndex):
        u"""Build the top of the article: type, title, author, etc. on the first page, if index is <b>0</b>.
        For all other pages build a smaller version of the top."""
        s = self.style
        class_ = self.C.CLASS_ARTICLETOP
        b.div(class_=class_, float=self.C.LEFT, width=Perc(100), paddingtop=Em(0.5))
        # Poster image
        if chapterIndex == 0 and s.showPoster:
            b.img(class_=self.C.CLASS_AUTOWIDTH, src=article.poster)
        # Article category
        if chapterIndex == 0 and article.category: # Text on text
            b.a(href='/%s-%s' % (self.C.PARAM_CATEGORY, article.category))
            b.h5(fontsize=s.categorySize, lineheight=s.categoryLineHeight, color=s.categoryColor, 
                fontweight=s.categoryWeight, margintop=Em(1), display=self.C.BLOCK)
            b.text(article.category)
            b._h5()
            b._a()
        # Article title or name (on respectively the first chapter page or the rest of the pages.
        if chapterIndex == 0: # Show large title on the chapter first page of the article
            b.h2(class_='articleTitle0', fontsize=s.titleSize, lineheight=s.titleLineHeight, 
                color=s.titleColor, marginbottom=Em(0.2), display=self.BLOCK)
            b.text(article.name)
            b._h2()
        else: # Show smaller title on the rest of the pages
            b.h2(class_='articleTitle1', fontsize=s.nameSize, lineheight=s.nameLineHeight, 
                color=s.nameColor, marginbottom=Em(0.2), display=self.BLOCK)
            b.text(article.name)
            b._h2()
        # Author
        if chapterIndex == 0 and article.author: # Test if there is an author defined.
            b.a(href='/%s-%s' % (self.PARAM_AUTHOR, article.author))
            b.h5(fontsize=s.authorSize, fontweight=s.authorWeight, authorcolor=s.authorColor,
                display=self.BLOCK)
            b.text('By %s' % article.author)
            b._h5()
            b._a()
        # Chapter title
        chapterTitle = 'AAAAAAA' #b.adapter.getChapterTitleByIndex(chapterIndex, component=article)
        if chapterIndex == 0: # Show large title on the chapter first page of the article
            b.h3(class_='chapterTitle0', fontsize=s.chapterTitleSize0, color=s.chapterTitleColor0,
                 margintop=s.chapterTitleMarginTop0, marginbottom=s.chapterTitleMarginBottom0)
            if chapterTitle is not None: 
                b.text(chapterTitle)
            b._h3()
        else: # Other chapter pages
            b.h3(class_='chapterTitle1', fontsize=s.chapterTitleSize1, color=s.chapterTitleColor1,
                 margintop=s.chapterTitleMarginTop1, marginbottom=s.chapterTitleMarginBottom1)
            if chapterTitle is not None: 
                b.text(chapterTitle)
            b._h3()
        b._div(comment=class_)
                
    def buildArticleStyle(self, b):
        s = self.style
        # SVG demo
        b.div(class_=self.CLASS_CHAPTER, color=s.chapterColor)
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
        b.p(class_=self.CLASS_FIRST, textindent=s.articleFirstIndent)
        b._p()
        # <p class="... last">
        b.p(class_=self.CLASS_LAST)
        b._p()
        # <lead>
        b.p(class_=self.CLASS_LEAD, fontsize=s.leadSize, lineheight=s.leadLineHeight, 
            color=s.leadColor, marginbottom=s.leadMarginBottom, 
            textindent=s.articleFirstIndent)
        self.buildPStyle(b)
        b._p()
        # <b>
        b.b(fontweight=self.BOLD)
        b._b()
        # <blockquote>
        b.blockquote(borderleft=s.blockQuoteBorderLeft or Border('solid', '4px', '#CCC'), 
            margin=s.blockQuoteMargin or Margin(Em(1.5), 10), 
            lineheight=s.blockQuoteLineHeight or Em(1.4), fontstyle=s.blockQuoteStyle or self.ITALIC,
            padding=s.blockQuotePadding or Padding(Em(0.5), 10), 
            color=s.blockQuoteColor or Color('#828487'))
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
        # <div class="imgBlock"><img/><div class="caption">...</div></div>
        b.div(class_=self.CLASS_IMAGEBLOCK, backgroundcolor=s.imgBackgroundColor, 
            margintop=s.imgMarginTop, marginbottom=s.imgMarginBottom,
            paddingtop=s.imgPaddingTop, paddingbottom=s.imgPaddingBottom,
            paddingleft=s.imgPaddingLeft, paddingright=s.imgPaddingRight,)
        b.img()
        b.div(class_=self.CLASS_CAPTION, fontfamily=s.captionFontFamily, fontsize=s.captionFontSize,
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
        b.sup(class_=self.CLASS_FOOTNOTE, top=s.footnoteTop or Em(-0.5), 
            fontsize=s.footnoteFontSize or Em(0.8), position=s.footnotePosition or self.RELATIVE,
            verticalalign=s.footnoteVerticalAlign or self.BASELINE)
        b._sup()
        b.em(fontweight=s.emWeight or self.BOLD)
        b._em()
    
class ArticleSideBar(ArticleColumn):
    BLUEPRINT = BluePrint( 
        # Layout stuff
        colWidth=4, # Default amount of columns for this component   
        # Chapter navigation
        showChapterNavigation=True, 
        chapterLabel='Chapters',
        chapterNameSize=Em(1.2),
        showChapterSummaryOnMax=10, # Not show summary if more than 10 chapters
        # Footnotes
        showFootNotes=True, 
        footnoteLabel='Footnotes', 
    )
    def getArticleUrlId(self, b):
        return b.e.form[self.C.PARAM_ARTICLE]
    
    def buildColumn(self, b):
        u"""Build the column of the article, as indicated in the urt."""
        article = self.adapter.getArticle(id=self.getArticleUrlId(b))
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
        b.div(class_=self.CLASS_FOOTNOTES, marginbottom=Em(0.5))
        b.h4(fontsize=Em(1.1))
        b._h4()
        b._div(comment=self.CLASS_FOOTNOTES)  
        
        # <div class="mobileChapterNavigation">
        b.div(class_=self.C.CLASS_MOBILECHAPTERNAVIGATION, marginbottom=Em(0.5), display=self.C.NONE,
            media=Media(max=self.C.M_MOBILE_MAX, display=self.C.BLOCK)
        )
        b.ul()
        b.li(backgroundcolor=s.mobileChapterButtonColor or Color('#444'))
        # <a>Chapter name</a>
        b.a(fontsize=s.summaryNameSize, color=s.mobileChapterButtonColor or Color(self.C.WHITE))
        b.h2(fontsize=Em(2), lineheight=Em(1.2),
             marginbottom=Em(0.2), margintop=Em(0.2), padding=Em(0.5))
        b._h2()
        b._a()
        b._li()
        b._ul()
        b._div(comment=self.C.CLASS_MOBILECHAPTERNAVIGATION) # Article mobile chapter navigation
        
        # <div class="chapterNavigation">
        b.div(class_=self.C.CLASS_CHAPTERNAVIGATION, marginbottom=Em(0.5), 
            display=s.mobileContainerDisplay,
            media=Media(max=self.C.M_MOBILE_MAX, display=self.C.NONE)
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
        b._div(comment=self.C.CLASS_CHAPTERNAVIGATION) # Article chapter navigation
    
    def buildMobileChapterNavigation(self, b, article):
        s = self.style
        chapters = article.items
        if chapters and len(chapters) > 1:
            b.div(class_=self.C.CLASS_MOBILECHAPTERNAVIGATION)
            b.ul()
            for index, chapter in enumerate(chapters):
                b.li() 
                b.a(class_=self.C.CLASS_NAME, 
                    href='/%s-%s/%s-%s' % (self.C.PARAM_ARTICLE, article.id, self.C.PARAM_CHAPTER, index), 
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
            b.div(class_=self.C.CLASS_CHAPTERNAVIGATION)
            b.h4()
            b.text(s.chapterLabel)
            b._h4()
            b.ul()
            for index, chapter in enumerate(chapters):
                b.li(margintop=Em(0.5))
                b.a(class_=self.C.CLASS_NAME, 
                    href='/%s-%s/%s-%s' % (self.C.PARAM_ARTICLE, article.id, self.C.PARAM_CHAPTER, index), 
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
        if article.footnotes:
            footnotes = article.footnotes[chapterIndex] # Get footnotes of this chapter
            if footnotes:
                b.div(class_=self.C.CLASS_FOOTNOTES) 
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
    
