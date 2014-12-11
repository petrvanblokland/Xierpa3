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
#    googletranslate.py
#
#   U N D E R  C O N S T R U C T I O N
#
from xierpa3.components import Column

class GoogleTranslate(Column):
    u"""
    The @GoogleTranslate@ is an abstract class that implements the language behavior of the application.
    """
    # ---------------------------------------------------------------------------------------------------------
    # 	L A N G U A G E S

    def initializeLanguage(self):
        u"""
        The @initializeLanguage@ method initializes @self.language@. The default behavior
        is to set it to the content of session value @self.SESSION_LANGUAGE@ or @self.LANGUAGE_DEFAULT@.
        To be redefined by the inheriting application class otherwise.
        """
        self.language = self.getSessionValue(self.SESSION_LANGUAGE) or self.LANGUAGE_DEFAULT

    def getLanguages(self):
        u"""
        The @getLanguages@ method answers a list with supported languages of the application. The default
        behavior is to answer @self.APP_LANGUAGES@.
        """
        return self.APP_LANGUAGES

    def buildJS(self, b):
        u"""
        The @buildJS@ method adds the Google translate javascript, if @USE_GOOGLETRANSLATE@ is @True@.
        Add @&lt;div id="self.TARGETID_GOOGLETRANSLATE"&gt;...&lt;/div&gt;@ to the page to implement the position
        of the language popup. See also "google translate":translate.google.com/translate_tools.
        """
        for component in self.components:
            component.buildJS(b) # Allow child components to export their Javascript.
        #
        if self.isGoogleTranslate():
            self.script()
            self.text("""
            function googleTranslateElementInit() {
                new google.translate.TranslateElement({
                pageLanguage: '%s'
              }, '%s');
            }""" % (self.getdefaultlanguage(), self.TARGETID_GOOGLETRANSLATE))
            self._script()
            self.script(src='http://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit')

    def buildBlock(self, b):
        u"""
        The @buildGoogleLanguageChoice@ method builds the container that will be filled by
        the google translator with the language choice popup. The optional class attribute <attr>class_</attr>
        defines the style of the enclosing div tag. The default value is @self.CLASS_GOOGLETRANSLATE@.
        """
        self.div(class_=self.CLASS_GOOGLETRANSLATE)
        self.div(id=self.TARGETID_GOOGLETRANSLATE)
        self._div()
        if self.e.form[self.PARAM_GOOGLETRANSLATE]:
            self.textLabel(self.LABEL_GOOGLETRANSLATECAPTION)
        self._div()

    def isGoogleTranslate(self, b):
        u"""
        The @isGoogleTranslate@ method answers the boolean flag if the page is in google translate mode, depending
        on the @self.getSessionValue(self.PARAM_GOOGLETRANSLATE)@.
        """
        s = self.style
        return s.useGoogleTranslate and 'translate' in b.e.form.keys()

