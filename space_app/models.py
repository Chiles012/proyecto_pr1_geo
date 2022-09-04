from msilib.schema import Class
from tkinter.tix import Tree
from django.db import models

class Ufo(models.Model):
    date_time = models.DateTimeField() # fecha y hora del avistamiento
    city = models.CharField(max_length=50) # ciudad
    country = models.CharField(max_length=50, blank=True, null=True) # país
    ufo_shape = models.CharField(max_length=50, blank=True, null=True) # forma del ufo
    length_of_encounter_seconds = models.IntegerField() # duración del avistamiento (en segundos) p.ej: 180
    described_duration_of_encounter = models.CharField(max_length=50) # duración del avistamiento (texto desciptivo) p.ej: about 3 mins
    description = models.TextField() # descripción del avistamiento
    latitude = models.DecimalField(max_digits=9, decimal_places=6) 
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    encounters = models.Manager() # Ufo.encounters.all() devuelve una lista con todos los objetos Ufo



class Meteorite(models.Model):
    name = models.CharField(max_length=100)  # nombre del meteorito
    clasification = models.CharField(max_length=50) # clasificación del meteorito
    mass = models.IntegerField() # masa del meteorito en gramos 
    fall = models.CharField(max_length=20) # indica si el meteorito fue visto cayendo (Fell) o si fue descubierto después del impaco (Found)
    year = models.IntegerField() # año en el que fue visto cayendo o fue descubierto
    latitude = models.DecimalField(max_digits=9, decimal_places=6) 
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    meteorites = models.Manager() # Meteorite.meteorites.all() devuelve una lista con todos los objetos Meteorite
