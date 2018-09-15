import requests
import json

# Custom exception class for errors thrown by API call
class ApiError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# Gets the JSON object containing diagnosis data
def get_diagnosis_json(symptoms, gender, year_of_birth):
    # Will write separate funtion to generate this (changes every 2 hours)
    api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InNoZXJyeWhsaUBob3RtYWlsLmNvbSIsInJvbGUiOiJVc2VyIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvc2lkIjoiMTExNSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvdmVyc2lvbiI6IjEwOCIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbGltaXQiOiIxMDAiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL21lbWJlcnNoaXAiOiJCYXNpYyIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbGFuZ3VhZ2UiOiJlbi1nYiIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvZXhwaXJhdGlvbiI6IjIwOTktMTItMzEiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL21lbWJlcnNoaXBzdGFydCI6IjIwMTgtMDktMTUiLCJpc3MiOiJodHRwczovL2F1dGhzZXJ2aWNlLnByaWFpZC5jaCIsImF1ZCI6Imh0dHBzOi8vaGVhbHRoc2VydmljZS5wcmlhaWQuY2giLCJleHAiOjE1MzcwMzMxOTQsIm5iZiI6MTUzNzAyNTk5NH0.zqPwR_UXDrpLASO0dyzEpqQVvYlfW-VTKvYsYsAB9Fo"
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