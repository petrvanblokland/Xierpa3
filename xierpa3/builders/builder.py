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
import os
from xierpa3.toolbox.stream.writer import Writer
from xierpa3.constants.constants import C
from xierpa3.toolbox.transformer import TX
from xierpa3.toolbox.stack import Stack
from xierpa3.descriptors.environment import Environment

class Builder(C):

    ID = None   # To be redefined by inheriting builder classes
    
    def __init__(self, e=None, result=None, verbose=True):
        self.e = e or Environment() # Store the theme.e environment in case running as server. Otherwise create.
        self.clear(result) # Clear the result stack or initialize with the optional result stack.
        self._verbose = verbose
        self._tabLevel = 0
        self._loopLevel = Stack() # Storage of inheriting classes that want to filter on loop iterations.
        self._footnoteCount = 0
        self.initialize()
        
    def clear(self, result=None):
        u"""Initialize the <b>self.result</b> from the optional <i>result</i> stack."""
        assert result is None or isinstance(result, Stack)
        if result is None:
            result = Stack()
        self.result = result
        if not self.result:
            self.result.push(self.newResultWriter())

    def initialize(self):
        u"""To be redefined by inheriting builder classes."""
        pass

    def save(self, path, makeDirectory=False):
        u"""Save the file in path. If <i>makeDirectory</i> is <b>True</b> (default is <b>False</b>)
        then create the directories in the path if they don’t exist."""
        if makeDirectory:
            dirPath = TX.path2Dir(path)
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
        f = open(path, 'wb')
        f.write(self.getResult())
        f.close()

    def getPath(self):
        u"""Answer the path of the current url, e.g. to select the right article data for this page.
        In CSS/SASS this gets overwritten by answering the path of the model document."""
        return self.e.path
  
    # T A B

    def tabs(self):
        # Output tabs to the current level
        if self._verbose:
            self.output('\n' + ('    ' * self._tabLevel))

    def tabIn(self):
        self._tabLevel += 1

    def tabOut(self):
        self._tabLevel = max(0, self._tabLevel - 1)

    def newline(self, count=1):
        if self._verbose:
            self.output('\n' * count)

    def newResultWriter(self, name=None):
        return Writer(name)

    def output(self, s):
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
    
    #   B U I L D E R  T Y P E
    
    def isType(self, type):
        u"""Answer the boolean flag if <b>self</b> builder is of <i>type</i>.
        In normal processing of the page this should never be necessary, but the test can be used by
        code that otherwise will do a lot of content processing (such as image scaling) in the
        CSS building phase. Also it can be used to short cut loops in content, to avoid the same
        definitions showing up in CSS. The comparison is not case-sensitive. <i>Type</i> can be a single
        string or a list/tuple of strings."""
        lcTypes = []
        if not isinstance(type, (list, tuple)):
            type = [type]
        for t in type:
            lcTypes.append(t.lower())  
        return self.ID.lower() in lcTypes
         
    #   B L O C K
    
    def snippet(self, component, name):
        u"""Allows inheriting (PHP) classes to save the block code to another snippet file,
        by redefining this method. Default behavior is to do nothing"""
        pass
    
    def _snippet(self, component):
        pass
    
    # R E Q U E S T  & F O R M
    
    def getCurrentArticleId(self):
        return self.e.form[C.PARAM_ARTICLE]

    def setCurrentArticleId(self, id):
        self.e.form.set(C.PARAM_ARTICLE, id)
    
    def getUrl(self):
        u"""Answer the url of the current page. To be implemented by inheriting classes
        that actually knows about urls. Default gehavior is to do nothing."""
        return None
        
    # G E N E R I C  B L O C K  B E H A V I O R
    
    def block(self, component):
        u"""Generic block, called at any block opening. To be redefined by inheriting builder
        classes. Default behavior is to do nothing."""
        pass
    
    def _block(self, component):
        pass
    
