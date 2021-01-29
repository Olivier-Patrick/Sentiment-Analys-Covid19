from pymongo import MongoClient
import pandas as pd

client = MongoClient('mongodb://localhost:27017/')
COVID = client['COVID']
collection = COVID['Tweets']

documents = []
for doc in collection.find():
        if "limit" in doc.keys():
            documents.append({"_id":doc["_id"],"created_at":"2020","id":"0","user":{"name":"nan","location":"nan","followers_count":0},"entities":{"hashtags":"array"},"text":"nan"})
        else:
            documents.append(doc)


_Id = []
Id = []
Created_at = []
Name = []
Location = []
Followers = []
Messages = []
hashtags = []
for i in range(len(documents)):
    _Id = [documents[i]['_id'] for i in range(len(documents))]
    Id = [documents[i]['id'] for i in range(len(documents))]
    Created_at = [documents[i]['created_at'] for i in range(len(documents))]
    Name = [documents[i]['user']['name'] for i in range(len(documents))]
    Location = [documents[i]['user']['location'] for i in range(len(documents))]
    Followers = [documents[i]['user']['followers_count'] for i in range(len(documents))]
    hashtags = [documents[i]['entities']['hashtags'] for i in range(len(documents))]
    Messages = [documents[i]['text'] for i in range(len(documents))]

list = [_Id,Id,Created_at,Name,Location,Followers,hashtags,Messages]
columns = ['_Id','Id','Created_at','Name','Location','Followers','hashtags','Messages']
data = pd.DataFrame(list,columns).T

df = data.to_csv("Twitter_data.csv")



