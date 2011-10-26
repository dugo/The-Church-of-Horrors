def common(request):
    from blog.models import Section,Subsection
    
    sections = Section.objects.all().order_by('name')[:]
    subsections = Subsection.objects.all().order_by('order')[:]
    
    return {
        'sections': sections,
        'subsections': subsections
    }
