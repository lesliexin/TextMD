from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from symptoms import get_locations, get_sublocations, get_symptoms, get_symptom_id
from diagnosis_parser import get_issue_names, get_issue_accuracy, get_suggested_specialists
from doctor_recommendation_provider import get_geocode, get_nearby_doctors
from diagnosis_provider import get_diagnosis_json

# The session object makes use of a secret key.
SECRET_KEY = "a secret key"
app = Flask(__name__)
app.config.from_object(__name__)

# Try adding your own number to this list!
patients = {
    "+14165581768": ["Leslie Xin", 0, "", "", "location", "sublocation",[]],
    "+14158675310": ["Finn Smith", 0, "", "", "location", "sublocation",[]],
    "+14158675311": ["Chewy White", 0, "", "", "location", "sublocation",[]],
    "+14166299630": ["Sherry", 0, "", "", "location", "sublocation",[]],
}

'''
class Address():
    def __init__(self, unit, street, city, province):
        self.unit = unit
        self.street = street
        self.city = city
        self.province = province

class Patient():
    def __init__(self, name, birth_year, sex, address):
        self.name = name
        self.birth_year = birth_year
        self.sex = sex
        self.address = address
'''

@app.route("/sms", methods=['GET', 'POST'])
def hello():
    # Respond with the number of text messages sent between two parties.

    # Increment the counter
    counter = session.get("counter", 0)
    counter += 1

    # Save the new counter value in the session
    session["counter"] = counter

    # Get user text
    text = request.values.get("Body", None)

    if text == "clear":
        session.clear()

    from_number = request.values.get("From")
    if from_number in patients:
        name = patients[from_number][0]
        counter += 1
    else:
        name = ""

    message = ""

    # New user
    if counter == 1:
        # Ask for name
        message = "\nHi there, what is your full name?"

    elif counter == 2:
        # Greeting
        if name == "":
            patients[str(from_number)] = []
            message = "\n\nHi there, {}! Welcome to TextMD! What year were you born?"
        else:
            message = "\n\nWelcome back, {}! What year were you born?"

    elif counter == 3:
        try: 
            int(str(text))
            patients[str(from_number)][1] = str(text)
            message = "\n\nWhat is your sex (male/female)?"
        except ValueError:
            counter -= 1
            session["counter"] = counter
            message = "Sorry, we do not understand. Please enter your birth year."

    elif counter == 4:
        if str(text).lower() != "male" and str(text).lower() != "female":
            counter -= 1
            session["counter"] = counter
            message = "Sorry, we do not understand. Please enter your sex."
        else:
            patients[str(from_number)][2] = str(text)
            message = "\n\nNext we need your address.\nWhat is your unit number?"

    elif counter == 5:
        try:
            int(str(text))
            patients[str(from_number)][3] = str(text)
            message = "\n\nWhat is your street name?"
        except:
            counter -= 1
            session["counter"] = counter
            message = "Sorry, we do not understand. Please enter your unit number."

    elif counter == 6:
        patients[str(from_number)][3] += ("+" + str(text))
        message = "\n\nWhat is your street suffix? (e.g. street, avenue, trail)"

    elif counter == 7:
        patients[str(from_number)][3] += ("+" + str(text))
        message = "\n\nWhat is your city?"

    elif counter == 8:
        patients[str(from_number)][3] += (",+" + str(text))
        message = "\n\nWhat is your province/state?"

    elif counter == 9:
        patients[str(from_number)][3] += (",+" + str(text))
        location_choices = get_locations()
        location_string = ""
        for i in range(len(location_choices)):
            if len(location_choices) == 1:
                location_string += location_choices[i]
            else:
                location_string += ", " + location_choices[i]
        message = "Now, please tell us where your discomfort is located. Choose from: " + location_string 

    elif counter == 10:
        patients[str(from_number)][4] = str(text).lower()
        sublocation_choices = get_sublocations(str(text).lower())
        sublocation_string = ""
        for i in range(len(sublocation_choices)):
            if len(sublocation_choices) == 1:
                sublocation_string += sublocation_choices[i]
            else:
                sublocation_string += ", " + sublocation_choices[i]
        message = "Let's narrow down the issue. Please choose a more specific location of your discomfort: " + sublocation_string

    elif counter == 11:
        patients[str(from_number)][5] = str(text).lower()
        symptom_choices = get_symptoms(str(text).lower())
        symptom_string = ""
        for i in range(len(symptom_choices)):
            if len(symptom_choices) == 1:
                symptom_string += symptom_choices[i]
            else:
                symptom_string += ", " + symptom_choices[i]
        message = "Please tell us your symptoms, separated by a comma: " + symptom_string
    
    elif counter == 12:
        symptom_array = str(text).lower().split(",")
        symptom_ids = []
        for symptom in symptom_array:
            print(symptom)
            symptom_ids.append(get_symptom_id(symptom))
            print(symptom_ids)

        if patients[str(from_number)][1] == None:
            print('year is null')
            return 
        if patients[str(from_number)][2] == None:
            print('sex is null')
            return
        print(symptom_ids)
        json_diagnosis = get_diagnosis_json(symptom_ids, patients[str(from_number)][2], str(patients[str(from_number)][1]))
        # print (json_diagnosis[0])
        issues = get_issue_names(json_diagnosis)
        accuracies = get_issue_accuracy(json_diagnosis)
        suggested_specialists = get_suggested_specialists(json_diagnosis)
        lat_and_lng = get_geocode(patients[str(from_number)][3])
        # doc_recommendations = get_nearby_doctors(suggested_specialists[0][0], lat_and_lng)
        # num_docs = len(doc_recommendations)
        # num_display = 3 if num_docs > 3 else num_docs
        message = "In order of most likely to least likely, your diagnosis is: "
        for j in range(len(issues)):
            if j == len(issues) - 1:
                message += issues[j] + " with an accuracy of" + str(accuracies[j]) + "."
            else:
                message += issues[j] + " with an accuracy of" + str(accuracies[j]) + ";"
        # message += " We suggest you visit:"
        # i = 0
        # while i < num_display:
        #     message += doc_recommendations[i].name + " at" + doc_recommendations[i].address + " with rating " + doc_recommendations[i].ratings + "/5. Open now: " + doc_recommendations[i].is_open + ". "
    
    else:
        session.clear()

    # Put it in a TwiML response
    resp = MessagingResponse()
    resp.message(message)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)