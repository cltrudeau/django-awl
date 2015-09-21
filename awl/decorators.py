# awl.decorators.py
import logging
from functools import wraps

from django.http import Http404

logger = logging.getLogger(__name__)

# ============================================================================
# View Decorators
# ============================================================================

def post_required(method_or_options=[]):
    """View decorator that enforces that the method was called using POST.
    This decorator can be called with or without parameters.  As it is
    expected to wrap a view, the first argument of the method being wrapped is
    expected to be a ``request`` object.

    .. code-block:: python

        @post_required
        def some_view(request):
            pass


        @post_required(['firstname', 'lastname'])
        def some_view(request):
            pass

    The optional parameter contains a single list which specifies the names of
    the expected fields in the POST dictionary.  The list is not exclusive,
    you can pass in fields that are not checked by the decorator.

    :param options:
        List of the names of expected POST keys.
    """
    def decorator(method):
        # handle wrapping or wrapping with arguments; if no arguments (and no
        # calling parenthesis) then method_or_options will be a list,
        # otherwise it will be the wrapped function
        expected_fields = []
        if not callable(method_or_options):
            # not callable means wrapping with arguments
            expected_fields = method_or_options

        @wraps(method)
        def wrapper(*args, **kwargs):
            request = args[0]
            if request.method != 'POST':
                logger.error('POST required for this url')
                raise Http404('only POST allowed for this url')

            missing = []
            for field in expected_fields:
                if field not in request.POST:
                    missing.append(field)

            if missing:
                s = 'Expected fields missing in POST: %s' % missing
                logger.error(s)
                raise Http404(s)

            # everything verified, run the view
            return method(*args, **kwargs)
        return wrapper

    if callable(method_or_options):
        # callable means decorated method without options, call our decorator 
        return decorator(method_or_options)
    return decorator
