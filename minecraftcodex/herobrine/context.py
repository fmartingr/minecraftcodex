from django.conf import settings

def templateContext(request):
    result = {}
    if hasattr(settings, 'TEMPLATE_CONTEXT'):
        for item in settings.TEMPLATE_CONTEXT:
            result[item[0]] = item[1]
    return result
