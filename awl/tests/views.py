from django.contrib import messages
from django.http import HttpResponse
from django.template import Template, RequestContext

def test_view_for_messages(request):
    messages.success(request, 'One')
    messages.error(request, 'Two')

    t = Template('')
    context = RequestContext(request)
    response = HttpResponse(t.render(context))
    return response
