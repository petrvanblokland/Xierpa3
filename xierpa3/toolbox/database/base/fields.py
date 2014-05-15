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
#     fields.py
#
try:
	import cPickle
except:
	import pickle
from xierpa3.toolbox.parsers.json import cjson
from xierpa3.toolbox.transformer import TX, Transformer
from xierpa3.toolbox.dating import DateTime, Duration, datetime
from xierpa3.toolbox.storage.preference import Preference
from xierpa3.toolbox.storage.status.status import Status
from xierpa3.toolbox.constants import C
from xierpa3.toolbox.tree.etreenode import EtreeNode
from xierpa3.toolbox.tree.state import State

class Field(object):
    u"""
    <doc>
    The abstract <code>Field</code> class, defines the default behavior of all field classes.
    </doc>
    """
    TX                                     = Transformer
    DEFAULT                              = None                    # Default of default. Each inheriting field class can have it's own default value.
    SQL_QUERYNULL_T                         = u'"%s" = NULL'        # SQL update snippet used for NULL value.
    SQL_QUERYVALUEUPDATE_T                 = u'"%s" = \'%s\''        # SQL update snippet used for dates and strings 
    SQL_QUERYVALUEINSERT_T                 = u'\'%s\''            # SQL insert snippet used for dates and strings 
    SQL_NULL                             = u'NULL'
    SQL_NOTNULL                             = u'NOT NULL'
    SQL_UNIQUE                             = u'UNIQUE'
    SQL_DEFAULT_T                         = u"DEFAULT '%s'"

    XML_DEFAULTROOT                         = '<root/>'
    
    # ---------------------------------------------------------------------------------------------------------
    #    SQL field types
    #    This might need some other inheritance order in case there are more 
    #    types of datastores needed.

    SQL_BOOLEANTYPE                         = 'BOOLEAN'
    SQL_INTEGERTYPE                         = 'INT2'        # Small integer, otherwise use LONGTYPE
    SQL_LONGTYPE                         = 'BIGINT'
    SQL_FLOATTYPE                         = 'FLOAT'
    SQL_DECIMALTYPE                         = 'NUMERIC'
    SQL_SERIALTYPE                         = 'SERIAL'
    SQL_RELATIONTYPE                     = SQL_LONGTYPE
    SQL_CHARTYPE                         = 'CHAR'
    SQL_TEXTTYPE                         = 'TEXT'
    SQL_DATETYPE                         = 'DATE'
    SQL_TIMETYPE                         = 'TIME'
    SQL_DATETIMETYPE                     = 'TIMESTAMP'
    SQL_INTERVALTYPE                     = 'INTERVAL'
    SQL_SLUGTYPE                         = SQL_TEXTTYPE
    SQL_URLTYPE                             = SQL_TEXTTYPE
    SQL_PATHTYPE                         = SQL_TEXTTYPE
    SQL_EMAILTYPE                         = SQL_TEXTTYPE
    SQL_XMLTYPE                             = SQL_TEXTTYPE
    SQL_XMLTREETYPE                         = SQL_TEXTTYPE
    SQL_IDENTIFIERTYPE                     = SQL_TEXTTYPE
    SQL_BINARYTYPE                         = 'BYTEA'
    SQL_VALUETYPE                         = SQL_TEXTTYPE
    SQL_PICKLEDTYPE                         = SQL_TEXTTYPE

    def __init__(self, default=None, null=True, unique=False, index=False, validate=False, inherit=False):
        self.default = default or self.DEFAULT
        self.null = null
        self.unique = unique
        self.index = index or unique #unique fields should always be indexed
        self.validate = validate
        
        #in a TreeModel, if this record's value is None, travel up the tree and inherit the parent's value
        self.inherit = inherit

        # These values are supposed to be set by the parent model when it is constructed.
        self.name = None
        self.model = None

    def copy(self):
        u"""
        <doc>
        The <code>copy</code> method answers a copy of <code>self</code>. This is used to copy the field attributes of
        inheriting models, to avoid that the <code>self.model</code> is overwritten by other models.
        </doc>
        """
        copy = self.__class__(default=self.default, null=self.null, unique=self.unique, index=self.index, validate=self.validate, inherit=self.inherit)
        copy.name = self.getName()
        copy.model = self.getModel()        
        return copy

    def __repr__(self):
        return '[Field: %s Model: %s] %s' % (self.getClassName(), self.model, self.getName() or '')

    def isRelation(self):
        u"""
        <doc>
        The <code>isRelation</code> method answers the boolean flag if this field is relational. The default behavior of
        this method is to answer <code>self.isRecord() or self.isSelection()</code>.
        </doc>
        """
        return self.isRecord() or self.isSelection()

    def isRecord(self):
        u"""
        <doc>
        The <code>isRecord</code> method answers the boolean flag if this field is answering a single <code>Record
        </code> instance. This method is redefined by the many-to-one fields. The behavior is to answer
        <code>False</code>.
        </doc>
        """
        return False

    def isSelection(self):
        u"""
        <doc>
        The <code>isRecord</code> method answers the boolean flag if this field is answering a <code>Selection</code>
        instance. This method is redefined by the one-to-many fields. The behavior is to answer <code>False</code>.
        </doc>
        """
        return False

    def createSql(self, custom=None):
        u"""
        <doc>
        The <code>asSql</code> method answers the SQL part of the field description that is needed to create a table.
        </doc>
        """
        t = [custom or self.getSqlType()]
        if not self.null:
            t.append(self.SQL_NOTNULL)
        if self.unique:
            t.append(self.SQL_UNIQUE)
        default = self.getDefault()
        if default:
            t.append(self.SQL_DEFAULT_T % self.value2Sql(default))
        return ' '.join(t)

    def value2SqlInsert(self, field, value, **args):
        u"""
        <doc>
        The <code>value2SqlInsert</code> method answers the SQL code snippet that is used by the datastore to create an
        insert query for this <attr>field</attr> with <attr>value</attr>. This method offers standard behavior for field
        values of <code>(int, float, long)</code>. If the value is <code>None</code> and null is allowed, then
        <code>'NULL'</code> is used to update the record.<br/>
        
        In order to generate the right SQL syntax, inheriting field classes can define a different method
        <code>self.value2SqlQueryValue(field, value)</code>.
        </doc>
        """
        if value is None:
            if self.null:
                return self.SQL_NULL
            # Not NULL allowed, use default value instead after checking if it exists.
            raise ValueError('[Field.value2SqlInsert] Either allow NULL (self.null = True) or make sure value for "%s" is not None' % field)
        return self.SQL_QUERYVALUEINSERT_T % self.value2Sql(value, **args)

    def value2SqlUpdate(self, field, value, binary=False, **args):
        u"""
        <doc>
        The <code>value2SqlUpdate</code> method answers the SQL code snippet that is used by the datastore to create an
        update query for this <attr>field</attr> with <attr>value</attr>. This method offers standard behavior for field
        values of <code>(int, float, long)</code>. If the value is <code>None</code> and null is allowed, then
        <code>'NULL'</code> is used to update the record.<br/>
        
        In order to generate the right SQL syntax, inheriting field classes can define a different method
        <code>self.value2SqlQueryValue(field, value)</code>.
        </doc>
        """
        if value is None:
            if self.null:
                return self.SQL_QUERYNULL_T % field
            # Not NULL allowed, use default value instead after checking if it exists.
            raise ValueError('[Field.value2SqlUpdate] Either allow NULL (self.null = True) or make sure value for "%s" is not None' % field)
        if not binary and type(value) == str:
            value = value.decode('utf-8')
        snippet = self.SQL_QUERYVALUEUPDATE_T % (field, self.value2Sql(value, **args))
        return snippet

    def value2Sql(self, value, **args):
        u"""
        <doc>
        The <code>value2Sql</code> method answers the <attr>value</attr> attribute converted to the SQL value. The
        default behavior is to answer the unchanged <code>value</code>. This method can be redefined by an inheriting
        field class definition.
        </doc>
        """
        return value

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        The <code>sql2Value</code> method answers the <attr>sqlvalue</attr> attribute converted to the Python value.
        Default behavior is answer a string. This method needs to be redefined by the inheriting field class. The
        <attr>id</attr> contains the id of the calling record, if it exists.
        </doc>
        """
        return sqlvalue or self.getDefault()

    @classmethod
    def getClassName(cls):
        u"""
        <doc>
        The <code>getFieldClassName</code> method answers the name of the class.
        </doc>
        """
        return cls.__name__

    def setName(self, name):
        u"""
        <doc>
        The <code>setName</code> method sets the <attr>name</attr> attribute, as it appears in the model. This attribute
        is set by the model constructor, to mark the actual name of the field.
        </doc>
        """
        self.name = name

    def getName(self):
        u"""
        <doc>
        The <code>getName</code> method answers the name of the field as defined in <code>record</code>.
        </doc>
        """
        return self.name

    def setModel(self, model):
        u"""
        <doc>
        The <code>setModel</code> method sets the <attr>model</attr> attribute. This attribute is set by the model
        constructor, to mark the actual name of the field.
        </doc>
        """
        self.model = model

    def getModel(self):
        u"""
        <doc>
        The <code>getModel</code> method answers the <attr>self.model</attr> attribute. This attribute is set by the
        model constructor, to mark the actual name of the field.
        </doc>
        """
        return self.model

    def getSqlType(self):
        u"""
        <doc>
        The <code>getSqlType</code> method answers the SQL query syntax for the type of this field. The default behavior
        it to raise an error, since this method needs to be redefined by the inheriting field class.
        </doc>
        """
        raise ValueError('[Field.getSqlType] Redefine in inheriting field class')

    def isNull(self):
        u"""
        <doc>
        The <code>isNull</code> methods answers the boolean flag if this field is nullable. Typically this is the
        value of <code>self.null</code>.
        </doc>
        """
        return self.null

    def isIndexed(self):
        u"""
        <doc>
        The <code>isIndexed</code> methods answers the boolean flag if this field is indexed. Typically this is the
        value of <code>self.index</code>.
        </doc>
        """
        return self.index

    def isUnique(self):
        u"""
        <doc>
        The <code>isUnique</code> methods answers the boolean flag if this field is unique. Typically this
        is the value of <code>self.unique</code>.
        </doc>
        """
        return self.unique

    def getDefault(self):
        u"""
        <doc>
        The <code>getDefault</code> method answers the default value for this field. The default behavior is to answer
        <code>self.default</code>. This method can be redefined by the inheriting field class.
        </doc>
        """
        return self.default

    def isIdField(self):
        u"""
        <doc>
        The <code>isIdField</code> method answers the boolean flag if this field is the primary field. The default
        behavior is to answer <code>False</code>.
        </doc>
        """
        return False

    def isOne2ManyField(self):
        u"""
        <doc>
        The <code>isOne2ManyField</code> method answers the boolean flag if this field is a one-to-many field. The
        default behavior is to answer <code>False</code>.
        </doc>
        """
        return False

    def isMany2OneField(self):
        u"""
        <doc>
        The <code>isMany2OneField</code> method answers the boolean flag if this field is a many-to-one field. The
        default behavior is to answer <code>False</code>.
        </doc>
        """
        return False

    def isMany2ManyField(self):
        u"""
        <doc>
        The <code>isMany2ManyField</code> method answers the boolean flag if this field is a many-to-many field. The
        default behavior is to answer <code>False</code>.
        </doc>
        """
        return False

    def isParentField(self):
        u"""
        <doc>
        The <code>isParentField</code> method answers the boolean flag if this field is a parent field. Only one parent
        field can exist in a model. The default behavior is to answer <code>False</code>.
        </doc>
        """
        return False

    def isChildrenField(self):
        u"""
        <doc>
        The <code>isParentField</code> method answers the boolean flag if this field is a parent field. Only one
        children field can exist in a model. The default behavior is to answer <code>False</code>.
        </doc>
        """
        return False

    def isInherited(self):
        return bool(self.inherit)


# Basic value fields
class BaseValueField(Field):
    u"""
    <doc>
    The <code>BaseValueField</code> field class implements the standard behavior for SQL fields that describe their
    values without quotes, such as numbers, relation ID's and booleans.
    </doc>
    """
    SQL_QUERYVALUEUPDATE_T = u'"%s" = %s'  # SQL update snippet used for numbers, relations and booleans
    SQL_QUERYVALUEINSERT_T = u'%s'  # SQL insert snippet used for numbers, relations and booleans

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        The <code>sql2Value</code> method answers the plain <attr>sqlvalue</attr> attribute converted to the Python
        value. Default behavior is answer a string. This method needs to be redefined by the inheriting field class. If
        <attr>sqlvalue</attr> is <code>None</code>, then answer the default value the is result of
        <code>self.getDefault()</code. The <attr>id</attr> contains the id of the calling record, if it exists.
        </doc>
        """
        if sqlvalue is None:
            sqlvalue = self.getDefault()
        return sqlvalue

class IntegerField(BaseValueField):
    def getSqlType(self):
        return self.SQL_INTEGERTYPE

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        The <code>sql2Value</code> method answers the <attr>sqlvalue</attr> attribute converted to the Python value. If
        <attr>sqlvalue</attr> is <code>None</code>, then answer the default value the is result of
        <code>self.getDefault()</code. The <attr>id</attr> contains the id of the calling record, if it exists.
        </doc>
        """
        if sqlvalue is None:
            sqlvalue = self.getDefault()
        if not sqlvalue in [None, '']:
            return int(sqlvalue)
        return None

    def value2Sql(self, value, **args):
        u"""
        <doc>
        The <code>value2Sql</code> method answers the plain <attr>value</attr> number value.
        </doc>
        """
        return value

class LongField(IntegerField):
    u"""
    <doc>
    The <code>LongField</code> field class specifies the value to be a long (SQL BigInt). This field type is
    specifically used for inheriting relational fields classes.
    </doc>
    """
    def getSqlType(self):
        return self.SQL_LONGTYPE

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        The <code>sql2Value</code> method answers the <attr>sqlvalue</attr> attribute converted to the Python value. If
        <attr>sqlvalue</attr> is <code>None</code>, then answer the default value the is result of
        <code>self.getDefault()</code. The <attr>id</attr> contains the id of the calling record, if it exists.
        </doc>
        """
        if sqlvalue is None:
            sqlvalue = self.getDefault()
        if not sqlvalue in [None, '']:
            return long(sqlvalue)
        return None

class FloatField(BaseValueField):
    def getSqlType(self):
        return self.SQL_FLOATTYPE

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        The <code>sql2Value</code> method answers the <attr>sqlvalue</attr> attribute converted to the Python value. If
        <attr>sqlvalue</attr> is <code>None</code>, then answer the default value the is result of
        <code>self.getDefault()</code. The <attr>id</attr> contains the id of the calling record, if it exists.
        </doc>
        """
        if sqlvalue is None:
            sqlvalue = self.getDefault()
        if not sqlvalue in [None, '']:
            return float(sqlvalue)
        return None

class DecimalField(BaseValueField):
    """
    <doc>
    <code>DecimalField</code> represents exact-precision decimal numbers with arbitrary significant digits and decimal
    points. Specify <attr>precision</attr> to set the maximum total digits (before and after decimal point), and
    <attr>scale</attr> to specify the number of digits after the decimal point. The default is
    <code>DecimalField(9,2)</code> which would allow you to store monetary values up to $9,999,999.99
    </doc>
    """
    def __init__(self, precision=9, scale=2, **args):

        if scale < 0:
            raise ValueError("DecimalField.scale must be >= 0")

        BaseValueField.__init__(self, **args)
        self.precision = precision
        self.scale = scale

    def copy(self):
        u"""
        <doc>
        This <code>copy</code> executes the regular Field <code>copy</code> and adds in the extra attributes specific to
        this field type.
        </doc>
        """
        copy = BaseValueField.copy(self)
        copy.precision = self.precision
        copy.scale = self.scale

        return copy

    def getSqlType(self):
        return self.SQL_DECIMALTYPE

    def createSql(self):
        u"""
        <doc>
        The <code>asSql</code> method answers the SQL part of the field description that is needed to create a table.
        </doc>
        """

        return Field.createSql(self, "{type}({p},{s})".format(type=self.getSqlType(), p=self.precision, s=self.scale))

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        The <code>sql2Value</code> method answers the <attr>sqlvalue</attr> attribute converted to the Python value. If
        <attr>sqlvalue</attr> is <code>None</code>, then answer the default value the is result of
        <code>self.getDefault()</code. The <attr>id</attr> contains the id of the calling record, if it exists.
        </doc>
        """
        if sqlvalue is None:
            sqlvalue = self.getDefault()
        if not sqlvalue in [None, '']:
            mult = pow(10, self.scale)
            return round(float(sqlvalue) * mult) / mult
        return None

    def value2Sql(self, value, **args):
        u"""
        <doc>
        The <code>value2Sql</code> method answers the plain <attr>value</attr> number value.
        </doc>
        """

        if value in [None, '']:
            return None

        # if value is a float, round it to the right number of digits
        mult = pow(10, self.scale)
        return round(mult * float(value)) / mult

class BooleanField(BaseValueField):

    def getSqlType(self):
        return self.SQL_BOOLEANTYPE

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        The <code>sql2Value</code> method answers the <attr>sqlvalue</attr> attribute converted to the Python value. If
        <attr>sqlvalue</attr> is <code>None</code>, then answer the default value the is result of
        <code>self.getDefault()</code>. The <attr>id</attr> contains the id of the calling record, if it exists.
        </doc>
        """
        if sqlvalue is None:
            sqlvalue = self.getDefault()
        return bool(sqlvalue)

    def value2Sql(self, value, **args):
        u"""
        <doc>
        The <code>value2Sql</code> method answers the <attr>value</attr> attribute converted to the SQL value. The value
        is <code>True</code> if <code>not value in self.FALSEVALUES</code>.
        </doc>
        """
        return {True: 'TRUE', False: 'FALSE'}[not value in C.FALSEVALUES]

class SerialField(IntegerField):
    def getSqlType(self):
        return '%s PRIMARY KEY' % self.SQL_SERIALTYPE

    def isIdField(self):
        u"""
        <doc>
        The <code>isIdField</code> method answers the boolean flag if this field is the primary field. This method
        answers <code>True</code>.
        </doc>
        """
        return True

class TypeField(IntegerField):

    ITEMTYPESET = C.ITEMTYPESET
    CHECKVALUE = True

    def __init__(self,types=None,check=True,**args):
        IntegerField.__init__(self,**args)
        self.CHECKVALUE = check
        if types:
            self.ITEMTYPESET = types

    def copy(self):
        u"""
        <doc>
        The <code>copy</code> method answers a copy of <code>self</code>. This is used to copy the field attributes of
        inheriting models, to avoid that the <code>self.model</code> is overwritten by other models.
        </doc>
        """
        import copy
        thecopy = IntegerField.copy(self)
        thecopy.ITEMTYPESET = copy.copy(self.ITEMTYPESET)
        thecopy.CHECKVALUE = self.CHECKVALUE        
        return thecopy


    def checkValue(self, value):
        if not self.CHECKVALUE:
            return True
        if not value in self.ITEMTYPESET:
            raise ValueError('[TypeField.checkValue] Value "%s" not allowed in TypeField (%s)' % (value, repr(self.ITEMTYPESET)))
        return True

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        The <code>sql2Value</code> method answers the <attr>sqlvalue</attr> attribute converted to the Python value.
        The value is checked to be in <code>self.ITEMTYPESET</code> that can be changed on initialize by an inheriting
        class. Default value is <code>C.ITEMTYPESET</code>. Otherwise an error is raised.<br/>
        
        If <attr>sqlvalue</attr> is <code>None</code>, then answer the default value the is result of
        <code>self.getDefault()</code. The <attr>id</attr> contains the id of the calling record, if it exists.
        </doc>
        """
        if sqlvalue is None:
            sqlvalue = self.getDefault()
        if not sqlvalue in [None, '']:
            value = int(sqlvalue)
            self.checkValue(value)
            return value
        return None

    def value2Sql(self, value, **args):
        u"""
        <doc>
        The <code>value2Sql</code> method answers the plain <attr>value</attr> number value. The value is checked to be
        in <code>self.ITEMTYPESET</code> that can be changed on initialize by an inheriting class. Default value is
        <code>C.ITEMTYPESET</code>. Otherwise an error is raised.<br/>
        </doc>
        """
        sqlvalue = int(value)
        self.checkValue(sqlvalue)
        return sqlvalue

# Text fields
class CharField(Field):
    def __init__(self, size=8, **args):
        Field.__init__(self, **args)
        self.size = size

    def getSqlType(self):
        return '%s(%d)' % (self.SQL_CHARTYPE, self.size)

    def copy(self):
        u"""
        <doc>
        This <code>copy</code> executes the regular Field <code>copy</code> and adds in the extra attributes specific to
        this field type.
        </doc>
        """
        copy = Field.copy(self)
        copy.size = self.size

        return copy

    def value2Sql(self, value, **args):
        u"""
        <doc>
        The <code>value2Sql</code> method answers the <attr>value</attr> attribute converted to the SQL value. The
        <attr>value</attr> string is converted to unicode.
        </doc>
        """
        return TX.escapeSqlQuotes(value)

class TextField(Field):
    def getSqlType(self):
        return self.SQL_TEXTTYPE

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        The <code>sql2Value</code> method answers the <attr>sqlvalue</attr> attribute converted to the Python value. If
        <attr>sqlvalue</attr> is <code>None</code>, then answer the default value the is result of
        <code>self.getDefault()</code>. Escape dangerous SQL quotes. The <attr>id</attr> contains the id of the calling
        record, if it exists.
        </doc>
        """
        if sqlvalue is None:
            sqlvalue = self.getDefault()
        return sqlvalue

    def value2Sql(self, value, **args):
        u"""
        <doc>
        The <code>value2Sql</code> method answers the <attr>value</attr> attribute converted to the SQL value. The
        <attr>value</attr> string is converted to unicode.
        </doc>
        """
        return TX.escapeSqlQuotes(value)

class LargeIndexedTextField(TextField):
    u"""
    <doc>
    The <code>LargeIndexedTextField</code> field splits large text fields into smaller pieces with a maximum of 2713
    bytes for Postgres indexing.
    </doc>
    """
    # Finish this later as an automatic split into records of a hidden table.

class UnicodeField(TextField):
    u"""
    <doc>
    <code>UnicodeField</code> is just like TextField, except it ensures that values are always properly UTF-8
    encoded/decoded.
    </doc>
    """
    def sql2Value(self, sqlvalue, id, db, **args):
        if sqlvalue is None:
            sqlvalue = self.getDefault()
        if isinstance(sqlvalue, basestring) and not isinstance(sqlvalue, unicode):
            return unicode(sqlvalue, 'utf-8')
        else:
            return sqlvalue


class XmlField(TextField):
    u"""
    <doc>
    The <code>XmlField</code> field class saves the data as a validated XML document. If the value is a string, then it
    is repaired to make sure that it is valid XML. If the value is an <code>EtreeNode</code> instance, that write a
    extracted XML to the field.
    </doc>
    """
    def getSqlType(self):
        return self.SQL_XMLTYPE

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        </doc>
        """
        return sqlvalue

    def value2Sql(self, value, **args):
        u"""
        <doc>
        The <code>value2Sql</code> method answers the <attr>value</attr> attributed converted to the SQL value, which is
        a validated XML UTF-8 string. If the <attr>value</attr> is a <code>basestring</code> then it is assumed to be
        XML source. The <code>XmlRepairMan</code> will check on consistency and repair if needed. If <attr>value</attr>
        is an instance of <code>EtreeNode</code>, then convert it to XML output string. For other types of <attr>value
        </attr> it is converted to a string and then fed into the repair man.
        </doc>
        """
        if isinstance(value, EtreeNode):
            value = value._toString()
        elif not isinstance(value, basestring):
            value = `value`
        xml = XmlRepairMan.repair(value)
        return TX.escapeSqlQuotes(xml)

class XmlTreeField(XmlField):
    u"""
    <doc>
    The <code>XmlTreeField</code> field class reads/saves an <code>etree</code> node tree as XML document.
    </doc>
    """
    def getSqlType(self):
        return self.SQL_XMLTREETYPE

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        The <code>sql2Value</code> method validate/repairs the XML string from the database and answers an <code>
        EtreeNode<code> instance. Note that this is both an efficient (etree) way of converting XML into a tree and it
        is cached by the record.
        </doc>
        """
        xml = XmlRepairMan.repair(sqlvalue, default=C.XML_DEFAULTROOT)
        return EtreeNode(xml=xml)

class DateTimeField(Field):
    def getSqlType(self):
        return self.SQL_DATETIMETYPE

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        The <code>sql2Value</code> method answers the <attr>sqlvalue</attr> attribute converted to the Python value. The
        default behavior is to answer <code>DateTime(date=sqlvalue[0], time=sqlvalue[1])</code>. If <attr>sqlvalue
        </attr> is <code>None</code>, then answer the default value the is result of <code>self.getDefault()</code. The
        <attr>id</attr> contains the id of the calling record, if it exists.
        </doc>
        """
        value = None
        if sqlvalue is None:
            sqlvalue = self.getDefault()
        if sqlvalue:
            # Translate here, or else DateTime crashes on the c-like datetime instance.
            date = '%s-%s-%s %s:%s:%s' % (sqlvalue.year, sqlvalue.month, sqlvalue.day, sqlvalue.hour, sqlvalue.minute, sqlvalue.second)
            value = DateTime(date_time=date)
        return value

    def value2Sql(self, value, **args):
        u"""
        <doc>
        The <code>value2Sql</code> method answers the <attr>value</attr> attribute converted to the SQL value.
        </doc>
        """
        if isinstance(value, (int, long, float)):
            value = DateTime(mtime=value)
        if isinstance(value, DateTime):
            value = value.date_time
        return value

class DateField(Field):
    def getSqlType(self):
        return self.SQL_DATETYPE

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        The <code>sql2Value</code> method answers the <attr>sqlvalue</attr> attribute converted to the Python value. The
        default behavior is to answer <code>DateTime(date=sqlvalue[0], time=sqlvalue[1])</code>. If <attr>sqlvalue
        </attr> is <code>None</code>, then answer the default value the is result of <code>self.getDefault()</code.
        The <attr>id</attr> contains the id of the calling record, if it exists.
        </doc>
        """
        value = None
        if sqlvalue is None:
            sqlvalue = self.getDefault()
        if sqlvalue:
            if not isinstance(sqlvalue, basestring):
                # Translate here, or else DateTime crashes on the c-like datetime instance.
                sqlvalue = '%s-%s-%s' % (sqlvalue.year, sqlvalue.month, sqlvalue.day)
            value = DateTime(date=sqlvalue)
        return value

    def value2Sql(self, value, **args):
        u"""
        <doc>
        The <code>value2Sql</code> method answers the <attr>value</attr> attribute converted to the SQL value.
        </doc>
        """
        if isinstance(value, DateTime):
            value = value.date
        return value

class DurationField(Field):
    def getSqlType(self):
        return self.SQL_INTERVALTYPE

    def sql2Value(self, sqlvalue, id, db, **args):
        """
        <doc>
        Converts from SQL INTERVAL type to Xierpa Duration object
        </doc>
        """
        if sqlvalue is None:
            return Duration()

        if isinstance(sqlvalue, datetime.timedelta):
            return Duration(td=sqlvalue)

        import re

        args = {}
        for num, unit in re.findall(r'(-?\d+)\s*([a-z]+)', sqlvalue.lower()):
            if unit.startswith('y'):
                args['years'] = num
            elif unit.startswith('mo'):
                args['months'] = num
            elif unit.startswith('w'):
                args['weeks'] = num
            elif unit.startswith('d'):
                args['days'] = num
            elif unit.startswith('h'):
                args['hours'] = num
            elif unit.startswith('min'):
                args['minutes'] = num
            elif unit.startswith('s'):
                args['seconds'] = num
            elif unit.startswith('milli'):
                args['milliseconds'] = num
            elif unit.startswith('micro'):
                args['microseconds'] = num

        colonic = re.search(r'(\d\d):(\d\d):(\d\d)(?:\.(\d+))?', sqlvalue)

        if colonic:
            (args['hours'], args['minutes'], args['seconds'], args['microseconds']) = colonic.groups()
            args['microseconds'] = '{0:<06}'.format(args['microseconds'])

        for k, v in args.items():
            args[k] = int(v)

        return Duration(**args)

    def value2Sql(self, value, **args):
        return "{m} months {d} days {s} seconds {u} microseconds".format(
            m=value.months, d=value.days, s=value.seconds, u=value.microseconds
        )

InvervalField = DurationField

class PickledField(TextField):
    def getSqlType(self):
        return self.SQL_PICKLEDTYPE

    def sql2Value(self, sqlvalue, id, db, **args):
        try:
            return cPickle.loads(sqlvalue)
        except (EOFError, TypeError):
            pass
        return None

    def value2Sql(self, value, **args):
        try:
            return cPickle.dumps(value)
        except (EOFError, TypeError):
            pass
        return ''

class UrlField(TextField):
    def getSqlType(self):
        return self.SQL_URLTYPE

    def value2Sql(self, value, **args):
        return TX.name2UrlName(value)

class PathField(TextField):
    def getSqlType(self):
        return self.SQL_PATHTYPE

class IdentifierField(TextField):
    def getSqlType(self):
        return self.SQL_IDENTIFIERTYPE

    def isIndexed(self):
        u"""
        <doc>
        The <code>isIndexed</code> methods answers the boolean flag if this field is indexed. 
        For an <code>IdentifierField</code> this is always <code>True</code>.
        </doc>
        """
        return True

class ListField(TextField):
    u"""
    <doc>
    The <code>ListField</code> behave as a Python list, which is stored in the database text field
    as s JSON source. If there is an error parsing, then answer the list <code>code>['cjson.DecodeError', sqlvalue]<code>.
    </doc>
    """
    def sql2Value(self, sqlvalue, id, db, **args):
        try:
            if sqlvalue: sqlvalue = sqlvalue.replace('\\\\', '\\')
            l = cjson.decode(sqlvalue or '[]')
        except cjson.DecodeError:
            l = []
        return l

    def value2Sql(self, value, **args):
        assert isinstance(value, (list, tuple))
        return TX.escapeSqlQuotes(cjson.encode(list(value or [])))

class DictionaryField(TextField):
    u"""
    <doc>
    The <code>DictionaryField</code> field behaves as a Python dictionary, which is stored in the database text field
    as a JSON source. If there is an error parsing, then answer the dictionary <code>{'json.DecodeError': sqlvalue}<code>.
    </doc>
    """
    def sql2Value(self, sqlvalue, id, db, **args):
        try:
            if sqlvalue: sqlvalue = sqlvalue.replace('\\\\', '\\')
            d = cjson.decode(sqlvalue or '{}')
        except cjson.DecodeError:
            d = {}
        return d

    def value2Sql(self, value, **args):
        # Make sure that all keys are string, otherwise JSON cannot store.
        assert isinstance(value, dict), '[DictionaryField supplied with non-dict: "%s"]' % value
        return TX.escapeSqlQuotes(cjson.encode(value or {}))

class JsonField(DictionaryField):
    # Compatible with DictionaryField. Takes an object and converts to JSON.
    pass

class SetField(DictionaryField):
    u"""
    <doc>The <code>SetField</code> field behaves as a standard Python <code>set()</code> instance. Note that the values
    of the set must convert into text, through JSON encoding. So only standard classes can be used. Since there is no
    Set type in JSON, the dictionary is used there with all the values set to 1.
    </doc>
    """
    def sql2Value(self, sqlvalue, id, db, **args):
        d = DictionaryField.sql2Value(self, sqlvalue, id, db, **args)
        return list(set(d.keys()))  # Just the keys, ignore the values, make set and then list again. To avoid JSON from
                                    # choking.

    def value2Sql(self, value, **args):
        if isinstance(value, (list, tuple)):
            value = set(value)
        elif isinstance(value, dict):
            value = set(dict.keys())
        assert isinstance(value, set)
        d = {}
        for key in value:
            d[key] = 1  # Default value to make the set into a dictionary
        return DictionaryField.value2Sql(self, d, **args)

class StateField(TextField):
    u"""
    <doc>
    The <code>StateField</code> field behaves as State instance, which is stored in the database text field
    as a JSON source. If there is an error parsing, then answer the dictionary <code>{'json.DecodeError': sqlvalue}<code>.
    </doc>
    """
    def sql2Value(self, sqlvalue, id, db, **args):
        return State._fromJson(sqlvalue or '{}')

    def value2Sql(self, state, **args):
        assert isinstance(state, State), ('[StateField supplied with non-state: "%s"]' % state)
        return TX.escapeSqlQuotes(State._asJson(state))

class StatusField(DictionaryField):
    u"""
    <doc>The <code>StatusField</code> field behaves the instance of <code>Status</code> that can handle the set and get
    of arbitrary names and values in the range of <code>(bool, int, basestring)</code>. This allows the field to be used
    as storage of all kind values about the record. Note that these values can not be part of a selection query. Or the
    field can be used e.g. for separate parts of an XML/HTML text (such as required in Treesaver), that are related,
    variable, but not efficient to render them from a tree.<br/>
    Otherwise a <code>SelectionField</code> should be used, which has the values openly visible for SQL. The <code>
    StatusField</code> key-values are stored as JSON dictionary.</doc>
    """
    def sql2Value(self, sqlvalue, id, db, **args):
        d = DictionaryField.sql2Value(self, sqlvalue, id, db, **args)
        return Status.fromDict(d)

    def value2Sql(self, value, **args):
        if not isinstance(value, Status):
            value = Status()
        return DictionaryField.value2Sql(self, value.getValues(), **args)

class PreferenceField(DictionaryField):
    u"""
    <doc>
    The <code>PrefereceField</code> class inherits from the <code>DictionaryField</code> to store a dictionary
    of basic Python classed as JSON source. The difference is that the JSON source decodes to a set of nested
    <code>Preference</code> dictionaries that allow path addressing (See also the description of the <code>Preference</code>
    class. An instance can get and set value with the key <code>preference['a/b/c'] = 1234</code>, which will create
    a tree of <code>Preference</code> instances. Another way of writing this key chain is <code>preference[('a','b','c')] = 1234</code>.
    </doc>
    """
    def sql2Value(self, sqlvalue, id, db, **args):
        if sqlvalue: sqlvalue = sqlvalue.replace('\\\\', '\\')
        return Preference.fromDict(cjson.decode(sqlvalue or '{}'))

class SelectionField(TextField):
    u"""
    <doc>
    The <code>SelectionField</code> field behaves as a list of index numbers. It saves as a comma separated string
    (not as a possible dedicated list field) to allow field to run on all database platforms.
    </doc>
    """

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>The <code>sql2Value</code> method answers the <attr>sqlvalue</attr> attribute converted to the Python
        value. Note that these will be string parts, not integers ID’s.<br/>
        If <attr>sqlvalue</attr> is already <code>list</code> or a <code>tuple</code>, then answer the unchanged
        value of the attribute. It is the responsibility of the database application to make sure that all values
        in the list are integers.<br/>
        If <attr>sqlvalue</attr> is <code>None</code>, then answer the default value the is result of <code>
        self.getDefault()</code>. The <attr>id</attr> contains the id of the calling record, if it exists.<br/>
        Note that the application setting field values should do this on a copy of the field value, or otherwise the
        changed-field detection of the record cannot know that the value changed.</doc>
        """
        if sqlvalue is None:
            sqlvalue = self.getDefault() or set()
        if isinstance(sqlvalue, (set, list, tuple)):  # Assuming that the list/tuple only contains integers.
            return set(sqlvalue)
        return TX.idCommaString2IdSet(sqlvalue)

    def value2Sql(self, value, **args):
        u"""
        <doc>The <code>value2Sql</code> method answers the <attr>value</attr> attribute converted to the SQL value.
        Since the order may be alphabetic on labels, the order of values is maintained. Remove all zero’s from the
        selection list. If there are only <code>0</code> values filled, then set the value to <code>None</code>.</doc>
        """
        return TX.value2IdCommaString(value)

class SlugField(Field):
    def getSqlType(self):
        return self.SQL_SLUGTYPE

    def value2Sql(self, value, **args):
        u"""
        <doc>
        The <code>value2Sql</code> method answers the <attr>value</attr> attribute converted to the SQL value.
        The default behavior is to answer <code>name2UrlName(value)</code>. The hyphen is allowed to be part
        of the <code>SlugField</code> content: all separators are translated into hyphens.
        </doc>
        """
        return TX.name2UrlName(value, usehyphen=True)

class EmailField(Field):
    def getSqlType(self):
        return self.SQL_EMAILTYPE

class ValueField(Field):
    def getSqlType(self):
        return self.SQL_VALUETYPE

class BinaryField(Field):
    u"""
    <doc><code>BinaryField</code> stores pure binary data directly in a BYTEA field. This is a change from Xierpa 1
    behaviour, where BinaryField was really just a text field. Also changed from earlier RealBinaryField, which stored
    base64-encoded data.</doc>
    """

    def getSqlType(self):
        return self.SQL_BINARYTYPE

    def value2SqlUpdate(self, field, value, **args):
        if value is None:
            return Field.value2SqlUpdate(self, field, value, **args)
        return "\"{0}\" = E'{1}'".format(field, self.value2Sql(value, **args))

    def value2SqlInsert(self, field, value, **args):
        if value is None:
            return Field.value2SqlInsert(self, field, value, **args)
        return "E'{0}'".format(self.value2Sql(value, **args))

    def value2Sql(self, value, **args):
        u"""
        <doc>
        The <code>BinaryField.value2Sql</code> converts a set of binary bytes into Postgres "BYTEA hex format":
        E'\\x<hex digits, two per byte>'
        </doc>
        """
        if isinstance(value, unicode):
            value = value.encode('utf-8')

        return r"\\x{0}".format(''.join(['{0:0>2X}'.format(ord(byte)) for byte in bytes(value)]))

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        <code>BinaryField.sql2Value</code> simply returns the raw value of the datatabase field as a <code>bytes</code>
        object. In Python 2.6+ this is an alias for the <code>str</code> type. As of Python 3.0 it is a separate type. 
        </doc>
        """
        if sqlvalue is None:
            return None

        return bytes(sqlvalue)

RealBinaryField = BinaryField

class EncryptedField(BinaryField):
    u"""
    <doc>
    <code>EncryptedField</code> automatically encrypts and decrypts values stored as BinaryFields in the database.
    In order to use this field you must do record._setEncryptionKey(field,key) before setting or getting the value.
    <attr>time</attr> can be specified to set approximately how long it should take to do the encryption/decryption.
    This helps prevent people from cracking encrypted values in our database en masse.
    </doc>
    """
    # amount of time we want the encryption/decryption to take
    # should be fast enough to not be annoying for users
    # but slow enough to make it difficult for malicious person to crack passwords en masse
    ENCRYPTION_TIME = 0.5

    def __init__(self, time=None, **args):
        BinaryField.__init__(self, **args)
        if isinstance(time, (int, float)) and time > 0:
            self.ENCRYPTION_TIME = time

    def copy(self):
        u"""
        <doc>
        The <code>copy</code> method answers a copy of <code>self</code>. This is used to copy the field attributes of
        inheriting models, to avoid that the <code>self.model</code> is overwritten by other models.
        </doc>
        """
        copy = BinaryField.copy(self)
        copy.ENCRYPTION_TIME = self.ENCRYPTION_TIME
        return copy

    def value2Sql(self, value, key, **args):
        import scrypt
        if value is None:
            return self.SQL_NULL
        if key in ('', None):
            raise ValueError("Empty encryption key passed to EncryptedField.value2Sql")
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        value = scrypt.encrypt(value, key, maxtime=self.ENCRYPTION_TIME)

        return BinaryField.value2Sql(self, value, **args)

    def sql2Value(self, sqlvalue, id, db, key, **args):
        import scrypt
        if sqlvalue is None:
            return None
        if key in ('', None):
            raise ValueError("Empty encryption key passed to EncryptedField.sql2Value")
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        return scrypt.decrypt(bytes(sqlvalue), key, maxtime=self.ENCRYPTION_TIME * 2)


class PasswordField(EncryptedField):
    u"""
    <doc>
    The <code>PasswordField</code> class defines the behavior of an auto-encrypted password storage 
    that cannot be reverted.
    </doc>
    """

    SALT_LENGTH = 32

    def value2Sql(self, value, **args):
        u"""
        <doc><code>PasswordField.value2Sql<code> creates a one-way randomized hash using the scrypt algorithm. See:
            http://www.tarsnap.com/scrypt.html
            http://pypi.python.org/pypi/scrypt/
        </doc>
        """
        import os
        # the value that we're encrypting doesn't actually matter.
        # we are just using the password as the encryption key.
        if value is None:
            return self.SQL_NULL

        salt = bytes(os.urandom(self.SALT_LENGTH))
        args['key'] = value * 5
        return EncryptedField.value2Sql(self, salt, **args)

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc><code>PasswordField.sql2Value<code> returns a string-like object, which replaces the standard __eq__ test
        with a function that tries to decrypt the database entry using the supplied operand for comparison. Encryption
        is using the scrypt algorithm:
            http://www.tarsnap.com/scrypt.html
            http://pypi.python.org/pypi/scrypt/
            sudo port install scrypt -> macports scrypt binaries
            sudo pip install scrypt -> python scrypt wrapper
        </doc>
        """
        if sqlvalue is None:
            return None

        class password(bytes):
            def __eq__(myself, test):
                import scrypt
                try:
                    if not isinstance(test, basestring) or len(test) == 0:
                        return False

                    # this will throw an error if it fails
                    myself.getsalt(test)

                    return True
                except scrypt.error, e:
                    #print e
                    return False

            def __ne__(myself, test):
                return not myself.__eq__(test)

            def getsalt(encrypted, thepassword, **args):
                args['key'] = thepassword * 5
                return EncryptedField.sql2Value(self, bytes(encrypted), id, db, **args)

        return password(sqlvalue)

# Foreign key fields
class KeyField(LongField):
    u"""
    <doc>The abstract <code>KeyField</code> class, defined the top abstraction of key fields. This is separated from the
    <code>ForeignKeyField</code> to allow plain id interpretation, e.g. in the case of <code>Many2ManyField</code>
    models, where the <code>TABLE_XREF</code> must interpret the id in relation to a variable defined table name.</doc>
    """
    pass

class ForeignKeyField(KeyField):
    u"""
    <doc>The abstract <code>ForeignKeyField</code> class, defines the general behavior of foreign keys, where the value
    refers to another record or a selection of other records. All foreign keys answer <code>True</code> to the <code>
    self.isRelation()</code> call.<br/>
    Upon creation of the containing model, the foreign key field attributes <code>self.model</code> and <code>self.name
    </code> are supposed to be filled in order to create the right relational query.<br/>
    <br/>
    Upon definition of the relation field the target <attr>model</attr> and <attr>field</attr> need to be defined. If
    the model attribute is omitted, then it is assumed that the relation is to the current model and field name. The
    default for the <attr>field</attr> is <code>self.FIELD_ID</code>.<br/>
    <code>ForeignKeyField</code> instances (in thus the specific types of relations) are basically represented as bigint
    values (the relation is solved by the field, not by the database). It might be an option to allow database foreign
    keys too, in the future because they may be faster, but on the other hand they allow less intermediate control of
    chained relations.</doc>
    """
    def __init__(self, model=None, field="id", index=False, **args):
        Field.__init__(self, **args)
        self.tomodel = model
        self.tofield = field
        self.index = index

    def copy(self):
        u"""
        <doc>This <code>copy</code> executes the regular Field <code>copy</code> and adds in the extra attributes
        specific to this field type.</doc>
        """
        copy = KeyField.copy(self)
        copy.tomodel = self.getToModel()
        copy.tofield = self.getToField()
        copy.index = self.index

        return copy

    def getDefault(self):
        return None

    def isRecord(self):
        u"""
        <doc>The <code>isRecord</code> method answers the boolean flag if this field is answering a single <code>Record
        </code> instance. It is assumed that all standard relation at least answer a record, unless they answer a
        selection. The behavior is to answer <code>True</code>.</doc>
        """
        return True

    def getToModel(self, db=None):
        u"""
        <doc>The <code>getToModel</code> method answers the model name that where this relation refers to. If the <code>
        self.tomodel</code> is not defined, then take the <code>self.model</code> as defined by containing model. This
        happened for tree records, where the referenced model is equal.</doc>
        """
        if db:
            assert self.tomodel or self.model
        return self.tomodel or self.model

    def getToField(self, db=None):
        u"""
        <doc>The <code>getToField</code> method answers the model name where this relation refers to. If the <code>
        self.tomodel</code> is not defined, then take the <code>self.model</code> as defined by containing model. This
        happened for tree records, where the referenced model is equal.</doc>
        """
        return self.tofield

    def getFromModel(self, db=None):
        u"""
        <doc>The <code>getFromModel</code> method answers the <code>model</code> where this relation refers from. If the
        <code>self.model</code> is not defined, then raise an error.This happened for tree records, where the referenced
        model is equal.</doc>
        """
        if db:
            assert self.model
        return self.model

    def getFromField(self, db=None):
        u"""
        <doc> The <code>getFromField</code> method answers the <code>field</code> where this relation refers from. If
        the <code>self.name</code> is not defined, then raise an error. This happened for tree records, where the
        referenced model is equal.</doc>
        """
        assert self.name
        return self.name

class Many2OneField(ForeignKeyField):
    u"""
    <doc>Not really a field but a record ID. It refers to another table, which is loaded automatically. The value of
    the field will be of type Selection.</doc>
    """

    def getSqlType(self):
        return self.SQL_RELATIONTYPE

    def isMany2OneField(self):
        u"""
        <doc>The <code>isMany2OneField</code> method answers the boolean flag if this field is a many-to-one field. The
        method answers <code>True</code>.</doc>
        """
        return True

    def value2Sql(self, value, **args):
        u"""
        <doc>The <code>value2Sql</code> method answers the SQL value of the relation: the ID integer of the referred
        record. If no reference exists, then answer <code>self.SQL_NULL</code>.</doc>
        """
        return TX.asId(value) or self.SQL_NULL

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>The <code>sql2Value</code> method answers the <attr>sqlvalue</attr> attribute converted to the Python
        value. The <attr>id</attr> contains the id of the calling record, if it exists.</doc>
        """
        tomodel = self.getToModel(db)

        if not sqlvalue:
            sqlvalue = self.getDefault()

        if sqlvalue:
            record = db.getRecord(tomodel, id=sqlvalue)
            if record:
                return record
        return None #db.getNoneRecord(tomodel)

class Many2SelfField(Many2OneField):
    u"""
    <doc>The <code>Many2SelfField</code> field answers the <code>Record</code> instance of a relation to the <code>
    self.model</code> table.</doc>
    """
    def getToModel(self, db=None):
        u"""
        <doc>
        The <code>getToModel</code> method answers the (self) model name where this relation refers to. 
        </doc>
        """
        return self.model

    def getToField(self, db=None):
        u"""
        <doc>
        The <code>getToField</code> method answers the (self) field name where this relation refers to. 
        </doc>
        """
        return self.name

class ParentField(Many2SelfField):
    u"""
    <doc>
    The <code>ParentField</code> field is a virtual field that answers the <code>Record</code> parent relation. The
    difference with the inherited <code>Many2SelfField</code> class, is that we want to determine the main parent tree
    reference in a tree record structure.
    </doc>
    """
    def isParentField(self):
        u"""
        <doc>The <code>isParentField</code> method answers the boolean flag if this field is a parent field. The method
        answers <code>True</code>.</doc>
        """
        return True

    def getToField(self, db=None):
        u"""
        <doc>The <code>getToField</code> method answers the (self) field name where this relation refers to.</doc>
        """
        if db:
            return db.getModel(self._getToModel())._getParentFieldName()
        elif self.model:
            return self.model._getParentFieldName()
        else:
            return None


class One2ManyField(ForeignKeyField):
    u"""
    <doc>The <code>One2ManyField</code> field is a virtual field that answers a <code>Selection</code> of all records
    that relate to the current model record.</doc>
    """

    def __init__(self, where=None, order=None, slice=None, **args):
        ForeignKeyField.__init__(self, **args)
        self.where = where or 'TRUE'
        self.order = order or 'id'
        self.slice = slice or 1000

    def copy(self):
        u"""
        <doc>This <code>copy</code> executes the regular Field <code>copy</code> and adds in the extra attributes
        specific to this field type.
        </doc>
        """
        copy = ForeignKeyField.copy(self)
        copy.where = self.where
        copy.order = self.order
        copy.slice = self.slice

        return copy

    def isOne2ManyField(self):
        u"""
        <doc>The <code>isOne2ManyField</code> method answers the boolean flag if this field is a one-to-many field. The
        method answers <code>True</code>.</doc>
        """
        return True

    def isSelection(self):
        u"""
        <doc>The <code>isRecord</code> method answers the boolean flag if this field is answering a <code>Selection
        </code> instance. The behavior is to answer <code>True</code>.</doc>
        """
        return True

    def value2Sql(self, value, **args):
        u"""
        <doc>The <code>value2Sql</code> method always stores <code>NULL</code> in one-to-many fields. The field in the
        database is a placeholder, but does not need to occupy any space.</doc>
        """
        return self.SQL_NULL

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>The <code>sql2Value</code> method answers the <attr>sqlvalue</attr> attribute converted to the Python
        value. The result is an instance of <code>Selection</code>, depending on the where clause that is the result of
        <code>self.getWhere()</code>. Note that the answered <code>Selection</code> instance is selected by the optional
        <code>where</code>, ordered by the <code>self.order</code> and sliced by <code>self.slice</code>. The
        <attr>id</attr> contains the id of the calling record, if it exists.</doc>
        """
        from selection import Selection
        tomodel = self.getToModel(db)
        tofield = self.getToField(db)

        if not sqlvalue:
            sqlvalue = self.getDefault()

        where = '%s AND %s=%s' % (self.where, tofield, sqlvalue)
        return Selection(db, tomodel, where=where, start=0, slice=self.slice, order=self.order)

class Self2ManyField(One2ManyField):
    u"""
    <doc>The <code>Self2ManyField</code> field answers a <code>Selection</code> of all records in the same table table
    that relate to the current model record. To make sure that the own model and field is used, <code>self.tomodel
    </code> and <code>self.tofield</code> are always cleared.</doc>
    """
    def getToModel(self, db=None):
        u"""
        <doc>The <code>getToModel</code> method answers the model name that where this relation refers to.</doc>
        """
        return self.model

    def getToField(self, db=None):
        u"""
        <doc>The <code>getToField</code> method answers the field name that where this relation refers to.</doc>
        """
        if db:
            return db.getModel(self.model)._getParentFieldName()
        elif self.model:
            return self.model._getParentFieldName()
        else:
            return None

class ChildrenField(Self2ManyField):
    u"""
    <doc>
    The <code>ChildrenField</code> field is a virtual field that answers a <code>Selection</code> of all records in the
    same table that relate to the current model record. To make sure that the own model and field is used,
    <code>self.tomodel</code> and <code>self.tofield</code> are always cleared. 
    </doc>
    """
    def isChildrenField(self):
        u"""
        <doc>
        The <code>isChildrenField</code> method answers the boolean flag if this field is a children field. Only one
        children field can exist in a model. The method answers <code>True</code>.
        </doc>
        """
        return True

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <doc>
        The <code>sql2Value</code> method answers the <attr>sqlvalue</attr> attribute converted to the Python value. The
        result is an instance of <code>Selection</code>, depending on the parent id. Note that the answered
        <code>Selection</code> instance is not instantiated. This allows the calling application to extend the where
        clause and add more parameters such as order, start and slice. The <attr>id</attr> contains the id of the
        calling record, if it exists.
        </doc>
        """
        from selection import Selection
        tofield = self.getToField(db)
        if id:
            return Selection(db, self.getToModel(db), where='%s=%s AND %s' % (tofield, id, C.SQL_NOTDELETED))
        return db.getNoneSelection(tofield)

class Many2ManyField(One2ManyField):
    u"""
    <doc>
    The <code>Many2ManyField</code> holds a many-to-many relation, creating a <code>Selection</code> instance is both
    ways. The construction is that it assumes the existence of a <code>XRefModel</code> with fields <code>table</code>,
    <code>xref1_id</code> and <code>xref2_id</code> fields in an cross-reference record in the table.
    </doc>
    """
    def isMany2ManyField(self):
        u"""
        <doc>
        The <code>isMany2ManyField</code> method answers the boolean flag if this field is a many-to-many field,
        <code>True</code>.
        </doc>
        """
        return True

    def sql2Value(self, sqlvalue, id, db, **args):
        u"""
        <code>
        The <code>sql2Value</code> method answers an instance of <code>Selection</code> that is defined by the
        <code>One2ManyField</code> of the related X-ref record. 
        </code>
        """
        from selection import Selection
        frommodel = self.getFromModel(db)
        fromfield = self.getFromField(db)
        tomodel = self.getToModel(db) or frommodel
        tofield = self.getToField(db) or fromfield

        if id:
            fields = 't."' + '",t."'.join(db.getFieldNames(tomodel)) + '"'
            query = """
                SELECT {fields} FROM "{totable}" t
                INNER JOIN {xref} x on (t.id = x.{toid})
                WHERE x.{fromtablename}='{fromtable}' AND x.{fromfieldname}='{fromfield}' AND x.{fromid}={id} 
                AND x.{totablename}='{totable}' AND x.{tofieldname}='{tofield}'
                {deletedclause} 
                ORDER BY {order} 
                LIMIT {limit}
            """.format(**{
                'xref': C.TABLE_XREF,
                'fields': fields,
                'fromtablename': C.FIELD_XSRCTABLE, 'fromtable': frommodel,
                'fromfieldname': C.FIELD_XSRCFIELD, 'fromfield': fromfield,
                'fromid': C.FIELD_XREFSRCID, 'id': id,
                'toid': C.FIELD_XREFDSTID,
                'totablename': C.FIELD_XDSTTABLE, 'totable': tomodel,
                'tofieldname': C.FIELD_XDSTFIELD, 'tofield': tofield,
                'order': 'x.sortorder, t.{0}'.format(self.order) if db.getModel(C.TABLE_XREF)._hasField('sortorder') else 't.{0}'.format(self.order),
                'limit': self.slice,
                'deletedclause': db.tableHasField(tomodel,'deleted') and "AND t.deleted is not true" or "",
            })
            return Selection(db, tomodel, query=query)
        # Record is not initialized yet, so there is not id. No XRef can have been created.
        return db.getNoneSelection(tofield)


