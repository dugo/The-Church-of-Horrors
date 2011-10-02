from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TheChurchofHorrors.views.home', name='home'),
    # url(r'^TheChurchofHorrors/', include('TheChurchofHorrors.foo.urls')),

    (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL[1:-1], 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT, 'show_indexes': True}),

    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
