from django.http import HttpResponse
from django.template import loader
from .models import Pokedex


def index(request):
    """
    Generates a response to a request. The response is described in django
    templates.

    Parameters
    ----------
    request :
        HTTP request

    Returns
    -------
    Response
        HTTP response

    """
    mypokedex = Pokedex.objects.all().values()
    template = loader.get_template('index.html')
    context = {
        'mypokedex': mypokedex,
        }
    return HttpResponse(template.render(context, request))
