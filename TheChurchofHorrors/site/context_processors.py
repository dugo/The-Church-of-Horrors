from blog.models import Number,Subsection

def common(request):
    
    subsections = Subsection.objects.filter(hidden=False).order_by('sort')[:]

    return {
        'subsections': subsections,
        'current_number':Number.get_current(),
        'anteriores':Number.get_anteriores(),
        'css':Subsection.get_css_colors(),
    }
