from django.shortcuts import render, HttpResponse
from space_app.models import Ufo, Meteorite
from pandas import read_csv

# Create your views here.
def index(request):
    return HttpResponse("Hello world!")

# save excel in database
def ufos(request):

    ufos = read_csv('space_app/static/ufo_sighting_data.csv')

    print(ufos)
    for index, row in ufos.iterrows():
        if index == 0:
            continue

        if index > 0 and index < 2501:
            ufo = Ufo()
            print(float(row[5]))
            hour = row[0].strip().split(' ')[1] 

            if hour == '24:00':
                hour = '00:00'

            ufo.date_time = row[0].strip().split('/')[2].split(" ")[0] + "-" + row[0].strip().split('/')[0] + "-" + row[0].strip().split('/')[1] + " " + hour
            ufo.city = row[1]
            ufo.country = row[3]
            ufo.ufo_shape = row[4]
            ufo.length_of_encounter_seconds = float(row[5])
            ufo.described_duration_of_encounter = row[6]
            ufo.description = row[7]
            ufo.latitude = row[9]
            ufo.longitude = row[10]
            ufo.save()
            print(ufo)


    return HttpResponse("Ufos")
