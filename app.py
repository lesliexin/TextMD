from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from symptoms_options import get_locations, get_sublocations, get_symptoms
from diagnosis_parser import get_issue_names, get_issue_accuracy, get_suggested_specialists
from doctor_recommendation_provider import get_geocode, get_nearby_doctors

# The session object makes use of a secret key.
SECRET_KEY = "a secret key"
app = Flask(__name__)
app.config.from_object(__name__)

# Try adding your own number to this list!
patients = {
    "+14165581768": ["Leslie Xin", 0, "", ""],
    "+14158675310": ["Finn Smith", 0, "", ""],
    "+14158675311": ["Chewy White", 0, "", ""],
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

    """Respond with the number of text messages sent between two parties."""

    # Increment the counter
    counter = session.get("counter", 0)
    counter += 1

    # Save the new counter value in the session
    session["counter"] = counter

    # get user text
    text = request.values.get('Body', None)


    from_number = request.values.get('From')

    if from_number in patients:
        name = patients[from_number][0]
        counter += 1
    else:
        name = ""

    message = ""

    # New user
    if counter == 1:
        # Ask for name
        message = "\nHi there, what is your full name? counter is {}" \
            .format(counter)

    elif counter == 2:
        # Greeting
        if name == "":
            patients[str(from_number)] = []
            message = "\n\nHi there, {}! Welcome to textMD! What year were you born? counter is {}" \
                .format(text, counter)
        else:
            message = "\n\nWelcome back, {}! What year were you born? counter is {}" \

                .format(name, counter)

    elif counter == 3:
        try: 
            int(str(text))
            patients[str(from_number)][1] = str(text)
            message = "\n\nWhat is your sex (male/female)?"
        except ValueError:
            counter -= 1
            message = "Sorry, we do not understand. Please enter your birth year."

    elif counter == 4:
        if str(text).lower() != "male" or str(text).lower() != "female":
            counter -= 1
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
            message = "Sorry, we do not understand. Please enter your unit number."

    elif counter == 6:
        patients[str(from_number)][3] += ('+' + str(text))
        message = "\n\nWhat is your street suffix? (e.g. street, avenue, trail)"

    elif counter == 7:
        patients[str(from_number)][3] += ('+' + str(text))
        message = "\n\nWhat is your city?"

    elif counter == 8:
        patients[str(from_number)][3] += (',+' + str(text))
        message = "\n\nWhat is your province/state?"
    
    elif counter == 9:
        patients[str(from_number)][3] += (',+' + str(text))
        message = "\n\nThank you! \n {}, {}, {}, {}" \
            .format(patients[str(from_number)][0], patients[str(from_number)][1], patients[str(from_number)][2], patients[str(from_number)][3])
    
    else:
        session.clear()



    # Put it in a TwiML response
    resp = MessagingResponse()
    resp.message(message)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)