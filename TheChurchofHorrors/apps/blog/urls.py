# coding=utf-8

from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',

    url(r'^$', 'home'),
    url(r'^contact/$', 'contact'),
    url(r'^staff/$', 'staff'),
    url(r'^author/(?P<user>\w+)/$', 'author'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)/$', 'archive'),
    url(r'(?P<slug>[\w-]+)/', 'common',name="common"),
    url(r'(?P<section>[\w-]+)/(?P<subsection>[\w-]+)/', 'section_subsection',name="section_subsection"),
    #url(r'(?P<section>[\w-]+)/(?P<subsection>[\w-]+)/(?P<entry>[\w-]+)/', 'entry',name="entry"),
    
    
)
