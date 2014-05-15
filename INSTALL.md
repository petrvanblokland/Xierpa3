+ -*- coding: UTF-8 -*-
+ -----------------------------------------------------------------------------
+    xierpa server
+    Copyright(c) 2014+ buro@petr.com, www.petr.com, www.xierpa.com
+   
+    X I E R P A  3
+    Distribution by the MIT License.
+
+ -----------------------------------------------------------------------------

Dependencies
Make sure that Python 2.7 is installed, otherwise install from http://python.org
Install Twisted Matrix server from https://twistedmatrix.com/trac/
Install element tree "lxml" from http://lxml.de/index.html
Install "sass" from http://sass-lang.com
Install "boto" from https://aws.amazon.com/sdkforpython/

Optional dependencies
Install "cjson" from http://sourceforge.net/projects/cjson/
Make sure "cStringIO" is installed, see http://pydoc.org/2.4.1/cStringIO.html
Make sure "cPickle" is installed, see http://pymotw.com/2/pickle 

Installation
Add xierpa3.pth to Python site-packages, referring to this git Xierpa3 install
Copy xierpa3/constants/config/COPYTO-config.py to xierpa3/constants/config.config.py and adjust
the parameters and access keys to your own settings. Make sure this config.py never writes back
into git (future development is to store this file in your local user folder).

Databases
A variety of database connections is possible: local and online SQL databases,
Amazon database services and S3. The access codes and IP/URL's need to be filled
into the config.py or defined locally in the site application.

+ -----------------------------------------------------------------------------
