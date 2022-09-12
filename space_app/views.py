from django.shortcuts import render, HttpResponse
from space_app.models import Ufo, Meteorite
import numpy as np

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

# Metricas
encounter_seconds_array = np.array(Ufo.encounters.values_list("length_of_encounter_seconds"))

def metricas(request, min = "0", max = "0"):
    menor = 0
    mayor = 0

    if min != "0":
        menor = encounter_seconds_array.min()
    elif max != "0":
        mayor = encounter_seconds_array.max()
    
    context = {
        "menor" : menor,
        "mayor" : mayor,
        "ufos" : Ufo.encounters.all()
    }

    return render(request, 'mapaMetricas.html', context)

def metricsMean(request):
    context = {
        "promedio" :encounter_seconds_array.mean()
    }
    return render(request, 'promedioMetricas.html', context)