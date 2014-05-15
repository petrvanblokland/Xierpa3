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
#    configmodel.py
#
#    The config.py defines the local settings for each server. Use configmodel.py as template to see the possible
#    parameters and create a local version of config.py.
#
import sys

class BaseConfig(object):
    u"""
    The abstract <b>ConfigModel</b> class implements the default values for the abstract <b>Config</b>
    class in <i>config.py</i> that defines all hardware specific class variables.
    """
    XIERPA_VERSION = '0.8' # Overall version of this Xierpa3

    PORT = 80
    DEBUG = False
    USE_ONLINE = True
    USE_LOCAL = not USE_ONLINE
    USE_FONTFACE = True and USE_ONLINE
    USE_MULTIPROCESSING = False and sys.version_info >= (2, 7)
 
    CONNECTION = 'fast'

    # ---------------------------------------------------------------------------------------------------------
    #    P Y T H O N
          
    PYTHONAPP = 'python2.7'

    # ---------------------------------------------------------------------------------------------------------
    #    S 3

    USE_S3 = True
    USE_LOCALS3 = (True and USE_S3) or not USE_ONLINE

    ACCESSKEYID = '' # Add your Amazon S3 access key here.
    SECRETACCESSKEY = '' # Add your Amazon S3 secret access key here.
    
    # ---------------------------------------------------------------------------------------------------------
    #    A M A Z O N  D Y N A M O  D B

    AMAZON_REGION = "us-east-1"
    AMAZON_HOST = "dynamodb.{0}.amazonaws.com".format(AMAZON_REGION)
    CONTENT_TYPE = "application/x-amz-json-1.0"
    DYNAMODB_URI = "/"
    DYNAMODB_TARGET = "" # To be defined by user account in config.py
    DYNAMODB_SIGNING_ALGORITHM = ""  # To be defined by user account in config.py

    # ---------------------------------------------------------------------------------------------------------
    #    D A T A B A S E

    DATABASEENGINE_PSYCOPG2 = 'postgresql_psycopg2'
    DATABASEENGINE_PYGRESQL = 'pygresql'
    DATABASEENGINE_AWS = 'amazon_web_services'

    DATABASETYPE_POSTGRES = 'postgresql'
    DATABASETYPE_SDB = 'SimpleDB'
    DATABASETYPE_DEFAULT = DATABASETYPE_POSTGRES

    DATABASE_NAME = None # Name of the database, redefined by the local application.
    DATABASE_ENGINE = '' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_HOST = '' # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '' # Set to empty string for default. Not used with sqlite3.
    DATABASE_USER = '' # Set to empty string for default. Not used with sqlite3.
    DATABASE_PASSWORD = '' # Set to empty string for default. Not used with sqlite3.
    DATABASE_OPTIONS = {} # Set to empty dictionary for default.
    DATABASE_TYPE = DATABASETYPE_DEFAULT # Define database type here.

    # ---------------------------------------------------------------------------------------------------------
    #    F O N T S

    DEFAULT_IMAGEFONT = None

    FONT_ROOTPATHS = ('/Library/Fonts',     # Default fonts path on OSX
        )
