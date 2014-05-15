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
#     simplex.py
#
import re
from xierpa3.tools.transformer import TX
from xpyth.xierpa.tools.validator import Validator

class Simplex():
    u"""
    <doc>See also:
    - http://moinmo.in/HelpOnMoinWikiSyntax
    - http://trac.edgewall.org/wiki/WikiFormatting
    - http://meta.wikimedia.org/wiki/WMDOC/Cheatsheet

    Use with ./_xsl/xml2simplex.xsl</doc>
    """
    SIMPLEXTAG = '<simplex>'
    SIMPLEX_TAG = '</simplex>'

    RE_SIMPLEXBULLET = re.compile('([^\*]*)(\*\*)(([^\*]*)(\n\*[^\*]*)*)(\*\*)')

    SIMPLEXCODESTAGLIST = (
        # Single tags
        (u'¶', None, '<para/>', None, u'New paragraph (Mac:alt-7)'),
        (u'-|', None, '<para/>', None, u'New paragraph (Windows)'),
        (u'-!', None, '<para/>', None, u'New paragraph (Windows)'),
        (u'&', None, '<amp/>', None, u'Ampersand'),
        (u'===', None, '<ruler2/>', None, u'Horizontal ruler type 2 or float end'),
        (u'---', None, '<ruler/>', None, u'Horizontal ruler type 1'),
        (u'--', None, '<shy/>', None, u'Soft-hyphen'),
        (u'++', None, '<nbsp/>', None, u'Non-breaking space'),
        (u'=missing=', None, '<missing/>', None, u'Missing'),

        # Block tags
        (u"=1=", None, '<h1>', '</h1>', u'Head level 1'),
        (u"=2=", None, '<h2>', '</h2>', u'Head level 2'),
        (u"=3=", None, '<h3>', '</h3>', u'Head level 3'),
        (u"=4=", None, '<h4>', '</h4>', u'Head level 4'),
        (u"=5=", None, '<h5>', '</h5>', u'Head level 5'),
        (u'=ank=', None, '<ankeiler>', '</ankeiler>', u'Ankeiler'),
        (u'=sum=', None, '<summary>', '</summary>', u'Summary'),

        # (u"'''''", None, '<em><im>', '</im></em>', u'Bold-italic'),
        (u"'''", None, '<em>', '</em>', u"Bold (triple ')"),
        (u"''", None, '<im>', '</im>', u"Italic (double ')"),

        # Change this later only to change text, not inside tag attribute definitions.
        # (u'"', None, '<quoted>', '</quoted>', u'Quoted “...” (single ")'),
        (u"'", None, '<squote/>', None, u'Single quote ’'),
        (u'^', None, '<sup>', '</sup>', u'Superior (sup)'),
        (u',,', None, '<sub>', '</sub>', u'Inferior (sub)'),
        (u'__', None, '<u>', '</u>', u'Underline'),
        (u'~~', None, '<s>', '</s>', u'Strike-through'),
        (u'??', None, '<question>', '</question>', u'Question'),
        (u'!!', None, '<answer>', '</answer>', u'Answer'),
        (u'::', None, '<associated>', '</associated>', u'Associated link<br/>::associated words::<br/>::www.xierpa.com::<br/>::image.png::<br/>::buro@petr.com::'),
        (u'****', None, '<ul>', '</ul>', u'Bullet list'),
        (u'***', None, '<ul>', '</ul>', u'Bullet list'),
        (u'**', None, '<ul>', '</ul>', u'Bullet list'),

        # (u'*', RE_SIMPLEXBULLET, None, None, u'Bullet'),
        (u'####', None, '<ol>', '</ol>', u'Numbered list'),
        (u'###', None, '<ol>', '</ol>', u'Numbered list'),
        (u'##', None, '<ol>', '</ol>', u'Numbered list'),
    )
    XML2SIMPLEX = (
        # (unicode(chr(164)), u'€'),    # Replace old Euro (currency) to real Euro sign
        (chr(7), ''),
        (chr(31), '--'),         # Soft-hyphen in Word?
        ('\n\r', "\r"),
        ('\r\n', "\r"),
        ('\n', "\r"),
        ('&amp;apos;', "'"),
        ('&apos;', "'"),
        ('&amp;quot;', '"'),
        ('&quot;', '"'),
        ('&', '&amp;'),     # Convert all ampersand types to simplex &amp;
        ('&amp;amp;', '&amp;'),
        ('<amp/>', '&amp;'),
        ('[empty]', '=missing='),
        ('<missing/>', '=missing='),
        ('&amp;#', '&#'),         # Solve saving of Cyrillic and other &#xxxx; code to unicode
        ('<icon>a</icon>', '((a))'),
        ('<icon>b</icon>', '((b))'),
        ('<icon>c</icon>', '((c))'),
        ('<twice/>', '((2x))')
    )

    SIMPLEX2XML = (
        # (unicode(chr(164)),    u'€'),    # Replace old Euro (currency) to real Euro sign
        (chr(7), ''),
        (chr(31), '--'),         # Soft-hyphen in Word?
        ('\n\r', "\r"),
        ('\r\n', "\r"),
        ('\n', "\r"),
        ('&amp;apos;', "'"),
        ('&apos;', "'"),
        ('&amp;quot;', '"'),
        ('&quot;', '"'),
        ('&amp;', '<amp/>'),     # Convert all ampersand types to <amp/>
        ('&', '<amp/>'),
        ('=missing=', '<missing/>'),
        ('<amp/>#', '&#'),         # Solve saving of Cyrillic and other &#...; code to Unicode.
        ('((a))', '<icon>a</icon>'),
        ('((b))', '<icon>b</icon>'),
        ('((c))', '<icon>c</icon>'),
        ('((2x))', '<twice/>'),
    )

    def xml2simplex(self, xml, template=None):
        u"""
        <doc>Revert XML from database to simplex format for the interface.</doc>
        """
        if not xml or not isinstance(xml, basestring):
            return xml
        if not self.USESIMPLEX:
            return xml

        for t1, t2 in self.XML2SIMPLEX:
            xml = xml.replace(t1, t2)

        template = template or self.PATH_XML2SIMPLEXTEMPLATE

        simplex = self.getxml2xml(xml=xml, python=False, copyunknown=True, nocache=True, template=template,
                                  addheader=True, addroot='simplex', onerrorescapexml=True)
        index = simplex.find(self.SIMPLEXTAG)
        if index >= 0:
            simplex = simplex[index + len(self.SIMPLEXTAG):]
        if simplex.endswith(self.SIMPLEX_TAG):
            simplex = simplex[:-len(self.SIMPLEX_TAG)]

        try:
            simplex = simplex.replace(u'¶', u'¶\r').strip()
        except Exception, e:
            # Breaks on larger Unicode characters.
            print e
        return simplex

    def getsimplexcodetaglist(self):
        u"""
        <doc>The <code>getsimplexcodetaglist</code> method answer the list with “Simplex” coding and the related XML
        tags. The default behaviour is to answer <code>self.SIMPLEXCODESTAGLIST</code>.</doc>
        """
        return self.SIMPLEXCODESTAGLIST

    def simplex2xml(self, s):
        u"""
        <doc>The <code>simplex2xml</code> method translates simplex-wiki code to the corresponding XML tags.</doc>
        """
        if not s or not isinstance(s, basestring):
            return s

        if not self.USESIMPLEX:
            return s

        for t1, t2 in self.SIMPLEX2XML:
            s = s.replace(t1, t2)

        for code, _, t1, t2, _ in self.getsimplexcodetaglist():
            if '**' in code or '##' in code:
                # Handle list or numbered list
                parts = s.split(code)
                s = ''
                for index in range(0, len(parts), 2):
                    s += parts[index]
                    if index < len(parts) - 1:
                        if '*' in code:
                            s += '<ul>'
                            splitsep = '\r*'
                        else:
                            s += '<ol>'
                            splitsep = '\r#'
                        for li in parts[index + 1].split(splitsep):
                            if li:
                                s += '<li>' + li + '</li>'
                        if '*' in code:
                            s += '</ul>'
                        else:
                            s += '</ol>'
            elif t2 is None:
                # Just a simple replacement code
                s = s.replace(code, t1)

            else:
                opencode = None
                parts = []
                for part in s.split(code):
                    if opencode is None:
                        # Add initial part of the string
                        parts.append(part)
                        opencode = False
                    elif opencode:
                        # Add string part
                        parts.append(part)
                        opencode = False
                    elif code == '::':
                        # This is an association. Try to find out the best match
                        self.parseSimplexAssociation(parts, part)
                        opencode = True
                    else:
                        # Simple open and close tag without attributes
                        parts.append(t1)
                        parts.append(part)
                        parts.append(t2)
                        opencode = True
                s = u''.join(parts)

        s = s.replace('\r', '\n')
        return s

    def parseSimplexAssociationAttributes(self, parts, attributes, allowedattributes):
        u"""
        <doc>The <code>parseSimplexAssociationAttributes</code> parses a list of string <attr>attributes</attr> with
        the format <code>'name=value'</code> and adds them to the (assumed open) tag string in <attr>parts</attr>. There
        is no checking for the allowed attribute names. That is must be done by the template converting the Simplex XML
        result. This make the Simplex independent for future extensions of the attribute list.  Some examples:

        ::buro@petr.com::                                    <email>buro@petr.com</email>
        ::./_images/abc.jpg::                                <image src="./_images/abc.jpg"/>
        ::abc.jpg::                                            <image src="path-to-abc.jpg"/>
        ::www.xierpa.com::                                    <www>www.xierpa.com</www>
        ::idname::
        ::id::
        </doc>
        """
        for attribute in attributes:
            attributeparts = attribute.split('=')
            if len(attributeparts) > 1 and attributeparts[0] in allowedattributes:
                value = '='.join(attributeparts[1:])
                if value:
                    parts.append(' %s="%s"' % (attributeparts[0], value.strip()))

    def simpleLink(self, parts, association, validator):
        u"""
        <doc>A simple link has just one component.</doc>
        """
        if validator.isimage(association):
            # Just display image.
            parts.append('<image src="%s"/>' % association)

        elif validator.isemail(association):
            # Make mailto link.
            parts.append('<email>%s</email>' % association)

        elif validator.ispdf(association):
            # Make PDF link.
            # <todo>TODO</todo> make an actual PDF link tag...
            parts.append('<image src="%s"/>' % association)

        elif validator.iszip(association):
            # Make link to zipfile.
            parts.append('<image src="%s"/>' % association)

        elif validator.isurl(association):
            # Make URL.
            parts.append('<www>%s</www>' % association)

        else:
            parts.append('<associatedlink>%s</associatedlink>' % association)

    def getAttributeDict(self, attributes):
        u"""
        <doc>Parses attribute strings into key-value pairs.</doc>
        """
        attributedict = {}

        for a in attributes:
            if not '=' in a: continue
            else:
                keyvalue = a.split('=')
                if len(keyvalue) > 2: continue
                else: attributedict[keyvalue[0]] = keyvalue[1]
        return attributedict


    def compoundLink(self, parts, prettyname, attributes, validator):
        u"""
        <doc><h1>Working</h1>
        ::abc.jpg|alt=abc::                    <image src="path-to-abc.jpg" alt="abc"/>
        ::abc.jpg|caption=right|alt=abc::    <image src="path-to-abc.jpg" caption="right" alt="abc"/>
        ::www.xierpa.com|target=external::    <www target="external">www.xierpa.com</www>
        ::pretty name|href=idname::            <associatedlink href="idname">pretty name</associatedlink>

        <h1>To Do</h1>

        ::pretty name|href=id::
        ::abc.jpg|href=www.xierpa.com::        <www>www.xierpa.com</www>

        <h1>Obsolete?</h1>
        ~~::Link|href=www.xierpa.com::                <link href="www.xierpa.com">Link</link>~~
        ~~::Link|href=www.xierpa.com|target=xyz::    <link href="www.xierpa.com" target="xyz">Link</link>~~
        </doc>
        """
        attributedict = self.getAttributeDict(attributes)

        if validator.isimage(prettyname) and attributedict.has_key('href'):
            parts.append('<imagelink src="%s" href="%s"' % (prettyname, attributedict['href']))
            self.parseSimplexAssociationAttributes(parts, attributes, self.ASSOCIATION_IMAGEATTRIBUTES)
            parts.append('/>')

        elif validator.isimage(prettyname):
            parts.append('<image src="%s"' % prettyname)
            self.parseSimplexAssociationAttributes(parts, attributes, self.ASSOCIATION_IMAGEATTRIBUTES)
            parts.append('/>')

        elif validator.isemail(prettyname):
            parts.append('<email')
            self.parseSimplexAssociationAttributes(parts, attributes, self.ASSOCIATION_EMAILATTRIBUTES)
            parts.append('>%s</email>' % prettyname)

        elif attributedict.has_key('href'):
            if attributedict['href'].startswith('http://') or attributedict['href'].startswith('www.'):
                parts.append('<a href="')
                parts.append(attributedict['href'])
                parts.append('">')
                parts.append(prettyname)
                parts.append('</a>')
            else:
                parts.append('<associatedlink')
                self.parseSimplexAssociationAttributes(parts, attributes, self.ASSOCIATION_LINKATTRIBUTES)
                parts.append('>%s</associatedlink>' % prettyname)

    def parseSimplexAssociation(self, parts, s):
        u"""
        <doc>The <code>parseSimplexAssociation</code> method parses the <attr>s</attr> attribute string by Simplex
        syntax and generates XML coding from the tokens.</doc>
        """
        validator = Validator()
        associatedparts = s.split('|')

        if len(associatedparts) == 1:
            # No attributes, just the link.
            self.simpleLink(parts, associatedparts[0], validator)

        else:
            # Got attributes, more complicated conversion.
            prettyname = associatedparts[0]
            attributes = associatedparts[1:]
            self.compoundLink(parts, prettyname, attributes, validator)

    def simplexentry(self, path=None, value=None, type=None, cols=None, rows=None, **kwargs):
        u"""
        <doc>The <code>simplexentry</code> method is a wrapper around <code>self.entry()</code> and <code>
        self.textarea()...self._textarea()</code>. If the class value <code>self.USESIMPLEX</code> is <code>True</code>
        (which is default), then the <attr>value</attr> attribute is transformed by <code>self.xml2simplex(value)</code>
        before feeding it in to <code>self.entry()</code> or <code>self.textarea()</code>.<br/>
        
        Note that since we have to translate the <attr>value</attr> into Simplex syntax, the equivalent <code>
        self.entry()</code> attribute <attr>values</attr> is not supported.</doc>
        """
        if self.USESIMPLEX:
            value = self.xml2simplex(value)

        if type == self.ENTRYTYPE_TEXTAREA:
            self.textarea(name=path, cols=cols, rows=rows, **kwargs)
            self.text(value)
            self._textarea()
        else:
            self.entry(path=path, value=value, type=type or self.ENTRYTYPE_TEXT, **kwargs)

    def buildsimplexjs(self):
        u"""
        <doc>The <code>buildsimplexjs</code> method implements the help JavaScript support for the Simplex help popup
        functionality. This method is redefined from the implementation of <code>SiteBuilder</code>.</doc>
        """
        self.script()
        self.text('''
        function %(function)s(state){
            var helpdiv = getElement('%(id)s');
            if (helpdiv){
                if (state)
                    helpdiv.style.visibility = 'visible';
                else
                    helpdiv.style.visibility = 'hidden';
                log(helpdiv, state, helpdiv.style.visibility);
            }
        }
        ''' % {'function': self.DEFSHOWSIMPLEXHELP, 'id': self.CMSTARGETID_SIMPLEXHELP})
        self._script()

    def buildsimplexhelpcss(self):
        self.css('div.' + self.CLASS_SIMPLEXHELP, position='absolute', x=0, y=0, z=1000, width=300, visibility='hidden',
            color='black', backgroundcolor='#F0F0F0', margin=100, padding='3px 3px 3px 3px', border='1px solid #ccc',
             boxshadow="#aaa 2px 1px 8px", borderradius='5px 5px 0 0')
        self.css(ids='a.' + self.CLASS_SIMPLEXHELPLINK, textdecoration='none', backgroundcolor='#808080',
            fontsize=self.CSS_FONTSIZETAB, color='white', padding='2px 4px 2px 4px', align='center', valign='middle')
        self.css(ids='a:hover.' + self.CLASS_SIMPLEXHELPLINK, backgroundcolor='#A0A0A0')

    def buildsimplexhelplink(self):
        u"""
        <doc>The <code>buildsimplexhelplink</code> method build a link (default is the string <code>
        self.LABEL_SIMPLEXHELP</code>) that implements a mouse-over popup showing a table with available Simplex
        codings.</doc>
        """
        self.link(href='#', onmouseover=self.JS_SHOWSIMPLEXHELP, onmouseout=self.JS_HIDESIMPLEXHELP,
                class_=self.CLASS_SIMPLEXHELPLINK)
        self.text(self.LABEL_SIMPLEXHELP)
        self._link()

        if not hasattr(self, 'buildsimplexhelplink_initialized'):
            self.initializesimplexlinkhelp()

    def initializesimplexlinkhelp(self):
        u"""
        <doc>The <code>initializesimplexlinkhelp</code> method builds the div content of the Simplex help. If in CMS
        mode this is done automatically.</doc>
        """
        doneblockcodeheader = False
        self.div(id=self.CMSTARGETID_SIMPLEXHELP, class_=self.CLASS_SIMPLEXHELP)
        self.table(width='100%')
        self.row()
        self.col(class_=self.CLASS_FORMLABELTOP, colspan=2)
        self.textlabel(self.LABEL_SIMPLEXHELPTITLE)
        self._col()
        self._row()
        for code, _, _, t2, comment in self.getsimplexcodetaglist():
            if t2 and not doneblockcodeheader:
                self.row()
                self.col(class_=self.CLASS_FORMLABELTOP, colspan=2)
                self.textlabel(self.LABEL_SIMPLEXHELPBLOCKTITLE)
                self._col()
                self._row()
                doneblockcodeheader = True
            self.row()
            self.col(class_=self.CLASS_FORMFIELDTOP, width='50%')
            if t2:
                self.text('%sabc%s' % (code, code))
            else:
                self.text(code)
            self._col()
            self.col(class_=self.CLASS_FORMFIELDTOP)
            self.text(comment)
            self._col()
            self._row()
        self._table()
        self._div()
        self.buildsimplexhelplink_initialized = True     # Only one simplex help div per page.

    # ---------------------------------------------------------------------------------------------------------
    #     X S L  S U P P O R T

    def question(self):
        u"""
        <doc>The <code>question</code> implements the XSL support for the <tag>question</tag> as generated by the
        Simplex <code>'??...??'</code> code. This method can be redefined by the inheriting application class. The
        default behaviour is to do nothing.</doc>
        """
        self._pushtag('question')

    def _question(self):
        self._poptag('question')

    def answer(self):
        u"""
        <doc>The <code>answer</code> implements the XSL support for the <tag>answer</tag> as generated by the Simplex
        <code>'!!...!!'</code> code. This method can be redefined by the inheriting application class. The default
        behaviour is to do nothing.</doc>
        """
        self._pushtag('answer')

    def _answer(self):
        self._poptag('answer')
