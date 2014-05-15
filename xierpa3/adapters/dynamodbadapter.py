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
#   dynamodbadapter.py
#
from xierpa3.adapters.adapter import Adapter
#from xierpa3.toolbox.database.dynamodb.dynamodbconnector import Connector

class Connector():
    #    @@@ Under development
    pass

class DynamoDBAdapter(Adapter):
    u"""
    Wrapper around the DynamoDB Connector, using:
    - Connector.getItem(id)
    - Connector.saveItem(item)
    - Connector.newItem(d)
    """

    #    @@@ Under development

    def __init__(self):
        Adapter.__init__(self)

    def getItem(self, id):
        return Connector.getItem(id)

    def newItem(self, d=None):
        return Connector.newItem(d)

    def saveItem(self, item):
        Connector.saveItem(item)

    def getMessage(self, component, count):
        return u'English is not native. For corrections on disaster misspellings please contact buro (at) petr.com'

    def getChapters(self, component, count):
        return []

    def getSocialMedia(self, component, count):
        return []

    def getFeaturedArticleThumbs(self, component, count):
        return []

    def getFeaturedArticles(self, component, countsite, count=1):
        # Answer count list of (imagePath, head, ankeiler, link)
        articles = ['Featured articles']
        return articles

    def getTagCloud(self, component, count):
        # Answer count tagCloud list entries as tuple (word, emphasisNumber)
        cloud = ['Tags']
        return cloud

    def getArticle(self, component, count):
        return ['Article']

    def getFooter(self, component, count):
        return ['Footer']

    def getLogo(self, component, count):
        return ['http://petr.com/_images/contact.png']

if __name__ == "__main__":
    pass
