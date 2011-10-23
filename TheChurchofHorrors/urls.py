from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    
    (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL[1:-1], 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT, 'show_indexes': True}),
    (r'favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '%sfavicon.ico' % settings.STATIC_URL}),
    (r'crossdomain\.xml$', 'django.views.generic.simple.redirect_to', {'url': '%crossdomain.xml' % settings.STATIC_URL}),

    (r'^tinymce/', include('tinymce.urls')),
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    (r'', include('blog.urls')),
)
