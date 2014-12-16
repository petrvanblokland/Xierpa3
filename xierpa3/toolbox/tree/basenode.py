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
#     basenode.py
#
import copy
from xierpa3.toolbox.transformer import Transformer
from attributes import Attributes

class BaseNode(object):
    u"""
    The abstract ``BaseNode`` class is a wrapper for an ``Attributes`` instance (that needs to be
    initialized by an inheriting node class). The basic attribute methods are implemented here. The
    ``BaseNode`` does not implement any tree functionality, allowing both ``Node`` an
    ``State`` classes to inherit. The first is a tree, but the latter is flat. Though both contain a set of
    attributes.
    """
    TX = Transformer
    ATTRIBUTEDEFAULTS = {}

    def getAttributes(self):
        u"""
        The ``getAttributes`` method answers the dictionary ``Attributes`` instance
        ``self._attributes``.
        """
        return self.__dict__.get('_attributes')

    def getAttributeDefault(self, name):
        u"""
        The ``getAttributeDefault`` method answers the default for attribute ``name``. The behavior is
        to answer the result of ``self.ATTRIBUTEDEFAULTS.get(name)``.
        """
        return self.ATTRIBUTEDEFAULTS.get(name)

    def getNewAttributes(self, attributes=None, args=None):
        u"""
        The ``getAttributes`` method answers ``attributes`` attribute or a new instance of
        ``Attributes``. The attribute set holds the @attributes of the ``self`` node. Note that the
        attribute set is stored “as such” without making a copy. So any change to the attribute set when manipulating
        the tree, will also reflect in the original attribute set.<br/>

        If the ``args`` dictionary is defined, then the these values are added over the the key-value of new
        create ``Attributes`` instance. This is a separate method to allow inheriting node classes to redefine
        the class of the attribute set. The ``args`` attribute can be either a dictionary or a list of
        dictionaries.
        """
        if isinstance(attributes, dict):
            attributes = Attributes(**attributes)
        if attributes is None:
            attributes = Attributes()
        if args is not None:
            if not isinstance(args, (list, tuple)):
                args = (args,)
            for arg in args:
                if arg is not None:
                    attributes.update(arg)
        return attributes
