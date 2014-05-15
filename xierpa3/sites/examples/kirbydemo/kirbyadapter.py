# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     xierpa server
#     Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#
#     X I E R P A  3
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   kirbyadapter.py
#
from xierpa3.constants.constants import C
from xierpa3.toolbox.transformer import TX
from xierpa3.adapters.adapter import Adapter

class KirbyAdapter(Adapter):
    u"""
    Adapter for Kirby PHP
    """

    def __init__(self):
        pass

    def thisUrl(self):
        return "<?php echo thisURL() ?>"
    
    def snippet(self, component, s1, s2=None):
        if s2 is None:
            return "<?php snippet('%s') ?>\n" % s1
        return "<?php snippet('%s', %s) ?>\n" % (s1, s2)
        
    def siteTitle(self):
        return "<?php echo h($site->title()) ?>"
    
    def pageTitle(self):
        return "<?php echo h($page->title()) ?>"
    
    def searchUrl(self):
        return "<?php echo html($pages->find('search')->url()) ?>"

    def previousLabel(self):
        return self.leftArrow() + u' Previous'
    
    def ifPageHasPrev(self):
        return "<?php if($page->hasPrev()): ?>"
    
    def pagePrevUrl(self):
        return "<?php echo $page->prev()->url() ?>"
    
    def nextLabel(self):
        return u'Next ' + self.rightArrow()
    
    def rightArrow(self):
        return u"»"
    
    def leftArrow(self):
        return u"«"
    
    def ifPageHasPrevAndNext(self):
        return "<?php if($page->hasPrev() && $page->hasNext()): ?>"
    
    def ifPageHasNext(self):
        return "<?php if($page->hasNext()): ?>"

    def pageNextUrl(self):
        return "<?php echo $page->next()->url() ?>"
    
    def pageUrl(self):
        return "<?php echo $page->url() ?>"
    
    def pagePublished(self):
        return "<?php echo html($page->published()) ?>"
    
    # Articles
    
    def ifArticlesHasPrev(self):
        return "<?php if($articles->pagination()->hasPrevPage()): ?>"
    
    def articlesPrevUrl(self):
        return "<?= $articles->pagination()->prevPageURL() ?>"
    
    def ifArticlesHasPrevAndNext(self):
        return "<?php if($articles->pagination()->hasPrevPage() && $articles->pagination()->hasNextPage()): ?>"
       
    def ifArticlesHasNext(self):
        return "<?php if($articles->pagination()->hasNextPage()): ?>" 
    
    def articlesNextUrl(self):
        return "<?= $articles->pagination()->nextPageURL() ?>"
    
    def articlePublished(self):
        return "<?php echo html($article->published()) ?>"

    def kirbyText(self):
        return "<?php echo kirbytext($page->text()) ?>"
    
    def logoUrl(self):
        return "<?php echo url('assets/images/logo_petr.png') ?>"
    
    def tagsLabel(self):
        return "Tags: "
    
    def forEachPageTag(self):
        return "<?php foreach(str::split($page->tags()) as $tag): ?>"
    
    def pageTags(self):
        return "<?php echo url('articles/tag:' . urlencode($tag)) ?>"
    
    def htmlTag(self):
        return "<?php echo html($tag) ?>"
    
    def articles(self):
        return """<?php if(param('tag')) {
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
            """
    
    def articleTagUrl(self):
        return "<?php echo url('articles/tag:' . urlencode($tag)) ?>"
           
    def forEachArticle(self):
        return "<?php foreach($articles as $article): ?>"
    
    def _forEach(self):
        return "<?php endforeach ?>"
    
    def ifPaginationHasPages(self):
        return "<?php if($articles->pagination()->hasPages()): ?>"
    
    def _if(self):
        return "<?php endif ?>"
    
    def feed(self):
        return """<?php       
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
        ?>"""
        
    def articleUrl(self):
        return "<?php echo $article->url() ?>"
    
    def articleTitle(self):
        return "<?php echo html($article->title()) ?>"
    
    def excerptArticle(self, length):
        return "<?php echo excerpt($article->text(), %d) ?>" % length
    
    def search(self):
        return """<?php
            $search = new search(array(
              'searchfield' => 'q',
              'words' => true,
              'in' => 'articles',
              'paginate'    => 10
            ));     
            $results = $search->results();
            $blog = $pages->find('articles');
            $tags = tagcloud($blog);
        ?>"""

    def ifResults(self):
        return "<?php if($results): ?>"
    
    def forEachResult(self):
        return "<?php foreach($results as $result): ?>"
    
    def resultUrl(self):
        return "<?php echo $result->url() ?>"
    
    def resultTitle(self):
        return "<?php echo $result->title() ?>"
    
    def resultDescription(self):
        return "<?php echo $result->description() ?>"
    
    def resultText(self, count):
        return "<?php echo excerpt($result->text(), %d) ?>" % count
    
    def readMoreLabel(self):
        return u"Read more."
    
    def elseIfSearchQuery(self):
        return "<?php elseif($search->query()): ?>"
    
    def htmlSearchQuery(self):
        return "<?php echo html($search->query()) ?>"
    
    def forEachTag(self):
        return "<?php foreach($tags as $tag): ?>"
    
    def tagUrl(self):
        return "<?php echo $tag->url() ?>"
    
    def tagName(self):
        return "<?php echo $tag->name() ?>"
    