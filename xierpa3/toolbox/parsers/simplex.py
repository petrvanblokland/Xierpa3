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
        (u'??', None, '<span class="%s">' % C.CLASS_QUESTION, None, '</span>', u'Question'),
        (u'!!', None, '<span class="%s">' % C.CLASS_ANSWER, None, '</span>', u'Answer'),
        (u'!!!', None, '<div class="%s">' % C.CLASS_PULLQUOTE, None, '</div>', u'Pull quote'),
        #(u'::', None, '<associated>', '</associated>', u'Associated link<br/>::associated words::<br/>::www.xierpa.com::<br/>::image.png::<br/>::buro@petr.com::'),
        (u'****', None, '<ul>', None, '</ul>', u'Bullet list'),
        (u'***', None, '<ul>', None, '</ul>', u'Bullet list'),
        (u'**', None, '<ul>', None, '</ul>', u'Bullet list'),

        # (u'*', RE_SIMPLEXBULLET, None, None, u'Bullet'),
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
$category Blog 
$level Novice
$title How to get into art school
$poster //data.doingbydesign.com.s3.amazonaws.com/_images/udemycourses/HowToApplyForArtSchool.png
$author Petr van Blokland
$contact ::buro@petr.com::
$topic Practical tips to get admitted into art school.
$summary Applying for admission in an art school can feel like a lottery. “Will they take me or not?” And for sure there is a factor of chance involved, especially if the amount of applying students is much bigger than the number of available seats. 
$featured manifest-on-skilss, generous-gesture, how-to-build-a-simple-kirby-site, how-to-build-a-xierpa3-site

=1=Why and how?=1=

=lead=
In a world where only a handful of people seem to have 
the knowledge and skills to perform a certain task, it hard for fresh students
to aqcuire these skills. Except for a few, who already do it and would have
done it anyhow. Not because of their education, but despite their education.
For all other fresh students this gap is increasing by the day. Not only
it is hard to motivation, it is also a challenge to maintain it for a number
of years, before skill and experience are on a level to compete witht the
happy few, those who already got it. Becasue they were fast learners
or because they were lucky enough to be raised in an evironment that
supported their ambitions.
=lead=

Applying for admission in an art school can feel like a lottery. “Will they take me or not?” And for sure there is a factor of chance involved, especially if the amount of applying students is much bigger than the number of available seats.¶ 

But in the other hand a lot can be said about very generic points of attention that almost always play a role in the selection of new students. Knowing about how selections work and what it is that the selectors want to put their focus on, certainly will help the student during the admission process. No matter the differences between art schools in different countries and cultures, there is a common ground that is true for most situations. 
This course shows students the steps that will improve their presentation and increase their chances to become admitted.¶

You have to present yourself in an extended elevator pitch. The procedures do vary from one art school to another, but the common ground is that you will be given a limited time slot and you want to says and show too. This course is about the selection process – what to say and what to show – and about the improvement of your presentation skills.¶

Art schools are interested to see the process: how did you get to final results. Can you make clear why you made the choices that you did.¶

!!!The processes and parameters described in this course may not seem compatible. These are all parameters that otherwise would have guided the course in a more dedicated direction.!!!

Art schools not interested seeing just the final results. It is hard to conclude from there how much you contributed to the solution and if the solution was a “lucky shot” or the result of a range of design decisions.

=C=

=1=Do’s and Don’ts=1=

=2=Do’s=2=

**
* Do remember that being an artist or designer is a profession. It is not something you are able to do after one or more creative courses.
* Have an opinion about your work, in relation to other things that you did and also in relation to other artists and designers.
* Stand out from the crowd. This could mean that you try to explore the boundaries of the admission rules. But never do less. While fully complying with the rules, there are always possibilities to interpret them in a way that the admission committee will remember you.
* Find the right balance between the “bright kid that will change the world” and the “enfant terrible” who is not willing to learn new trick and just will give trouble.
**

=2=Don’ts=2=

**
* Don’t be shy about what your skills are. Without being untrue, you apply for a position where it matters what you think and what you do.
* Never copy work of other, while pretending it is your own. Don’t mix your work with the work of others. And if you cannot avoid it (e.g. using photo’s in a research thesis or in the design of a page), make sure always to mention the source. Remember that the reviewers at art schools often have an excellent visual memory. This also applies to traced drawings of existings photo’s. They are able to tell that you did so.
**

=C=

=1=Aspects of matriculations=1=

=2=Preparation=2=

**
* Admission day
* Selecting art schools
* Preparing the port folio
* Write the admission motivation
* Credentials and diplomas
* Dates for submission
* Open days
* Writing a thesis
* Do research
* Execution of specific assignments at home
* Visa and other issues regarding legal documents
* Paying the yearly fee
* Language
**

:://www.thetimes.co.uk/tto/multimedia/archive/00515/Art_School__20_best_515680a.jpg::

=2=Admission day=2=
**
* Execution of assignments during the day of admission
* Showing of portfolio
* Admission interview (live or through skype/hangout)
**

=2=Selecting art schools=2=

**
* Online information, printed information, recommendations and open days
* (Online) galleries
* What are your educational goals?
* Type of education (groups, individually, online, personal counseling, …)
* Study the work of alumni students
* Ratio between theory and practice
* Ratio between technical skills, esthetical skills, critical skills and research skills.
* Admission criteria
* Geographical position
* Value and level of the graduation, some courses, Bachelor, Master and/or Phd, depends if you want to engance your creativity or want to make a living with your skills.
* Lenght of the study
* Cost
**

=2=Preparing the port folio=2=

**
* Collecting work
* Making new stuff
* Dummies and sketchbooks
* Selecting work. Completeness is not important. It is important to give a relevant and reliable overview on your skills. Your best work may not be the one that tells most. Show both diversty and depth. Both processes and finals.
* Writing background information. If your work is older than 3-4 years, make sure that there is a date on it, and add your motivation why it is in your port folio.
* Making the physical presentation
* Making a PDF file, website or other digital document
Volgens Yvo de Ruiter
* Je portfolio is een werkstuk op zich; niet alleen het werk dat je laat zien is belangrijk, maar de vormgeving van je portfolio zelf wordt net zo beoordeeld
* Laat de vorm van je portfolio niet het werk overstemmen
* Toon minimaal 5 en maximaal 15 projecten; kiezen (redactie) is ook een belangrijke kunde
* Toon per pagina 1 of 2 beelden; niet teveel kleine plaatjes bij elkaar zetten om heel veel te willen laten zien, maar liever een pagina meer
* Beelden niet herhalen (bv drie keer hetzelfde ontwerp in een ander kleurtje of uit een niet iets andere hoek gefotografeerd
* Gebruik ruimte om je werk (dus niet aflopend van de pagina, maar met wat lucht er omheen)
* Per project een kort tekstje (voor wie, wanneer, wat was opdracht, wat was je concept (gedachtegang), hoe heb je het opgelost
* Liever een klein mapje, losse bladen of digitale presentatie dan een grote A1 map met glanzende plastic tassen
* Zorg voor een begin, midden en eind in de opbouw; ken waarde toe aan verschillende projecten
* Zorg voor ritme; wissel grote beelden af met kleine, laat af en toe een pagina leeg, benoem hoofdstukken
* Duidelijk naam vermelden
* Doe een CV in je portfolio
* Maak foto's van je werk en geen printje van het werkdocument
* Maak goede foto's van je werk, dus met wat diffuus licht en goed contrast, witte achtergrond
* Oefen een paar keer wat je per project wilt vertellen (tekstje bij project fungeert ook als spiekbrief!)
* Bedenk van tevoren vragen die JIJ wilt stellen aan de beoordelaar van je portfolio (probeer het gesprek te leiden en wees assertief)
* Maak het authentiek, geef het een eigen sfeer en wees niet bang je eigen identiteit te tonen
* Laat iets achter (bv een mini-versie van je portfolio)
* Maak indruk, geef een reden om jou te onthouden
**

=2=Write the admission motivation=2=
**
* Study the requirements given by the art school
* Write a motivation that fully fits these requirements and think about adding personal angles.
* Start early, it may need several versions to make the final one. And if writing is not one of your main skills, then there is even more reason not to postpone this part of the admission until it is too late.
* Make bullets lists about what you want to say. Think about their order and relevance.
* Let the language and spelling check by someone else
* Design the motivation document, or let someone help you with the layout if graphic design and typography is not part of your basis skills
* Design the presentation of the document, depending on the required technique and medium.
Credentials tests and diplomas
* Although the skills of art and design are hard to quantify (good artists and designers by definition do not fit in existing categories), art schools often are a department of larger educational institutes, the do have a strict description of required credentials and diplomas. Make sure that yours fit what the institution needs. It is a waste of time and effort if the admission is rejected purely on formal issues.
* SAT/ACT/TOFEL scores http://collegeapps.about.com/od/standardizedtests/
* Make sure that the diplomas you have are valied and recognized, if you apply in another country.
**

=2=Dates for submission=2=

=2=Open days=2=

=2=Writing a thesis=2=
Sometimes applying for an art school requires writing a thesis about a given subject. Schools do that to test your abilities of writing besides your visual skills. Also they want to test if you can do research, thinking and writing about a given subject, that is related to your future profession.
**
* General tips & tricks about researching a new topic here.
* General tips & tricks about writing here.
Do research
* Prepare yourself by doing research in the kind of questions to can expect during the interview. The reviewers want to get an idea about your current state of knowledge and skills. They will test you, sometimes with a trick question. Do research on the institution that you are applying, its history.
Execution of specific assignments at home.
**
 
=2=Visa and other issues regarding legal documents=2=

=2=Paying the yearly fee=2=
**
* The cost of art school can be very different, from almost free to $50.000 per year. Besides the obvious that you need to have that amount of money available, 
* There is a certain relation between the cost of the course and the offered quality, but the relation on not very fixed. There are very good courses that cost a lot less and there are very expensive ones that don’t add so much to your artistic skills, rather than giving you an academic tittle.
* Verify what additional cost you can expect during your course, such as a required computer, materials, books and memberships.
* If you are going abroad, then also add the cost for travelling (how often do you want to go home during the time of your study), housing, additional courses e.g. to speak the native language of the course, of that is necessary.
**

=2=Language=2=

=2=Execution of assignments during the day of admission=2=

=2=Showing of portfolio=2=

**
* Verify if you will be presenting the port folio in person or if they admission comiittee will go through it without you being there. The difference is that you have to add you comments in written form, if you are not there to present it.
Admission interview (live or through skype/hangout)
* Show up on time
* Your clothes and the rest of your visual presentation may be important. Check out in advance to what extend this is true.
* Decide on what the most important things are that you want to tell. Make sure you have a list with you to check if you addressed them all.
* Make notes about what people tell you about your work. In case there is a possibility to
* An interview in person always works better than on through skype of hangout.
* If you are not in the position to go there, then prepare your online presentation well: rehearse the presentation with someone else, to make sure that the technique works and to verify that there iis enough band width in your place. Wear headphones (preferably an invisible in-ear model) to avoid echos on the other side. If the language of the presentation is not your native language then practice the interview with other people in that language.
* Be aware of what you write on Twitter or Facebook. Art school teachers also read online.
**

=2=Summary=2=

This course does focus on the admission into art schools. But many of the rules of thumb are also valid in other situations where the artist or designer needs to convince other people about his/her skills and capacities. Presenting to a potential customer, to a subsidy committee or when applying for a job in a creative function, identical or similar processes are important.

=3=Links=3=
:://www.wikihow.com/Get-Into-an-Art-School::
:://www.creativebloq.com/career/5-things-you-must-do-when-applying-art-college-5132555::
:://artbistro.monster.com/education/articles/10997-how-to-get-into-art-school::


"""
    simplex = Simplex()
    data = simplex.compile(src)
    print data.field1
    print data.field2
    for chapter in data.items:
        print chapter
    print data.fields
