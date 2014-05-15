# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#    theme.py
#
import os
from xierpa3.components.theme import Theme

class DemoBlog(Theme):

    def getStyle_Theme(self):
        s = Style('body', fontfamily='Georgia', fontsize='12px', backgroundcolor = '#606060')
        s.addStyle(tag='div', padding='4px', float='left', width='100%')
        s.addMedia(max=500, color='red', fontfamily='Verdana', fontsize='18px', fontweight='bold')
        return s
    
    def getComponents_Theme(self):
        # Header
        header = Header('Header', id='header', fontsize=48) 
        header.addMedia(max=500, color='white', fontsize=32)
        # Menu
        menu = Menu(Text('Menu ' * 10), backgroundcolor='white', width='100%')
        # Article
        article = Article(Text('Article ' * 100), backgroundcolor='orange', width='96%')
        article.addMedia(max=500, width='100%', fontsize=18)
        # Sidebar
        sidebar = Sidebar(Text('Sidebar ' * 100), float='left', backgroundcolor='yellow', width='33%')
        sidebar.addMedia(max=500, width='100%', backgroundcolor='blue', color='yellow')
        # Main = Article + Sidebar
        main = Group(components=(article, sidebar), width='100%', float='left')
        main.addMedia(max=800, backgroundcolor='#B0B0B0')
        # Footer
        footer = Footer(Text('Footer ' * 40), backgroundcolor='white', width='100%')
        # Pages = Header + Menu + Main + Footer
        pages = [Page((header, menu, main, footer), name='index', margin='4px')]
        return pages
    
if __name__ == "__main__":
    from xierpa3.builders.htmlbuilder import HtmlBuilder
    from xierpa3.builders.sassbuilder import SassBuilder
    from xierpa3.descriptors.style import Style
    from xierpa3.descriptors.environment import Environment
    from xierpa3.components import *
    path = '/Library/WebServer/Documents/xierpa3'
    # Build without style, still should build a complete working blog site.  
    t = SimpleBlog()
    hb = HtmlBuilder()
    t.build(hb)
    print hb.getResult()
    hb.save(path + '/index.html')
    
    sb = SassBuilder()
    t.build(sb)
    print sb.getResult()
    sb.save(path + '/style.scss')
    
    os.system('open "http://localhost/xierpa3/index.html"')
    os.system('open ' + path + '/index.html')
    os.system('open ' + path + '/style.scss')
    os.system('open ' + path + '/style.css')
