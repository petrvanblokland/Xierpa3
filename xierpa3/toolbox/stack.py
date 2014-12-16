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
#    stack.py
#
class Stack:

    def __init__(self):
        self.clear()

    def __len__(self):
        return len(self.data)

    def __setitem__(self, index, value):
        self.data[index] = value

    def __getitem__(self, index):
        return self.data[index]

        # assert abs(index) in range(len(self.data)), ('[stack.__getitem__()] Error: index "%s" out of range in stack "%s"<br>' % (`index`, `self`))
        # item = self.data[index]
        # assert not item is None, '[stack.__getitem__()] Error: item is None<br>'
        # return item

    def __repr__(self):
        if not self.data:
            return 'None'
        if len(self.data) == 1:
            s = self.data[0]
        else:
            s = self.data
        if isinstance(s, basestring):
            return s
        return `s`

    def clear(self):
        u"""
        
        The <code>clear</code> method clears the stack.
        
        """
        self.data = []

    def setitem(self, item):
        u"""
        
        The <code>setitem</code> method sets the stack content to <code>[item]</code>.
        
        """
        self.data = [item]

    def push(self, item):
        u"""
        
        The <code>push</code> method pushes the <attr>item</attr> on stack.
        
        """
        self.data.append(item)

    def getAll(self):
        u"""
        
        The <code>getAll</code> method answers the whole list with stacked elements.
        
        """
        return self.data

    def replace(self, item):
        u"""
        
        The <code>replace</code> method replaces the top element of the stack by <attr>item</attr>.
        
        """
        self.data[-1] = item

    def top(self):
        u"""
        
        The <code>top</code> method peeks the top level of the stack. This is identical to <code>self.peek()</code>.
        If the stack is empty, then answer <code>None</code>.
        
        """
        if not self.data:
            return None
        return self.data[-1]

    def peek(self, index=0):
        u"""
        The <code>peek</code> method peeks into the stacked list of elements. The optional <attr>index</attr> (default
        value is <code>0</code>) goes backwards, so an <attr>index</attr> of <code>0</code> is the top of the stack.
        """
        if index >= len(self.data):
            return None
        return self.data[-index - 1]

    def root(self):
        u"""
        
        The <code>root<code> method answers the root <code>self.data[0]</code> element of the stack.
        
        """
        return self.data[0]

    def pop(self):
        u"""
        
        The <code>pop</code> method pops the stack and answers the popped element.
        If the stack is empty, then answer <code>None</code>. This is a “friendly” error, so the application
        can decide what to do with the wrong sized stack.
        
        """
        if len(self.data):
            return self.data.pop()
        return None

