from django.contrib.sitemaps import Sitemap
from django.contrib.auth.models import User
from apps.blog.models import Entry,Section,Subsection
from datetime import date

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Entry.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.created
        
class SectionSitemap(Sitemap):
    changefreq = "always"
    priority = 0.9

    def items(self):
        return Section.objects.all()

    def lastmod(self, obj):
        try:
            return Entry.objects.filter(section__id=obj.id,published=True).order_by("-created")[0:1].get().created
        except Entry.DoesNotExist:
            return date.today()

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

class SectionSubsectionSitemap(Sitemap):
    changefreq = "always"
    priority = 0.8

    def items(self):
        subsections = []
        for s in Section.objects.all()[:]:
            for ss in Subsection.objects.all()[:]:
                ss.section = s
                subsections.append(ss)
        return subsections

    def lastmod(self, obj):
        try:
            return Entry.objects.filter(subsection__id=obj.id,section=obj.section.id,published=True).order_by("-created")[0:1].get().created
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
