from django.contrib.syndication.views import Feed
from apps.blog.models import Entry
from django.utils.translation import ugettext as _
from django.conf import settings

class LatestEntriesFeed(Feed):
    title = "thechurchofhorrors.com %s" % _(u'magazine cultural')
    link = "/"
    description = _("Actualizaciones en thechurchofhorrors.com")

    def items(self):
        return Entry.get_last()[:settings.BLOG_RSS_LAST_ENTRIES]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.get_brief()
