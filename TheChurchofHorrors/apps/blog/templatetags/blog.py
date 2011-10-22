from django import template

register = template.Library()

@register.inclusion_tag('preview-entry.html')
def preview_entry(entry, n=0):
	return {'e':entry,'parity':n%2}
	
@register.inclusion_tag('mini-author.html')
def mini_author(author):
	return {'author':author}
