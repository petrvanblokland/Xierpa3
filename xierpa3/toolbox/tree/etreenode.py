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
#     etreenode.py
#
from lxml import etree
from xierpa3.toolbox.transformer import TX
from xierpa3.constants.constants import Constants

class EtreeNode:
    u"""
    The ``EtreeNode`` class provides a wrapper around any etree node, to make a more convenient and robust
    Python based API.<br/>
    Note that if <attr>xml</attr> is supplied to the constructor, it needs to be validated XML, since not other checking
    or transformation is performed at this stage.<br/>
    The same is true the other way around. This especially is applies for the instance read and written from ``
    XmlTreeField`` fields. For documentation on Etree see <a href="http://lxml.de/tutorial.html">the official
    tutorial</a>.
    """
    C = Constants
    
    def __init__(self, tree=None, xml=None):
        if xml is not None:
            tree = etree.fromstring(xml)
        assert not isinstance(tree, EtreeNode)
        assert tree.__class__.__name__ in ('_Comment', '_Element') # Just to be sure it is an etree
        self._etree = tree

    def __repr__(self):
        if self._etree is None:
            return self.__class__.__name__
        return u'EtreeNode: ' + self._toString()

    def __nonzero__(self):
        return self._tree is None

    def __ne__(self, other):
        return not self is other

    def __eq__(self, other):
        return self is other

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        nodes = self._getTree()
        if len(nodes):
            for i in nodes:
                yield self.__class__(i)

    @classmethod
    def getXPath(cls, tree, xpath):
        u"""
        The ``getXPath`` class method queries the <attr>tree</attr> by <attr>xpath</attr> and answers a
        list of ``EtreeNode`` instances for every matching entry. There are several answering conditions: if
        <attr>tree</attr> is ``None`` then answer ``None``. If there is no result, then answer
        ``None``. If the result is a list of ``basestring`` instances (tested on the first of the
        list) then answer the list untouched. Otherwise make a new list with the result ``etree`` nodes wrapped
        as ``EtreeNode`` instances.
        """
        if tree is None:
            return None
        if isinstance(tree, cls):
            tree = tree._getTree()
        result = tree.xpath(xpath)
        if not result:
            return None
        if isinstance(result[0], basestring):
            return result
        enodes = []
        for n in result:
            enodes.append(cls(n))
        return enodes

    @classmethod
    def getXPathNode(cls, tree, xpath, index=0):
        u"""
        The ``getXPathNode`` class method does the same as ``cls.getXPath`` except that it
        answers the element of the list indicated by <attr>index</attr>. If there is no result, or if the <attr>index
        </attr> exceeds the length of the result list, then ``None`` is answered. Default value for the
        optional <attr>index</attr> attribute is ``0``, resulting in the first element if it exists.
        """
        if tree is None:
            return None
        if isinstance(tree, cls):
            tree = tree._getTree()
        result = tree.xpath(xpath)
        if not result or len(result) < index:
            return None
        if isinstance(result[index], basestring):
            return result[index]
        return cls(result[index])

    def __getattr__(self, key):
        if key.startswith('_'):
            return self.__dict__.get(key)
        return self._get(key)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            self.__dict__[key] = value
        else:
            self._set(key, value)

    def _xpath(self, xpath):
        u"""
        The ``_xpath`` function is the instance equivalent of ``cls.getXPathNode``.
        """
        return self.__class__.getXPath(self._getTree(), xpath)

    def _xpathNode(self, xpath):
        u"""
        The ``_xpathNode`` function is the instance equivalent of ``cls.getXPathNode``.
        """
        return self.__class__.getXPathNode(self._getTree(), xpath)

    def _xpathString(self, xpath):
        u"""
        The ``_xpathString`` method answers the concatenated string of all results (strings or elements)
        of <attr>xpath</attr>.
        """
        result = self._xpath(xpath)
        if result is not None:
            return ''.join(result)
        return ''

    def _set(self, key, value):
        tree = self._getTree()
        if tree is not None:
            key = TX.xmlAttrName2PyAttrName(key)
            tree.set(key, `value`)

    def _get(self, key):
        key = TX.pyAttrName2XmlAttrName(key)
        value = self._xpath('@' + key)
        if value:
            return TX.xmlValue2PyValue(value[0], self.C.XSL_XMLCONVERSIONS)
        return None

    def _getTag(self):
        tree = self._getTree()
        if tree is not None and hasattr(tree, 'tag'):
            tag = tree.tag
            if isinstance(tag, basestring):
                return tag
        return ''

    def _getTree(self):
        return self._etree

    def _getText(self):
        return self._getTree().text

    def _getTail(self):
        return self._getTree().tail

    def _getAttributes(self):
        attributes = {}
        for index, value in enumerate(self._xpath('@*') or []):
            attrname = TX.xmlAttrName2PyAttrName(self._xpath('name(@*[%d])' % (index + 1)))
            attributes[attrname] = TX.xmlValue2PyValue(value, self.C.XSL_XMLCONVERSIONS)
        return attributes

    def _getNodes(self, name=None):
        u"""
        Gets all nodes that match name.
        """
        if name is None:
            name = '*'
        return self._xpath('./' + name)

    def _getFirstNode(self, name=None):
        u"""
        Gets first node that matches name.
        """
        nodes = self._getNodes(name)
        if nodes:
            return nodes[0]
        return None

    def _toString(self):
        tree = self._getTree()
        if tree is not None:
            return etree.tostring(tree, encoding='utf-8').decode('utf-8')
        return None

    def _childrenToString(self, method=None):
        result = []
        for child in self._getTree():
            # Use html output by default (no self-closing tags).
            result.append(etree.tostring(child, encoding='utf-8', method=method or 'html').decode('utf-8'))
        return ''.join(result)

    def _childrenNodes(self):
        u"""
        Returns etree child nodes as EtreeNode objects.
        """
        result = []
        for child in self._getTree():
            result.append(EtreeNode(child))
        return result

if __name__ == '__main__':
    tree = etree.fromstring(u'<aaa><bbb test="123">zzz</bbb><ccc test="345">yyy</ccc><ddd/><eee/></aaa>')
    node = EtreeNode(tree)
    print node
    print node._getNodes()
    print node._getNodes('bbb')
    print node._getFirstNode('bbb')
    bbb = node._getFirstNode('bbb')
    print bbb.testx
    print bbb.test
    print bbb.test * 10
    bbb.textx = 234
    print bbb.textx
    for t in node:
        print t._getTag()
