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
#   article.py
#
class Article(object):
    u"""Generic data instance, answered by every adapter query. The attributes of the *Data* instance
    can be accessed as dictionary key and as attribute.
        >>> article = Article(a=1, b=2, c=3)
        >>> article.a
        1
        >>> article['b']
        2
    """
    def __init__(self, **kargs):
        self.fields = set() # Attribute names, besides self.fields and self.items
        self.chapters = [] # Make sure that self.chapters can always be iterated.
        for key, item in kargs.items():
            self[key] = item

    def __iter__(self):
        """Example iteration. Note that in real articles the elements of *self.chapters* are
        likely to be of type @Article@ too.

            >>> td = Article(chapters=[1,2,3])
            >>> for k in td:
            ...   k
            1
            2
            3
            >>>
        """
        return iter(self.chapters)

    def __getattr__(self, key):
        u"""Answer the list of all attribute names.
            >>> article = Article(a=1, b=2, c=3)
            >>> article.b
            2
        """
        return self.__dict__.get(key)

    def __setattr__(self, key, value):
        u"""Set the attribute and add the name to @self.fields@.

            >>> article = Article(a=1, b=2)
            >>> article.c = 10
            >>> article.fields

            >>> article.c

        """
        self.__dict__[key] = value
        if not key in ('fields', 'chapters'): # Not part of the field names.
            self.fields.add(key)

    def __repr__(self):
        u"""
            >>> article = Article(a=1, b=2, c=3)
            >>> article
            [Article a, b, c]
        """
        return '[%s %s]' % (self.__class__.__name__, ', '.join(sorted(self.fields)))

    def __setitem__(self, key, item):
        u"""
            >>> article = Article(a=1, b=2, c=3)
            >>> article['d'] = 10
            >>> article.d
            10
            >>> article.d = 20
            >>> article.d
            20
        """
        if not key in ('fields', 'chapters'):
            self.fields.add(key)
        setattr(self, key, item)
        
    def __getitem__(self, key):
        u"""
            >>> article = Article(a=1, b=2, c=3)
            >>> article.d = 10
            >>> article['d']
            10
        """
        if hasattr(self, key):
            return getattr(self, key)
        return None

    def items(self):
        u"""
            >>> article = Article(a=1, b=2, c=3)
            >>> article.items()
            [('a', 1), ('b', 2), ('c', 3)]
        """
        items = []
        for key in self.keys():
            items.append((key, self[key]))
        return items

    def keys(self):
        u"""Answer the list of all attribute names.
            >>> article = Article(a=1, b=2, c=3)
            >>> article.keys()
            ['a', 'b', 'c']
        """
        return sorted(self.fields)

    def has_key(self, key):
        u"""
            >>> article = Article(a=1, b=2)
            >>> article.has_key('a')
            True
        """
        return key in self.fields
