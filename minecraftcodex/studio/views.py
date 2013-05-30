from django.shortcuts import render_to_response
from django.template import RequestContext
from database.models import Texture


def main(request):
    textures = Texture.objects.all()

    data = {
        'textures': textures
    }

    context = RequestContext(request, data)
    return render_to_response('studio/main.html', context_instance=context)
