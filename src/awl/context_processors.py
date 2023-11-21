# awl.context_processors.py
import os

def extra_context(request):
    """Adds useful global items to the context for use in templates.

    * *request*: the request object
    * *HOST*: host name of server
    * *IN_ADMIN*: True if you are in the django admin area
    """
    host = os.environ.get('DJANGO_LIVE_TEST_SERVER_ADDRESS', None) \
        or request.get_host()
    d = {
        'request':request,
        'HOST':host,
        'IN_ADMIN':request.path.startswith('/admin/'),
    }

    return d
