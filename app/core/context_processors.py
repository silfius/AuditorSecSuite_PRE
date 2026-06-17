from .version import APPLICATION_NAME, APPLICATION_VERSION

def application_version(request):
    return {
        "APPLICATION_NAME": APPLICATION_NAME,
        "APPLICATION_VERSION": APPLICATION_VERSION,
    }
