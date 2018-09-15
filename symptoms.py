import json
import pprint

with open('./symptoms.JSON') as f:
    data = json.load(f)

loc = "head"        # user input
subloc = "throat"   # user input
symptoms = []       # needs to be reset every session

# get_locations returns an array of the body locations the user can pick from 
def get_locations():
    locations = []
    for x in data:
        locations.append(x["location"])
    pprint.pprint(locations)
    return locations

# get_sublocations takes the location specified and returns an array of
#   sublocations that the user can pick from
def get_sublocations(location):
    sublocations = []
    for x in data:
        if (location == x["location"]):
            for y in x["items"]:
                sublocations.append(y["sublocation"])
    pprint.pprint(sublocations)
    return sublocations

# get_symptoms takes the location and sublocation specified and returns an
#   array of symptom IDs to be passed to the ApiMedic API for diagnosis
def get_symptoms(location, sublocation):
    for x in data:
        if (location == x["location"]):
            for y in x["items"]:
                if (sublocation == y["sublocation"]):
                    for z in y["symptoms"]:
                        symptoms.append(z["id"])
    pprint.pprint(symptoms)
    return symptoms

get_locations()
get_sublocations(loc)
get_symptoms(loc, subloc)