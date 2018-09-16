import json
import pprint
import pymongo

client = pymongo.MongoClient("mongodb+srv://textmd_read:textmd_read@cluster-tpkrt.mongodb.net/test?retryWrites=true")
db = client["textmd"]
bodycol = db["body"]
sympcol = db["symptoms"]

location = "head"           # user input
sublocation = "throat"      # user input
symptom = "hiccups"         # user input
symptoms = []               # needs to be reset every session

# get_locations returns an array of the body locations the user can pick from 
def get_locations():
    loc = []
    query = bodycol.find()
    for doc in query:
        loc.append(doc["location"])
    pprint.pprint(loc)
    return loc

# get_sublocations takes the location specified and returns an array of
#   sublocations that the user can pick from
def get_sublocations(location):
    subloc = []
    query = bodycol.find( { "location": location } )
    for doc in query:
        subloc = doc["sublocations"]
    pprint.pprint(subloc)
    return subloc

# get_symptoms takes the location and sublocation specified and returns an
#   array of symptoms
def get_symptoms(sublocation):
    symp = []
    query = sympcol.find( { "sublocation": sublocation } )
    for doc in query:
        symp.append(doc["name"])
    pprint.pprint(symp)
    return symp

# get_symptom_id takes the symptom and returns an array of symptom IDs to be 
#   passed to ApiMedic for diagnosis
def get_symptom_id(symptom):
    id = 0
    query = sympcol.find( { "name": symptom } )
    for doc in query:
        id = doc["id"]
    pprint.pprint(id)
    return id

get_locations()
get_sublocations(location)
get_symptoms(sublocation)
get_symptom_id(symptom)