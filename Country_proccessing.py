import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from influxdb import InfluxDBClient


client = InfluxDBClient(host='localhost', port='8086')
client.switch_database('covid19')


data = pd.read_csv("countries_update_2.csv")
pays = data["Country"].tolist()
rest_pay = data["Country"].iloc[1271:].to_list()
latitude = []
longitude = []
for name in pays:
    geolocator = Nominatim(user_agent="Agent1")
    location = geolocator.geocode(name)
    latitude.append(location.latitude)
    longitude.append(location.longitude)

latitud = []
longitud = []
for name in rest_pay:
    geolocator = Nominatim(user_agent="Agent2")
    location = geolocator.geocode(name)
    latitud.append(location.latitude)
    longitud.append(location.longitude)

location = pays[:1269] + rest_pay
latitude = latitude + latitud
longitude = longitude + longitud

countries = pd.DataFrame([location,latitude,longitude], ["Location","Latitude","Longitude"]).T
countries['Metric'] = countries.groupby('Location')['Location'].transform('count')
countries.to_csv("train_geo_countries.csv")


""" Insertion des pays de la donnée train dans influxdb pour la visualisation sur la map du monde """


countries = pd.read_csv("train_geo_countries.csv")

for row_ind, row in countries.iloc[0:].iterrows():
    json_body = [{
        'measurement' : 'train_country_tweets',
        'tags':{"Id":row[0]},
        'fields':{
            "name":row[1],
            "latitude":row[2],
            "longitude":row[3],
            "metric":row[4]
                  }
    }]

    client.write_points(json_body)
print("done")


""" Insertion des pays de la donnée tests dans influxdb pour la visualisation sur la map du monde """

"""
countries = pd.read_csv("test_geo_countries.csv")

for row_ind, row in countries.iloc[0:].iterrows():
    json_body = [{
        'measurement' : 'test_country_tweets',
        'tags':{"Id":row[0]},
        'fields':{
            "name":row[1],
            "latitude":row[2],
            "longitude":row[3],
            "metric":row[4]
                  }
    }]

    client.write_points(json_body)
print("done")
"""