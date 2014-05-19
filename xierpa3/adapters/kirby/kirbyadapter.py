# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
# 	xierpa server
# 	(c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#
# 	X I E R P A  3
# 	No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   kirbyadapter.py
#
from xierpa3.toolbox.storage.status.status import Data
from xierpa3.adapters.adapter import Adapter

class KirbyAdapter(Adapter):
    u"""
    Adapter for Kirby PHP
    """

    def __init__(self):
        pass
    
    def getPages(self, component, count): 
        return Data(items=[])

    def getSnippet(self, s1, s2=None):
        if s2 is None:
            return Data(text="<?php snippet('%s') ?>\n" % s1)
        return Data(text="<?php snippet('%s', %s) ?>\n" % (s1, s2))
        
    # ===============

    def getPageTitle(self, component, **kwargs):
        return Data(text='Untitled') # To be redefined by inheriting adapter class.
    
    def thisUrl(self):
        return Data(url="<?php echo thisURL() ?>")
    
    def chapters(self):  
        return Data(loop='Chapters')
    
    def featuredArticles(self):
        return Data(loop='Featured Kirby articles')
         
    def siteTitle(self):
        return Data(text="<?php echo h($site->title()) ?>")
    
    def pageTitle(self):
        return Data(text="<?php echo h($page->title()) ?>")
    
    def searchUrl(self):
        return Data(url="<?php echo html($pages->find('search')->url()) ?>")

    def previousLabel(self):
        return Data(text=self.leftArrow() + u' Previous')

    def ifPageHasPrev(self):
        return Data(text="<?php if($page->hasPrev()): ?>")
    
    def pagePrevUrl(self):
        return Data(url="<?php echo $page->prev()->url() ?>")
    
    def nextLabel(self):
        return Data(text=u'Next ' + self.rightArrow())
    
    def rightArrow(self):
        return Data(text=u"»")
    
    def leftArrow(self):
        return Data(text=u"«")
    
    def ifPageHasPrevAndNext(self):
        return Data(text="<?php if($page->hasPrev() && $page->hasNext()): ?>")
    
    def ifPageHasNext(self):
        return Data(text="<?php if($page->hasNext()): ?>")

    def pageNextUrl(self):
        return Data(text="<?php echo $page->next()->url() ?>")
    
    def pageUrl(self):
        return Data(url="<?php echo $page->url() ?>")
    
    def pagePublished(self):
        return Data(text="<?php echo html($page->published()) ?>")
    
    # Articles
    
    def ifArticlesHasPrev(self):
        return Data(text="<?php if($articles->pagination()->hasPrevPage()): ?>")
    
    def articlesPrevUrl(self):
        return Data(url="<?= $articles->pagination()->prevPageURL() ?>")
    
    def ifArticlesHasPrevAndNext(self):
        return Data(text="<?php if($articles->pagination()->hasPrevPage() && $articles->pagination()->hasNextPage()): ?>")
       
    def ifArticlesHasNext(self):
        return Data(text="<?php if($articles->pagination()->hasNextPage()): ?>")
    
    def articlesNextUrl(self):
        return Data(url="<?= $articles->pagination()->nextPageURL() ?>")
    
    def articlePublished(self):
        return Data(text="<?php echo html($article->published()) ?>")

    def kirbyText(self):
        return Data(text="<?php echo kirbytext($page->text()) ?>")
    
    def logoUrl(self):
        return Data(url="<?php echo url('assets/images/logo_petr.png') ?>")
    
    def tagsLabel(self):
        return Data(text="Tags: ")
    
    def forEachPageTag(self):
        return Data(text="<?php foreach(str::split($page->tags()) as $tag): ?>")
    
    def pageTags(self):
        return Data(loop="<?php echo url('articles/tag:' . urlencode($tag)) ?>")
    
    def htmlTag(self):
        return Data(text="<?php echo html($tag) ?>")
    
    def articles(self):
        return Data(text="""<?php if(param('tag')) {
            $articles = $pages->find('articles')
                ->children()
                ->visible()
                ->filterBy('tags', param('tag'), ',')
                ->flip()
                ->paginate(10);
            } else {
            $articles = $pages->find('articles')
                ->children()
                ->visible()
                ->flip()
                ->paginate(10);
            } ?>
            """)
    
    def articleTagUrl(self):
        return Data(url="<?php echo url('articles/tag:' . urlencode($tag)) ?>")
           
    def forEachArticle(self):
        return Data(loop="<?php foreach($articles as $article): ?>")

    def _forEach(self):
        return Data(text="<?php endforeach ?>")
    
    def ifPaginationHasPages(self):
        return Data(text="<?php if($articles->pagination()->hasPages()): ?>")
    
    def _if(self):
        return Data(text="<?php endif ?>")
    
    def feed(self):
        return Data(text="""<?php       
            // get any list of items    
            // in this case we get all visible children of the blog section, 
            // flip them to get them in reverse order and make sure we only get the last 10
            $items = $pages->find('articles')->children()->visible()->flip()->limit(10);
            // this is how you embed the feed snippet with some options    
            snippet('feed', array(
              'link'  => url('articles'),
              'items' => $items,
              'descriptionField'  => 'text', 
              'descriptionLength' => 300
            ));
        ?>""")
        
    def articleUrl(self):
        return Data(url="<?php echo $article->url() ?>")
    
    def articleTitle(self):
        return Data(text="<?php echo html($article->title()) ?>")
    
    def excerptArticle(self, length):
        return Data(text="<?php echo excerpt($article->text(), %d) ?>" % length)
    
    def search(self):
        return Data(loop="""<?php
            $search = new search(array(
              'searchfield' => 'q',
              'words' => true,
              'in' => 'articles',
              'paginate'    => 10
            ));     
            $results = $search->results();
            $blog = $pages->find('articles');
            $tags = tagcloud($blog);
        ?>""")

    def ifResults(self):
        return Data(text="<?php if($results): ?>")
    
    def forEachResult(self):
        return Data(text="<?php foreach($results as $result): ?>")
    
    def resultUrl(self):
        return Data(url="<?php echo $result->url() ?>")
    
    def resultTitle(self):
        return Data(text="<?php echo $result->title() ?>")
    
    def resultDescription(self):
        return Data(text="<?php echo $result->description() ?>")
    
    def resultText(self, count):
        return Data(text="<?php echo excerpt($result->text(), %d) ?>" % count)
    
    def readMoreLabel(self):
        return Data(text=u"Read more.")
    
    def elseIfSearchQuery(self):
        return Data(text="<?php elseif($search->query()): ?>")
    
    def htmlSearchQuery(self):
        return Data(text="<?php echo html($search->query()) ?>")
    
    def forEachTag(self):
        return Data(text="<?php foreach($tags as $tag): ?>")
    
    def tagUrl(self):
        return Data(url="<?php echo $tag->url() ?>")
    
    def tagName(self):
        return Data(text="<?php echo $tag->name() ?>")
    
    