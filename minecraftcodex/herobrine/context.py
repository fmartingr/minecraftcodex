from os import environ


def AppVersionContext(request):
    result = {}
    if 'APP_VERSION' in environ:
        result = {
            'app_version': environ['APP_VERSION']
        }

    return result
