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
#   simpledbadapter.py
#
from random import randint
from xierpa3.adapters.adapter import Adapter
#from xierpa3.toolbox.database.simpledb.simpledbdict import SimpleDBDict

class SimpleDBAdapter(Adapter):

    #    @@@ Under development

    def __init__(self):
        Adapter.__init__(self)
        #self.blurb = SimpleDBDict

    def getChapters(self, site, count=1):
        return []

    def getSocialMedia(self, site, count=1):
        return [self.blurb.getBlurb('design_theory_title')]

    def getFeaturedArticleThumbs(self, site, count=1):
        return [self.blurb.getBlurb('design_headline')]

    def getFeaturedArticles(self, site, count=1):
        # Answer count list of (imagePath, head, ankeiler, link)
        articles = []
        for _ in range(1, (count or 1) + 1):
            pass
            #image = choice(images)
            #articles.append((image, self.blurb.getBlurb('design_headline', 8) + '.',
            #    self.blurb.getBlurb('article_ankeiler', 30) + '.', 'Link'))
        return articles

    def getTagCloud(self, site, count=1):
        # Answer count tagCloud list entries as tuple (word, emphasisNumber)
        cloud = ['Tags']
        for _ in range(10):
            cloud.append(dict(text=self.blurb.getBlurb('design_magazines'), emphasis=randint(10, 24)))
        return cloud

    def getArticle(self, site, count=1):
        return [self.blurb.getBlurb('article')]

    def getFooter(self, site, count=1):
        return ['Footer: ' + self.blurb.getBlurb('events_headline')]

    def getLogo(self, site, count=1):
        return ['Logo']

if __name__ == "__main__":
    """
    from xierpa3.toolbox.database.simpledb.simpledbdict import SimpleDBDict
    db = SimpleDBDict('petr.com', {}, C.ACCESSKEYID, C.SECRETACCESSKEY)
    domain = db.getDomain('petr.com')
    # item = domain.new_item('record1')
    item = domain.get_item('record1')
    # item['text'] = 1234
    print item
    """

