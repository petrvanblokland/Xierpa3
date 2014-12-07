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

    def getMessage(self, count):
        return self.newArticle(text=u'English is not native. For corrections on disaster misspellings please contact buro (at) petr.com')

    def getLogo(self, count):
        return self.newArticle(url='http://petr.com/_images/contact.png')

if __name__ == "__main__":
    pass
