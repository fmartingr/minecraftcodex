from blog.models import BlogEntry
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime


def blog(request):
    section = 'blog'

    items = BlogEntry.objects.all()
    paginator = Paginator(items, 4)
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
    return render_to_response('blog.html', context_instance=context)


def blog_item(request, year, month, day, slug):
    item = BlogEntry.objects.get(
        slug=slug,
        date__year=int(year),
        date__month=int(month),
        date__day=int(day)
    )

    data = {
        'item': item
    }
    context = RequestContext(request, data)
    return render_to_response('blog_entry.html', context_instance=context)
