# coding=utf-8

from django.conf.urls.defaults import *
from feeds import LatestEntriesFeed

urlpatterns = patterns('blog.views',

    url(r'^$', 'home',name='home'),
    url(r'^numero-(?P<number>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', 'number',name='number'),
    url(r'^contact/$', 'contact',name='contact'),
    #url(r'^search/$', 'search',name='search'),
    url(r'^staff/$', 'staff',name='staff'),
    url(r'^info/$', 'info',name='info'),
    url(r'^sitios/$', 'authors',name='authors'),
    url(r'^sitios/(?P<user>[\w\._-]+)/$', 'author',name='author'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)/$', 'archive',name='archive'),
    url(r'^feed/$', LatestEntriesFeed(),name='feed'),
    url(r'^numero-(?P<number>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<subsection>[\w-]+)/$', 'subsection',name="subsection"),
    url(r'^numero-(?P<number>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<subsection>[\w-]+)/(?P<slug>[\w-]+)/$', 'entry',name="entry"),
    url(r'^(?P<slug>[\w-]+)/$', 'subsection',name="subsection"),
    url(r'^(?P<slug>[\w-]+)/$', 'common',name="common"),
    url(r'^(?P<subsection>[\w-]+)/(?P<tag>[\w-]+)/$', 'subsection_tag',name="subsection_tag"),
    #url(r'(?P<section>[\w-]+)/(?P<subsection>[\w-]+)/(?P<entry>[\w-]+)/', 'entry',name="entry"),
    
    
)
