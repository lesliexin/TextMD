import json
import pprint
import pymongo

client = pymongo.MongoClient("mongodb+srv://textmd_read:textmd_read@cluster-tpkrt.mongodb.net/test?retryWrites=true")
db = client["textmd"]
bodycol = db["body"]
sympcol = db["symptoms"]

# get_locations returns an array of the body locations the user can pick from 
def get_locations():
    loc = []
    query = bodycol.find()
    for doc in query:
        loc.append(doc["location"])
    return loc

# get_sublocations takes the location specified and returns an array of
#   sublocations that the user can pick from
def get_sublocations(location):
    subloc = []
    query = bodycol.find( { "location": location } )
    for doc in query:
        subloc = doc["sublocations"]
    return subloc

# get_symptoms takes the location and sublocation specified and returns an
#   array of symptoms
def get_symptoms(sublocation):
    symp = []
    query = sympcol.find( { "sublocation": sublocation } )
    for doc in query:
        symp.append(doc["name"])
    return symp

# get_symptom_id takes the symptom and returns a symptom ID to be passed to 
#   ApiMedic for diagnosis
def get_symptom_id(symptom):
    id = 0
    query = sympcol.find( { "name": symptom } )
    for doc in query:
        id = doc["id"]
    return id
