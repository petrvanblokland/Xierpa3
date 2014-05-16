## Installing Xierpa

Various possibilities are available to install Python packages Xierpa depends on, as well as third-party applications. On OSX, you can either get the Python dependencies through easy_install, pip, or directly from the Python package index. Make sure that packages that have C/C++ bindings are compiled with the same version of GCC as the version of Python you're using. It is also possible to pull most of the Python dependencies from MacPorts or Homebrew. On Linux, most packages are available from package managers such as apt-get / aptitude or yum.

### Installation

 * Add xierpa3.pth to Python site-packages, referring to the folder where Xierpa3 has been cloned from git. For example, the site-packages for a prepackaged Python on a recent OSX machine can be found here: /Library/Python/2.7/site-packages.
 * Copy xierpa3/constants/config/COPYTO-config.py to xierpa3/constants/config.config.py and adjust the parameters and access keys to your own settings. Make sure this config.py never writes back into git (future development is to store this file in your local user folder).

### Dependencies

 * Make sure that Python 2.7 is installed, otherwise get it from http://python.org. Recent versions of OSX and Linux come with a completely installed Python environment.
 * Install the Twisted Matrix server, https://twistedmatrix.com/trac/ or https://pypi.python.org/pypi/Twisted
 * Install element tree "lxml", http://lxml.de/index.html or https://pypi.python.org/pypi/lxml/, which needs the libxml2 and libxslt binaries.
 * Install "sass" from http://sass-lang.com. For this you first need to install Ruby and then get the sass gem like this:
   * sudo gem install sass
 * Install "boto" from https://aws.amazon.com/sdkforpython/ or https://pypi.python.org/pypi/boto

### Optional Dependencies

 * Install "cjson" from http://sourceforge.net/projects/cjson/ or https://pypi.python.org/pypi/python-cjson for (much) faster JSON parsing.
   * Make sure "cStringIO" is installed, see http://pydoc.org/2.4.1/cStringIO.html
   * Make sure "cPickle" is installed, see http://pymotw.com/2/pickle

### Databases

A variety of database connections is possible: local and online SQL databases, Amazon database services and S3. The access codes and IP/URL's need to be filled into the config.py or defined locally in the site application.

-----------------------------------------------------------------------------
