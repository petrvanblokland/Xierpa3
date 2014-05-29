from xierpa3.attributes import Perc
from xierpa3.components import Theme, Page, Container, Text
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder
from xierpa3.descriptors.blueprint import BluePrint
        
class SimpleWebSite(Theme):
    TITLE = u'The Simple Website Example Page' # Use as title of window.

    CLASS_MAINCOLUMN = 'mainColumn'
    
    CC = Theme
    BLUEPRINT = BluePrint(
        mainWidth=Perc(75),
        mainBackgroundColor='yellow', 
    )
    def baseComponents(self):
        s = self.style
        mainContent = Container(class_=self.CLASS_MAINCOLUMN, components=(Text('main content'),), 
            width=s.mainWidth, backgroundcolor=s.mainBackgroundColor, float=self.LEFT)
        homePage = Page(class_='index', name=self.TEMPLATE_INDEX, 
            title=self.TITLE,
            components=(mainContent,),
            css=self.URL_CSS)
        return [homePage]
    
    def make(self):
        cssBuilder = CssBuilder()
        cssBuilder.save(self) 
        htmlBuilder = HtmlBuilder()
        return htmlBuilder.save(self)  
    
