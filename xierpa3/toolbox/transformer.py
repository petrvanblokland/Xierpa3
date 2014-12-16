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
#     transformer.py
#
import os
import re
import urllib
import inspect
from xierpa3.constants.constants import Constants
from xierpa3.toolbox.dating import uniqueId

class Transformer(object):

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Constants

    # ---------------------------------------------------------------------------------------------------------
    #     M E A S U R E

    @classmethod
    def px(cls, n):
        u"""
        
        The ``px`` method interprets the value <attr>n</attr>. If it converts to an integer, then
        add ``'px'``. So when the number needs to be a plain value (e.g. as in line-height), then 
        write the number as float or a string that converts to a float (containing a ``'.'``). 
        If the value is ``0`` then don't add ``'px'``.
        If the value is list or tuple each item is added as ``px(item)`` to the returned string.
        
        """
        if n is None:    # If not defined, then don't transform
            return None
        if isinstance(n, basestring) and n.startswith('#'): # Ignore colors
            return n
        if not (isinstance(n, float) or (isinstance(n, basestring) and '.' in n)) and cls.isInt(n):
            return str(n) + 'px'
        if isinstance(n, (list, tuple)):
            # If a list, build as separate items
            l = []
            for item in n:
                l.append(cls.px(item))
            return ' '.join(l)
        return str(n)

    # ---------------------------------------------------------------------------------------------------------
    #     J A V A S C R I P T

    @classmethod
    def args2JsArguments(cls, **args):
        u"""
        
        The ``args2JsArguments`` method translates the arguments <attr>**args</attr> into
        a dictionary Javascript source. The value of the argument is tested on type and converted
        into the right Javascript syntax. If the value starts with ``'js:'`` then this
        prefix is removed, and the value is used as such, assuming that it is a chunk of Javascript
        source code. This way the value Ajax event call of e.g. popups can get their own value on
        mouseup.
        
        """
        result = []
        for k, v in args.items():
            if v is None:
                continue
            if isinstance(v, bool):
                result.append(u"'%s':%s" % (k, repr(v).lower()))
            elif isinstance(v, (int, float)):
                result.append(u"'%s':%s" % (k, v))
            elif isinstance(v, long):
                result.append(u"'%s':%s" % (k, repr(v)[:-1]))
            elif isinstance(v, basestring) and v.startswith('js:'):
                result.append(u"'%s':%s" % (k, v[3:]))
            elif isinstance(v, basestring):
                result.append(u"'%s':'%s'" % (k, v))
            elif isinstance(v, dict):
                result.append(u"'%s':%s" % (k, cls.args2JsArguments(**v)))
            elif isinstance(v, dict):
                result.append(u"'%s':%s" % (k, cls.args2JsArguments(**v)))
            elif isinstance(v, (list, tuple)):
                if len(v) == 1 and isinstance(v[0], dict):
                    result.append(u"'%s':%s" % (k, cls.args2JsArguments(**v[0])))
                else:
                    result.append(u"'%s':%s" % (k, list(v)))
                    # result.append(u"'%s':['%s']" % (k, cls.joinArgumentList(v)))
                    # result.append(u"'%s':['%s']" % (k, "','".join(v)))
        return "{" + ','.join(result) + "}"

    @classmethod
    def ajaxJavascriptCall(cls, method='ajaxlink', **args):
        u"""
        
        The ``ajaxJavascriptCall`` method answers the Javascript source for a function call
        named <attr>method`` (default value is ``'ajaxlink'``) and with arguments <attr>**args</attr>
        as a dictionary that is the result of ``args2JsArguments(**args)``.
        
        """
        return "%s(%s,this);" % (method, cls.args2JsArguments(**args))

    # ---------------------------------------------------------------------------------------------------------
    #     U R L

    @classmethod
    def obj2List(cls, obj):
        u"""
        
        The ``obj2List`` method convert to <attr>obj</attr> attribute to a list.
        If the <attr>obj</attr> is a ``basestring`` then perform a comma split.
        Tuples are converted to lists.
        
        """
        if isinstance(obj, basestring):
            l = obj.split(',')
        else:
            l = list(obj)
        return l

    @classmethod
    def swapKeyValue(cls, dict):
        u"""
        
        The ``swapKeyValue`` method swaps the key and value of <attr>dict</attr>, 
        and answers that a new dict.
        
        """
        swapped = {}
        for key, value in dict.items():
            swapped[value] = key
        return swapped

    @classmethod
    def obj2Dict(cls, obj):
        u"""
        
        The ``obj2Dict`` method answers the <attr>obj</attr> attribute converted to a dictionary.
        If the <attr>obj</attr> is a string, then it is firstly converted into a list, separated on commas.
        Then the list is concerted into a dictionary, using the index as key.
        If the <attr>obj</attr> is a list of 2-item tuples as ``((key, value), ...)`` then
        interpret the first one as key and the second one as value.<br/>
        If the <attr>obj</attr> is already a dictionary, then is it answered untouched.
        
        """
        d = {}
        if isinstance(obj, (basestring, list, tuple)):
            obj = cls.obj2List(obj)
        if isinstance(obj, (list, tuple)):
            if obj and len(obj[0]) == 2:
                for key, value in obj:
                    d[key] = value
            else:
                for index, value in enumerate(obj):
                    d[index] = value
        elif isinstance(obj, dict):
            d = obj
        return d

    @classmethod
    def dict2ReversedDict(cls, d):
        u"""
        
        The ``dict2ReversedDict`` answers a new dictionary where the key/valye pair of 
        <attr>d</attr> is reversed.
        
        """
        reversed = {}
        for key, value in d.items():
            reversed[value] = key
        return reversed

    ACCENT2ASCII = {
        u'ë': 'e', u'è': 'e', u'é': 'e', u'ê': 'e',
        u'ö': 'o', u'ò': 'o', u'ó': 'o', u'ô': 'o', u'õ': 'o', u'ø': 'o',
        u'ü': 'u', u'ù': 'u', u'ú': 'u', u'û': 'u',
        u'ï': 'i', u'ì': 'i', u'í': 'i', u'î': 'i',
        u'ä': 'a', u'à': 'a', u'á': 'a', u'â': 'a', u'ã': 'a', u'å': 'a',
        u'ñ': 'n',
        u'ç': 'c',
        u'æ': 'ae',
        u'œ': 'oe',
        u'Ë': 'e', u'È': 'e', u'É': 'e', u'Ê': 'e',
        u'Ö': 'o', u'Ò': 'o', u'Ó': 'o', u'Ô': 'o', u'Õ': 'o', u'Ø': 'o',
        u'Ü': 'u', u'Ù': 'u', u'Ü': 'u', u'Û': 'u',
        u'Ï': 'i', u'Ì': 'i', u'Í': 'i', u'Î': 'i',
        u'Ä': 'a', u'À': 'a', u'Á': 'a', u'Â': 'a', u'Ã': 'a', u'Å': 'a',
        u'Ñ': 'n',
        u'Ç': 'c',
        u'Æ': 'ae',
        u'Œ': 'oe',
        # @@@ To be finished
    }

    @classmethod
    def extensionOf(cls, path):
        u"""
        
        The ``extensionOf`` method answers the lowercase extension of the <attr>path</attr>.
        If there is no extension, answers an empty string. If the extension cannot be derived,
        then answer ``None``.
        
        """
        parts = path.split('/')[-1].split('.')
        if len(parts) > 1:
            return parts[-1].lower()
        return None

    @classmethod
    def name2UrlName(self, name, pattern=None, usehyphen=True, lower=True):
        u"""
        
        The ``name2UrlName`` method converts the <attr>name</attr> attribute to a name that is safe to be used
        in an URL. This method is used for uploaded images with unknown (and probably wrong) filenames. Also it is used
        to derive the ``self.FIELD_IDNAME`` content from ``self.FIELD_NAME``. The processing also
        takes care that not multiple hyphen exist in a row.<br/>
        
        The optional <attr>pattern</attr> (default set to
        ``'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-1234567890'``) allows the use of other
        patterns.<br/>
        
        If there is a period in the name, then it might be part of the extension. Split the name into a
        ``name.extension`` and recursively solve the parts.<br/>
        
        If the <attr>usehyphen</attr> attribute is set (default value is ``True``), then allow the use of
        hyphens (divider between parameter and value in Xierpa syntax), otherwise all hyphens are replaced by
        underscores.
        
        """
        if not name:
            return
        if name.startswith('/'):
            name = name[1:]
        if isinstance(name, str):
            # Convert to Unicode.
            name = name.decode('utf-8')

        if pattern is None:
            pattern = u'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_1234567890'

        urlname = []
        hadHyphen = True

        for c in name:
            if c in ' /':
                c = '-'
            elif not c in pattern:
                cc = ''
                for key, accents in self.ACCENT2ASCII.items():
                    if c in accents:
                        cc = key
                c = cc

            if c != '-' or not hadHyphen:
                urlname.append(c)

            hadHyphen = c == '-'

        urlname = ''.join(urlname)
        if not usehyphen:
            urlname = urlname.replace('-', '_')
        while urlname and urlname[-1] in '-_':
            urlname = urlname[:-1]
        if lower:
            urlname = urlname.lower()
        return urlname

    @classmethod
    def path2LinkLabel(cls, path):
        return path.split('/')[-1]

    @classmethod
    def path2Dir(cls, path):
        return '/'.join(path.split('/')[:-1])
    
    @classmethod
    def asDir(cls, path):
        u"""Make sure that path expands local user and always ends with a slash."""
        if path is None:
            path = ''
        path = os.path.expanduser(path)
        if not path.endswith('/'):
            path += '/'
        return path
    
    @classmethod
    def path2NoExtension(cls, path):
        u"""Remove the extension from the path if it exists in the filename part."""
        parts = path.split('/')
        fileNameParts = parts[-1].split('.')
        return '/'.join(parts[:-1]) + '/' + '.'.join(fileNameParts[:-1])
    
    @classmethod
    def path2Name(cls, path):
        u"""Remove the path and the extension from the file name."""
        fileName = path.split('/')[-1]
        fileNameParts = fileName.split('.')
        if len(fileNameParts) > 1:
            return '.'.join(fileNameParts[:-1])
        return fileName
    
    @classmethod
    def path2PathParams(cls, path, params):
        params = dict(params)
        while path.endswith('/'):
            # Remove trailing slashes
            path = path[:-1]
        keys = params.keys()
        keys.sort()
        for key in keys:
            values = params[key]
            if not isinstance(values, (list, tuple)):
                values = [values]
            for value in values:
                if value is None:
                    continue
                elif value in [1, '1']:
                    path += '/' + key
                elif not isinstance(value, basestring):
                    path += '/%s-%s' % (key, str(value))
                else:
                    path += '/%s-%s' % (key, value)
        return path

    @classmethod
    def module2Path(cls, module):
        fspath = module.__file__
        for s in ('/__init__.pyc', '/__init__.py'):
            fspath = fspath.replace(s, '')
        return fspath

    @classmethod
    def class2Path(cls, o):
        # Answer the file path where the class of o if defined. This only works with real object.
        try:
            return '/'.join(inspect.getfile(o.__class__).split('/')[:-1])
        except TypeError:
            return None

    @classmethod
    def asGetMethodName(self, contentID):
        # Answer the contentID as method get identifier.
        return 'get' + contentID[0].upper() + contentID[1:]

    # ---------------------------------------------------------------------------------------------------------
    #     F I L E

    @classmethod
    def isFsPathChanged(cls, srcfspath, dstfspath):
        u"""
        
        The ``isFsPathChanged`` method answers the boolean flag if <attr>srcfspath</attr> is modified
        after <attr>dstfspath</attr> was modified. Note that these files need not be the same (kind of) files. 
        
        """
        return cls.isPathModified(srcfspath, cls.getPathModificationTime(dstfspath))

    @classmethod
    def isPathModified(cls, fspath, mtime):
        u"""
        
        The ``isPathModified`` method answers the boolean flag if the <attr>fspath</attr> is modified
        after the <attr>mtime</attr>.
        
        """
        return bool(cls.getPathModificationTime(fspath) > mtime)

    @classmethod
    def getPathModificationTime(cls, fspath):
        u"""
        
        The ``getPathModifocationTime`` method answers the modification time of the <attr>fspath</attr>.
        
        """
        return os.stat(fspath).st_mtime

    @classmethod
    def asPath(cls, fspath):
        u"""
        
        The ``asPath`` method answers the <attr>fspath</attr> converted to a string
        that starts with a slash and does not end with a slash.
        
        """
        while fspath and fspath.endswith('/'):
            fspath = fspath[:-1]
        if fspath and not fspath.startswith('/'):
            fspath = '/' + fspath
        return fspath

    # ---------------------------------------------------------------------------------------------------------
    #     G E T T E R

    @classmethod
    def getDictValue(cls, d, path='', default=''):
        u"""
        
            The ``getDictValue`` returns a deep dict key value if the key is in the dict, 
            such as ``dict['aa']['bb']`` where the keys is defined in <attr>path</attr> - 
            a slash separated string list or a list. There's no errors if the <attr>path</attr> is 
            not in the dict, an empty string or <attr>default</attr> is returned.<br/>
            getDictValue(dict, 'aa/bb')<br/>
            getDictValue(dict, ['aa','bb'])<br/>
        
        """
        if not path:# or not isinstance(d, dict):
            return default
        if not isinstance(path, (list, tuple)):
            path = path.split('/')
        value = d.get(path[0])
        if len(path) > 1:
            if isinstance(value, dict):
                value = cls.getDictValue(value, path[1:], default)
            else:
                value = default
        return value

    # ---------------------------------------------------------------------------------------------------------
    #     I D  &  F I E L D

    @classmethod
    def tableAtField(cls, table, field, db=None, editor=None):
        u"""
        
        The ``tableAtField`` method answers the name of a form field as ``'table@field'``
        from the <attr>table</attr> and <attr>field</attr> attributes. This name will be automatically recognized
        and connected to the a table and field in the record saving mechanism. <br/>
        If <attr>editor</attr> is defined, it is added to the field name as ``'table@field:editor'`` 
        so the field can be recognized for that editor only.
        
        """
        if db is None:
            tableatfield = '%s@%s' % (table, field)
        else:
            tableatfield = '%s:%s@%s' % (db, table, field)
        if editor:
            tableatfield += ':%s' % editor
        return tableatfield

    @classmethod
    def path2Field(cls, path):
        """
        
        The ``path2Field`` splits a path of format ``'db:table@field`` and answers the field.<br/>
        If the <attr>path</attr> attribute does not contain a ``@``, then answer the full path.
        
        """
        if not path:
            return None
        return path.split('@')[-1]

    @classmethod
    def path2DbName(cls, path):
        """
        
        The ``path2Field`` splits a path of format ``'db:table@field`` and answers the db name.<br/>
        If the <attr>path</attr> attribute does not contain a ``@``, then answer the full path.
        
        """
        return path.split(':')[0]

    @classmethod
    def path2TableName(cls, path):
        """
        
        The ``path2TableName`` splits a path of format ``'db:table@field`` and answers the table name.<br/>
        If the <attr>path</attr> attribute does not contain a ``@``, then answer the full path.
        
        """
        parts = path.split(':')
        if len(parts) > 2:
            return None
        parts = parts[-1].split('@')
        if len(parts) > 2:
            return None
        return parts[0]

    @classmethod
    def asId(cls, value, default=0):
        u"""
        The ``asId`` method transforms the <attr>value</attr> attribute either to an instance of ``
        long`` or to ``None``, so it can be used as <attr>id</attr> field in a ``Record``
        instance. If the value cannot be converted, then the optional <attr>default</attr> (default value is ``0
        ``) is answered.<br/>
        """
        try:
            value = long(value)
            if value <= 0:
                return default
            return value
        except (ValueError, TypeError):
            return default

    @classmethod
    def isId(cls, value):
        u"""
        
        The ``isId`` method tests if the <attr>value</attr> can be converted to an id (long or int). The
        boolean result is answered.
        
        """
        try:
            return bool(cls.asId(value))
        except ValueError:
            pass
        return False

    LETTERS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_1234567890')

    @classmethod
    def asIdentifier(cls, value):
        u"""
        
        The ``asIdentifier`` method answers <attr>value</attr> as identifier by filtering all non-alphanumeric
        from the string.
        
        """
        if not isinstance(value, basestring):
            value = `value`
        identifier = ''
        for c in value:
            if c in cls.LETTERS:
                identifier += c
            else:
                identifier += cls.ACCENT2ASCII.get(c) or ''
        return identifier

    @classmethod
    def asString(cls, s):
        u"""
        
        The ``asString`` method converts the object <attr>s<attr> to string.
        
        """
        if isinstance(s, basestring):
            return s
        return `s`

    @classmethod
    def asList(cls, o):
        if not isinstance(o, (list, tuple)):
            o = [o]
        return o

    # ---------------------------------------------------------------------------------------------------------
    #     S Q L  C O N V E R S I O N S

    @classmethod
    def escapeSqlQuotes(cls, s):
        u"""
        
        Prevent hacking: escape single quote in SQL string, change every single quote to ``''``. Postgres/SQL
       interprets and inserts only a single quote in the database.
        
        """
        if s is not None and isinstance(s, basestring):
            s = s.replace("'", "''").replace('\\', '\\\\')
        return s

    # ---------------------------------------------------------------------------------------------------------
    #     X M L  C O N V E R S I O N S

    @classmethod
    def dataAttribute2Html5Attribute(cls, key):
        u"""
        
        The ``dataAttribute2Html5Attribute`` method converts an <attr>key</attr> attribute that starts with
        ``'data_'`` to the HTML5 attribute that starts with ``'data-'``. Otherwise the <attr>key<attr>
        attribute is answered unchanged.
        
        """
        if key.startswith(u'data_'):
            return 'data-' + key[5:]
        return key

    @classmethod
    def pyAttrName2XmlAttrName(cls, key):
        u"""
        The ``pyAttrName2XmlAttrName`` converts the Python XML attribute name ``key`` to an
        appropriate XML attribute identifier.<br/>.
        If the <attr>key</attr> is ``'class_'`` then it is translated into ``'class'``.
        If there is an HTML5 attribute <attr>data_xxxx</attr> used, then change that to <attr>data-xxxx</attr>.
        """
        if key == 'class_':
            key = 'class'
        if key.startswith('data'):
            key = key.replace('_', '-')
        return key

    @classmethod
    def xmlAttrName2PyAttrName(cls, key):
        u"""
        
        The ``xmlAttrName2PyAttrName`` method converts the XML attribute name <attr>key</attr> to an
        appropriate Python attribute identifier.<br/>
        If the <attr>key</attr> is ``'class'`` then it is translated into ``'class_'``. If a namespace
        is defined (to be recognized on {...}, then replace that by prefix ``'ns_'``.<br/>
        If there is an HTML5 attribute <attr>data-xxxx</attr> used, then change that to <attr>data_xxxx</attr>.
        
        """
        if key == 'class':
            key = 'class_'
        elif key.startswith('{'):
            key = 'ns_' + key.split('}')[-1]
        elif '-' in key:
            # In case of new HTML5 data-xxxx attributes.
            key = key.replace('-', '_')
        return key

    @classmethod
    def xmlValue2PyValue(cls, value, conversions):
        u"""
        
        The ``xmlValue2PyValue`` method converts the XML string attribute to the appropriate Python object
        type, if the class is defined in the list <attr>conversions</attr>. If the <attr>value</attr> is not a string,
        it must have been converted before (e.g. by self.EXPR), the answer it untouched.
        
        """
        if not isinstance(value, basestring):
            return value

        strippedvalue = value.strip()

        if int in conversions:
            try:
                return int(strippedvalue)
            except ValueError:
                pass

        if long in conversions:
            try:
                return long(strippedvalue)
            except ValueError:
                pass

        if float in conversions:
            try:
                return float(strippedvalue)
            except ValueError:
                pass

        if bool in conversions:
            if strippedvalue.lower() in ['true', 'false']:
                return strippedvalue.lower() == 'true'

        if dict in conversions or list in conversions or tuple in conversions:
            if ((strippedvalue.startswith('{') and strippedvalue.endswith('}')) or
                (strippedvalue.startswith('[') and strippedvalue.endswith(']')) or
                (strippedvalue.startswith('(') and strippedvalue.endswith(')'))):
                try:
                    # In theory this is a security leak, since there maybe
                    # "strange" objects inside the dictionary. Problem to be
                    # solved in the future?
                    return eval(strippedvalue)
                except (SyntaxError, NameError):
                    pass

        # Can't do anything with this value. Return unstripped and untouched.
        return value

    # Remove all tags from the string
    REMOVETAGS = re.compile(r'<.*?>')

    @classmethod
    def stripTags(cls, xml):
        return cls.REMOVETAGS.sub('', xml)

    REMOVEMULTIPLEWHITESPACE = re.compile(r'\n\s+')

    @classmethod
    def stripMultipleWhiteLines(cls, s):
        return cls.REMOVEMULTIPLEWHITESPACE.sub('\n\n', s)

    # support single or double quotes while ignoring quotes preceded by \
    XMLATTRS = re.compile(r'''([A-Z][A-Z0-9_]*)\s*=\s*(?P<quote>["'])(.*?)(?<!\\)(?P=quote)''', re.IGNORECASE)

    @classmethod
    def xmlAttrString2PyAttr(cls, s, conversions):
        attrs = {}
        for key, _, value in cls.XMLATTRS.findall(s):
            attrs[key] = value
        return cls.xmlAttr2PyAttr(attrs, conversions)

    @classmethod
    def xmlAttr2PyAttr(cls, par_dict, conversions):
        """
        
        Transform an XML attribute dictionary to a Python attribute dictionary. The <attr>class</attr> attribute name is
        translated into <attr>class_</attr> and all values are tested to convert into either ``int``,
        ``long``, ``float`` or boolean as represented by one of ``'TRUE'``,
        ``True``, ``true``, ``FALSE``, ``False``, ``false``. If the
        conversion fails, then pass the value unchanged. If there the attribute name is of format
        ``'{http://www.w3.org/XML/1998/namespace}space'``, e.g. as generated by Xopus XML Schema, then just
        remove the name space prefix.<br/>
        If there is an HTML5 attribute <attr>data-xxxx</attr> used, then change that to <attr>data_xxxx</attr>.<br/>
        
        """
        pydict = {}

        for key, value in par_dict.items():
            key = cls.xmlAttrName2PyAttrName(key)
            value = cls.xmlValue2PyValue(value, conversions)
            pydict[key] = value
        return pydict

    @classmethod
    def tableField2JoinedField(cls, table, field):
        if field.startswith(table):
            return field
        return '%s_%s' % (table, field)

    @classmethod
    def value2TagName(cls, value):
        u"""
        
        The ``value2TagName`` class method converts the <attr>value</attr> object into a value XML tag name.
        
        """
        tagname = []
        if not isinstance(value, basestring):
            value = `value`
        if value.lower().startswith('xml'):
            tagname.append('_')
        for c in value:
            if c in ' !?@#$%^&*()[]\t\r\n/\\':
                pass
            elif c.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890:.':
                tagname.append(c)
            else:
                tagname.append('_')
        return ''.join(tagname)

    @classmethod
    def html2Xml(cls, html):
        return html


    HTML_SPECIAL_CHARS = u'&<>' # ampersand must be first to avoid double conversion

    @classmethod
    def escapeHtmlChars(cls, text, dotag=True):
        """
        
        ``TX.escapeHtmlChars`` replaces risky characters with HTML entities.
        If <attr>dotag</attr> is ``False`` (default is ``True``),
        then don’t alter the tag, since we want to create valid XML here.
        
        """

        for c in cls.HTML_SPECIAL_CHARS:
            if dotag or not c in '<>':
                text = text.replace(c, '&#{0};'.format(ord(c)))
        return text

        # the method below escapes a lot more characters (accented chars, punctuation)

        """
        from htmlentitydefs import codepoint2name

        if not isinstance(text,basestring):
            return text
        
        if not hasattr(cls,'unicode2entity'):         
            cls.unicode2entity = {}
            for c,e in codepoint2name.items():
                cls.unicode2entity[unichr(c)] = '&{entity};'.format(entity=e)
        
        for c,r in cls.unicode2entity.items():
            text = text.replace(c,r)
        
        return text
        """

    @classmethod
    def smartquotes(cls, text, html=False):
        """
        
        Convert straight quotes into curly quotes in a block of text.
        
        """
        htmltrans = {
            u'“': '&ldquo;',
            u'”': '&rdquo;',
            u'‘': '&lsquo;',
            u'’': '&rsquo;',
        }
        import re
        text = re.sub(r'(?<=\s)\'(?=\d0\D)', '&rsquo;', text) # '90s
        text = re.sub(r'^\'(?=\d0\D)', '&rsquo;', text) # '90s
        text = re.sub(r'(?<=[\s\(\[\{])\'(?=\S)', '&lsquo;', text)
        text = re.sub(r'^\'(?=\S)', '&lsquo;', text)
        text = re.sub(r'(?<=\S)\'', '&rsquo;', text)
        text = re.sub(r'(?<=[\s\(\[\{])(?:"|&quot;)(?=\S)', '&ldquo;', text)
        text = re.sub(r'^(?:"|&quot;)(?=\S)', '&ldquo;', text)
        text = re.sub(r'(?<=\S)(?:"|&quot;)', '&rdquo;', text)

        if html:
            # undo any quotes inside HTML attributes
            while True:
                m = re.search(r'<[^>]+(&[lr]([sd])quo;)[^>]*>', text)
                if not m: break
                orig = m.group(0)
                new = orig.replace(m.group(1), '"' if m.group(2) == 'd' else "'")
                text = text.replace(orig, new)
        else:
            for uni, ent in htmltrans.items():
                text = text.replace(ent, uni)

        return text

    @classmethod
    def make_links(cls, text):
        """
        
        Convert plain URLs into <a> links in a block of text.
        
        """
        return re.sub(r'''(?<!=['"])https?://\S+?(?=[\s,]|$)''', r'<a href="\g<0>">\g<0></a>', text)

    @classmethod
    def htmlize(cls, text):
        """
        
        Takes plain text and returns a version of the text that will display well as HTML. This includes:
            * converting multiple newlines into <p> blocks
            * converting single newlines into <br>
            * converting straight quotes into real quotes
        If the input already looks like HTML, it will not be modified.
        
        """

        text = cls.smartquotes(text, html=True)
        text = cls.make_links(text)

        # paragraphize
        text = text.replace("\\r", "\r")
        text = text.replace("\\n", "\n")
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        if (text.find('<p>') < 0):
            text = re.sub(r'\n\n+', "</p><p>", text);
            text = re.sub(r'(?<!<br>)\n', "<br>\n", text);
            text = "<p>" + text + "</p>";

        text = re.sub('&(?!#?\w+;)', '&amp;', text)

        return text

    # ---------------------------------------------------------------------------------------------------------
    #     W I N D O W

    @classmethod
    def id2WindowId(cls, id):
        u"""
        
        The ``id2WindowId`` transformer method answers the unique window id that is used to store the state of
        a window in the session. If <attr>id</attr> is ``None`` then create a unique id.
        
        """
        return 'floatWin_%s' % id or uniqueId()

    # ---------------------------------------------------------------------------------------------------------
    #     V A L U E S

    @classmethod
    def isNumber(cls, value):
        return cls.asInt(value) is not None or cls.asFloat(value) is not None

    @classmethod
    def isFloat(cls, value):
        f = cls.asFloat(value)
        return f is not None and f != int(f)

    @classmethod
    def asInt(cls, value, default=None):
        u"""
        
        The ``asInt`` method answers <attr>value</attr> converted to ``int(value)``. If the conversion
        was not successful, then answer ``None</attr>. If <attr>value</attr> is ``None``, then answer the
        <attr>default</attr> attribute.<br/>
        If <attr>value</attr> is a list or tuple of one element, then use that value.
        print X.asInt(123)
        print X.asInt('2344')
        print X.asInt('0xFF')
        print X.asInt('FF')
        print X.asInt('#FFAA33')
        print X.asInt('11')
        print X.asInt('1A')
        print X.asInt('2.5')
        print X.asInt(2.4)
        print X.asInt(2.5)
        
        """
        if value is None:
            value = default
        if isinstance(value, (list, tuple)):
            if len(value) == 1:
                value = value[0]
        if isinstance(value, basestring):
            try:
                return int(round(float(value)))
            except (ValueError, TypeError):
                pass
            try: # Try hex value
                while value and value.startswith('#'):
                    value = value[1:]
                if value.startswith('0x'):
                    return int(value, 16)
                return int('0x' + value, 16)
            except (ValueError, TypeError):
                pass
        try:
            return int(round(float(value)))
        except (ValueError, TypeError, KeyError):
            pass
        return None

    @classmethod
    def asBool(cls, value, default=None):
        u"""Answer the translated *value* as boolean. Test on "True" and "False" strings."""
        if value is None:
            return bool(default)
        if value in ('True', 'true', 'T', 't', '1'):
            return True
        if value in ('False', 'false', 'F', 'f', '0'):
            return False
        return bool(value)

    @classmethod
    def asDict(cls, value):
        u"""
        
        The ``asDict`` method answers the dict instance that can be translated from the <attr>value</attr>. For
        now ``dict`` and ``((key, v), (key, v),...`` are supported.
        
        """
        d = {}
        if isinstance(value, dict):
            d = value
        elif isinstance(value, (list, tuple)):
            for k, v in value:
                d[k] = v
        return d

    @classmethod
    def isInt(cls, value):
        u"""
        
        The ``isInt`` method answers the boolean flag if the <attr>value</attr> would convert to a valid
        ``int`` by ``asInt(value)``.
        
        """
        return cls.asInt(value) is not None

    @classmethod
    def asFloat(cls, value, default=None):
        u"""
        
        The ``asFloat`` method answers <attr>value</attr> converted to ``float(value)``. If the
        conversion was not successful, then answer ``None</attr>. If <attr>value</attr> is ``None``, then
        answer the <attr>default</attr> attribute.
        
        """
        try:
            return float(value)
        except (ValueError, TypeError, KeyError):
            pass
        return default

    @classmethod
    def value2Bool(cls, v):
        u"""
        
        The ``value2Bool`` method answers the interpreted value of <attr>v</attr> as boolean. The following
        values (independent of case) interpret as ``False``: ``['', '0', 'f', 'F', 'none', 'false']``.
        If <attr>v</attr> is a list or tuple, then it is ``True`` if there is at least one element 
        the renders to ``True``, so it performs a an ``OR``.
        
        """
        if (isinstance(v, (tuple, list))):
            for vv in v:
                if cls.value2Bool(vv):
                    return True
            return False
        return not str(v).lower() in cls.C.FALSEVALUES

    @classmethod
    def toBase62(cls, value, base=62):
        """
        
        ``toBase62`` converts the integer value into a base-62 string using characters A-Z,a-z,0-9.
        
        """

        if base > 62:
            base = 62
        elif base < 2:
            base = 2
        else:
            base = int(base)

        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        result = []

        intpart = cls.asInt(value)
        negative = False

        if intpart is None:
            return value
        elif intpart == 0:
            return '0'
        elif intpart < 0:
            negative = True
            intpart = -intpart
            value = -value

        while intpart > 0:
            result.append(chars[intpart % base])
            intpart /= base

        result.reverse()
        result = (negative and '-' or '') + ''.join(result)

        if isinstance(value, float) and value != intpart:
            result += '.' + cls.toBase62(cls.asInt(str(value).split('.')[1]), base)

        return result

    @classmethod
    def fromBase62(cls, value, base=62):
        """
        
        ``fromBase62`` converts base-62 string with characters A-Z,a-z,0-9, into a base-10 int.
        
        """

        if base > 62:
            base = 62
        elif base < 2:
            base = 2
        else:
            base = int(base)

        chars = {}

        i = 0
        for c in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            chars[c] = i
            i += 1

        if not isinstance(value, basestring):
            return value

        negative = (value[0] == '-')

        if negative:
            value = value[1:]

        parts = value.split('.')

        if len(parts) > 2:
            raise ValueError("More than two decimal-separated parts in value.")

        results = []
        for p in parts:
            v = 0
            for c in p:
                if c not in chars:
                    raise ValueError(u"Invalid character '{0}' found in value.".format(c))
                v *= base
                v += chars[c]

            results.append(v)

        if len(results) == 1:
            return (negative and -1 or 1) * cls.asInt(results[0])
        else:
            return (negative and -1.0 or 1.0) * cls.asFloat("{0}.{1}".format(*results))

    @classmethod
    def randomBase62(cls, length=8, base=62):
        from random import choice
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"[:max(base, 2)]
        return ''.join([choice(chars) for i in range(length)])

    # ---------------------------------------------------------------------------------------------------------
    #     P A T H  S T U F F

    @classmethod
    def path2ParentDirectory(cls, path):
        u"""
        
        The ``path2ParentDirectory`` method answers the directory chunk of <attr>path</attr> by cutting the
        last ``'/'`` part off. No checking is done if the ``path`` is actually a file.
        
        """
        return '/'.join(path.split('/')[:-1])

    @classmethod
    def path2IdName(cls, path):
        u"""
        
        The ``path2IdName`` method takes the path and answers the possible idname of the URL. Remove the
        extension (probably ``'.html'``.
        
        """
        idname = path.split('/')[-1]
        if idname.endswith('.html'):
            idname = '.'.join(idname.split('.')[:-1])
        return idname

    @classmethod
    def label2ParamId(cls, label):
        u"""
        The ``label2ParamId`` takes an arbitrary label string and converts it to a valid param
        identifier, by copying only the valid characters. Spaces will be replaced by a hyphen.
        """
        param = ''
        label = label.lower().replace('&amp;', '')
        for c in label.lower():
            if c in 'abcdefghijklmnopqrstuvwxyz-0123456789':
                param += c
            elif c in ' \t\r\n':
                param += '-'
        return param

    @classmethod
    def label2Param(cls, label):
        u"""
        The ``label2Param`` method converts the label to a valid url parameters through
        ``urllib.quote_plus(label)``.
        """
        return urllib.quote_plus(label)

    @classmethod
    def param2Label(cls, param):
        return urllib.unquote_plus(param)

    # ---------------------------------------------------------------------------------------------------------
    #     L I S T  S T U F F 

    @classmethod
    def list2IntFloatList(cls, l):
        floatPat = re.compile('^\d+(\.\d+)$')
        l = list(cls.obj2List(l))
        for i in range(len(l)):
            if l[i]:
                if not isinstance(l[i], (float, int)):
                    if l[i].isdigit():
                        l[i] = int(l[i])
                    elif floatPat.match(l[i]):
                        l[i] = float(l[i])
                    else:
                        l[i] = 0
            else:
                l[i] = 0
        return l

    @classmethod
    def list2Lines(cls, l):
        u"""Answer the list as string with line-endings. It is assumed that all items of the list are strings."""
        return '\n'.join(l)
    
    # ---------------------------------------------------------------------------------------------------------
    #     S T R I N G  C O N V E R S I O N S

    @classmethod
    def idCommaString2IdSet(cls, s):
        u"""
        
        Transform a string width comma separated items into a set of id integers.
        
        """
        t = set()
        if s is not None:
            for value in s.split(','):
                value = cls.asInt(value)
                if value is not None:
                    t.add(value)
        return t

    @classmethod
    def value2IdCommaString(cls, value):
        u"""
        
        Transform a list with numbers into a comma separated string. This can be used to convert a list of record ids
        into a SQL compatible list of ids, without integers showing up as ``1234L``.
        
        """
        t = []
        if not isinstance(value, (set, list, tuple)):
            value = str(value).split(',')
        for item in value:
            if cls.isInt(item):
                t.append('%s' % item) # Avoid longs show up as 1234L
        return ', '.join(t)

    @classmethod
    def commaSpaceString2WordList(cls, s):
        u"""
        
        Transform a comma or whitespace separated string to a list with words.
        
        """
        if s is None:
            s = ''
        t = []
        for c in ',\t\r\n':
            s = s.replace(c, ' ')
        for word in s.split(' '):
            if word:
                t.append(word)
        return t

    @classmethod
    def object2SpacedString(cls, s):
        if isinstance(s, (list, tuple)):
            s = ' '.join(s)
        elif not isinstance(s, basestring):
            s = u'%s' % s
        return s
    
    @classmethod
    def fileSizeAsMb(cls, size):
        u"""
        
        The ``fileSizeAsMb`` method shows the <attr>size</attr> number as a rounded value using one of the
        ``["bytes", "KB", "MB", "GB", "TB"]`` as measure.
        
        """
        for q in ["bytes", "KB", "MB", "GB", "TB"]:
            if size < 1024 or q == "TB":
                s = str(round(size, 1))
                if s.endswith(".0"):
                    s = s[:-2]
                return "%s %s" % (s, q)
            size = size / 1024.0
        # not reachable
        return `size`


    @classmethod
    def wordSplit(cls, s, lower=False):
        u"""
        
        The ``wordSplit`` method splits <attr>s</attr> into parts with no trailing spaces. If the
        <attr>lower</attr> is ``True</attr> (default is ``False``) the all words are converted to lower
        case.
        
        """
        words = []
        for word in s.split(' '):
            if lower:
                word = word.lower()
            words.append(word.strip())
        return words

    @classmethod
    def abbreviate(cls, s, length=None):
        u"""
        
        The ``abbreviate`` method answers the abbreviated string ``s`` if it length exceeds the value
        of the <attr>length</attr> attribute and adds ``'...'``. If <attr>length</attr> is ``None``
        then the <attr>s</attr> string is answered unchanged.
        
        """
        if not s is None:
            s = s.strip()
            if length is not None and len(s) > length:
                return s[:length] + '...'
        return s

    @classmethod
    def unicodify(cls, s):
        u"""
        
        Make sure, whatever <attr>s</attr> is, that there is a value unicode string answered. If <attr>s</attr> is not a
        string then use ``str(s)`` to convert to a string first. This will make database records convert to a
        string of their id, instead of showing the record ``repr`` result. <em>Note that is might be that
        ``str`` will cause an error of the content of the object such as a list has unicode strings.</em>.
        ``None`` is replaced by an empty string.
        
        """
        if s is None:
            return u''
        # if isinstance(s, unicode):
        #     return s
        if not isinstance(s, basestring):
            s = str(s)
        try:
            return s.encode('utf-8')
        except UnicodeDecodeError:
            return s

        raise ValueError(u"Can‚Äôt handle string s")

    CAMEL_RE = re.compile(r'(?<=[a-z])(?=[A-Z0-9])')
    @classmethod
    def unCamelCase(cls, s):
        return cls.CAMEL_RE.sub(' ', s)


    # ---------------------------------------------------------------------------------------------------------
    #     C L A S S

    @classmethod
    def flatten2Class(cls, *args):
        u"""
        
        The ``flatten2Class`` method answers the class string, made from space separated class names. If
        <attr>class_</attr> is a ``tuple`` or ``list``, then merge the content. Check recursively in
        case the names are nested. If the <attr>classes</attr> is empty or ``None`` or contain an empty
        element, then this is ignored.
        
        """
        result = []
        for class_ in args:
            if isinstance(class_, basestring):
                result.append(class_)
            elif isinstance(class_, (tuple, list)):
                s = []
                for part in class_:
                    flattened = cls.flatten2Class(part)
                    s.append(flattened)
                result.append(' '.join(s))
            elif class_ is None:
                continue
            else:
                raise TypeError('[Transformer.flatten2Class] Class part must be None, string, tuple or list, not "%s"' % class_)
        return ' '.join(result)

    #    L A Y O U T
    
    @classmethod
    def col2Class(cls, col):
        u"""Translate the <i>col</i> number to a column width class name. If the <i>col</i>
        class cannot be found, e.g. because it is **None** then answer the class of **C.MAXCOL**."""        
        colClass = cls.C.COL2CLASS.get(col)    
        if colClass is None:
            colClass = cls.C.COL2CLASS.get(cls.C.MAXCOL)
        return colClass
    
    #    C U R R E N C Y
    
    CURRENCY_SYMBOLS = {
        'euro': u'€',
        'pound': u'£',
        'cent': u'¢',
        'dollar': u'$',
        'yen': u'¥'
    }

    @classmethod
    def numberFormat(cls, value, places=None, decimal='.', thousands=',', words=False):
        """
        
        ``numberFormat`` takes a numeric value and optionally adds thousand-separators
        and/or formats to the specified number of decimal places.
        If <attr>thousands</attr> is True or default, a comma will be used, otherwise specify the char you want to use.
        
        """

        number = cls.asFloat(value, None)

        if number is None:
            return value

        remainder = int(number)

        result = ''

        if remainder >= 1000:
            parts = []
            while remainder > 0:
                parts.append('{0:03d}'.format(remainder % 1000))
                remainder /= 1000
            result = thousands.join(reversed(parts)).lstrip('0')
        else:
            result = str(remainder)


        if places is None:
            numberstring = str(value)
            if '.' in numberstring:
                result += decimal + numberstring.split('.').pop()
        elif places > 0:
            exp = 10 ** places
            result += ('{d}{v:0' + str(int(places)) + 'd}').format(d=decimal, v=int(number * exp % exp))

        return result


    @classmethod
    def makeMoney(cls, value, currency='$', shorten=False, position="before", places=2, **args):
        u"""
        
        ``makeMoney`` takes a number and returns a price string.
        You can optionally specify:
        <attr>currency</attr>: the currency character
        <attr>decimal</attr>: number of decimal places
        <attr>shorten</attr>: whether to throw away the decimal part when it is .00
        <attr>position</attr>: where the currency char should go: "before" or "after" 
        Examples:
        ``makeMoney(12)`` returns "$12.00"
        ``makeMoney(12,shorten=True)`` returns "$12"
        ``makeMoney(1234,currency=u"¥",decimal=0,position="after")`` returns "1234¥"
        
        """

        if cls.asFloat(value) is None:
            return value

        if shorten and value - int(value) < 0.005:
            places = 0

        numberstring = cls.numberFormat(value, places=places, **args)

        if currency.lower() in cls.CURRENCY_SYMBOLS:
            currency = cls.CURRENCY_SYMBOLS[currency.lower()]

        l = ''
        r = ''

        if position in ("after", "right"):
            r = currency
        else:
            l = currency

        return u"{l}{n}{r}".format(l=l, n=numberstring, r=r)

TX = Transformer
