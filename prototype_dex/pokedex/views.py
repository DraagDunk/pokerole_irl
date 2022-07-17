from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
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


def add(request):
    template = loader.get_template('add.html')
    return HttpResponse(template.render({}, request))


def addrecord(request):
    name = request.POST['name']
    primarytype = request.POST['primarytype']
    secondarytype = request.POST['secondarytype']

    dex_member = Pokedex(name=name, primarytype=primarytype,
                         secondarytype=secondarytype)
    dex_member.save()
    return HttpResponseRedirect(reverse('index'))


def delete(request, id):
    dex_member = Pokedex.objects.get(id=id)
    dex_member.delete()
    return HttpResponseRedirect(reverse('index'))


def update(request, id):
    dex_member = Pokedex.objects.get(id=id)
    template = loader.get_template("update.html")
    context = {
        "dex_member": dex_member
    }
    return HttpResponse(template.render(context, request))


def updaterecord(request, id):
    name = request.POST['name']
    primarytype = request.POST['primarytype']
    secondarytype = request.POST['secondarytype']

    dex_member = Pokedex.objects.get(id=id)
    dex_member.name = name
    dex_member.primarytype = primarytype
    dex_member.secondarytype = secondarytype
    dex_member.save()
    return HttpResponseRedirect(reverse('index'))
