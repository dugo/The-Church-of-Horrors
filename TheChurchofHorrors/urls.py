from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

from apps.blog.sitemaps import *

sitemaps = {'section':SectionSitemap(),'subsection':SubsectionSitemap(),'sectionsubsection':SectionSubsectionSitemap(),'blog':BlogSitemap(),'author':AuthorSitemap()}

urlpatterns = patterns('',
    
    (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL[1:-1], 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT, 'show_indexes': True}),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '%sfavicon.ico' % settings.STATIC_URL}),
    (r'robots\.txt$', 'django.views.generic.simple.redirect_to', {'url': '%srobots.txt' % settings.STATIC_URL}),
    (r'crossdomain\.xml$', 'django.views.generic.simple.redirect_to', {'url': '%scrossdomain.xml' % settings.STATIC_URL}),
    (r'firma\.png$', 'django.views.generic.simple.redirect_to', {'url': '%sfirma.png' % settings.STATIC_URL}),

    (r'^tinymce/', include('tinymce.urls')),
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    (r'', include('blog.urls')),
)
