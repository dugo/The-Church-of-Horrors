from django.contrib.sitemaps import Sitemap
from django.contrib.auth.models import User
from apps.blog.models import Entry,Subsection
from taggit.models import Tag
from datetime import date

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Entry.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.created
        

class SubsectionSitemap(Sitemap):
    changefreq = "always"
    priority = 0.9

    def items(self):
        return Subsection.objects.all()

    def lastmod(self, obj):
        try:
            return Entry.objects.filter(subsection__id=obj.id,published=True).order_by("-created")[0:1].get().created
        except Entry.DoesNotExist:
            return date.today()

class SectionTagSitemap(Sitemap):
    changefreq = "always"
    priority = 0.8

    def items(self):
        subsections = []
        for s in Subsection.objects.all()[:]:
            for t in s.tags.all()[:]:
                subsections.append(t)
                
        return subsections

    def lastmod(self, obj):
        try:
            return Entry.objects.filter(subsection__id=obj.subsection.id,tags__id__in=[obj.tag.id],published=True).order_by("-created")[0:1].get().created
        except Entry.DoesNotExist:
            return date.today()
            
class AuthorSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return User.objects.all()

    def lastmod(self, obj):
        try:
            return Entry.objects.filter(author__id=obj.id,published=True).order_by("-created")[0:1].get().created
        except Entry.DoesNotExist:
            return date.today()
