from asyncio.windows_events import NULL
from django.shortcuts import render, HttpResponse
from space_app.models import Ufo, Meteorite
from pandas import read_csv, isna

# Create your views here.
def index(request):
    return HttpResponse("Hello world!")

def mapa_meteorite(request):

    meteorites = Meteorite.meteorites.all()

    print(meteorites)

    context = {
        'meteorites': meteorites
    }

    return render(request, 'mapaMeteorites.html', context)

def mapa(request):
    ufos = Ufo.encounters.all()

    print(ufos)

    context = {
        'ufos': ufos
    }

    return render(request, 'mapa.html', context)
