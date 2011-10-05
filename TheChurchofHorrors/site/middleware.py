

class CommonBlogMiddleware(object):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        
        from apps.blog.models import Section,Subsection,Entry
        from django.http import Http404,HttpResponsePermanentRedirect
        
        request.section = request.section = request.entry = None
        
        if view_func.__name__ == "common":
            try:
                request.section = Section.objects.get(slug=view_kwargs['slug'])
            except Section.DoesNotExist:
                pass
                
            try:
                request.subsection = Subsection.objects.get(slug=view_kwargs['slug'])
            except Subsection.DoesNotExist:
                pass
                
            try:
                entry = Entry.objects.get(slug=view_kwargs['slug'])
                
                return HttpResponsePermanentRedirect(entry.get_absolute_url())
            except Entry.DoesNotExist:
                raise Http404()
        
        elif view_func.__name__ == "section_subsection":

            try:
                request.section = Section.objects.get(slug=view_kwargs['slug'])
            except Section.DoesNotExist:
                raise Http404()
                
            try:
                request.subsection = Subsection.objects.get(slug=view_kwargs['slug'])
            except Subsection.DoesNotExist:
                raise Http404()
                        
        elif view_func.__name__ == "entry":
            
            try:
                request.entry = Entry.objects.get(slug=view_kwargs['entry'])
            except Entry.DoesNotExist:
                raise Http404()
            
            request.section = request.entry.section
            request.subsection = request.entry.subsection
        
        
            
            
