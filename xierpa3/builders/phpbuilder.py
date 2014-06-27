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
#   phpbuilder.py
#
#   Following standard
#   https://google-styleguide.googlecode.com/svn/trunk/htmlcssguide.xml
#
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.constants.constants import C

class PhpBuilder(HtmlBuilder):
    u"""
    The <b>PhpBuilder checks if the there is already a PHP frame work at the target
    directory of the site, otherwise the default framework is copied there. 
    Then the multiple result streams are saved at the destination in the framework.
    """
    ID = C.TYPE_PHP # Also the default extension of the output format.
    EXTENSION = ID
    ATTR_POSTFIX = ID # Postfix of dispatcher and attribute names above generic names.

    def page(self, component):
        u"""Put the result of <b>self.page()</b> by the parent class HtmlBuilder
        in a separate result stream, that can be save into header.php.
        This method assumes that the parent method builds _div+_body+_html,
        to fit the standard footer.php file structure."""
        self.pushResult()
        HtmlBuilder.page(self, component)
        self.phpHeader = self.popResult()
        pass
    
    def _page(self, component):
        u"""Put the result of <b>self._page()</b> by the parent class HtmlBuilder
        in a separate result stream, that can be saved into footer.php.
        This method assumes that the parent method builds html+head+_head+body+div,
        to fit the standard header.php file structure."""
        self.pushResult()
        HtmlBuilder._page(self, component)
        self.phpFooter = self.popResult()
        pass
                   
    def save(self, component, root=None, path=None, extension=None):
        u"""Save the result streams in the PHP framework. in path."""
        # Write the templates
        rootPath = root + 'app/templates/default/' # Extend the path to save the template files.
        if path is None: # Allow full overwrite of path
            path = self.getFilePath(component, rootPath)
        dirPath = self.makeDirectory(path) # Make sure that the directory part of path exists.
        # Write header and footer
        for fileName, content in (('header.php', self.phpHeader), ('footer.php', self.phpFooter)):
            filePath = rootPath + fileName
            f = open(filePath, 'wb')
            f.write(content)
            f.close()
        # Save the main template files.
        for template in component.getTemplates():
            filePath = dirPath + '/' + template.name + '.' + (extension or self.EXTENSION) # .html or .php
            template.build(self)
            f = open(filePath, 'wb')
            f.write(self.getResult())
            f.close()
        return path

