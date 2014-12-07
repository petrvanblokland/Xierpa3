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
#    adaptertester.py
#
from xierpa3.toolbox.storage.article import Article
from xierpa3.toolbox.transformer import TX

class AdapterTester(object):
    u"""The AdapterTester is used to test the validity of the API of an adapter.

        >>> from textilefileadapter import TextileFileAdapter
        >>> from xierpa3.sites import doingbydesign
        >>> # Root path where to find the article Simples wiki file for this example page.
        >>> articleRoot = TX.module2Path(doingbydesign) + '/files/articles/'
        >>> adapter = TextileFileAdapter(articleRoot)
        >>> AdapterTester.test(adapter)

    """
    @classmethod
    def test(cls, adapter):
        article = adapter.getArticle(id='index')
        cls.testArticle(article)
        cls.testChapters(article)

    @classmethod
    def testArticle(cls, article):
        if not isinstance(article, Article):
            cls.error('Article ("%s") should be subclass of "%s"' % (article.__class__.__name__, Article.__name__))

    @classmethod
    def testChapters(cls, article):
        if not article.has_key('chapters'):
            cls.error('Article "index" has no "chapters" attribute.')
        elif not isinstance(article.chapters, (tuple, list)):
            cls.error('Article.chapters must be of type "list" or "tuple"')
        elif len(article.chapters) == 0:
            cls.warning('Article.chapters should not be empty')

    @classmethod
    def error(cls, s):
        print u'[%s] %s' % (cls.__name__, s)
