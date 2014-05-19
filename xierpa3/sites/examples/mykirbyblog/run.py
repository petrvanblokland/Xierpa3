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
#    mykirbyblog.py
#
#    Example theme to build a kirby blog site.
#
from xierpa3.constants.constants import C
from xierpa3.themes.blog.blog import Blog
from xierpa3.adapters.kirby.kirbyadapter import KirbyAdapter
from xierpa3.builders.kirby.kirbybuilder import KirbyBuilder
from xierpa3.components import Page, Navigation

class MyKirbyBlog(Blog):
    u"""The <b>Blog</b> class implements the standard example blog."""
    TITLE = 'Blog Petr van Blokland + Claudia Mens'
    SUBTITLE = 'Notes on design and education.'

    def baseComponents(self):
        u"""Create a theme site with just one single template home page. Answer a list
        of page instances that are used as templates for this site.
        Note that the blog and page classes don't know anything about Kirby, or the
        kind of builder they will be processed by."""
        # Create an instance (=object) of the text component to be placed on the page.
        navigation = Navigation()
        # Create an instance (=object) of the page, containing the page components.
        homePage = Page(name=C.TEMPLATE_INDEX, components=(navigation,),
            title=self.TITLE)
        # Answer a list of types of pages for this site.
        return [homePage]
    
if __name__ == '__main__':
    # This adapter will be answering Kirby PHP snippets instead of fixed content.
    adapter = KirbyAdapter() 
    blog = MyKirbyBlog(adapter=adapter, )
    # Create the main blog builder, which will split into building the
    # CSS and PHP/HTML files, using the Kirby PHP snippets as content.
    builder = KirbyBuilder()
    # Make the Kirby source directly save to MAMP, so it is served by local server.
    builder.setRootPath('/Applications/MAMP/htdocs/')
    # Create the required directories for Kirby.
    # Build the CSS and and PHP/HTML files in the MAMP directory.
    builder.save(blog)
        

