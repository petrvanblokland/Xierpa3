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
from xierpa3.adapters.adapter import Adapter
from xierpa3.contributions.filibuster.blurb import Blurb

class BlurbAdapter(Adapter):
    u"""
    The Adapter classes connect the templates to Blurb content. Note that an adapter always returns plain text/content
    elements (which can include plain HTML), not components. The conversion needs to be done by the calling component.
    """
    IMAGES = [
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/bahrain.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/bush.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/chinatown.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/earthquake.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/egypt.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/electrical-storm.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/felix-graph-3.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/googleglass.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/googleglass2.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/googleglass3.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/googleglass4.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/guaguacrater.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/katrina.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/kiss.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/libya.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/little_italy.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/news.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/newspaper.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/nkorealaunch.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/obama.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/obama2.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/obama03.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/olympicpast.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/olympicpast2.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/perfect_storm1_large.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/polarbears.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/rahm.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/rolyaluk2.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/royaluk.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/shuttle.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/storm-nbpier.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/swarmybigshot.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/tibet.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/transport.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/travel.jpg',
        '//lib.xierpaweb.com.s3.amazonaws.com/_images/newspaper/images/news/verticalfashionshow.jpg',
    ]

    def __init__(self):
        Adapter.__init__(self)
        self.blurb = Blurb()

    def getMessage(self, count=1, **kwargs):
        return self.newData(text=u'English is not native. For corrections on disaster misspellings please contact buro (at) petr.com')

    def getSocialMedia(self, count=1, **kwargs):
        return self.newData(text=self.blurb.getBlurb('design_theory_title'))

    def getTagCloud(self, count=10, **kwargs):
        # Answer count tagCloud list entries as tuple (word, emphasisNumber)
        cloud = []
        for _ in range(10):
            cloud.append(self.newData(text=self.blurb.getBlurb('design_magazines'), emphasis=randint(10, 24)))
        return self.newData(items=cloud)

    def getArticleIds(self, start=0, count=1, selector=None, order=None, **kwargs):
        ids = []
        for index in range(start, count):
            ids.append(self.blurb.getBlurb('news_headline', 10))
        return ids

    def getArticle(self, id=None, index=0, selector=None, order=None, **kwargs):
        data = self.newData(
            headline=self.blurb.getBlurb('news_headline', 10),
            poster=choice(self.IMAGES),
            ankeiler=self.blurb.getBlurb('article_ankeiler', 30),
            text=self.blurb.getBlurb('article'),
        )
        return data

    def getChapter(self, index=0, **kwargs):
        u"""Answer a blurb article as chapter."""
        return self.getArticle()
    
    # P A G E  S T U F F
        
    def getFooter(self, count=1, **kwargs):
        return self.newData(text='Footer: ' + self.blurb.getBlurb('events_headline'))
    
    def getLogo(self, **kwargs):
        return self.newData(url='//petr.com/_images/contact.png')
    
    def getPageTitle(self, **kwargs):
        return self.newData(text=self.blurb.getBlurb('news_headline'))
    
    def getDescription(self, **kwargs):
        u"""Answer a blurb description of the site."""
        return self.newData(text=self.blurb.getBlurb('article_ankeiler', 40))
    
    def getKeyWords(self, **kwargs):
        u"""Answer a blurb set of keywords of the site, comma-space separated."""
        return self.newData(text=self.blurb.getBlurb('news_headline', 60).replace(' ', ', '))
    