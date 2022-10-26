from django.db import models
from django.db.models import Q

class Ufo(models.Model):
    id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField() # fecha y hora del avistamiento
    city = models.CharField(max_length=100) # ciudad
    country = models.CharField(max_length=100, blank=True, null=True) # país
    ufo_shape = models.CharField(max_length=100, blank=True, null=True) # forma del ufo
    length_of_encounter_seconds = models.DecimalField(max_digits=9, decimal_places=1) # duración del avistamiento (en segundos) p.ej: 180
    described_duration_of_encounter = models.CharField(max_length=100) # duración del avistamiento (texto desciptivo) p.ej: about 3 mins
    description = models.TextField() # descripción del avistamiento
    latitude = models.DecimalField(max_digits=9, decimal_places=6) 
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    encounters = models.Manager() # Ufo.encounters.all() devuelve una lista con todos los objetos Ufo


class MeteoriteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(year__gte= 860, year__lte=2016, longitude__lte=180, longitude__gte=-180).exclude(latitude=0, longitude=0) 

class Meteorite(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # nombre del meteorito
    clasification = models.CharField(max_length=50) # clasificación del meteorito
    mass = models.IntegerField() # masa del meteorito en gramos 
    fall = models.CharField(max_length=20) # indica si el meteorito fue visto cayendo (Fell) o si fue descubierto después del impaco (Found)
    year = models.IntegerField() # año en el que fue visto cayendo o fue descubierto
    latitude = models.DecimalField(max_digits=9, decimal_places=6) 
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    meteorites = models.Manager() # Meteorite.meteorites.all() devuelve una lista con todos los objetos Meteorite
    validMeteorites = MeteoriteManager() # devuelve solo meteoritos con coordenadas y años válidos

class Point(models.Model):
    id = models.AutoField(primary_key=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6) 
    lng = models.DecimalField(max_digits=9, decimal_places=6)

class Kmean(models.Model):
    id = models.AutoField(primary_key=True)
    numclusters = models.IntegerField() 
    tolerancia = models.DecimalField(max_digits=9, decimal_places=6)
    numiteraciones = models.IntegerField()
    dispersion = models.DecimalField(max_digits=9, decimal_places=6)