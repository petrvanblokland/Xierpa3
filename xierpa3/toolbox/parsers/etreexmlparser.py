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
#    etreexmlparser.py
#
import os
from lxml import etree

XIERPANAMESPACE = 'http://www.xierpa.com/xslt'

CACHING = False

class UnbasedPathResolver(etree.Resolver):
    """
    XML parsing solution based on LXML etree. Implements a resolver for XSL files that can search upwards the path when
    an relative path is defined.
    """
    cache = {}

    def resolve(self, url, id, context):
        u"""
        The ``resolve`` method resolves the file system path for finding XSL modules to include. URL is a full
        fspath built up by LXML, we have to disassemble it to find the parts of the tree that we then separately test on
        the existence of _xsl and the run upwards until we find a match. Store the found XSL source in the class cache
        under the URL as key with a time stamp.
        """
        cachedxsl = UnbasedPathResolver.cache.get(url)
        if CACHING and cachedxsl is not None:
            timestamp, path, xsl = cachedxsl
            if timestamp == os.path.getmtime(path):
                # Nothing changed, use the cache XSL content.
                return self.resolve_string(xsl, context)

        fsroot = None

        # Remove FSROOT
        if fsroot and url.startswith(fsroot):
            path = url[len(fsroot):]
        else:
            path = url

        # Split on _xsl and split the search path
        index = url.find('/_xsl')
        dirs = url[:index].split('/')
        path = url[index:]

        # Run over search path to test if file exists
        for i in range(len(dirs), 0, -1):
            p = fsroot + '/'.join(dirs[:i]) + path
            if os.path.exists(p):
                f = open(p, 'rb')
                xsl = f.read()
                f.close()
                UnbasedPathResolver.cache[url] = xsl
                return self.resolve_string(self.unicodify(xsl), context)
        return None


    def unicodify(self, s):
        u"""
        
        Make sure, whatever ``s`` is, that there is a value Unicode string answered. If ``s`` is not a
        string then use ``str(s)`` to convert to a string first. This will make database records convert to a
        string of their id, instead of showing the record ``repr`` result. <em>Note that it might be that
        ``str`` will cause an error on the content of the object such as a list.</em>. ``None`` is
        replaced by an empty Unicode string.
        
        """
        if s is None:
            return u''
        if isinstance(s, unicode):
            return s
        if not isinstance(s, basestring):
            s = str(s)
        try:
            return unicode(s, 'utf-8')
        except UnicodeDecodeError:
            return s

        raise ValueError("can't handle string s")

class XmlParser:
    def __init__(self, e, nocache):
        self.e = e
        if nocache:
            UnbasedPathResolver.cache = {}

        self.parser = etree.XMLParser()
        self.parser.resolvers.add(UnbasedPathResolver())

    def _gete(self, e, key):
        data = e[key]
        if data is None:
            return False
        return data

    def _getform(self, e, key):
        data = e.form[key]
        if data is None:
            return False
        return data

    def _getsession(self, e, args):
        #
        #   For all arguments, try to get the value from session and the
        #   contained lists and dicts.
        #   A dict
        #
        #   Data                                        args                answer
        #   e.session['aa'] = 12                        ['aa']              12
        #   e.session['aa'] = {'bb': 100, 'cc': 200}    ['aa', 'bb']        100
        #   e.session['aa'] = ['bb', 'cc']              ['aa', 'bb']        True
        #
        data = e.session
        if not args:
            # No arguments, just answer if the session exists.
            return bool(data)
        for arg in args:
            if hasattr(data, 'has_key'):
                # Data (initially e.session) behaves as a dict
                data = data.get(arg)
                continue

            if isinstance(data, (list, tuple)):
                data = arg in data
            elif isinstance(data, (bool, int, float, long, basestring)):
                pass
            elif not data:
                data = False
            else:
                # Unknown object, just show its string representation
                data = str(data)
            break

        return data

    def isvalidxml(self, xml):
        u"""
        The ``isvalidxml`` method answers the boolean flag id ``xml`` is a valid XML string. The
        method adds a module root tag, so the ``xml`` does not need to have a root tag. 
        """
        try:
            etree.fromstring(u'<module>' + (xml or '') + '</module>')
            return True
        except etree.XMLSyntaxError, e:
            print e
        return False

    def parse(self, src=None, xml=None, checkunicode=False, catchexception=True):
        u"""
        The ``parse`` method with parse either a ``src`` or ``xml``. If defined the
        ``xml`` attribute must be of type unicode. If the ``checkunicode`` attribute (default value is
        ``False``) is ``True`` then an error is raised if the ``xml`` string is not unicode.
        <br/>
        
        If the optional ``catchexception`` (default value is ``True``) is set to ``False``
        then the parser does not try to catch as parser error. This allows the calling application class to  get a
        better view on the type of XML error.
        """
        if src is None:
            if checkunicode:
                assert isinstance(xml, unicode), '[XmlParser.parse] XML must be unicode: "%s"' % xml

            if not catchexception:
                return etree.fromstring(xml)
            else:
                try:
                    doc = etree.fromstring(xml)
                    return doc
                except etree.XMLSyntaxError:
                    try:
                        xml = '' + xml + ''
                        doc = etree.fromstring(xml)
                        return doc
                    except etree.XMLSyntaxError:
                        msg = 'Error while parsing docstring for xml'
                        print 'source:', src, 'xml:', xml.encode('utf-8')
                        return etree.fromstring(msg)

        if src.startswith('/_root'):
            src = src[len('/_root'):]
        else:
            src = self.e.path2fspath(src)
        return etree.parse(src, self.parser)

    def transform(self, sourcedoc, template, functions):

        # We have to build these three methods here, or else we don't have
        # the e available when called back from XSLT
        def gete(dummy, key):
            return self._gete(self.e, key)

        def getform(dummy, key):
            return self._getform(self.e, key)

        def getsession(dummy, *args):
            return self._getsession(self.e, args)

        # Build the name space for the three get functions
        prefixmap = {'xp': XIERPANAMESPACE}
        ns = etree.FunctionNamespace(XIERPANAMESPACE)
        ns['e'] = gete
        ns['form'] = getform
        ns['session'] = getsession
        # Add all required extension functions
        if functions is not None:
            for name, function in functions.items():
                ns[name] = function

        if template is None:
            resultdoc = None
        else:
            # <todo>TODO</todo>: Maybe add caching of style docs in the future?
            styledoc = etree.parse(self.e.path2fspath(template), self.parser)
            # style = etree.XSLT(styledoc, prefixmap)
            style = etree.XSLT(styledoc)
            resultdoc = style.apply(sourcedoc)
        return resultdoc

    def tostring(self, doc):
        return etree.tostring(doc.getroot())
