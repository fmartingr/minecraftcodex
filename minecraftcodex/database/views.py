from django.shortcuts import render_to_response
from database.models import Version, Item, Block
from django.core.paginator import Paginator
from django.template import RequestContext
from django.http import HttpResponseForbidden, Http404


def home(request):
    context = RequestContext(request, {'section': 'home'})
    return render_to_response('home.html', context_instance=context)


def versions(request):
    section = 'versions'
    versions = Version.objects.filter(snapshot=False).\
        order_by('-date', '-version_number')
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
    section = 'versions'
    items = Version.objects.filter(status=status, version_number=version).\
        order_by('-date')
    data = {
        'version_number': version,
        'status': status,
        'section': section,
        'items': items,
        'results': len(items)
    }
    context = RequestContext(request, data)
    return render_to_response('version.html', context_instance=context)


def items(request):
    section = 'items'

    items = Item.objects.all().order_by('data_value')
    paginator = Paginator(items, 48)
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
    return render_to_response('items.html', context_instance=context)


def items_detail(request, data_value):
    section = 'items'
    if request.user.is_authenticated():
        item = Item.objects.get(data_value=int(data_value)-256)
        data = {
            'section': section,
            'item': item
        }
        context = RequestContext(request, data)
        return render_to_response('items_detail.html', context_instance=context)
    else:
        raise Http404


def blocks(request):
    section = 'blocks'

    items = Block.objects.all().order_by('data_value')
    paginator = Paginator(items, 48)
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
    return render_to_response('blocks.html', context_instance=context)


def blocks_detail(request, data_value):
    section = 'blocks'
    if request.user.is_authenticated():
        item = Block.objects.get(data_value=int(data_value))
        data = {
            'section': section,
            'item': item
        }
        context = RequestContext(request, data)
        return render_to_response('blocks_detail.html', context_instance=context)
    else:
        raise Http404

def about(request):
    context = RequestContext(request, {'section': 'about'})
    return render_to_response('about.html', context_instance=context)


def error404(request):
    from raven.contrib.django.raven_compat.models import sentry_exception_handler
    sentry_exception_handler(request=request)
    context = RequestContext(request)
    return render_to_response('errors/404.html', context_instance=context)


def error500(request):
    data = {
        'request': request
    }
    context = RequestContext(request, data)
    return render_to_response('errors/500.html', context_instance=context)
