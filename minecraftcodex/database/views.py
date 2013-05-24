from django.shortcuts import render_to_response
from database.models import Version
from django.core.paginator import Paginator
from django.template import RequestContext


def home(request):
    context = RequestContext(request)
    return render_to_response('home.html', context_instance=context)


def versions(request):
    section = 'versions'
    versions = Version.objects.filter(snapshot=False).order_by('-date', '-version_number')
    paginator = Paginator(versions, 50)
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
    context = RequestContext(request, data)

    return render_to_response('versions.html', context_instance=context)

def version(request, version, status='release'):
    item = Version.objects.get(status=status, version_number=version)
    context = RequestContext(request, { 'item': item })
    return render_to_response('version.html', context_instance=context)


def about(request):
    context = RequestContext(request)
    return render_to_response('about.html', context_instance=context)
