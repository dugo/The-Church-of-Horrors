from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()

@register.inclusion_tag('preview-entry.html')
def preview_entry(entry, n=0):
	return {'e':entry,'parity':n%2}
	
@register.inclusion_tag('mini-author.html')
def mini_author(author):
	return {'author':author}
	
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
		
		token = path.split('/')[0]
		
		if mapping.get(token):
			urls.append( (path, mapping.get(token),) )
	
	if urls and (not section or not subsection):
		urls.insert(0, ("/", "HOME") )
	
	return {'urls':urls}

@register.filter
@stringfilter
def remove_linebreaks(value):
    return value.replace('\n','').replace('\r','')
