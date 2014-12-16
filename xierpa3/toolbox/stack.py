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
        
        The ``clear`` method clears the stack.
        
        """
        self.data = []

    def setitem(self, item):
        u"""
        
        The ``setitem`` method sets the stack content to ``[item]``.
        
        """
        self.data = [item]

    def push(self, item):
        u"""
        
        The ``push`` method pushes the <attr>item</attr> on stack.
        
        """
        self.data.append(item)

    def getAll(self):
        u"""
        
        The ``getAll`` method answers the whole list with stacked elements.
        
        """
        return self.data

    def replace(self, item):
        u"""
        
        The ``replace`` method replaces the top element of the stack by <attr>item</attr>.
        
        """
        self.data[-1] = item

    def top(self):
        u"""
        
        The ``top`` method peeks the top level of the stack. This is identical to ``self.peek()``.
        If the stack is empty, then answer ``None``.
        
        """
        if not self.data:
            return None
        return self.data[-1]

    def peek(self, index=0):
        u"""
        The ``peek`` method peeks into the stacked list of elements. The optional <attr>index</attr> (default
        value is ``0``) goes backwards, so an <attr>index</attr> of ``0`` is the top of the stack.
        """
        if index >= len(self.data):
            return None
        return self.data[-index - 1]

    def root(self):
        u"""
        
        The ``root`` method answers the root ``self.data[0]`` element of the stack.
        
        """
        return self.data[0]

    def pop(self):
        u"""
        
        The ``pop`` method pops the stack and answers the popped element.
        If the stack is empty, then answer ``None``. This is a “friendly” error, so the application
        can decide what to do with the wrong sized stack.
        
        """
        if len(self.data):
            return self.data.pop()
        return None

