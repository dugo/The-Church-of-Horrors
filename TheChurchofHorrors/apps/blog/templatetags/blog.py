from django.template.defaultfilters import stringfilter
from django import template
from apps.blog.models import Entry
import re, htmlentitydefs

register = template.Library()

@register.inclusion_tag('preview-entry.html')
def preview_entry(entry, n=0):
	return {'e':entry,'parity':n%2}
	
@register.inclusion_tag('mini-author.html')
def mini_author(author):
	return {'author':author}
    
@register.inclusion_tag('gallery-entry.html')
def entry_gallery(entry):
    
    images = entry.images.order_by("order")[:]
    
    return {'images':images}
    
@register.inclusion_tag('gallery.html')
def home_gallery():
    import random,time
    random.seed(time.time())
    
    gallery = list(Entry.get_home_gallery())
    random.shuffle(gallery)
    total = len(gallery)
    
    return {'gallery':gallery, "total":total }
	
@register.inclusion_tag('breadcrumb.html')
def breadcrumb(path,section=None,subsection=None):
	
	urls = []
	
	if section:
		urls.append( (section.get_absolute_url(),unicode(section),) )
	
	if subsection:
		urls.append( (subsection.get_absolute_url(),unicode(subsection),) )

	if not section and not subsection:
		from django.conf import settings

		mapping = settings.BLOG_BREADCRUMB_URL_MAPPING

		token = path.split('/')[1]
		
		if mapping.get(token):
			urls.append( (path, mapping.get(token),) )
	
	if urls and (not section or not subsection):
		urls.insert(0, ("/", "HOME") )
	
	return {'urls':urls}

@register.filter
@stringfilter
def remove_linebreaks(value):
    return value.replace('\n','').replace('\r','')
    
##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
@register.filter
@stringfilter
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

@register.filter
@stringfilter
def sexualize(value, arg=u'o,a'):
    
    FEM_VOCALS = ('a',)
    VOCALS = ('a','e','i','o','u',)
    
    bits = arg.split(u',')
    if len(bits) <> 2:
        return u''
    masc_suffix, fem_suffix = bits[:2]

    # find the last vocal of value
    for i in range(len(value)-1,-1,-1):
        if value[i] in VOCALS:
            vocal = value[i]
            break
    else:
        return u''
    
    if vocal in FEM_VOCALS:
        return fem_suffix
    
    return masc_suffix
sexualize.is_safe = False
