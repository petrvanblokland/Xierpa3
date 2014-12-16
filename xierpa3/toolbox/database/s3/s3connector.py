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
#   s3connector.py

import boto
from boto.s3.key import Key

class S3Connector():
    u"""
    Xierpa wrapper for Amazon S3 connection and bucket using the boto library. Enables us to send and retrieve
    files from the  data storage. Multiple instances are possible for data retrieval from different buckets.
    """

    BUCKET         = None
    CONNECTION     = None

    def __init__(self, domain, accesskeyid, secretaccesskey):
        u"""
        
        Set up basic access and load the bucket for our client site.
        
        """
        if S3Connector.CONNECTION is None:
            S3Connector.CONNECTION = boto.connect_s3(accesskeyid, secretaccesskey)
        # Make sure domain bucket is initialized.
        self.BUCKET = self.getBucket(domain)

    def getBucket(self, name=None, create=True):
        u"""
        
        Get an AWS bucket with exception handling. Creates the bucket if it doesn't already exist.
        
        """
        try:
            return self.CONNECTION.get_bucket(name)
        except boto.exception.S3ResponseError:
            if create:
                bucket = self.CONNECTION.create_bucket(name)
                print 'created new bucket %s' % name
                return bucket
        return None
    
    def listAllBuckets(self):
        u"""
        
        Auxiliary definition showing all available buckets.
        
        """
        print self.getAllBuckets()

    def getAllBuckets(self):
        return self.CONNECTION.get_all_buckets()

    def getMime(self, keyname):
        if keyname.endswith('.html'):
            return 'text/html'
        elif keyname.endswith('.xml'):
            return 'text/xml'
        if keyname.endswith('.css'):
            return 'text/css'
        return 'text/plain'
        
    #    R E A D  &  W R I T E 
    
    def writeString(self, keyname, string, mimetype=None):
        u"""
        
        Writes text to the file with key as name.
        
        """
        try:
            k = Key(self.BUCKET)
            k.key = keyname
            k.set_metadata('Content-Type', mimetype or self.getMime(keyname))
            k.set_contents_from_string(string)
            k.set_acl("public-read")
            return True
        except IOError: # ???
            return False
        
    def writeFileToS3(self, keyname, path,  mimetype=None, acl="public-read"):
        u"""
        
        Writes file contents from local file to S3 with key as name.
        
        """
        try:
            k = Key(self.BUCKET)
            k.key = keyname
            k.set_metadata('Content-Type', mimetype or self.getMime(keyname))
            k.set_contents_from_filename(path)
            k.set_acl(acl)
            return True
        except IOError, e:
            print 'Could not write file to S3:', e
            return False
        
    def readString(self, keyname):
        k = Key(self.BUCKET)
        k.key = keyname
        return k.get_contents_as_string()
    
    def readFileFromS3(self, keyname, path):
        u"""
        The ``readFileFromS3`` method reads the content of <attr>keyname</attr>
        from S3 and writes it the file with <attr>path</attr>. Answer the a boolean flag
        to indicate of the operation succeeded.
        """
        try:
            k = Key(self.BUCKET)
            k.key = keyname
            k.get_contents_to_filename(path)
            return True
        except IOError:
            return False
        
    def getKey(self, key):
        u"""
        
        We describe keys as paths within buckets. Returns None if the key doesn't exist.
        
        """
        return self.BUCKET.get_key(key)

    def hasKey(self, key):
        return bool(self.getKey(key))
    
    def getAllKeys(self, headers=None, prefix='', delimiter='', maxkeys=10000):
        u"""
        
        A lower-level method for listing contents of a bucket. This closely models the actual S3 API and requires you to
        manually handle the paging of results. For a higher-level method that handles the details of paging for you, you
        can use the list method.
        Parameters:    

        max_keys (int) – The maximum number of keys to retrieve.
        prefix (string) – The prefix of the keys you want to retrieve.
        marker (string) – The “marker” of where you are in the result set.
        delimiter (string) – If this optional, Unicode string parameter is included with your request, then keys that
        contain the same string between the prefix and the first occurrence of the delimiter will be rolled up into a
        single result element in the CommonPrefixes collection. These rolled-up keys are not returned elsewhere in the
        response.

        Return type:    ResultSet
        Returns:        The result from S3 listing the keys requested
        
        """
        return self.BUCKET.get_all_keys(headers, prefix=prefix, delimiter=delimiter, max_keys=maxkeys)
    
    def getFolderList(self, headers=None, prefix='', delimiter=''):
        u"""
        
        
        """
        l = []
        for k in self.getAllKeys(headers=headers, prefix=prefix, delimiter=delimiter):
            path = k.name.replace(prefix, '')
            if path == '':
                continue
            l.append(path)

        return l

    def getList(self, headers=None, prefix='', delimiter='', marker=''):
        return self.BUCKET.list(headers=headers, prefix=prefix, delimiter=delimiter, marker=marker)

    def deleteKey(self, key):
        u"""
        
        Deletes the key that is passed.
        
        """
        key.delete()

    def deleteKeyFromBucket(self, keyname):
        self.BUCKET.delete_key(keyname)

    def sendFile(self, key, file):
        #TODO: get this working.
        k = Key(self.BUCKET)
        k.key = key
        k.send_file(file)

    def makeFilePointerByPath(self, s3path, tmppath):
        u"""
        
        Gets a file from S3 using the path and store it on a temporary location for further processing.
        
        """
        key = self.getKey(s3path)
        self.makeFilePointer(key, tmppath)

    def makeFilePointer(self, key, tmppath):
        u"""
        
        Gets a file from S3 using the key and store it on a temporary location for further processing.
        
        """
        fp = open(tmppath, 'w')
        self.getFile(key, fp)
        fp.close()

    def getFile(self, key, fp):
        u"""
        
        Puts a file in the fp file pointer, which is a temporary file object:
        
        ``
         fp = open(<tmp-path>, 'w')
         ``
        
        
        Throws an exception if key is none.
        """
        try:
            key.get_file(fp)
        except:
            print 'Error in S3Connector.getFile()'
            print key

    def list(self):
        # TODO: higher level version of getAllKeys(), returns an iterator.
        pass
