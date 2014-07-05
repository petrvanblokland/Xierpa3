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
#    socialmedia.py
#
from xierpa3.components.column import Column
from xierpa3.descriptors.media import Media
from xierpa3.descriptors.blueprint import BluePrint
from xierpa3.attributes import Perc

class SocialMedia(Column):

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Column.C 
   
    BLUEPRINT = BluePrint( 
        # layout
        colWidth=4,
        # Twitter
        # https://dev.twitter.com/docs/tweet-button
        twitterAccount=None, twitterLabel='Tweet',
        # FaceBook
        # https://developers.facebook.com/docs/plugins/share-button/
        facebookAccount=None,
        # Mobile
        mobileDisplay=C.NONE,
    )            
    def buildColumn(self, b):
        s = self.style
        if s.twitterAccount or s.facebookAccount:
            b.div(class_=self.C.CLASS_SOCIALMEDIA, display=self.C.BLOCK, float=s.float or self.C.LEFT,
                width=s.width or Perc(100),
                media=Media(max=self.C.M_MOBILE_MAX, display=s.mobileDisplay)
            )
            # getUrl does not seem to work with twitter. Script only tests http or https. 
            if s.twitterAccount:
                b.div(id="twitter", float=self.C.LEFT)
                b.a(href="https://twitter.com/share", data_href=b.getUrl(), 
                    class_="twitter-share-button", data_lang="en", data_via="doingbydesign", 
                    data_count="none", data_related="anywhere")
                b.text(s.twitterLabel)
                b._a()
                b.script()
                b.text("""!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');""")
                b._script()
                b._div()
            if s.facebookAccount:
                b.div(id="fb-root", float=self.C.LEFT)
                b._div()
                b.script()
                b.text("""(function(d, s, id) {
                  var js, fjs = d.getElementsByTagName(s)[0];
                  if (d.getElementById(id)) return;
                  js = d.createElement(s); js.id = id;
                  js.src = "//connect.facebook.net/en_US/all.js#xfbml=1";
                  fjs.parentNode.insertBefore(js, fjs);
                }(document, 'script', 'facebook-jssdk'));
                """)
                b._script()
                b.div(class_="fb-share-button", float=self.C.LEFT, 
                    data_href=b.getUrl(), data_type="button_count")
                b._div()
            b._div()
        
