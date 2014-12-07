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
#   phpadapter.py
#
from xierpa3.toolbox.storage.article import Article
from xierpa3.adapters.adapter import Adapter

class PhpAdapter(Adapter):
    u"""
    Adapter for PHP output.

    TODO: Make matching with http://simplemvcframework.com/documentation/v2/install
    """

    def __init__(self):
        pass

    def getPages(self, count):
        return self.newArticle(chapters=[])

    def getSnippet(self, s1, s2=None):
        if s2 is None:
            return self.newArticle(text="<?php snippet('%s') ?>\n" % s1)
        return self.newArticle(text="<?php snippet('%s', %s) ?>\n" % (s1, s2))

    # ===============

    def getPageTitle(self, **kwargs):
        return self.newArticle(text='<?php echo "PHP generated title" ?>')
        #return self.newArticle(text='<?php echo h($site->title()) ?> : %s' % (kwargs.get('title', 'Untitled')))  # To be redefined by inheriting adapter class.

    def thisUrl(self):
        return self.newArticle(url="<?php echo thisURL() ?>")

    def chapters(self):
        return self.newArticle(loop='Chapters')

    def featuredArticles(self):
        return self.newArticle(loop='Featured Kirby articles')

    def siteTitle(self):
        return self.newArticle(text="<?php echo h($site->title()) ?>")

    def pageTitle(self):
        return self.newArticle(text="<?php echo h($page->title()) ?>")

    def searchUrl(self):
        return self.newArticle(url="<?php echo html($pages->find('search')->url()) ?>")

    def previousLabel(self):
        return self.newArticle(text=self.leftArrow() + u' Previous')

    def ifPageHasPrev(self):
        return self.newArticle(text="<?php if($page->hasPrev()): ?>")

    def pagePrevUrl(self):
        return self.newArticle(url="<?php echo $page->prev()->url() ?>")

    def nextLabel(self):
        return self.newArticle(text=u'Next ' + self.rightArrow())

    def rightArrow(self):
        return self.newArticle(text=u"»")

    def leftArrow(self):
        return self.newArticle(text=u"«")

    def ifPageHasPrevAndNext(self):
        return self.newArticle(text="<?php if($page->hasPrev() && $page->hasNext()): ?>")

    def ifPageHasNext(self):
        return self.newArticle(text="<?php if($page->hasNext()): ?>")

    def pageNextUrl(self):
        return self.newArticle(text="<?php echo $page->next()->url() ?>")

    def pageUrl(self):
        return self.newArticle(url="<?php echo $page->url() ?>")

    def pagePublished(self):
        return self.newArticle(text="<?php echo html($page->published()) ?>")

    # Articles

    def ifArticlesHasPrev(self):
        return self.newArticle(text="<?php if($articles->pagination()->hasPrevPage()): ?>")

    def articlesPrevUrl(self):
        return self.newArticle(url="<?= $articles->pagination()->prevPageURL() ?>")

    def ifArticlesHasPrevAndNext(self):
        return self.newArticle(text="<?php if($articles->pagination()->hasPrevPage() && $articles->pagination()->hasNextPage()): ?>")

    def ifArticlesHasNext(self):
        return self.newArticle(text="<?php if($articles->pagination()->hasNextPage()): ?>")

    def articlesNextUrl(self):
        return self.newArticle(url="<?= $articles->pagination()->nextPageURL() ?>")

    def articlePublished(self):
        return self.newArticle(text="<?php echo html($article->published()) ?>")

    def kirbyText(self):
        return self.newArticle(text="<?php echo kirbytext($page->text()) ?>")

    def logoUrl(self):
        return self.newArticle(url="<?php echo url('assets/images/logo_petr.png') ?>")

    def tagsLabel(self):
        return self.newArticle(text="Tags: ")

    def forEachPageTag(self):
        return self.newArticle(text="<?php foreach(str::split($page->tags()) as $tag): ?>")

    def pageTags(self):
        return self.newArticle(loop="<?php echo url('articles/tag:' . urlencode($tag)) ?>")

    def htmlTag(self):
        return self.newArticle(text="<?php echo html($tag) ?>")

    def articles(self):
        return self.newArticle(text="""<?php if(param('tag')) {
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
        return self.newArticle(url="<?php echo url('articles/tag:' . urlencode($tag)) ?>")

    def forEachArticle(self):
        return self.newArticle(loop="<?php foreach($articles as $article): ?>")

    def _forEach(self):
        return self.newArticle(text="<?php endforeach ?>")

    def ifPaginationHasPages(self):
        return self.newArticle(text="<?php if($articles->pagination()->hasPages()): ?>")

    def _if(self):
        return self.newArticle(text="<?php endif ?>")

    def feed(self):
        return self.newArticle(text="""<?php
            // get any list of chapters
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
        return self.newArticle(url="<?php echo $article->url() ?>")

    def articleTitle(self):
        return self.newArticle(text="<?php echo html($article->title()) ?>")

    def excerptArticle(self, length):
        return self.newArticle(text="<?php echo excerpt($article->text(), %d) ?>" % length)

    def search(self):
        return self.newArticle(loop="""<?php
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
        return self.newArticle(text="<?php if($results): ?>")

    def forEachResult(self):
        return self.newArticle(text="<?php foreach($results as $result): ?>")

    def resultUrl(self):
        return self.newArticle(url="<?php echo $result->url() ?>")

    def resultTitle(self):
        return self.newArticle(text="<?php echo $result->title() ?>")

    def resultDescription(self):
        return self.newArticle(text="<?php echo $result->description() ?>")

    def resultText(self, count):
        return self.newArticle(text="<?php echo excerpt($result->text(), %d) ?>" % count)

    def readMoreLabel(self):
        return self.newArticle(text=u"Read more.")

    def elseIfSearchQuery(self):
        return self.newArticle(text="<?php elseif($search->query()): ?>")

    def htmlSearchQuery(self):
        return self.newArticle(text="<?php echo html($search->query()) ?>")

    def forEachTag(self):
        return self.newArticle(text="<?php foreach($tags as $tag): ?>")

    def tagUrl(self):
        return self.newArticle(url="<?php echo $tag->url() ?>")

    def tagName(self):
        return self.newArticle(text="<?php echo $tag->name() ?>")

