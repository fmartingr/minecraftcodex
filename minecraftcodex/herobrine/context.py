from django.conf import settings

def TemplateContext(request):
    result = {}
    if hasattr(settings, 'TEMPLATE_CONTEXT'):
        for item in settings.TEMPLATE_CONTEXT:
            result[item[0]] = item[1]
    return result


def SiteTitleContext(request):
    return {
        'site_title': settings.SITE_TITLE
    }
