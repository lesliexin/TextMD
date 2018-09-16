# Loads the TextMD database
# Only needs to be run to refresh data or to initiate a new cluster

import json
import pymongo

client = pymongo.MongoClient("mongodb+srv://textmd:textmd@cluster-tpkrt.mongodb.net/test?retryWrites=true")
db = client["textmd"]

def load_db(col, file):
    col = db[col]
    with open(file) as f:
        data = json.load(f)
    
    x = col.delete_many({})
    x = col.insert_many(data)

load_db("body", './locations.JSON')
load_db("symptoms", './symptoms.JSON')
