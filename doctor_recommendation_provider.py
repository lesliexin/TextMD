import requests
import json

# Custom exception class for errors thrown by API call
class ApiError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# Class representing doctor recommendations, containing doctor's name, value
#   indicating if they're open, their Google ratings, and their address
class doc_recommendation:
    def __init__(self, name, is_open, ratings, address):
        self.name = name
        self.is_open = is_open
        self.ratings = ratings
        self.address = address

# Returns array containing the latitude and longitude of the patient,
#   address parameter should be in form of "200+University+Avenue+W,+Waterloo,+ON"
def get_geocode(address):
    api_url = "https://maps.googleapis.com/maps/api/geocode/json"
    api_key = "AIzaSyAwgNrQxJcURAcWavGIjscRigXHey1M7EY"
    response = requests.get(api_url + "?address=" + address + "&key=" + api_key)
    if response.status_code != 200:
        raise ApiError("An error with status code {} occurred" .format(response.status_code))
    else:
        json_response = response.json()
        lat = json_response["results"][0]["geometry"]["location"]["lat"]
        lng = json_response["results"][0]["geometry"]["location"]["lng"]
        geocode = [lat, lng]
        return geocode


# Consumes keyword as string and geocode as [lat, long]
# Returns array of objects containing doctor name, opening hours, rating, and address
def get_nearby_doctors(keyword, geocode):
    api_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    api_key = "AIzaSyAwgNrQxJcURAcWavGIjscRigXHey1M7EY"
    response = requests.get(api_url + "?key=" + api_key + "&location=" + str(geocode[0]) + "," + str(geocode[1]) + "&radius=50000&type=doctor&keyword=" + keyword)
    if response.status_code != 200:
        raise ApiError("An error with status code {} occurred" .format(response.status_code))
    else:
        json_response = response.json()
        name = ""
        is_open = ""
        ratings = ""
        address = ""
        json_results = json_response["results"]
        num_doctors = len(json_results)
        all_recommendations = []
        for i in range(num_doctors):
            name = json_results[i]["name"]
            # print(json_results[i])
            if "opening_hours" in json_results[i]:
                is_open = json_results[i]["opening_hours"]["open_now"]
            else:
                is_open = "Opening hours are not available."
            ratings = json_results[i]["rating"]
            address = json_results[i]["vicinity"]
            recommendation = doc_recommendation(name, is_open, ratings, address)
            all_recommendations.append(recommendation)
        return all_recommendations