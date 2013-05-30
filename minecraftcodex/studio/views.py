from django.shortcuts import render_to_response
from django.template import RequestContext


def main(request):
    context = RequestContext(request)
    return render_to_response('studio/main.html', context_instance=context)
