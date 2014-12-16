# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#        xierpa server
#        (c) 2006-2013  buro@petr.com, www.petr.com, www.xierpa.com, www.xierpad.com
#
#        X I E R P A 3
#        No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#        page.py
#
import re
import codecs

class Page(object):

    FINDCODES = re.compile('\[\[([a-z]*)\]\]')
    
    def __init__(self, path):
        self.path = path # Template path
        self.id = path.split('/')[-1].split('.')[0]
        self.links = [] # Storage for links to other pages in the site
        self.html = None
        # Indices kept for <chapterIndex/>, <articleIndex/>, <h1Index/> and <h2Index/>
        self.chapterIndex = 1
        self.articleIndex = 1
        self.h1Index = 1
        self.expandIndex = 1
        
    def addLink(self, url):
        self.links.append(url)
                    
    def getTemplate(self):
        print '====', self.path
        # Read the template
        f = codecs.open(self.path, encoding='utf-8', mode='r+')
        html = f.read()
        f.close()
        return html
        
    def build(self, tree):
        hook = 'build_' + self.id
        if hasattr(self, hook):
            getattr(self, hook)(self.id, tree)
        else:
            print '[### Cannot find method for template "%s"]' % hook
    
    def save(self, dirPath):
        if self.html is not None:
            f = codecs.open(dirPath + '/' + self.path.split('/')[-1], encoding='utf-8', mode='w')
            f.write(self.html)
            f.close()
    
    def error(self, s):
        return '<span style="color:red;font-weight:bold;">[[Error: %s]]</span>' % `s`.replace('<','').replace('>','')
        
    # T E M P L A T E S
            
    def build_home(self, id, tree):
        # Read the HTML template file, indicated by self.path, and do the transformation
        # of components that are coded by <contentname/> in the template.
        print 'Build from "%s" template.' % id
        self.html = self.getTemplate()
        for component in self.FINDCODES.findall(self.html):
            # Dispatch the codes and test if there is method to build that part.
            hook = 'component_' + component
            if hasattr(self, hook):
                replacement = getattr(self, hook)(tree)
                if replacement is not None:
                    self.html = self.html.replace('[[' + component + ']]', replacement)
            else:
                print '[### Cannot find method for component "%s"]' % component
    
    build_images = build_home
    build_index = build_home
    build_literature = build_home
    build_words = build_home
    
    # G E T S
        
    def text(self, element, default=None):
        if element is not None:
            text = element.text
        elif element is None:
            text = None
        else:
            text = default
        return text

    def getAuthor(self, tree, ignore=False):
        surname = self.text(tree.find('.//meta/author/surname'))
        preposition = self.text(tree.find('.//meta/author/preposition'))
        name = self.text(tree.find('.//meta/author/name'))
        if not name:
            if ignore:
                author = ''
            else:
                author = self.error('NO AUTHOR')
        else:
            author = surname + ' ' + (preposition or '') + ' ' + name
        return author
    
    def getTitleText(self, tree, ignore=False):
        title = tree.find('.//meta/title')
        if title is not None:
            return title.text
        return 'Untitled'
    
    def getTitle(self, tree, ignore=False):
        return self.buildElement(tree.find('.//meta/title'))    
    
    def getPostTitle(self, tree):
        return self.buildElement(tree.find('.//meta/posttitle'))

    def getSubTitle(self, tree):
        return self.buildElement(tree.find('.//meta/subtitle'))

    def getWebSite(self, tree, ignore=False):
        return self.text(tree.find('.//meta/website')) or ''
        
    def getPublicationDate(self, tree, ignore=False):
        day = self.text(tree.find('.//meta/publicationdate/day'))
        month = self.text(tree.find('.//meta/publicationdate/month'))
        year = self.text(tree.find('.//meta/publicationdate/year'), 2014)
        if day or month:
            return '%s/%s/%s' % (day, month, year)
        season = self.text(tree.find('.//meta/publicationdate/season'))
        if season:
            return '%s %s' % (season, year)
        if not ignore:
            return self.error('NO PUBLICATION DATE')
        return '' 
        
    def getImages(self, tree):
        return tree.findall('.//image')
    
    def getLiteratureReferences(self, tree):
        return tree.findall('.//references/*')
    
    def getDefinitions(self, tree):
        return tree.findall('.//definitions/*')
                    
    # H O M E  C O M P O N E N T S
    
    def component_title(self, tree):
        return '%s: %s' % (self.getTitleText(tree), self.id.capitalize())
    
    def component_homelink(self, tree):
        return '<a href="home.html">Home</a>'
        
    def component_navigation(self, tree):
        result = ['<ol>']
        for link in self.links:
            result.append('<li><a href="%s">%s</a></li>' % (link, link.replace('.html', '').capitalize()))
        result.append('</ol>')
        return '\n'.join(result)
    
    def component_mobilenavigation(self, tree):
        result = ['<ul id="nav">']
        for link in self.links:
            result.append('<a href="%s"><li>%s</li></a>' % (link, link.replace('.html', '').capitalize()))
        return '\n'.join(result)
        
    def component_footer(self, tree):
        result = [u'&copy; ' + self.getPublicationDate(tree) + ' ']
        website = self.getWebSite(tree)
        if website:
            result.append('<a href="%s" target="Extern">')
        result.append(self.getAuthor(tree))
        if website:
            result.append('</a>')
        return ''.join(result)

    def component_sidebar(self, tree):
        return '<h2>Side bar</h2>\n'
 
    # E L E M E N T S
    
    TAGS_IGNORE = ('meta',)
    TAGS_TEXT = ('svg',)
        
    def buildElement(self, element):
        result = []
        if element is not None and not element.tag in self.TAGS_IGNORE:
            hook = 'element_%s' % element.tag
            if 'Comment' in hook:
                result.append('<div class="error">Comment:')
            elif hasattr(self, hook):
                openTag = getattr(self, hook)(element)
                if openTag is not None:
                    result.append(openTag)
            else:
                result.append(self.error(hook))
            if element.text is not None:
                result.append('%s' % element.text)
            for child in element:
                result.append(self.buildElement(child)) # @@@ Do something here for SVG
            hook = '_element_%s' % element.tag
            if 'Comment' in hook:
                result.append('</div>')
            elif hasattr(self, hook):
                closeTag = getattr(self, hook)(element)
                if closeTag is not None:
                    result.append(closeTag)
            if element.tail:
                result.append('%s' % element.tail)
            return ''.join(result)
        
    # <chapters>
        
    def element_chapters(self, element):
        self.chapterIndex = 1 # Reset counts
        return '<div class="chapters">'
            
    def _element_chapters(self, element):
        return '</div> <!-- .chapters -->\n'
        
    # <chapter>
                
    def element_chapter(self, element):
        self.chapterIndex += 1 # Keep count
        return '<div class="chapter">'
            
    def _element_chapter(self, element):
            return '</div> <!-- .chapter -->\n'
        
    def element_chapterIndex(self, element):
            return '<span class="chapterIndex">%s</span>' % self.chapterIndex
            
    # <articles>
        
    def element_articles(self, element):
        self.articleIndex = 1 # Reset count        
        return '<div class="articles">'
            
    def _element_articles(self, element):
        return '</div> <!-- .articles -->\n'
        
    # <article>
            
    def element_article(self, element):
        self.articleIndex += 1 # Keep count
        self.h1Index = 1
        return '<div class="article">'
            
    def _element_article(self, element):
        return '</div> <!-- .article -->\n'
        
    def element_articleIndex(self, element):
        return '<span class="articleIndex">%s</span>' % self.articleIndex

    # video
    
    def element_video(self, element):
        return '<a href="%s" target="External">' % element.get('href')
        
    def _element_video(self, element):
        return "</a>"
    
    # link
    def element_link(self, element):
        return '<a href="%s" target="External">' % element.get('href')
        
    def _element_link(self, element):
        return '</a>'
        
    # <pullquote>
    
    def element_pullquote(self, element):
        return '<div class="pullquote">'
        
    def _element_pullquote(self, element):
        return '</div> <!-- .pullquote -->\n'
    
    # <quote>
    
    def element_quote(self, element):
        result = ['<div class="quote">']
        pageStart = element.find('.//pagestart')
        pageEnd = element.find('.//pageend')
        if pageStart is not None and pageStart.text:
            result.append('<div class="pageNumberFirst">%s' % pageStart.text)
            if pageEnd is not None and pageEnd.text:
                result.append('-%s' % pageEnd.text)
            result.append('</div> <!-- .pageNumberFirst -->\n')
        result.append('<div class="quoteText">\n')
        return ''.join(result)
        
    def _element_quote(self, element):
        result = ['</div>']
        pageStart = element.find('.//pagestart')
        pageEnd = element.find('.//pageend')
        if pageStart is not None and pageStart.text:
            result.append('<div class="pageNumberLast">%s' % pageStart.text)
            if pageEnd is not None and pageEnd.text:
                result.append('-%s' % pageEnd.text)
            result.append('</div> <!-- .pageNumberLast -->\n')
        result.append('</div> <!-- .quote -->\n')
        return ''.join(result)
                
    # <h1>
                
    def element_h1(self, element):
        self.h1Index += 1 # Keep count
        return '<h1>'
            
    def _element_h1(self, element):
        return '</h1>\n'
            
    def element_h1Index(self, element):
        return '<span class="h1Index">%s</span>' % self.h1Index
        
    # <h2>
                
    def element_h2(self, element):
        return '<h2>'
            
    def _element_h2(self, element):
        return '</h2>\n'
        
    # <h3>
                
    def element_h3(self, element):
        return '<h3>'
            
    def _element_h3(self, element):
        return '</h3>'
                    
    # <p>
                
    def element_p(self, element):
        return '<p>'
            
    def _element_p(self, element):
        return '</p>\n'
        
    # <images>
        
    def element_images(self, element):
        return '<div class="images">'
            
    def _element_images(self, element):
        return '</div> <!-- .images -->\n'
            
    # <image>
                
    def element_image(self, element):
        return '<div class="%s"><a name="%s" href="images.html#%s"><img src="../images/%s" class="autowidth"/></a>' % \
            (element.get('type') or 'image', element.get('src'), element.get('src'), element.get('src'))
            
    def _element_image(self, element):
        return '</div> <!-- .image -->\n'
        
    # <conclusion>
        
    def element_conclusion(self, element):
        return '<div class="conclusion">'
            
    def _element_conclusion(self, element):
        return '</div> <!-- .conclusion -->\n'
            
    # <introduction>
        
    def element_introduction(self, element):
        return '<div class="introduction">'
            
    def _element_introduction(self, element):
        return '</div> <!-- .introduction -->\n'
            
    # <title>
        
    def element_title(self, element):
        return '<h1 class="title">'
            
    def _element_title(self, element):
        return '</h1>\n'
            
    # <posttitle>
        
    def element_posttitle(self, element):
        return '<h2 class="posttitle">'
            
    def _element_posttitle(self, element):
        return '</h2>\n'
            
    # <subtitle>
        
    def element_subtitle(self, element):
        return '<h3 class="subtitle">'
            
    def _element_subtitle(self, element):
        return '</h3>\n'
            
    # <caption>
        
    def element_caption(self, element):
        return '<div class="caption">'
            
    def _element_caption(self, element):
        return '</div> <!-- .caption -->'
        
    # <lit>
        
    def element_lit(self, element):
        return '<span class="lit">['
            
    def _element_lit(self, element):
        return ']</span>'
        
    # <definition>
        
    def element_definition(self, element):
        return '<a class="definition">'
            
    def _element_definition(self, element):
        return '</a>'
        
    # <em>
        
    def element_em(self, element):
        return '<em>'
            
    def _element_em(self, element):
        return '</em>'
        
    # <im>
        
    def element_im(self, element):
        return '*'
            
    def _element_im(self, element):
        return '*'
        
    # <text>
        
    def element_text(self, element):
        return '' # Ignore the text tag
            
    def _element_text(self, element):
        return ''
            
    # <ul>
        
    def element_ul(self, element):
        return '<ul>'
            
    def _element_ul(self, element):
        return '</ul>\n'
            
    # <li>
    
    def element_li(self, element):
        return '<li>'
        
    def _element_li(self, element):
        return '</li>\n'

    # <br/>
  
    def element_br(self, element):
        return '<br>'
             
    # <span>
  
    def element_span(self, element):
        return '<span>'
             
    def _element_span(self, element):
        return '</span>'
     
    # <amp>
        
    def element_amp(self, element):
        return '&amp;'
    
    # <table>
    
    def element_table(self, element):
        return '<table>'
            
    def _element_table(self, element):
        return '</table>'
            
    def element_tr(self, element):
        return '<tr>'
            
    def _element_tr(self, element):
        return '</tr>'
            
    def element_th(self, element):
        return '<th>'
            
    def _element_th(self, element):
        return '</th>'
            
    def element_td(self, element):
        return '<td>'
            
    def _element_td(self, element):
        return '</td>'
    
    # <expand>
    def element_expand(self, element):
        s= """<span class="expand" onclick="var relatedImage = $(this).parent().parent().find('img'); var newImageURL = relatedImage.attr('src') == relatedImage.attr('data-defaultimage') ? relatedImage.attr('data-alternativeimage') : relatedImage.attr('data-defaultimage'); relatedImage.attr('src', newImageURL);var expand=getElementById('expand%d');if(expand.style.display=='block')expand.style.display='none';else expand.style.display='block';"> + </span> <span class="expanded" id="expand%d" style="display:none;">""" % (self.expandIndex, self.expandIndex) 
        self.expandIndex += 1
        return s

    def _element_expand(self, element):
        return '</span>'
    
        # <spelling>
        
    def element_spelling(self, element):
        return '<span class="spelling">'
        
    def _element_spelling(self, element):
        return '</span>'    
        
    # <pronunciation>
    
    def element_pronunciation(self, element):
        return '<span class="pronunciation">'
        
    def _element_pronunciation(self, element):
        return '</span>'
            
    # S V G
    
    # <svg>
    
    def element_svg(self, element):
        return '<div class="svg"><svg>'
        
    def _element_svg(self, element):
        return '</svg></div>\n'
            
    # A R T I C L E  C O M P O N E N T S
    
    # Components have the pattern [[componentName]] in the HTML template
 
    def component_articletop(self, tree):
        # Caller makes the tag
        result = []
        postTitle = self.getPostTitle(tree)
        if postTitle:
            result.append(postTitle)
        result.append(self.getTitle(tree))
        subTitle = self.getSubTitle(tree)
        if subTitle:
            result.append(subTitle)
        author = self.getAuthor(tree, ignore=True)
        if author:
            result.append('<div class="titleAuthor">%s</div>' % author)
        return '\n'.join(result) 

    def component_chapters(self, tree):
        result = []
        for chapters in tree.findall('.//chapters'):
            result.append('<!-- Chapters title -->\n')
            result.append(self.getTitle(chapters))
            if chapters is not None:
                result.append('<!-- Chapters element -->\n')
                result.append(self.buildElement(chapters))
        return ''.join(result)
            
    # W O R D S  C O M P O N E N T S

    def component_wordstop(self, tree):
        result = []
        result.append('<h1>%s</h1>' % self.getTitle(tree))
        result.append('<h2>Words index</h2>')
        return '\n'.join(result)
    
    def component_wordsindex(self, tree):
        definitions = self.getDefinitions(tree)
        result = []
        for definition in definitions:
            result.append('<div class="definition">')
            title = definition.find('.//title')
            if title is not None and title.text:
                result.append('<div class="definintionTitle">%s</div>' % title.text)
            subTitle = definition.find('.//subtitle')
            if subTitle is not None and subTitle.text:
                result.append('<div class="definintionSubTitle">%s</div>' % subTitle.text)
            t = definition.find('.//text')
            if t is not None:
                result.append(self.buildElement(t))            
            result.append('</div>')
        return '\n'.join(result)
        
    def component_wordssidebar(self, tree):
        return self.error('What to put in the words side bar?')
         
    # I M A G E S  C O M P O N E N T S

    def component_imagestop(self, tree):
        result = []
        result.append('<h1>%s</h1>' % self.getTitle(tree))
        result.append('<h2>Images index</h2>')
        return '\n'.join(result)
    
    def component_imagesindex(self, tree):
        result = ['<table width="100%">']
        images = self.getImages(tree)
        for image in images:
            src = image.get('src')
            result.append(u'<tr><td width="20%%" class="image">')
            # Link to the place in the document where the image is used.
            result.append('<a href="home.html#%s">' % src)
            result.append('<img src="../images/%s" class="autowidth"/></td>' % src)
            result.append('</a>')
            result.append('<td class="metaimage">')
            website = self.getWebSite(image, ignore=True)
            author = self.getAuthor(image, ignore=True)
            title = self.getTitle(image, ignore=True)
            publicationDate = self.getPublicationDate(image, ignore=True)
            meta = []
            if title:
                w = []
                if website:
                    w.append('<a href="%s" target="Extern">' % website)
                w.append(title)
                if website:
                    w.append('</a>')
                meta.append(''.join(w))
            if author:
                meta.append(author)
            if publicationDate:
                meta.append(publicationDate)
            if meta:
                result.append('<h1>')
                result.append(', '.join(meta))
                result.append('</h1>')
            caption = image.find('.//caption')
            if caption is not None:
                result.append(self.buildElement(caption))
            result.append('</td>')
            result.append('</tr>')
        result.append('</table>')
        return '\n'.join(result)
    
    def component_imagessidebar(self, tree):
        return self.error('What to put in the images side bar')
                         
    # L I T E R A T U R E  C O M P O N E N T S
               
    def component_literaturetop(self, tree):
        result = []
        result.append('<h1>%s</h1>' % self.getTitle(tree))
        result.append('<h2>Literature index</h2>')
        return '\n'.join(result)
        
    def component_literatureindex(self, tree):    
        # Affective influences on [Anderson, 2005, p.26] the attentional dynamics
        
        #[Journal article:]
        # surname: Anderson, 
        # name: A. K. 
        # year: (2005). 
        # title: Affective influences on the attentional dynamics supporting awareness. 
        # journal: Journal of Experimental Psychology: General, 
        # issuenumber: 154, 
        # pages: 258–281.

        #[Book:]

        # surname: Wechsler, 
        # name: D. 
        # year: (1997). 
        # title: Technical manual for the Wechsler Adult Intelligence and Memory Scale. 
        # publisher/place: New York, NY: 
        # publisher/name: Psychological Corporation.

        #[Website:]
        # title: American Psychological Association. 
        # subtitle: Basics of APA Style Tutorial. 
        # Derived from 
        # publisher/website: www.apastyle.org on 
        # publishingdate: 26 September 2012.
    
        references = self.getLiteratureReferences(tree)
        result = []
        for reference in references:
            result.append('<div class="literatureReference">')
            lit = reference.find('.//lit')
            if lit is not None and lit.text:
                result.append('<span class="literatureId">%s</span>' % lit.text)
            title = reference.find('.//title')
            # Author, sorting order: Author name, Author initials, year/date
            if title is not None and title.text:
                result.append('<span class="literatureTitle">%s</span>' % title.text)
            subTitle = reference.find('.//subtitle')
            if subTitle is not None and subTitle.text:
                result.append('<span class="literatureSubTitle">%s</span>' % subTitle.text)
            publicationDate = reference.find('.//publicationdate')
            if publicationDate is not None and publicationDate.text:
                result.append('<span class="literaturePublicationDate">%s</span>' % publicationDate.text)
            issueNumber = reference.find('.//issuenumber')
            if issueNumber is not None and issueNumber.text:
                result.append('<span class="literatureIssueNumber">%s</span>' % issueNumber.text)
            website = reference.find('.//website')
            if website is not None and website.text:
                result.append(u"""<span class="literatureWebsite">
                    <a href="%s" target="external">Website &#8594;</a></span>""" % website.text)
            result.append('</div>')
        return '\n'.join(result)
        
    def component_literaturesidebar(self, tree):
        return self.error('What to put in the literature side bar?')
         
    
                
