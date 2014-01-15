# coding=utf-8

from django.core.management.base import BaseCommand
import urllib,urllib2,simplejson,re,datetime
from django.db.models import Sum
import sys,traceback
from django.conf import settings
from blog.models import *

class Command(BaseCommand):

    def handle(self, *args, **options):

        # para todos los concursos
        today = datetime.date.today()
        for number in Number.get_published():
            for entry in number.all_entries:
        
                # FACEBOOK
                # 1) obtener las urls (ingles y español) de la portada (external url)
                urls = ["http://thechurchofhorrors.com%s"%entry.get_absolute_url()]

                if settings.DEBUG:
                    urls = ['http://thechurchofhorrors.com/numero-1/2014/1/comic/humano-demasiado-humano/']

                # 2) hacer consulta a facebook y obtener MG
                data = {"query":"select total_count,like_count,comment_count,share_count,click_count from link_stat where url in (%s)"%(",".join(["'%s'"%u for u in urls]))}
                data['format'] = 'json'
                url = "https://api.facebook.com/method/fql.query?%s"%urllib.urlencode(data)

                total = 0

                try:
                    data = urllib2.urlopen(url,timeout=60).read()
                    data = simplejson.loads(data)
                    print data
                    for d in data:
                        total+= int(d['share_count']) + int(d['like_count'])

                    print "FB SHARE",entry,total
                except:
                    print url
                    traceback.print_exc(file=sys.stdout)

                # 2) obtener las veces que se han compartido cada uno de los enlaces
                for u in urls:
                    url = "http://urls.api.twitter.com/1/urls/count.json?url=%s"%u
                    try:
                        data = urllib2.urlopen(url,timeout=60).read()
                        data = simplejson.loads(data)
                        total += data['count']
                        print "TW SHARES",total
                    except:
                        print url
                        traceback.print_exc(file=sys.stdout)

                entry.shared = total
                entry.save()


