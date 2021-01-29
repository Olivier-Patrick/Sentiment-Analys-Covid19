import pandas as pd
from influxdb import InfluxDBClient


client = InfluxDBClient(host='localhost', port='8086')
client.switch_database('covid19')


############################## INSERER LES DONNEES NETTOYEES DANS INFLUXDB  ##############################
'''
data = pd.read_csv("clean_data.csv")
data.dropna(inplace=True)
print(data.shape)

for row_ind, row in data.iloc[1:].iterrows():
    json_body = [{
        'measurement' : 'sentiment',
        'tags':{"Messages":row[1]},
        'fields':{"sentiment_label":row[2]}
    }]

    client.write_points(json_body)
print("done")

'''
############################## INSERER LES DONNEES DE PAYS DANS INFLUXDB  ##############################

'''
data = pd.read_csv("countries.csv")
data.dropna(inplace=True)
print(data.shape)

for row_ind, row in data.iloc[1:].iterrows():
    json_body = [{
        'measurement' : 'covid_tweets',
        'tags':{"country":row[0]},
        'fields':{
            "name":row[0],
            "latitude":row[2],
            "longitude":row[3],
            "metric":row[4]
                  }
    }]

    client.write_points(json_body)
print("done")
'''

############################## INSERER LES DONNEES DE PAYS DANS INFLUXDB  ##############################

'''
data = pd.read_csv("polarity.csv")
data.dropna(inplace=True)
print(data.shape)

for row_ind, row in data.iloc[1:].iterrows():
    json_body = [{
        'measurement' : 'polarity',
        'tags':{"Id":row[0]},
        'fields':{
            "sentiment":row[1],
                  }
    }]

    client.write_points(json_body)
print("done")
'''
############################## INSERER LA POLARITE DES DONNEES TEXT DANS INFLUXDB  ##############################

data = pd.read_csv("test_polarity.csv")
data.dropna(inplace=True)
print(data.shape)

for row_ind, row in data.iloc[1:].iterrows():
    json_body = [{
        'measurement' : 'Test_polarity',
        'tags':{"Id":row[0]},
        'fields':{
            "sentiment":row[1],
                  }
    }]

    client.write_points(json_body)
print("done")
