# coding=utf-8

from django.conf.urls.defaults import *
from feeds import LatestEntriesFeed

urlpatterns = patterns('blog.views',

    url(r'^$', 'home',name='home'),
    url(r'^contact/$', 'contact',name='contact'),
    url(r'^staff/$', 'staff',name='staff'),
    url(r'^!/(?P<user>\w+)/$', 'author',name='author'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)/$', 'archive',name='archive'),
    url(r'^feed/$', LatestEntriesFeed(),name='feed'),
    url(r'^(?P<slug>[\w-]+)/$', 'common',name="common"),
    url(r'^(?P<section>[\w-]+)/(?P<subsection>[\w-]+)/$', 'section_subsection',name="section_subsection"),
    #url(r'(?P<section>[\w-]+)/(?P<subsection>[\w-]+)/(?P<entry>[\w-]+)/', 'entry',name="entry"),
    
    
)
