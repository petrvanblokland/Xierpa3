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
from xierpa3.constants.constants import Constants
from xierpa3.toolbox.storage.data import Data
from xierpa3.toolbox.parsers.validator import Validator

class Simplex(object):
    u"""
    The <b>Simplex</b> parser takes a Wiki-like syntax string and converts it into HTML.
    The result is answered as <b>Data</b> instance, as it also can contain other fields.
    See also:
    - http://moinmo.in/HelpOnMoinWikiSyntax
    - http://trac.edgewall.org/wiki/WikiFormatting
    - http://meta.wikimedia.org/wiki/WMDOC/Cheatsheet
    """
    C = Constants
    
    DATACLASS = Data
    
    USESIMPLEX = True

    SIMPLEXTAG = '<div class="simplex">'
    _SIMPLEXTAG = '</div> <!-- .simplex -->'

    DEFSHOWSIMPLEXHELP = 'showsimplexhelp'
    JS_SHOWSIMPLEXHELP = DEFSHOWSIMPLEXHELP + '(1)'
    JS_HIDESIMPLEXHELP = DEFSHOWSIMPLEXHELP + '(0)'

    CMSTARGETID_SIMPLEXHELP = 'simplexhelp'

    CLASS_SIMPLEXHELPLINK = 'simplexhelplink'
    CLASS_SIMPLEXHELP = 'simplexhelp'

    RE_SIMPLEXBULLET = re.compile('([^\*]*)(\*\*)(([^\*]*)(\n\*[^\*]*)*)(\*\*)')

    SIMPLEXCODESTAGLIST = (

        # Open, Close, HTML open, content, HTML close, comment
        # Make sure to put larger patterns first, in case of overlaps.
        
        # Single tags
        (u'¶', None, '<br>', None, None, u'New paragraph (Mac:alt-7)'),
        (u'-|', None, '<br>', None, None, u'New paragraph (Windows)'),
        (u'-!', None, '<br>', None, None, u'New paragraph (Windows)'),
        (u'&', None, '&amp;', None, None, u'Ampersand'),
        (u'===', None, '<hr class="%s">' % C.CLASS_RULER2, None, None, u'Horizontal ruler type 2 or float end'),
        (u'---', None, '<hr class="%s">' % C.CLASS_RULER1, None, None, u'Horizontal ruler type 1'),
        (u'--', None, '&shy;', None, None, u'Soft-hyphen'),
        (u'++', None, '&nbsp;', None, None, u'Non-breaking space'),
        (u'=missing=', None, '<span class="%s">' % C.CLASS_MISSING, 'missing', '</span>', u'Missing'),

        # Block tags
        #=C= Chapter split will be done separate.
        (u"=T=", None, '<div class="%s">' % C.CLASS_TITLE, None, '</div> <!-- .title -->', u'Title'),
        (u"=1=", None, '<h1>', None, '</h1>', u'Head level 1'),
        (u"=2=", None, '<h2>', None, '</h2>', u'Head level 2'),
        (u"=3=", None, '<h3>', None, '</h3>', u'Head level 3'),
        (u"=4=", None, '<h4>', None, '</h4>', u'Head level 4'),
        (u"=5=", None, '<h5>', None, '</h5>', u'Head level 5'),
        (u"=6=", None, '<h6>', None, '</h6>', u'Head level 6'),
        (u'=ank=', None, '<div class="%s">' % C.CLASS_ANKEILER, None, '<div> <!-- .ankeiler -->', u'Ankeiler'),
        (u'=lead=', None, '<div class="%s">' % C.CLASS_LEAD, None, '<div> <!-- .lead -->', u'Lead'),
        (u'=sum=', None, '<div class="%s">' % C.CLASS_SUMMARY, None, '<div> <!-- .summary -->', u'Summary'),
        (u'||', None, '<!-- ', None, ' -->', u'Comment'),
        
        # (u"'''''", None, '<em><im>', '</im></em>', u'Bold-italic'),
        (u"'''", None, '<em>', None, '</em>', u"Bold (triple ')"),
        (u"''", None, '<i>', None, '</i>', u"Italic (double ')"),

        # Change this later only to change text, not inside tag attribute definitions.
        # (u'"', None, '<quoted>', '</quoted>', u'Quoted “...” (single ")'),
        #(u"'", None, 'singlequote', None, None, True, u'Single quote ’'),
        (u'^', None, '<sup>', None, '</sup>', u'Superior (sup)'),
        (u',,', None, '<sub>', None, '</sub>', u'Inferior (sub)'),
        (u'__', None, '<span class="%s">' % C.CLASS_UNDERLINE, None, '</span>', u'Underline'),
        (u'~~', None, '<span class="%s">' % C.CLASS_STRIKETHROUGH, None, '</span>', u'Strike-through'),
        (u'!!!', None, '<div class="%s">' % C.CLASS_PULLQUOTE, None, '</div>', u'Pull quote'),
        (u'!!', None, '<span class="%s">' % C.CLASS_ANSWER, None, '</span>', u'Answer'),
        (u'??', None, '<span class="%s">' % C.CLASS_QUESTION, None, '</span>', u'Question'),
        #(u'::', None, '<associated>', '</associated>', u'Associated link<br/>::associated words::<br/>::www.xierpa.com::<br/>::image.png::<br/>::buro@petr.com::'),

        # Lists. Use matching levels on open/close strings, for nested lists.
        (u'****', None, '<ul>', None, '</ul>', u'Bullet list'),
        (u'***', None, '<ul>', None, '</ul>', u'Bullet list'),
        (u'**', None, '<ul>', None, '</ul>', u'Bullet list'),
        # (u'*', RE_SIMPLEXBULLET, None, None, u'Bullet'),
        (u'#####', None, '<ol>', None, '</ol>', u'Numbered list'),
        (u'####', None, '<ol>', None, '</ol>', u'Numbered list'),
        (u'###', None, '<ol>', None, '</ol>', u'Numbered list'),
        (u'##', None, '<ol>', None, '</ol>', u'Numbered list'),
        
        # Associations
        (u'::', None, None, None, None, u'Associations, depending on Validator match.')
    )

    XXX_XML2SIMPLEX = (
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
        ('&amp;#', '&#'),         # Solve saving of Cyrillic and other &#xxxx; code to Unicode
        ('<icon>a</icon>', '((a))'),
        ('<icon>b</icon>', '((b))'),
        ('<icon>c</icon>', '((c))'),
        ('<twice/>', '((2x))')
    )

    SIMPLEX2HTML = (
        # Clean up text that may be polluted by control characters or HTML tags.
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
        ('&amp;', '<amp/>'),     # Convert all ampersand types to <amp/>
        ('&', '<amp/>'),
        ('<amp/>#', '&#'),         # Solve saving of Cyrillic and other &#...; code to Unicode.
    )
    def newData(self, **kwargs):
        return self.DATACLASS(**kwargs)
    
    def makeData(self, s):
        u"""Make Data instance from the HTML string s."""
        data = self.newData()
        text = []
        # Split into fields and plain text.
        for line in s.split('\r'):
            if line.startswith('$'):
                parts = line.split(' ')
                if len(parts) > 2:
                    # Get field name and restore rest of the line.
                    data[parts[0][1:].lower()] = ' '.join(parts[1:])
                else:
                    data.error = 'Error in field syntax: "%s"' % line
            else:
                text.append(line)
        data.items = ('\r'.join(text)).split('=C=')
        return data
    
    def compile(self, s):
        u"""Compile the simplex wiki source to HTML."""
        if not s or not isinstance(s, basestring):
            return s

        for t1, t2 in self.SIMPLEX2HTML:
            s = s.replace(t1, t2)
    
        for code, _, t1, content, t2, comment in self.getsimplexcodetaglist():
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
            elif t1 and not t2:
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

        # Split the fields of type $FieldName ...  and create rest of data instance.
        return self.makeData(s)

    def XXXxml2simplex(self, xml, template=None):
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
        <doc>The <code>getsimplexcodetaglist</code> method answer the list with “Simplex” coding and
        the related XML tags. The default behavior is to answer <code>self.SIMPLEXCODESTAGLIST</code>.
        </doc>
        """
        return self.SIMPLEXCODESTAGLIST


    def parseSimplexAssociationAttributes(self, parts, attributes, allowedattributes):
        u"""
        <doc>The <code>parseSimplexAssociationAttributes</code> does parse a list of string <attr>attributes</attr> with
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
        if validator.isImage(association):
            # Just display image.
            parts.append('<img src="%s"/>' % association)

        elif validator.isEmail(association):
            # Make mailto link.
            parts.append('<a href="mailto:%s" class="%s">%s</a>' % (association, self.C.CLASS_MAILTO, association))

        elif validator.isPdf(association):
            # Make PDF link.
            parts.append('<a href="%s" target="download">%s</a>' % (association, association.split('/')[-1]))

        elif validator.isZip(association):
            # Make link to zip file.
            parts.append('<a href="%s" target="download">%s</a>' % (association, association.split('/')[-1]))

        elif validator.isUrl(association):
            # Make URL.
            parts.append('<a href="%s">%s</a>' % association)

        else:
            parts.append('[%s]' % association)

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
        ::abc.jpg|alt=abc::                    <img src="path-to-abc.jpg" alt="abc"/>
        ::abc.jpg|caption=right|alt=abc::    <img src="path-to-abc.jpg" caption="right" alt="abc"/>
        ::www.xierpa.com|target=external::    <a href="www.xierpa.com" target="external">www.xierpa.com</www>
        ::pretty name|href=idname::            <a href="mailto:idname" class="mailto">pretty name</a>

        <h1>To Do</h1>

        ::pretty name|href=id::
        ::abc.jpg|href=www.xierpa.com::        <www>www.xierpa.com</www>

        <h1>Obsolete?</h1>
        ~~::Link|href=www.xierpa.com::                <link href="www.xierpa.com">Link</link>~~
        ~~::Link|href=www.xierpa.com|target=xyz::    <link href="www.xierpa.com" target="xyz">Link</link>~~
        </doc>
        """
        attributedict = self.getAttributeDict(attributes)

        if validator.isImage(prettyname) and attributedict.has_key('href'):
            parts.append('<a href="%s"><img src="%s"></a>' % (attributedict['href'], prettyname))
            self.parseSimplexAssociationAttributes(parts, attributes, self.ASSOCIATION_IMAGEATTRIBUTES)
            parts.append('/>')

        elif validator.isImage(prettyname):
            parts.append('<img src="%s"' % prettyname)
            self.parseSimplexAssociationAttributes(parts, attributes, self.ASSOCIATION_IMAGEATTRIBUTES)
            parts.append('/>')

        elif validator.isEmail(prettyname):
            parts.append('<a href="mailto:%s' % prettyname)
            self.parseSimplexAssociationAttributes(parts, attributes, self.ASSOCIATION_EMAILATTRIBUTES)
            parts.append('">%s</a>' % prettyname)

        elif attributedict.has_key('href'):
            href = attributedict['href']
            if not href.startswith('http://') and not href.startswith('//'):
                href = '//' + href
            parts.append('<a href="')
            parts.append(href)
            parts.append('">')
            parts.append(prettyname)
            parts.append('</a>')

    def parseSimplexAssociation(self, parts, s):
        u"""
        <doc>The <code>parseSimplexAssociation</code> method parses the <attr>s</attr> attribute
        string using Simplex syntax and generates XML coding from the tokens.</doc>
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
        
    def XXXsimplexentry(self, path=None, value=None, type=None, cols=None, rows=None, **kwargs):
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

    def XXXbuildsimplexjs(self):
        u"""
        <doc>The <code>buildsimplexjs</code> method implements the help JavaScript support for the
        Simplex help popup functionality. This method is redefined from the implementation of
        <code>SiteBuilder</code>.</doc>
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

    def XXXbuildsimplexhelpcss(self):
        self.css('div.' + self.CLASS_SIMPLEXHELP, position='absolute', x=0, y=0, z=1000, width=300, visibility='hidden',
            color='black', backgroundcolor='#F0F0F0', margin=100, padding='3px 3px 3px 3px', border='1px solid #ccc',
             boxshadow="#aaa 2px 1px 8px", borderradius='5px 5px 0 0')
        self.css(ids='a.' + self.CLASS_SIMPLEXHELPLINK, textdecoration='none', backgroundcolor='#808080',
            fontsize=self.CSS_FONTSIZETAB, color='white', padding='2px 4px 2px 4px', align='center', valign='middle')
        self.css(ids='a:hover.' + self.CLASS_SIMPLEXHELPLINK, backgroundcolor='#A0A0A0')

    def XXXbuildsimplexhelplink(self):
        u"""
        <doc>The <code>buildsimplexhelplink</code> method build a link (default is the string <code>
        self.LABEL_SIMPLEXHELP</code>) that implements a mouse-over popup showing a table with
        available Simplex codings.</doc>
        """
        self.link(href='#', onmouseover=self.JS_SHOWSIMPLEXHELP, onmouseout=self.JS_HIDESIMPLEXHELP,
                class_=self.CLASS_SIMPLEXHELPLINK)
        self.text(self.LABEL_SIMPLEXHELP)
        self._link()

        if not hasattr(self, 'buildsimplexhelplink_initialized'):
            self.initializesimplexlinkhelp()

    def initializesimplexlinkhelp(self):
        u"""
        <doc>The <code>initializesimplexlinkhelp</code> method builds the div content of the Simplex
        help. If in CMS mode this is done automatically.</doc>
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

        
if __name__ == '__main__':
    # Unit testing
    src = u"""
$field1 This is ''text'' of field 1.
$field2 This is '''text''' of field 2
=C=
=1=Head=1=
This is a __Simplex__ testing text using hy--phe--na--tion.¶
---
=C=
=2=Head level 2=2=
This is a ??Simplex?? testing text.
||This is comment.||
This is a bold ''Simplex'' testing text.
**
*This is a bullet
*This is a bullet
**
##
#This is a numbered list
#This is a numbered list
##
This is an email address ::buro@petr.com::
This is the reference to an image ::/HowToApplyForArtSchool.png::
This is a link ::Home page|href=//petr.com::
This is a link ::Home page|href=//petr.com|alt=abc::
:://www.wikihow.com/Get-Into-an-Art-School::
:://www.creativebloq.com/career/5-things-you-must-do-when-applying-art-college-5132555::
    """
    simplex = Simplex()
    data = simplex.compile(src)
    print data.field1
    print data.field2
    for chapter in data.items:
        print chapter
    print data.fields
