from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from database.models import Texture
from django.utils import simplejson as json
from django.core import serializers


def main(request):
    textures = Texture.objects.filter(type='blocks')

    data = {
        'textures': textures
    }

    context = RequestContext(request, data)
    return render_to_response('studio/main.html', context_instance=context)


def textures(request):
    textures = Texture.objects.all()
    data = serializers.serialize('json', textures, fields=('name', 'type', 'image',))
    response = HttpResponse(data, 'application/json')
    return response
