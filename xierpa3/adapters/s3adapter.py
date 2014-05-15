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
from fileadapter import FileAdapter
      
class S3Adapter(FileAdapter):
    u"""
    Adapter for XML file serving from S3 storage.
    """ 

    #    @@@ Under development

    def readXmlFile(self, fsPath): 
        raise "to_be_implemented"
        """
        if not fsPath.endswith('.xml'):
            fsPath += '.xml'           
        if os.path.exists(fsPath):
            f = codecs.open(fsPath, encoding='utf-8', mode='r+')
            xml = f.read()
            f.close()
        else:
            xml = None
        return xml
        """
