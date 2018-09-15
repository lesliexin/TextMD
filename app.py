from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse

# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)

# Try adding your own number to this list!
callers = {
    "+14165581768": "Leslie",
    "+14158675310": "Finn",
    "+14158675311": "Chewy",
}


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
    if from_number in callers:
        name = callers[from_number]
        counter += 1
    else:
        name = ""

    message = ''

    # new user
    if counter == 1:
        # ask for name 
        message = 'Hi there, what is your name? counter is {}' \
            .format( counter)

    elif counter == 2:
        # greet user]

        if name == "":
            callers[str(from_number)] = str(text)
            message = 'Hi there, {}! Welcome to textMD! counter is {}' \
                .format(text, counter)

        else:
            message = 'Welcome back, {}! counter is {}' \
                .format(name, counter)

    else:
        message = 'counter is {}' \
            .format(name, counter)
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