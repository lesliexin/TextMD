from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse

# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)

# Try adding your own number to this list!
patients = {
    "+14165581768": ["Leslie Xin", 0, "", ""],
    "+14158675310": ["Finn Smith", 0, "", ""],
    "+14158675311": ["Chewy White", 0, "", ""],
    }

# class Address():

#     def __init__(self, unit, street, city, province):
#         self.unit = unit
#         self.street = street
#         self.city = city
#         self.province = province


# class Patient():

#     def __init__(self, name, birth_year, sex, address):
#         self.name = unit
#         self.street = street
#         self.city = city
#         self.province = province


@app.route("/sms", methods=['GET', 'POST'])
def hello():
    """Respond with the number of text messages sent between two parties."""

    # Increment the counter
    counter = session.get('counter', 0)
    counter += 1

    # Save the new counter value in the session
    session['counter'] = counter

    # get user text
    text = request.values.get('Body', None)


    from_number = request.values.get('From')
    if from_number in patients:
        name = patients[from_number][0]
        counter += 1
    else:
        name = ""

    message = ''

    # new user
    if counter == 1:
        # ask for name 
        message = '\nHi there, what is your full name? counter is {}' \
            .format( counter)

    elif counter == 2:
        # greet user]

        if name == "":
            patients[str(from_number)] = [str(text), 0, ""]
            message = '\n\nHi there, {}! Welcome to textMD! What year were you born? counter is {}' \
                .format(text, counter)

        else:
            message = '\n\nWelcome back, {}! What year were you born? counter is {}' \
                .format(name, counter)

    elif counter == 3:
        patients[str(from_number)][1] = str(text)
        message = '\n\nWhat is your sex?'

    elif counter == 4:
        patients[str(from_number)][2] = str(text)
        message = '\n\nNext we need your address.\nWhat is your unit number?'

    elif counter == 5:
        patients[str(from_number)][3] = str(text)
        message = '\n\nWhat is your street name?'

    elif counter == 6:
        patients[str(from_number)][3] += ('+' + str(text))
        message = '\n\nWhat is your street suffix? (street, avenue, trail)'

    elif counter == 7:
        patients[str(from_number)][3] += ('+' + str(text))
        message = '\n\nWhat is your city?'

    elif counter == 8:
        patients[str(from_number)][3] += (',+' + str(text))
        message = '\n\nWhat is your province/state?'
    
    elif counter == 9:
        patients[str(from_number)][3] += (',+' + str(text))
        message = '\n\nThank you! \n {}, {}, {}, {}' \
            .format(patients[str(from_number)][0], patients[str(from_number)][1], patients[str(from_number)][2], patients[str(from_number)][3])
    
    else:
        session.clear()


    # Build our reply
    # message = '{} has messaged {} {} times.' \
    #     .format(name, request.values.get('To'), counter)

    # Put it in a TwiML response
    resp = MessagingResponse()
    resp.message(message)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)