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
#    simpledbconnector.py
#
import boto

class SimpleDBConnector():
    u"""
    <doc>
    Wrapper class for an Amazon SDB connector.
    </doc>
    """
    CONNECTION            = None
    DOMAIN                = None
    DEFAULT_HOST        = 'simpledb.amazonaws.com'
    DEFAULT_PORT        = 443
    DEFAULT_PROTOCOL    = 'https'
    
    def __init__(self, name, accesskeyid, secretaccesskey):
        if self.CONNECTION is None:
            self.CONNECTION = boto.connect_sdb(accesskeyid, secretaccesskey, port=self.DEFAULT_PORT,
                                            host=self.DEFAULT_HOST)
        if self.DOMAIN is None:
            self.DOMAIN = self.getDomain(name)

    @classmethod
    def createDomain(self, name):
        u"""
        <doc>
        </doc>
        """
        self.CONNECTION.create_domain(name)

    @classmethod
    def getDomain(self, domain_or_name):
        u"""
        <doc>
        </doc>
        """
        return self.CONNECTION.get_domain(domain_or_name)
    
    def deleteDomain(self, domain_or_name):
        u"""
        <doc>
        </doc>
        """
        return self.CONNECTION.delete_domain(domain_or_name)

    def query(self, domain_or_name, query='', max_items=None, next_token=None):
        u"""
        <doc>
        Returns a list of item names within domain_name that match the query.
        </doc>
        """
        return self.CONNECTION.query(domain_or_name, query, max_items, next_token)

    @classmethod
    def rawQuery(self, name, query):
        u"""
        <doc>
        </doc>
        """
        return self.CONNECTION.select(self.DOMAIN, query, 0)
    
    def write(self, table, id, fields, forceinsert=False, **attributes):
        u"""
        <doc>
        Should determine if item needs to be created or already exists; also if data is larger than 1024 bytes and
        needs to be written into S3 bucket.
        </doc>
        """
        item = self.DOMAIN.new_item('item')
        
        for key, value in attributes.items():
            item[key] = value

    def getUsage(self):
        u"""
        <doc>
        Returns the BoxUsage accumulated on this SDBConnection object.
        </doc>
        """
        return self.CONNECTION.get_usage()
