from django.contrib.syndication.views import Feed
from apps.blog.models import Number
from django.utils.translation import ugettext as _
from django.conf import settings

class LatestEntriesFeed(Feed):
    title = "thechurchofhorrors.com %s" % _(u'magazine cultural')
    link = "/"
    description = _("Actualizaciones en thechurchofhorrors.com")

    def items(self):
        return Number.get_current().other_entries()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.get_brief()
