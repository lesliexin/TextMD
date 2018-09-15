from twilio.rest import Client
from twilio import twiml
from twilio.rest import TwilioRestClient

account_sid = "AC5d92079d159d055d3a1a28f56a88eab4"
auth_token = "1d4b66048bb25a32931c3c8cdf75e7e3"
client = Client(account_sid, auth_token)

client.messages.create(
        to = "+14165581768",
        from_ = "+16474930709",
        #Example of mass message to send 
        body= "Hey there!",
    )