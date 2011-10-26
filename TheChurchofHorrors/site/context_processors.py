def common(request):
    from blog.models import Section,Subsection
    
    sections = Section.objects.all().order_by('name')[:]
    subsections = Subsection.objects.all().order_by('sort')[:]
    
    return {
        'sections': sections,
        'subsections': subsections
    }
