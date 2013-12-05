def common(request):
    from blog.models import Subsection,Entry,Number
    from dateutil.relativedelta import relativedelta
    import datetime
    
    #sections = Section.objects.all().order_by('name')[:]
    subsections = Subsection.objects.all().order_by('sort')[:]

    first = Entry.objects.all().order_by("created")[0].created
    last = Entry.objects.all().order_by("-created")[0].created

    current = datetime.date(first.year,first.month,1)
    archives = []
    while True:
        if Entry.get_archive(current.year,current.month).count()>0:
            archives.append( current )

        if current.year == last.year and current.month == last.month:
            break

        current += relativedelta(months=1)

    archives.reverse()

    return {
        #'sections': sections,
        'subsections': subsections,
        'archives': archives,
        'current_number':Number.get_current(),
    }
