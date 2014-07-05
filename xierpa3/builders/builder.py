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
#   builder.py
#
import os, shutil
from xierpa3.toolbox.stream.writer import Writer
from xierpa3.constants.constants import Constants
from xierpa3.toolbox.transformer import TX
from xierpa3.toolbox.stack import Stack
from xierpa3.descriptors.environment import Environment

class Builder(object):

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Constants 

    ID = None   # To be redefined by inheriting builder classes
    EXTENSION = ID # To be redefined by inheriting class. Default extension of output files.
    #DEFAULT_PATH = 'files/' # Default path for saving files with self.save()
    DO_INDENT = False
    ROOT_PATH = None # Root path to be redefined by inheriting builder classes. 
    
    def __init__(self, e=None, result=None, verbose=True, doIndent=True):
        self.e = e or Environment() # Store the theme.e environment in case running as server. Otherwise create.
        self._verbose = verbose
        self._doIndent = doIndent # Use indent for blocks on the output
        self._tabLevel = 0 # If indenting, keep tab level here.
        self._newLine = '\n' # Newline code to add˙at all closing of blocks
        self._loopLevel = Stack() # Storage of inheriting classes that want to filter on loop iterations.
        self._footnoteCount = 0
        # Initialize the stack of result writers
        self.initializeResult(result)
        # Allow inheriting builder classes to do initialization.
        self.initialize() 
        
    def initializeResult(self, result):
        u"""Initialize the <b>self.result</b> from the optional <i>result</i> stack."""
        assert result is None or isinstance(result, Stack)
        if result is None:
            result = Stack()
        self.result = result
        if not self.result: # If empty stack, so push a new root result writer
            self.result.push(self.newResultWriter())

    def initialize(self):
        u"""To be redefined by inheriting builder classes. Default behavior is to nothing."""
        pass
    
    #    P A T H
    
    def getPath(self):
        u"""Answer the path of the current URL, e.g. to select the right article data for this page.
        In CSS/SASS this gets overwritten by answering the path of the model document."""
        return self.e.path
  
    def getExtension(self):
        u"""Answer the default extension of the output file of this type of builder.
        Typically <b>self.EXTENSION</b> is answered."""
        return self.EXTENSION
    
    def getComponentFileName(self, root, component):
        u"""Answer the file path of the component. @@@ This should be based on URL too."""
        return component.name + '.' + self.getExtension()

    def getFilePath(self, component, root=None):
        u"""Answer the file path of <b>component</b>."""
        return TX.asDir(root or self.ROOT_PATH) + self.getComponentFileName(root, component)

    def copyTree(self, srcPath, dstPath, force=False):
        for fileName in os.listdir(srcPath):
            if fileName.startswith('.'):
                continue
            srcPath2 = srcPath + fileName
            dstPath2 = dstPath + fileName 
            if os.path.isdir(srcPath2):
                if not os.path.exists(dstPath2):
                    os.mkdir(dstPath2)
                self.copyTree(srcPath2 + '/', dstPath2 + '/', force)
            elif force or not os.path.exists(dstPath2):
                shutil.copy2(srcPath2, dstPath2)

    def makeDirectory(self, path):
        u"""Make sure that the directory of path (as file) exists. Otherwise create it.
        Answer the directory path for convenience of the caller."""
        dirPath = TX.path2Dir(path)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        return dirPath
    
    def save(self, component, root=None, path=None):
        u"""Save the <b>self.getResult()</b> in path. If the optional <i>makeDirectory</i> attribute is 
        <b>True</b> (default is <b>True</b>) then create the directories in the path 
        if they don’t exist."""
        if path is None: # Allow full overwrite of complete path.
            path = self.getFilePath(component, root)
        self.saveAsFile(path, self.getResult(), makeDir=True)
        return path
    
    def saveAsFile(self, path, content, makeDir=False):
        u"""Save content as a file under path. If the file exists it is overwritten.
        If <b>makeDirs</b> is <b>True</b> (default is <b>False</b>), the try to create the directory first."""
        if makeDir:
            self.makeDirectory(path) # Make sure that the directory part of path exists.
        f = open(path, 'wb')
        f.write(content)
        f.close()

    # P A R A M
    
    def getParamNames(self):
        u"""Answer the names of the params in the URL"""
        return self.e.form.keys()
    
    def getParamItems(self):
        u"""Answer the <b>(name, value)</b> tuple of URL params."""
        return self.e.form.items()
    
    # T A B

    def tabs(self):
        """"Output tabs to the current level and add newlines, depending on the setting of <b>self._newline</b>
        (string with newlines) and <code>self._tabLevel</code> (number of indents)."""
        if self._verbose:
            self.output(self._newLine + (self.C.TAB_INDENT * self._tabLevel)) 

    def tabIn(self):
        if self._doIndent:
            self._tabLevel += 1

    def tabOut(self):
        if self._doIndent:
            self._tabLevel = max(0, self._tabLevel - 1)

    def newline(self, count=1):
        if self._verbose:
            self.output(self._newLine * count)

    def newResultWriter(self, name=None):
        return Writer(name)

    def output(self, s):
        u"""Output the <b>s</b> string to the result stream."""
        # See all output:
        #print s,
        self.result.peek().write(s)

    #  R E S U L T  The stack of output streams.

    def peekResult(self):
        u"""Answer the current writer stream."""
        return self.result.peek()

    def getResult(self):
        u"""Check if there is only one output writer left. This call should be made at the end of a rendering.
        Pop the writer and answer the result."""
        assert len(self.result) == 1
        return self.popResult()

    def pushResult(self, writer=None, name=None):
        u"""Push the optional <i>writer</i>. If the attribute is <b>None</b>, then create a new writer."""
        if writer is None:
            # Save an optional identifier, so the caller knows at closing of the block.
            writer = self.newResultWriter(name)
        self.result.push(writer)

    def popResult(self):
        u"""Answer the writer result if it exists. Answer <b>None</b> otherwise."""
        if self.result:
            return self.result.pop().getValue()
        return None

    def popNameResult(self):
        u"""Answer the tuple of <b>writer.name</b> and the writer result."""
        if self.result:
            writer = self.result.pop()
            return writer.name, writer.getValue()
        return None, None
    
    #   E R R O R
    
    def error(self, s):
        self.div(color='red')
        self.text(s)
        self._div()
        
    #   B U I L D E R  T Y P E
    
    def isType(self, builderType):
        u"""Answer the boolean flag if <b>self</b> builder is of <i>builderType</i>.
        In normal processing of the page this should never be necessary, but the test can be used by
        code that otherwise will do a lot of content processing (such as image scaling) in the
        CSS building phase. Also it can be used to short cut loops in content, to avoid the same
        definitions showing up in CSS. The comparison is not case-sensitive. <i>Type</i> can be a single
        string or a list/tuple of strings."""
        lcTypes = []
        if not isinstance(builderType, (list, tuple)):
            builderType = [builderType]
        for t in builderType:
            lcTypes.append(t.lower())  
        return self.ID.lower() in lcTypes
         
    #   B L O C K
    
    def snippet(self, component, name):
        u"""Allows inheriting (PHP) classes to save the block code to another snippet file,
        by redefining this method. Default behavior is to do nothing"""
        pass
    
    def _snippet(self, component):
        pass
    
    #  R E Q U E S T  &  F O R M
    
    def getCurrentArticleId(self):
        return self.e.form[self.C.PARAM_ARTICLE]

    def setCurrentArticleId(self, aid):
        self.e.form.set(self.C.PARAM_ARTICLE, aid)
    
    def getUrl(self):
        u"""Answer the url of the current page. To be implemented by inheriting classes
        that actually knows about URLs. Default behavior is to do nothing."""
        return None
        
    #  G E N E R I C  B L O C K  B E H A V I O R
    
    def block(self, component):
        u"""Generic block, called at any block opening. To be redefined by inheriting builder
        classes. Default behavior is to do nothing."""
        pass
    
    def _block(self, component):
        pass
    
