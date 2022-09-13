import json
from django.shortcuts import render, HttpResponse
from space_app.models import Ufo, Meteorite
import numpy as np
from django.db.models import Count

# Create your views here.
def index(request):
    return render(request, 'index.html')

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

def grafica(request):

    ufos_label = Ufo.encounters.values_list("city").distinct()[0:100]
    ufos_values = Ufo.encounters.values_list("city").annotate(Count("city"))[0:100]

    meteorites_s = Meteorite.meteorites.values_list("mass")

    ufos_json_label = json.dumps(list(ufos_label))
    ufos_json_data = json.dumps(list(ufos_values))
    meteorites_json = json.dumps(list(meteorites_s))


    context = {
        'ufos_labels': ufos_json_label,
        'ufos_data': ufos_json_data,
        'meteorites': meteorites_json
    }

    return render(request, 'graficas.html', context)