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
#     defaultmodels.py
#
from fields import *
from models import Model, TreeModel, DateTimeModel, NamedModel

class Item(TreeModel):
    u"""
    <doc>The <code>Item</code>model supports the unique kind of information in a publication such and texts, images,
    downloads, etc. Every piece of information in a publication that can be published on multiple positions, needs to be
    the instance of <code>Item</code>. In order to create a hierarchical tree of items, the class inherits from <code>
    TreeModel</code>, that implements a <code>self.FIELD_PARENTID</code> field.</doc>
    """
    # Specific text item fields
    xmlen = TextField()  # Just one language as example for now
    srcen = TextField()  # Plain source saved from the WYSIWYG editor
                                                            # to avoid distortion from translating in two directions
    # Specific image item field in case
    type = TypeField()  # One single integer id to define the type of this item
    isimage = BooleanField()  # Flag if this record is an image
    url = UrlField()  # Holds the URL if there is an external image reference.
    movieurl = UrlField()  # Optional URL reference to related movie.
    srcpath = PathField()  # Source path of the original image on client system
    filepath = PathField()  # Filepath of the image file that item refers to
    extension = TextField()
    binary = BinaryField()  # Binary field, in case storage is done in database.
    width = IntegerField()  # Size of the image or page
    height = IntegerField()
    status = StatusField()  # Holding arbitrary status information for the application

class Address(TreeModel):
    """
    CREATE TABLE address (
    creationdatetime timestamp without time zone,
    creationuser_id bigint,
    id serial,
    modificationdatetime timestamp without time zone,
    modificationuser_id bigint,
    roles text,
    preferences text,
    email text,
    login text,
    firstname text,
    middlename text,
    familyname text,
    lastlogin timestamp without time zone,
    );
    """
    firstname = UnicodeField(index=True)
    middlename = UnicodeField(index=True)
    familyname = UnicodeField(index=True)
    login = TextField(index=True, unique=True)
    email = EmailField(index=True, unique=True)
    password = PasswordField()
    preferences = PreferenceField()
    roles = SelectionField()
    lastlogin = DateTimeField()

class Cache(DateTimeModel):

    url = UrlField(index=True)
    s3path = TextField()  # If the cached page content it too large to hold in a text field, store it here.
    xhtml = TextField()

class Log(Model):

    user_id = Many2OneField(Constants.TABLE_ADDRESS)
    name = TextField()
    description = TextField()
    value = IntegerField()

    # ---------------------------------------------------------------------------------------------------------
    #     C O M P O S I N G

class Hyphenation(NamedModel):
    u"""
    <doc>The <code>Hyphenation</code> class is used by the <code>Hyphenator</code> class to hyphenate words in defined
    languages.</doc>
    """
    # record.name is used for the word
    hyphenated = TextField()
    language = CharField(size=4, index=True)

class Design(NamedModel):
    u"""
    <doc>The <code>Design</code> class is used to store the entire design in a single record, using the <code>PickledField
    </code>.</doc>
    """
    design = PickledField()
    deleted = BooleanField(default=False)
    isprotected = BooleanField(default=False)
    usage = SelectionField()  # Checkbox options how this design should be used, medium, etc.

    # ---------------------------------------------------------------------------------------------------------
    #     A S S O C I A T I O N  M O D E L S

class XRef(Model):
    u"""
    <doc>The <code>XRef</code> model is used by the <code>Many2ManyField</code> to defined the counted cross reference
    between the source and destination table. Since the model is used as generic approach for references of all tables,
    the names of the related tables and fields are stored in the record.</doc>
    """
    xsrctable = IdentifierField()  # Src table name of the cross reference.
    xsrcfield = IdentifierField()  # Src field name of the cross reference.
    xrefsrc_id = ForeignKeyField(index=True)  # Src reference id, to variable table name

    xdsttable = IdentifierField()  # Destination table name of the cross reference.
    xdstfield = IdentifierField()  # Destination field name of the cross reference.
    xrefdst_id = ForeignKeyField(index=True)  # Destination reference id, to variable table name

class Association(XRef):
    u"""
    <doc>The <code>Association</code> model is used by the <code>AssociationField</code> to defined the counted cross
    reference between two tables and fields. Since the model is used as generic approach for references of all tables,
    the names of the related table and field are stored in the record.</doc>
    """
    count = LongField()  # Association count from source to destination.


MODELS = {
    Constants.TABLE_ITEM:            Item(),
    Constants.TABLE_ADDRESS:        Address(),
    Constants.TABLE_CACHE:            Cache(),
    Constants.TABLE_LOG:            Log(),
    Constants.TABLE_DESIGN:            Design(),
    Constants.TABLE_XREF:            XRef(),
    Constants.TABLE_ASSOCIATION:    Association(),
}
