import json
from diagnosis_provider import get_diagnosis_json

# Placeholder values for testing at the moment
symptoms = [233,17] # Change to function call
gender = "male" # Change to function call
year_of_birth = "1988" # Change to function call

json_diagnosis = get_diagnosis_json(symptoms, gender, year_of_birth)

# Returns array of all possible health issue names
def get_issue_names(json_diagnosis):
    num_diagnosis = len(json_diagnosis)
    issue_names = []
    i = 0
    while i < num_diagnosis:
        issue_names.append(json_diagnosis[i]["Issue"]["Name"])
        i += 1
    return issue_names

# Returns array of accuracy values for possible health issues
def get_issue_accuracy(json_diagnosis):
    num_diagnosis = len(json_diagnosis)
    issue_accuracies = []
    i = 0
    while i < num_diagnosis:
        issue_accuracies.append(json_diagnosis[i]["Issue"]["Accuracy"])
        i += 1
    return issue_accuracies

# Returns array of arrays of suggested specialists
def get_suggested_specialists(json_diagnosis):
    num_diagnosis = len(json_diagnosis)
    suggested_specialists = []
    i = 0
    while i < num_diagnosis:
        num_specialists = len(json_diagnosis[i]["Specialisation"])
        specialists = []
        j = 0
        while j < num_specialists:
            specialists.append(json_diagnosis[i]["Specialisation"][j]["Name"])
            j += 1
        suggested_specialists.append(specialists)
        i += 1
    return suggested_specialists