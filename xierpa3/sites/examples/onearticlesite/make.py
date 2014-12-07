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
#    make.py
#
#    Demo site for the simple "onecolumnsite" example.
#    The "run.py" program creates the files:
#        files/css/style.scss
#        files/css/style.css
#        files/oneColumnSite.html
#    from the one OneColumnSite theme instance by applying respectively the
#    CssBuilder and HtmlBuilder to the theme.
#    Each of the builders takes the information from the theme to build its
#    own type of file.
#
import webbrowser
from xierpa3.attributes import Em, Margin, Perc, Color
from xierpa3.components import Theme, Page, Column, Container
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.descriptors.media import Media
from xierpa3.descriptors.blueprint import BluePrint
from xierpa3.toolbox.transformer import TX
from xierpa3.adapters.textilefileadapter import TextileFileAdapter

# Load @fontface fonts for this example from www.webtype.com
BODYFAMILY = '"Benton Sans RE", Verdana, sans'
HEADFAMILY = '"Hermes FB Semibold", Impact, Verdana, sans'

class ExampleArticle(Column):
    
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Column.C

    ARTICLE_ID = 'programming-python'

    BLUEPRINT = BluePrint(
        # Page stuff
        pageBackgroundColor=Color('#EEE'), doc_pageBackgroundColor=u'Page background color.',
        # Responsive stuff
        minWidth=300, doc_minWidth='Column minimal width.',
        minWidthMobile=0, doc_minWidthMobile=u'Column minimal width for mobile.',
        maxWidth=700, doc_maxWidth='Column maximal width.',
        maxWidthMobile=C.AUTO, doc_maxWidthMobile='Column maximal width for mobile',
        # Column stuff
        fontFamlily=BODYFAMILY, doc_fontFamily=u'Column body font family.',
        fontSize=Em(1), doc_fontSize=u'Column body font size.',
        fontSizeMobile=Em(1.2), doc_fontSizeMobile=u'Column body font size for mobile.', 
        lineHeight=Em(1.4), doc_lineHeight=u'Column body leading.',
        margin=Margin(0, C.AUTO, 0, C.AUTO), doc_margin=u'Column margin.',
        marginMobile=0, doc_marginMobile=u'Column margin mobile', 
        color=Color('#222'), doc_color='Column text color.',
        backgroundColor=Color('#FFF'), doc_backgroundColor='Column background color.',
        width=Perc(50), doc_width=u'Column width.',
        widthMobile=C.AUTO, doc_widthMobile=u'Column width for mobile, shoud always be “auto” with the row construction.',
        padding=Em(2), doc_padding=u'Column margin in the page.',
        paddingMobile=Em(1.4), doc_paddingMobile=u'Column margin in the page for mobile.',
        # h1
        h1FontFamily=HEADFAMILY, doc_h1FontFamily=u'Column h1 font family.',
        h1FontSize=Em(1.6), doc_h1FontSize=u'Column h1 font size',
        h1LineHeight=Em(1.1), doc_h1LineHeight=u'Column h1 leading', 
        h1Color=Color('#666'), doc_h1Color=u'Column h1 color.',
        h1MarginBottom=Em(0.5), doc_h1MarginBottom=u'Column h1 margin bottom',
        # h2
        h2FontFamily=HEADFAMILY, doc_h2FontFamily=u'Column h2 font family.',
        h2FontSize=Em(1.4), doc_h2FontSize=u'Column h2 font size',
        h2LineHeight=Em(1.2), doc_h2LineHeight=u'Column h2 leading',
        h2Color=Color('#888'), doc_h2Color=u'Column h2 color.',
        h2Style=C.ITALIC, doc_h2Style=u'Column h2 style', 
        h2MarginTop=Em(1), doc_h2MarginTop=u'Column h2 margin top',
        h2MarginBottom=Em(0.5), doc_h2MarginBottom=u'Column h2 margin bottom',
        # p
        textIndent=Em(1), doc_textIndent=u'Indent of first line of paragraph.',
        textFirstIndent=0, doc_textFirstIndent=u'Indent of first paragraph after another element.',
        # p.end
        textLastIndent=0, doc_textLastIndent=u'Indent of last paragraph before another element',
        textEndMarginTop=Em(0.5), doc_textEndMarginTop=u'Margin top of last paragraph before another element.', 
        textEndMarginBottom=Em(0.5), doc_textEndMarginBottom=u'Margin bottom of last paragraph before another element.', 
        # img
        imgMarginTop=Em(0.5), doc_imgMarginTop=u'Image margin top',
        imgMarginBottom=Em(0.5), doc_imgMarginBottom=u'Image margin bottom',
        # blockquote.pullQuote
        pullQuoteFontFamily=BODYFAMILY, doc_pullQuoteFontFamily=u'Pull quote font family.',
        pullQuotePadding=Margin(Em(0.5), Em(1)), doc_pullQuotePadding=u'Pull quote padding.',
        pullQuoteSize=Em(1.2), doc_pullQuoteSize=u'Pull quote font size.',
        pullQuoteLineHeight=Em(1.3), doc_pullQuoteLineHeight=u'Pull quote line height.',
        pullQuoteMarginTop=Em(0.5), doc_pullQuoteMarginTop=u'Pull quote margin top.',
        pullQuoteMarginBottom=Em(0.5), doc_pullQuoteMarginBottom=u'Pull quote margin bottom',
        pullQuoteStyle=C.ITALIC, doc_pullQuoteStyle=u'Pull quote style', 
        pullQuoteBackgroundColor=Color('#EEE'), doc_pullQuoteBackgroundColor=u'Pull quote background color.',
        pullQuoteColor=Color('#333'), doc_pullQuoteColor=u'Pull quote color.', 
        pullQuoteBorder=None, doc_pullQuoteBorderu='Pull quote border.', #Border('solid', 2, Color('#E1E2E2')),
    )
    def buildBlock(self, b):
        u"""Build the column. Note that although the "div" suggest that it is just
        HTML building there, the method get called both with *b* as CssBuilder
        and as HtmlBuilder. Each builder will filter out the appropriate attributes and
        translates it into its own syntax. The HTML tags generated by the article
        are set in CSS by the empty statements."""
        s = self.style # Get compile style from cascading blue prints of inheriting classes.
        b.div(class_=s.classColumn, color=s.color, margin=s.margin, 
              width=s.columnWidth, maxwidth=s.maxWidth, minwidth=s.minWidth, 
              backgroundcolor=s.backgroundColor, fontfamily=s.fontFamily, 
              fontsize=s.fontSize, lineheight=s.lineHeight, padding=s.padding,
              # Remove margins on mobile, showing the column on full screen width.
              media=Media(max=self.C.M_MOBILE_MAX, margin=s.marginMobile, float=self.C.NONE,
                fontsize=s.fontSizeMobile, lineheight=s.lineHeight, padding=s.paddingMobile,
                width=s.widthMobile, maxwidth=s.maxWidthMobile, minwidth=s.minWidthMobile),
        )
        # Since the self.adapter.getArticle answers an article that already 
        # includes XHTML tags, we cannot do the styling there. In order to 
        # define the unique CSS styles, a blank document content is created 
        # for the CssBuilder to evaluate, so we have all the definitions inside 
        # div.column, in case they are used in the article.
        # Note that this is in conflict with the purpose of components, who
        # should not know about the type of builder that they are talking to.
        # In future this will be solved by supplying more default style parameters
        # to the component, that include the styles of tags that are not used
        # in the main building.
        # See also the code for components/article, which includes a _model.txt
        # document for this purpose.
        article = self.adapter.getArticle(id=self.ARTICLE_ID)
        if b.isType(self.C.TYPE_CSS):
            self.buildCssColumnTemplate(b)
        elif article is None:
            b.text('Cannot find article with id "%s" and selector "%s"' % (0, self.C.SELECTOR_FEATURED))
        else:
            # Build the headline without style attribute, as these are already defined
            # in the self.buildCssColumnTemplate call.
            b.h1(fontfamily=s.h1FontFamily, fontsize=s.h1FontSize, lineheight=s.h1LineHeight)
            b.text(article.headline)
            b._h1()
            if article.poster:
                # Build the image that came with the featured article, if it exists.
                # Make it class autowidth to solve the width="100%" incompatibility
                # between browsers.
                b.img(src=article.poster, class_=s.imgClass, maxwidth=s.imgMaxWidth,
                    minwidth=s.imgMinWidth, margintop=s.imgMarginTop,
                    marginbottom=s.imgMarginBottom)
            # Output the rest of the featured article.
            for chapterText in article.chapters:
                b.text(chapterText)
                
        # Add reference about the content of this page
        b.hr()
        b.div(class_='colophon', fontsize=Em(0.8), color=s.color, fontfamily=BODYFAMILY,
            lineheight=Em(1.4))
        b.text('The text and image selection on this page is blurb, created by Filibuster.')
        b._div()
        
        # Add reference to sponsored Webtype webfonts.
        b.a(href='//webtype.com', color=s.color, fontfamily=BODYFAMILY, fontsize=Em(0.8),
            lineheight=Em(1.4), target='external')
        b.text('The typefaces in this example %s and %s are sponsored by &lt;Webtype&gt;' % (BODYFAMILY, HEADFAMILY))
        b._a()
        b._div()
        
    def buildCssColumnTemplate(self, b):
        u"""Build the single CSS for all expected tags in an article that is answered
        by *self.adapter*. We cannot check on that here, since the content may
        vary and even is hidden by e.g. calls to a PHP adapter.""" 
        s = self.style
        b.h1(fontfamily=s.h1FontFamily, color=s.h1Color, fontsize=s.h1FontSize, 
             lineheight=s.h1LineHeight, marginbottom=s.h1MarginBottom)
        # Headling made by BlurbAdapter
        b._h1()
        b.h2(fontfamily=s.h2FontFamily, fontstyle=s.h2Style, color=s.h2Color,
             fontsize=s.h2FontSize, lineheight=s.h2LineHeight, 
             margintop=s.h2MarginTop, marginbottom=s.h2MarginBottom)
        # Headling made by BlurbAdapter
        b._h2()
        b.h3(fontfamily=s.h3FontFamily, fontstyle=s.h3Style, color=s.h3Color,
             fontsize=s.h3FontSize, lineheight=s.h3LineHeight,
             margintop=s.h3MarginTop, marginbottom=s.h3MarginBottom)
        # Headling made by BlurbAdapter
        b._h3()
        b.img(margintop=s.imageMarginTop, marginbottom=s.imageMarginBottom)
        b.p(textindent=s.textIndent, fontfamily=BODYFAMILY)
        # Main paragraphs have an indent.
        b._p()
        b.p(class_='start', textindent=s.textFirstIndent, margintop=Em(0.7))
        # The start paragraph (the element before was not a <p>) has no indent.
        b._p()
        b.p(class_='end', marginbottom=s.textLastMarginBottom,
            margintop=s.textLastMarginTop, textindent=s.textLastIndent)
        # Mark the end paragraph (the element after is not a <p>) in case something
        # special needs to be done, e.g. change the marginbottom.
        # @@@ TODO: Mark as p.end preceding <blockquote> too.
        b._p()
        b.p(class_='lead', textindent=0, fontsize=Em(1.5), lineheight=Em(1.4))
        # The lead paragraph (the element before was not a <p>) has no indent.
        b._p()
        # Italic blockquotes with an indent and backgroundcolor.
        b.blockquote(class_=self.C.CLASS_PULLQUOTE, padding=s.pullQuotePadding, 
            fontsize=s.pullQuoteSize, fontfamily=s.pullQuoteFontFamily, 
            fontstyle=s.pullQuoteStyle, lineheight=s.pullQuoteLineHeight,
            margintop=s.pullQuoteMarginTop, marginbottom=s.pullQuoteMarginBottom, 
            border=s.pullQuoteBorder,
            backgroundcolor=s.pullQuoteBackgroundColor, color=s.pullQuoteColor)
        b._blockquote()

class OneArticleSite(Theme):
    u"""The *TextColumn* generates an HTML file with a column of random blurb text. 
    Double click the generated file or drag to a browser see the result."""
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Theme.C

    TITLE = u'The Single Column Example Page.' # Use as title of window.
    XIERPA3_DEMOFONTS = "//cloud.webtype.com/css/34d3e5fe-7dee-4122-9e87-ea5ee4a90a05.css"
    URL_FONTS = [
        # Note that this package contains the a set of latest featured font, and may be changed in the future.
        # If using the font in this package, safest is to refer to the functional constant names below,
        # instead of making a direct reference to the family name.
        # Of course, taking your own account at //www.webtype.com is even better :)
        XIERPA3_DEMOFONTS, # Webtype @fontface fonts, to be used for localhost demo purposes.
    ]    
    # The single column is filled by the self.adapter article query result.
    # The default b.adapter (if nothing else is defined) is the BlurbAdapter,
    # which generates random pieces of text.

    def baseStyle(self):
        u"""Answer the single basis style that will be defined as overall CSS, before
        specific block definitions start."""
        s = ExampleArticle.BLUEPRINT
        root = self.newStyle() # Create root style
        root.addStyle('body', fontfamily=BODYFAMILY, fontsize=s.fontSize,
            backgroundcolor=s.pageBackgroundColor, lineheight=s.lineHeight)
        s.addStyle('h1, h2, h3, h4, h5, p.lead', fontfamily=HEADFAMILY)
        s.addStyle('h6', fontfamily=BODYFAMILY)
        s.addStyle('b', fontweight=self.C.BOLD)
        return root
        
    def baseComponents(self):
        u"""Create a theme site with just one single template home page. Answer a list
        of page instances that are used as templates for this site."""
        # Create an instance (=object) of components to be placed on the page.
        # Import current example site, as anchor for the article files.
        from xierpa3.sites import doingbydesign
        # Root path where to find the article Simples wiki file for this example page.
        articleRoot = TX.module2Path(doingbydesign) + '/files/articles/'
        adapter = TextileFileAdapter(articleRoot) # Preferred adapter class for articles in this site.

        column = ExampleArticle()
        container = Container(components=column)
        # Create an instance (=object) of the page, containing the navigation components.
        # The class is also the page name in the url.
        homePage = Page(class_=self.C.TEMPLATE_INDEX, components=container, adapter=adapter,
            title=self.TITLE, fonts=self.URL_FONTS)
        # Answer a list of types of pages for this site. In this case just one template.
        return [homePage]
    
    def make(self, root=None):
        u"""The instance of this class builds CSS and HTML files at the optional path *root*.
        If not defined, then the default ~/Desktop/Xierpa3Examples/[component.name] is used as export path,
        as set by Builder.DEFAULT_ROOTPATH"""
        # Create an "instance" (=object) of type "HelloWorldLayout". The type (=class) defines
        # the behavior of the object that is made by calling the class.

        # C S S
        # Create the main CSS builder instance to build the SASS/CSS part of the site.
        cssBuilder = CssBuilder()
        # Compile (=build) the SCSS to CSS and save the file in "css/style.css".
        self.build(cssBuilder) # Build from entire site theme, not just from template. Result is stream in builder.
        cssBuilder.save(self, root) 
    
        # H T M L
        # Create the main HTML builder instance to build the HTML part of the site.
        htmlBuilder = HtmlBuilder()
        # Compile the HTML and save the resulting HTML file in "helloWorld.html".
        self.build(htmlBuilder) # Build from entire site theme, not just from template. Result is stream in builder.
        # Answer the path, so we can directly open the file with a browser.
        return htmlBuilder.save(self, root)  
    
if __name__ == '__main__':
    # This construction "__name__ == '__main__'" makes this Python file only 
    # be executed when called in direct mode, such as "python make.py" in the terminal.         
    # Since no rootPath is added to make(), the file export is in ~/Desktop/Xierpa3Examples/OneColumnSite/   
    path = OneArticleSite().make()
    webbrowser.open(path)
