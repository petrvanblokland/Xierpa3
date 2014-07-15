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
#    s3adapter.py
#
#    Like FileAdapter, but then get the files from S3
#
#    xpath examples: http://msdn.microsoft.com/en-us/library/ms256086(v=vs.110).aspx
#  
from textilefileadapter import TextileFileAdapter
      
class S3Adapter(TextileFileAdapter):
    u"""
    Adapter for Textile file serving from S3 storage.
    """ 

    #    @@@ Under development

    @classmethod  
    def readWikiFile(cls, fsPath): 
        raise "to_be_implemented"
        u"""Read the raw wiki (Textile syntax) file and answer the unicode string."""
        extension = '.'+cls.C.EXTENSION_TXT
        if not fsPath.endswith(extension):
            fsPath += extension           
        '''
        if os.path.exists(fsPath):
            f = codecs.open(fsPath, encoding='utf-8', mode='r+')
            wiki = f.read()
            f.close()
        else:
            wiki = None
        return wiki
        '''
