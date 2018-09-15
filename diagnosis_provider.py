import requests
import json
from access_token_provider import get_access_token

# Custom exception class for errors thrown by API call
class ApiError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# Gets the JSON object containing diagnosis data
def get_diagnosis_json(symptoms, gender, year_of_birth):
    api_token = get_access_token()
    api_url = "https://healthservice.priaid.ch/diagnosis"
    symptoms_string = ""
    for i in range(len(symptoms)):
        if i == 0:
            symptoms_string += str(symptoms[i])
        else:
            symptoms_string += "," + str(symptoms[i])

    response = requests.get(api_url + "?token=" + api_token + "&language=en-gb" + "&symptoms=[" + symptoms_string + "]&gender=" + gender + "&year_of_birth=" + str(year_of_birth))
    if response.status_code != 200:
        raise ApiError("An error with status code {} occurred" .format(response.status_code))
    else:
        json_response = response.json()
        return json_response