def common(request):
    from blog.models import Section,Subsection,Entry
    
    sections = Section.objects.all().order_by('name')[:]
    
    if request.section is None:
        subsections = Subsection.objects.all().order_by('name')[:]
    else:
        subsections = []
        for s in Subsection.objects.all().order_by('name')[:]:
            s.section=unicode(request.section)
            subsections.append(s)
    
    if not request.entry is None:
        entries = Entry.get_last_by_author(user=request.user,author=request.entry.author)
    else:
        entries = Entry.get_last_by_section(user=request.user,section=request.section)
    
    return {
        'sections': sections,
        'subsections': subsections,
        'entries': entries,
    }
