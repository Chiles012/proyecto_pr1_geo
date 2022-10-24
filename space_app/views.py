import json
from django.shortcuts import render, HttpResponse
from space_app.models import Ufo, Meteorite
import numpy as np
from django.db.models import Count
from sklearn.datasets import make_blobs
from django.views.decorators.csrf import csrf_exempt

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

def mapa_poblacion(request):
    points = Point.objects.all()

    return render(request, 'mapaPoblacion.html', {
        'points': points
    })

@csrf_exempt
def crear_poblacion(request):
    rangoslng = request.POST['rangoslng']
    rangoslat = request.POST['rangoslat']
    num_puntos = request.POST['numpuntos']
    dispersion = request.POST['dispersion']

    rangoslng = rangoslng.split(',')
    rangoslat = rangoslat.split(',')
    num_puntos = int(num_puntos)
    dispersion = float(dispersion)

    if (len(rangoslng) != 2 and len(rangoslat) != 2):
        return render(request, 'index.html', {
            'error': 'Los rangos deben ser de 2 valores'
        })
    elif (num_puntos <= 0):
        return render(request, 'index.html', {
            'error': 'El número de puntos debe ser mayor a 0'
        })
    elif (dispersion <= 0 or dispersion > 1):
        return render(request, 'index.html', {
            'error': 'La dispersión debe ser mayor a 0 y menor o igual a 1'
        })
    else:
        x, y = make_blobs(n_samples=num_puntos, 
                            centers=1, cluster_std=dispersion, 
                            center_box=([rangoslng[0], rangoslat[0]], [rangoslng[1], rangoslat[1]]), 
                            random_state=1
                        )

        for i in x:
            point = Point()
            point.lat = i[0]
            point.lng = i[1]
            point.save()

        points = Point.objects.all()

        return render(request, 'mapa-poblaciones.html', {
            'points': points
        })