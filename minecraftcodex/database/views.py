from django.shortcuts import render_to_response
from database.models import Version
from django.core.paginator import Paginator
from django.template import Context

def home(request):
    return render_to_response('home.html')

def versions(request):
    section = 'versions'
    versions = Version.objects.all().order_by('-date', '-version_number')
    paginator = Paginator(versions, 10)
    page_number = 1

    if 'page' in request.GET:
        page_number = int(request.GET['page'])

    page = paginator.page(page_number)

    data = {
        'section': section,
        'page': page,
        'page_number': page_number,
        'paginator': paginator,
    }

    return render_to_response('versions.html', data)

def about(request):
    return render_to_response('about.html')
