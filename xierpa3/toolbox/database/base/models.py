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
#     models.py
#
#     Based on the Django models approach:
#     http://docs.djangoproject.com/en/dev/ref/models/fields
#


import inspect

from basemodel import BaseModel
from fields import *

class Model(BaseModel):
    u"""
    <doc>The <code>Model</code> model is the base model of all inheriting model classes. A <code>Model</code> instance
    describes the behavior of a single table. By default it defines the type and behavior of the fields <code>self.id
    </code> as <code>SerialField</code> and <code>self.version</code> as <code>IntegerField</code>.<br/>
    The naming convention of attributes is that all plain names are field definitions and all additional attributes and
    method have an initial <code>'_'</code>.<br/>
    Upon construction of a model instance, the model and name attributes is defined in the field instances.
    </doc>
    """
    id = SerialField()
    version = IntegerField()

    def __init__(self, name=None, asname=None, lower=True):
        u"""
        <doc>The abstract <code>Model</code> class defines the generic behavior of Xierpa models. The <attr>name</attr>
        attribute defines the name of the model. It can either be a <code>basestring</code> or a model class. On
        construction all field attributes from inherited models are collected. Then a copy of the attribute is made (to
        avoid overwriting the field name and model of higher defined field definitions) and appended to <code>
        self._fields</code>.</doc>
        """
        super(Model, self).__init__()
        self._setName(name, lower)
        self._asname = asname
        self._fieldnames = []  # List of all field names (inherited attribute names not starting with '_')
        for baseclass in self.__class__.mro():
            for field, attribute in baseclass.__dict__.items():
                if isinstance(attribute, Field) and not self._fields.has_key(field):
                    # If the field is not defined yet (mro() goes up in the inheritance tree)
                    # then we want the field. Test, or else inherited field will overwrite.
                    # Make a copy of this attribute, or else we overwrite the model
                    # of inherited field models. This was a tough bug to find.
                    attribute = attribute.copy()
                    attribute.setName(field)  # Set the name of the field
                    attribute.setModel(self._getName())

                    self._fieldnames.append(field)
                    self._fields[field] = attribute

    def __getitem__(self, field):
        u"""
        <doc>
        The <code>__getitem__</code> methods allows the model to be searched for by a constructed name.
        </doc>
        """
        return self._fields.get(field)

    def _hasField(self, field):
        u"""
        <doc>The <code>_hasField</code> method answers the boolean flag if the model contains a field named <attr>
        field</attr>.</doc>
        """
        return self._fields.has_key(field)

    # Remember to redefine the method references below, if _hasField gets redefined by an inheriting field class.
    has_key = _has_key = _hasField

    def _getName(self):
        u"""
        <doc>The <code>getName</code> method answers the table name of <code>self</code>.</doc>
        """
        return self._name

    def _setName(self, name=None, lower=True):
        u"""
        <doc>The <code>_setName</code> method sets the name of the model. If the <attr>name</attr> is <code>None</code>
        then derive the name from the class name of <code>self</code>. The <attr>lower</attr> attribute (default is
        <code>True</code> is used to decide if the class name is lower case only.</doc>
        """
        if name is None:
            name = self.__class__.__name__
        elif inspect.isclass(name):
            name = name.__name__
        if lower:
            name = name.lower()
        self._name = name

    def _getFieldNames(self):
        u"""
        <doc>The <code>_getFieldNames</code> method answers the list of field names in a preserved order of <code>
        self._fieldnames</code>. Note that these fields are a mix between real SQL fields and virtual fields.</doc>
        """
        return self._fieldnames

    def createSql(self, indexlength=None, drop=True):
        u"""
        <doc>The <code>createSql</code> method answers the SQL query to create this table. The writing of the SQL file
        is triggered by the <code>'//initializesystem'</code> parameter.</doc>
        """
        indexed = []
        table = self._getName()

        t = []

        if drop:
            t.append('DROP TABLE IF EXISTS "%s";\n' % table)

        t.append('CREATE TABLE "%s"' % table)
        if self._asname:
            t.append(' AS' + self._asname)
        fields = []
        fieldnames = self._getFieldNames()
        fieldnames.sort()
        for fieldname in fieldnames:
            field = self[fieldname]
            fields.append('"%s" %s' % (fieldname, field.createSql()))
            if field.isIndexed() and not field.isUnique(): #unique automatically creates an index
                indexed.append((fieldname, field))
        if fields:
            t.append(' (\n\t')
            t.append(',\n\t'.join(fields))
            t.append(')')
        t.append(';\n')
        if indexed:
            if indexlength is not None:
                indexlength = '(%s)' % indexlength
            else:
                indexlength = ''
            for fieldname, field in indexed:
                t.append('CREATE INDEX "%s_%s_idx" ON "%s" ("%s"%s);\n' % (table, fieldname, table, fieldname, indexlength))
        t.append('\n')
        return ''.join(t)

class DateTimeModel(Model):
    creationDateTime = DateTimeField()
    creationUser_id = Many2OneField(Constants.TABLE_ADDRESS)
    modificationDateTime = DateTimeField()
    modificationUser_id = Many2OneField(Constants.TABLE_ADDRESS)

class NamedModel(DateTimeModel):
    name = UnicodeField(index=True)
    idName = SlugField()

class TreeModel(NamedModel):
    parent_id = ParentField(index=True)
    children = ChildrenField()
    deleted = BooleanField(default=False)

    def _getParentFieldName(self):
        u"""
        <doc>The <code>_getParentFieldName</code> method answers the field name of the parent relation of the model. The
        first field found that is an instance of <code>ParentField</code> is answered. Answer <code>None</code> if the
        model does not have a parent relation.</doc>
        """
        for fieldname, field in self._fields.items():
            if isinstance(field, ParentField):
                return fieldname
        return None

    def _getChildrenFieldName(self):
        u"""
        <doc>The <code>_getChildrenFieldName</code> method answers the field name of the children relation of the model.
        The first field found that is an instance of <code>ChildrenField</code> is answered as field name. Answer <code>
        None</code> if the model does not have a children relation.</doc>
        """
        for fieldname, field in self._fields.items():
            if isinstance(field, ChildrenField):
                return fieldname
        return None


