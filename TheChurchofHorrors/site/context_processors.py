from blog.models import Number,Subsection

def common(request):
    
    subsections = Subsection.objects.all().order_by('sort')[:]

    return {
        'subsections': subsections,
        'current_number':Number.get_current(),
        'css':Subsection.get_css_colors(),
    }
