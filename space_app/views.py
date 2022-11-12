from array import array
from dis import dis
import json
from django.shortcuts import render, HttpResponse
from space_app.models import Kmean, Point, Ufo, Meteorite
import numpy as np
from django.db.models import Count
from sklearn.datasets import make_blobs
from django.views.decorators.csrf import csrf_exempt
from sklearn.cluster import KMeans
from sklearn import cluster

# Create your views here.
def index(request):
    return render(request, 'index.html')

# Mapas

def mapa(request):
    ufos = Ufo.encounters.all()

    print(ufos)

    context = {
        'ufos': ufos
    }

    return render(request, 'mapa.html', context)

def mapa_meteorite(request):

    meteorites = Meteorite.meteorites.all()

    print(meteorites)

    context = {
        'meteorites': meteorites
    }

    return render(request, 'mapaMeteorites.html', context)

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

# Gráficas

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

# Mapa poblaciones

def mapaPoblaciones(request):
    points = Point.objects.all()

    return render(request, 'mapaPoblaciones.html', {
        'points': points
    })

@csrf_exempt
def crearPoblacion(request):
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

        return render(request, 'mapaPoblaciones.html', {
            'points': points
        })

# Mapa personalizado

def mapaPersonalizado(request):
    points = Point.objects.all()

    return render(request, 'mapaPersonalizado.html', {
        'points': points
    })

@csrf_exempt
def entrenarModelo(request):
    num_clusters = request.POST['numclusters']
    tolerancia = request.POST['tolerancia']
    num_iteraciones = request.POST['numiteraciones']
    dispersion = request.POST['dispersion']

    num_clusters = int(num_clusters)
    tolerancia = float(tolerancia)
    num_iteraciones = int(num_iteraciones)
    dispersion = float(dispersion)

    if (num_iteraciones > 300):
        return render(request, 'index.html', {
            'error': 'El máximo de iteraciones es 300'
        })
    else:

        kmean = Kmean()
        kmean.numclusters = num_clusters
        kmean.tolerancia = tolerancia
        kmean.numiteraciones = num_iteraciones
        kmean.dispersion = dispersion
        kmean.save()

        km = KMeans(
            n_clusters=num_clusters,
            init='random',
            max_iter=num_iteraciones,
            tol=tolerancia,
            random_state=dispersion
        )

        points = Point.objects.all()
        x = array([])
        for i in points:
            lat = points[i].lat
            lng = points[i].lng
            x.append([lat,lng])

        # Clusters con los puntos
        train_km = km.fit_predict(x)

        return render(request, 'mapaPersonalizado.html', {
            'points': points
        })