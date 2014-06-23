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
#   blurbadapter.py
#
from random import choice, randint
from xierpa3.adapters.adapter import Adapter, Data
from xierpa3.contributions.filibuster.blurb import Blurb

class BlurbAdapter(Adapter):
    u"""
    The Adapter classes connect the templates to Blurb content. Note that an adapter always returns plain text/content
    elements (which can include plain HTML), not components. The conversion needs to be done by the calling component.
    """

    def __init__(self):
        Adapter.__init__(self)
        self.blurb = Blurb()

    def getMessage(self, count=1, **kwargs):
        return u'English is not native. For corrections on disaster misspellings please contact buro (at) petr.com'

    def getChapters(self, count=1, **kwargs):
        return []

    def getSocialMedia(self, count=1, **kwargs):
        return [self.blurb.getBlurb('design_theory_title')]

    def getFeaturedArticleThumbs(self, count=1, **kwargs):
        return [self.blurb.getBlurb('design_headline')]

    def getFeaturedArticles(self, count=1, **kwargs):
        # Answer count list of (imagePath, head, ankeiler, link)
        images = [
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/bahrain.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/bush.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/chinatown.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/earthquake.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/egypt.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/electrical-storm.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/felix-graph-3.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/googleglass.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/googleglass2.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/googleglass3.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/googleglass4.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/guaguacrater.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/katrina.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/kiss.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/libya.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/little_italy.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/news.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/newspaper.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/nkorealaunch.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/obama.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/obama2.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/obama03.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/olympicpast.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/olympicpast2.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/perfect_storm1_large.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/polarbears.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/rahm.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/rolyaluk2.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/royaluk.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/shuttle.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/storm-nbpier.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/swarmybigshot.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/tibet.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/transport.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/travel.jpg',
            'http://lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/verticalfashionshow.jpg',
        ]
        articles = []
        for _ in range(1, (count or 1) + 1):
            data = Data()
            data.image = choice(images)
            data.headline = self.blurb.getBlurb('design_headline', 8) + '.'
            data.items = [self.blurb.getBlurb('article_ankeiler', 30)]
            articles.append(data)
        return Data(items=articles)

    def getTagCloud(self, count=10, **kwargs):
        # Answer count tagCloud list entries as tuple (word, emphasisNumber)
        data = Data()
        data.items = cloud = ['Tags']
        for _ in range(10):
            cloud.append(dict(text=self.blurb.getBlurb('design_magazines'), emphasis=randint(10, 24)))
        return data

    def getArticle(self, id=None, **kwargs):
        data = Data()
        data.headline = self.blurb.getBlurb('news_headline')
        data.items = [self.blurb.getBlurb('article'), self.blurb.getBlurb('article'), self.blurb.getBlurb('article')]
        return data
    
    def getFooter(self, count=1, **kwargs):
        data = Data()
        data.items = ['Footer: ' + self.blurb.getBlurb('events_headline')]
        return data
    
    def getLogo(self, **kwargs):
        data = Data()
        data.items = ['http://petr.com/_images/contact.png']
        return data
    
    def getDescription(self, **kwargs):
        u"""Answer a blurb description of the site."""
        return Data(text=self.blurb.getBlurb('article_ankeiler', 40))
    
    def getKeyWords(self, **kwargs):
        u"""Answer a blurb set of keywords of the site, comma-space separated."""
        return Data(text=self.blurb.getBlurb('news_headline', 60).replace(' ', ', '))
    