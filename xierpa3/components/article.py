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
#    Side knowledge: Scale images on OSX by:
#    http://lifehacker.com/5962420/batch-resize-images-quickly-in-the-os-x-terminal
#    sips -Z 640 *.jpg
#
from xierpa3.components import Column
from xierpa3.toolbox.transformer import TX
from xierpa3.attributes import Perc, Em, Border, Margin, Padding, Color
from xierpa3.descriptors.media import Media
from xierpa3.descriptors.blueprint import BluePrint

class ArticleColumn(Column):
    u"""Generic column for articles."""
    def getChapterIndex(self, b, articleData):
        return min(max(0, TX.asInt(b.e.form[self.C.PARAM_CHAPTER]) or 0), len(articleData.items or [])-1)
     
class Article(ArticleColumn):
    u"""The Article component is the main medium to display article content."""
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = ArticleColumn.C
    
    # Default parameters for the article layout, to make sure that the default 
    # behavior makes reasonable good  typography. Each of these values can be redefined
    # by changing the BluePrint parameters in the Article() constructor call.
    # These values can be change either through inheriting from the Article class,
    # or by altering the BluePrint values in the Article(...) constructor call.
    CHAPTERCOLOR = Color('#202020')
    SUMMARYCOLOR= CHAPTERCOLOR
    CHAPTERTITLECOLOR0 = Color('#1F1F1F')
    CHAPTERTITLECOLOR1 = CHAPTERTITLECOLOR0
    H1COLOR = Color('#333')
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
        gutter=8, doc_gutter=u'Gutter width between columns.',
        # Chapter behavior
        splitChapters=True, doc_splitChapters=u'Boolean flag if the chapters should be listening to url chapter index.', 
        # Poster
        showPoster=False, doc_showPoster=u'Boolean flag if the poster image should be shown at start of the article.',                    
        # Blog response
        blogResponse=True, doc_blogResponse=u'Boolean flag if a blog response form should be added if @article.blogresponse@ is also @True@.',
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
        chapterSizeMobile=Em(2), doc_chapterSizeMobile=u'Chapter font size for mobile.',
        chapterLineHeight=Em(1.4), doc_chapterLineHeight=u'Chapter leading.',  
        chapterLineHeightMobile=Em(1.4), doc_chapterLineHeightMobile=u'Chapter leading for mobile.',
        # Chapter lead stuff
        leadSize=Em(1.4), doc_leadSize=u'Chapter lead font size.',
        leadLineHeight=Em(1.2), doc_leadLineHeight=u'Chapter lead leading.',
        leadMarginTop=Em(0.5), doc_leadMarginTop=u'Chapter lead margin top.',
        leadMarginBottom=Em(0.5), doc_leadMarginBottom=u'Chapter lead margin bottom.',
        leadColor=LEADCOLOR, doc_leadColor=u'Chapter lead color.',
        leadWeidth=None, doc_leadWeight=u'Chapter lead font weight.',
        leadStyle=None, doc_leadStyle=u'Chapter lead font style.',
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
        h1Size=Em(2.5), doc_h1Size=u'Article h1 font size.',
        h1FontSize=None, doc_h1FontStyle=u'Article h1 font style.',
        h1FontWeight=None, doc_h1FontWeight=u'Article h1 font weight.',
        h1LineHeight=Em(1.4), doc_h1LineHeight=u'Article h1 leading.',
        h1PaddingTop=Em(1), doc_h1PaddingTop=u'Article h1 padding top.',
        h1PaddingBottom=0, doc_h1PaddingBottom=u'Article h1 padding bottom.',
        h1Color=H1COLOR, doc_h1Color=u'Article h1 color in article.',
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
        articleIndent=Em(1), doc_articleInden=u'Article p indent.',
        articleFirstIndent=0, doc_firstIndent=u'Article p first indent.',
        # Bullet list
        bulletType='disc', doc_bulletType=u'Article bullet type',
        bulletPosition=C.OUTSIDE, doc_bulletPosition=u'Article bullet position. One of (inside, outside).',
        bulletPaddingLeft=Em(1), doc_bulletPaddingLeft=u'Article bullet padding left.',
        bulletMarginBottom=0, doc_bulletMarginBottom=u'Article bullet margin bottom.',
        bulletMarginTop=Em(0.5), doc_bulletMarginTop=u'Article bullet margin top.',
        bulletItemMarginBottom=Em(0.5), doc_bulletItemMarginBottom=u'Article bullet item margin bottom.',
        # Ordered list
        numberedListType='decimal', doc_numberedListType=u'Article numbered list type', 
        numberedListPosition=C.OUTSIDE, doc_numberedListPosition=u'Article numbered list position. One of (inside, outside).',
        numberedListPaddingLeft=Em(1), doc_numberedListPaddingLeft=u'Article numbered list padding left.',
        numberedListMarginBottom=0, 
        numberedListMarginTop=Em(0.5),
        numberedListItemMarginBottom=Em(0.5),
        # Image & caption block
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
        # Plain Textile image with class autoWidth, not indenting.
        # Full width, growing until maximal size of image. Then centered on column width.
        imgAutoWidthMarginLeft=C.AUTO, doc_imgAutoWidthMarginLeft=u'img.autoWidth margin left.',
        imgAutoWidthMarginRight=C.AUTO, doc_imgAutoWidthMarginRight=u'img.autoWidth margin right.',
        imgAutoWidthTextIndent=0, doc_imgAutoWidthTextIndent=u'img.autoWidth text indent.',
        imgAutoWidthDisplay=C.BLOCK, doc_imgAutoWidthDisplay=u'img.autoWidth display.',
        # Code
        preFontFamily='Courier', doc_preFontFamily=u'Font family of pre code blocks.',
        preFontSize=Em(1.1), doc_preFontSize=u'Font size of pre code blocks.', 
        prePaddingLeft=Em(1), doc_prePaddingLeft=u'Padding left of pre code blocks.',
        prePaddingTop=Em(0.5), doc_prePaddingTop=u'Padding top of pre code blocks.', 
        prePaddingBottom=Em(0.5), doc_prePaddingBottom=u'Padding bottom of pre code blocks.',
        preMarginTop=Em(0.5),  doc_preMarginTop=u'Margin left of pre code blocks.',
        preMarginBottom=Em(0.5), doc_preMarginBottom=u'Margin bottom of pre code blocks.',
        preColor=Color(Color(0)), doc_preColor=u'Color of pre code blocks.',
        preBackgroundColor=Color(Color('#DDD')), doc_preBackgroundColor=u'Background color of pre code blocks.',
    )
    def buildBlock(self, b):
        self.buildColumn(b)
        
    def buildColumn(self, b):
        u"""Build the article column. The article data is derived from the adapter by matching with the hard coded url pattern
        (@$url@ field in the article source) or with the @b.getCurrentArticleId()@, which is @/article-[articleId]@ in the
        url of the page."""
        s = self.style
        articleData = self.adapter.getArticle(id=b.getCurrentArticleId(), url=b.e.path)
        b.div(class_=self.getClassName(), width=Perc(70), #s.width, 
              float=self.C.LEFT,
              paddingRight=s.gutter, #marginright=s.gutter, # Gutter between main column and article side bar.
              marginright=0,
              media=Media(max=self.C.M_MOBILE_MAX, width=self.C.AUTO, float=self.C.NONE,
                    paddingleft=Em(0.5), paddingright=Em(0.5),
                    marginright=0),
        )
        if articleData is None: 
            # If not article defined, then this must be a call for building the CSS.
            self.buildArticleStyle(b)
        else:
            self.buildArticleData(b, articleData)
            
        # Build blog response form, if required.
        if s.blogResponse and articleData is not None and articleData.blogresponse == 'True':
            
            b.div(class_=self.C.CLASS_BLOGRESPONSE, width=Perc(100),
                  backgroundcolor=Color('#888'))
            # TODO: Add blog response form here.
            b.text('[Develop Blog Response here] ' * 20)
            b._div(comment=self.C.CLASS_BLOGRESPONSE)
        b._div()
        
    def buildArticleData(self, b, articleData):
        u"""Build the article. If there is a "/chapter-2" url parameter defined and it is in
        the range of available chapters, then show that chapter. Other values are cropped to
        min and max index of the chapter list."""
        s = self.style
        #b.element(tag='img', class_=self.C.CLASS_AUTOWIDTH, margintop=Em(1), marginbottom=Em(1))
        if b.isType(('css', 'sass')): 
            if articleData is None: # No specific article id specified, use _mode.txt file
                # as model for calculating the SASS/CSS
                articleData = self.adapter.getModelData()
            self.buildArticleTop(b, articleData, 0) # Separate CSS for first chapter and the rest.
            self.buildArticleTop(b, articleData, 1)
            self.buildArticleStyle(b) # Build the CSS style template of an article here
        elif articleData is None:
            b.text('Cannot find article')
        elif b.e.form[self.C.PARAM_EDIT]: # and b.e.isLoggedIn():
            if articleData.source is not None:
                b.div(class_=self.C.CLASS_CHAPTER, width=self.C.NONE, contenteditable=self.C.TRUE,
                    float=self.C.NONE)           
                # Form and button bar is already generated by the page.
                b.text(articleData.source.replace('\n', '<br/>\n'))
                b._div()
            else:
                b.error('Cannot find source of article "%s"' % articleData.id)
        elif articleData.items:
            # Collect the chapter indices to show. If splitting chapter, we need a list of
            # the one chapter index that is indicated by the url with /chapter-2
            if s.splitChapters:
                chapterIndices = [self.getChapterIndex(b, articleData)]
            else:
                chapterIndices = range(len(articleData.items))
            # Build the chapters in the index list
            for chapterIndex in chapterIndices:
                # Build the top of the article, making a difference between the first chapter
                # and the chapters with index >= 1
                self.buildArticleTop(b, articleData, chapterIndex)
                b.div(class_=self.C.CLASS_CHAPTER, width=self.C.NONE, float=self.C.NONE)           
                chapter = self.adapter.getChapterByIndex(chapterIndex, article=articleData)
                if isinstance(chapter, basestring): # Chapter result can be converted to plain output.
                    b.text(chapter)
                elif chapter is not None: # Still a tree object. Build the element nodes.
                    self.buildElement(b, chapter) # Render the indexed chapter element as builder calls.
                b._div(comment=self.C.CLASS_CHAPTER)
        elif articleData.text:
            b.text(articleData.text)
                    
    def buildArticleTop(self, b, articleData, chapterIndex):
        u"""Build the top of the article: type, title, author, etc. on the first page, if index is <b>0</b>.
        For all other pages build a smaller version of the top."""
        s = self.style
        class_ = self.C.CLASS_ARTICLETOP
        b.div(class_=class_, float=self.C.LEFT, width=Perc(100), paddingtop=Em(0.5),
              media=Media(max=self.C.M_MOBILE_MAX, width=self.C.AUTO, float=self.C.NONE,
                paddingleft=0, paddingright=0),
        )
        if articleData is not None:
            # Poster image
            if chapterIndex == 0 and s.showPoster:
                b.img(class_=self.C.CLASS_AUTOWIDTH, src=articleData.poster,
                    marginleft=self.C.AUTO, marginright=self.C.AUTO)
            # Article category
            if chapterIndex == 0 and articleData.category: # Text on text
                b.a(href='/%s-%s' % (self.C.PARAM_CATEGORY, articleData.category))
                b.h5(fontsize=s.categorySize, lineheight=s.categoryLineHeight, color=s.categoryColor, 
                    fontweight=s.categoryWeight, margintop=Em(1), display=self.C.BLOCK)
                b.text(', '.join(articleData.category))
                b._h5()
                b._a()
    
            # Article title or name (on respectively the first chapter page or the rest of the pages.
            title = articleData.name or articleData.title
            if title:
                if chapterIndex == 0: # Show large title on the chapter first page of the article
                    b.h2(class_='articleTitle0', fontsize=s.titleSize, lineheight=s.titleLineHeight, 
                        color=s.titleColor, marginbottom=Em(0.2), display=self.C.BLOCK)
                    b.text(title)
                    b._h2()
                else: # Show smaller title on the rest of the pages
                    b.h2(class_='articleTitle1', fontsize=s.nameSize, lineheight=s.nameLineHeight, 
                        color=s.nameColor, marginbottom=Em(0.2), display=self.C.BLOCK)
                    b.text(title)
                    b._h2()
            # Author
     
            if chapterIndex == 0 and articleData.author: # Test if there is an author defined.
                b.h5(fontsize=s.authorSize, fontweight=s.authorWeight, authorcolor=s.authorColor,
                    display=self.C.BLOCK)
                b.a(href='/%s-%s' % (self.C.PARAM_AUTHOR, articleData.author))
                b.text('By %s' % articleData.author)
                b._a()
                if articleData.authorEmail:
                    b.text(' ' + articleData.authorEmail)
                b._h5()
            # Chapter title
            """
            chapterTitle = self.adapter.getChapterTitleByIndex(chapterIndex, articleData)
            if chapterTitle:
                if chapterIndex == 0: # Show large title on the chapter first page of the article
                    b.h3(class_='chapterTitle0', fontsize=s.chapterTitleSize0, color=s.chapterTitleColor0,
                         margintop=s.chapterTitleMarginTop0, marginbottom=s.chapterTitleMarginBottom0)
                    b.text(chapterTitle)
                    b._h3()
                else: # Other chapter pages
                    b.h3(class_='chapterTitle1', fontsize=s.chapterTitleSize1, color=s.chapterTitleColor1,
                         margintop=s.chapterTitleMarginTop1, marginbottom=s.chapterTitleMarginBottom1)
                    b.text(chapterTitle)
                    b._h3()
            """
        b._div(comment=class_)
                
    def buildArticleStyle(self, b):
        s = self.style
        # SVG demo
        b.div(class_=self.C.CLASS_CHAPTER, color=s.chapterColor)
        # TODO: Should move from here. Make sure that svgExamples get SCSS builder calls.
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
        self._buildPStyle(b)
        b._p()
        # <p class="... first">
        b.p(class_=self.C.CLASS_FIRST, textindent=s.articleFirstIndent)
        b._p()
        # <p class="... last">
        b.p(class_=self.C.CLASS_LAST)
        b._p()
        # <lead>
        b.p(class_=self.C.CLASS_LEAD, fontsize=s.leadSize, lineheight=s.leadLineHeight,
            fontweight=s.leadWeight, fontstyle=s.leadStyle, 
            color=s.leadColor, marginbottom=s.leadMarginBottom, margintop=s.leadMarginTop,
            textindent=s.articleFirstIndent)
        self._buildPStyle(b)
        b._p()
        # <b>
        b.b(fontweight=self.C.BOLD)
        b._b()
        # <blockquote>
        b.blockquote(borderleft=s.blockQuoteBorderLeft or Border('solid', '4px', '#CCC'), 
            margin=s.blockQuoteMargin or Margin(Em(1.5), 10), 
            lineheight=s.blockQuoteLineHeight or Em(1.4), fontstyle=s.blockQuoteStyle or self.C.ITALIC,
            padding=s.blockQuotePadding or Padding(Em(0.5), 10), 
            color=s.blockQuoteColor or Color('#828487'))
        b._blockquote()
        # <em>
        b.em(fontstyle=s.emFontStyle, fontweight=s.emFontWeight,
            color=s.emColor, fontfamily=s.emFontFamily)
        b._em()
        # <pre>
        b.pre(fontstyle=s.preFontStyle, fontweight=s.preFontWeight, fontsize=s.preFontSize,
            color=s.preColor, fontfamily=s.preFontFamily, paddingtop=s.preMarginTop,
            paddingbottom=s.prePaddingBottom, paddingleft=s.prePaddingLeft,
            paddingright=s.prePaddingRight, backgroundcolor=s.preBackgroundColor,
            margintop=s.preMarginTop, marginbottom=s.preMarginBottom,
        )
        b._pre()
        # <div class="imgBlock"><img/><div class="caption">...</div></div>
        b.div(class_=self.C.CLASS_IMAGEBLOCK, backgroundcolor=s.imgBackgroundColor, 
            margintop=s.imgMarginTop, marginbottom=s.imgMarginBottom,
            paddingtop=s.imgPaddingTop, paddingbottom=s.imgPaddingBottom,
            paddingleft=s.imgPaddingLeft, paddingright=s.imgPaddingRight,)
        b.img()
        b.div(class_=self.C.CLASS_CAPTION, fontfamily=s.captionFontFamily, fontsize=s.captionFontSize,
            color=s.captionColor, fontstyle=s.captionFontStyle, 
            margintop=s.captionMarginTop)
        b._div() # .caption
        b._div() # .imageBlock
        # <img> Plain Textile img tag, generated by !(autoWidth)--url--!
        b.img(class_=self.C.CLASS_AUTOWIDTH, marginleft=s.imgAutoWidthMarginLeft, 
            marginright=s.imgAutoWidthMarginRight, margintop=s.imgMarginTop,
            marginbottom=s.imgMarginBottom, textindent=s.imgAutoWidthTextIndent, 
            display=s.imgAutoWidthDisplay)
        # <ul><li>...</li></ul>
        b.ul(liststyletype=s.bulletType, liststyleimage=s.bulletImage, 
            liststyleposition=s.bulletPosition, paddingleft=s.bulletPaddingLeft,
            marginbottom=s.bulletMarginBottom, margintop=s.bulletMarginTop)
        self._buildLiStyle(b)
        b._ul()
        # <ol><li>...</li></ol>
        b.ol(liststyletype=s.numberedListType,  
            liststyleposition=s.numberedListPosition, paddingleft=s.numberedListPaddingLeft,
            marginbottom=s.numberedListMarginBottom, margintop=s.numberedListMarginTop)
        self._buildLiStyle(b)
        b._ol()
        
        b._div() # Article chapter
             
    def _buildLiStyle(self, b):
        u"""Private method. Build the style parameters of a bullet list."""
        # <li> in side article XML
        s = self.style
        b.li(marginbottom=s.bulletItemMarginBottom)
        b._li()
               
    def _buildPStyle(self, b):
        u"""Private method. Build the style parameters of a paragraph tag."""
        # <footnote> inside article XML
        s = self.style
        b.sup(class_=self.C.CLASS_FOOTNOTE, top=s.footnoteTop or Em(-0.5), 
            fontsize=s.footnoteFontSize or Em(0.8), position=s.footnotePosition or self.C.RELATIVE,
            verticalalign=s.footnoteVerticalAlign or self.C.BASELINE)
        b._sup()
        b.em(fontweight=s.emWeight or self.C.BOLD)
        b._em()
    
class ArticleSideBar(ArticleColumn):
    u"""The *ArticleSideBar* class implements a component that can show meta information
    of the current article, such as the chapter navigation (if the boolean flag
    @self.style.splitChapters@ is set to @true@), or links to the @article.featured@
    articles. The standard functions in the @ArticleSideBar@ can be turned on/off by
    boolean style flags. E.g. @self.style.showChapterNavigation@."""
    
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = ArticleColumn.C
    
    BLUEPRINT = BluePrint( 
        # Layout stuff
        colWidth=4, # Default amount of columns for this component  
        width=Perc(20), doc_width=u'Width of the main column inside the row.', 
        widthMobile=Perc(100), doc_widthMobile=u'Width of the main column inside the row for mobile.',
        # Column
        padding=Em(0.35), doc_padding=u'Padding of the main column container.',
        backroundColor=Color('white'), doc_backgroundColor=u'Background color of side bar container.',
        # Chapter navigation
        showChapterNavigation=True, doc_showChapterNavigation=u'Boolean flag to indicate that chapter navigation must be shown. If the article source has chapters, but the main article component @article.style.splitChapters@ is @False@, then in-page navigation will be made.',
        chapterLabel='Chapters', doc_chapterLabel=u'Title of chapter navigation, shown as h2 heading.',
        chapterNameSize=Em(1.2), doc_chapterNameSize=u'Font size of chapter title.',
        showChapterSummaryOnMax=10, # Not show summary if more than 10 chapters
        mobileChapterButtonColor=Color(C.WHITE), doc_mobileChapterButtonColor=u'Color of chapter button for mobile.',
        mobileChapterButtonBackgroundColor=Color('#444'), doc_mobileChapterButtonBackgroundColor=u'Background color of chapter button for mobile.',
    )
    def getArticleUrlId(self, b):
        u"""Answer the url parameter of the current page from @b.e.form[self.C.PARAM_ARTICLE]@."""
        return b.e.form[self.C.PARAM_ARTICLE] # /article-xxx
    
    def buildColumn(self, b): 
        u"""Build meta information from the article. @@@ Add to style that calling site can change
        the order."""
        s = self.style
        articleData = self.adapter.getArticle(id=b.getCurrentArticleId(), url=b.e.path)
        b.div(class_=self.getClassName(), width=s.width, float=self.C.LEFT,
            backgroundcolor=s.backroundColor,
            padding=s.padding,
            media=Media(max=self.C.M_MOBILE_MAX, width=s.widthMobile,
                display=self.C.BLOCK, float=self.C.NONE),
        )
        if articleData is None:
            self.buildArticleSideBarStyle(b)
        else:
            self.buildArticleFeatures(b, articleData)
        #if s.showChapterNavigation:
            #self.buildMobileChapterNavigation(b, articleData)
            #self.buildChapterNavigation(b, articleData)
        #if s.showFootNotes:
        #    self.buildFootNotes(b, article)
        b._div(comment=self.getClassName())
            
    def buildArticleFeatures(self, b, articleData):
        u"""Build the links to the featured article of the current article as
        stored in @article.featured@."""
        s = self.style
        featuredArticles = []
        if articleData is not None and articleData.featured:
            for featured in articleData.featured:
                featuredArticle = self.adapter.getArticle(id=featured)
                # Check if found and not referring to cyrrent article.
                if not featuredArticle in (None, articleData):
                    featuredArticles.append(featuredArticle)
        # If there are featured articles
        if featuredArticles:
            b.h3()
            b.text('Featured')
            b._h3()
            for featuredArticle in featuredArticles:
                b.p()
                b.a(href='%s-%s' % (self.C.PARAM_ARTICLE, featuredArticle.id))
                b.text(featuredArticle.title)
                b._a()
                b._p()
                
    def buildArticleSideBarStyle(self, b): 
        u"""Build the styles for the articles side bar.  # @@@ Clean up, using model for article side bar?"""
        s = self.style
        # <h2>Featured</h2>
        b.h3()
        
        b._h3()
        # <ul><li>...</li></ul>
        b.ul()
        b.li(backgroundcolor=s.mobileChapterButtonColor)
        # <a>Chapter name</a>
        b.h2(fontsize=Em(2), lineheight=Em(1.2),
             marginbottom=Em(0.2), margintop=Em(0.2))
        b.a(fontsize=s.summaryNameSize, color=s.mobileChapterButtonColor)
        b._a()
        b._h2()
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
            
    def XXXbuildFootNotes(self, b, article):
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
    
