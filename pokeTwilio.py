from twilio.rest import Client
import config

#   This file holds a function to call a player with a statement. In this case, finding a shiny.
#
#   Setup:
#   Create a config.py folder that includes the following varibles:
#   to_phone_number = 'your number'
#   from_phone_number = 'Twilio number'
#   account_sid = 'from Twilio'
#   auth_token = 'from Twilio'
#
#   Have fun and happy hunting!
#   Cooper Flourens

def found_shiny_call(found_pokemon = '', to_num = config.to_phone_number, from_num = config.from_phone_number): 
    # This function calls a user and says the message "You Found a Shiny!". Usage: found_shiny_call(to_num, from_num). Num format: Country Code + Area Code + Number (example: '+12223333333')
    sentence = 'You Found a Shiny ' + found_pokemon
    formatted = '<Response><Say>' + sentence + '</Say></Response>'
    account_sid = config.account_sid
    auth_token = config.auth_token
    client = Client(account_sid, auth_token)
    client.calls.create(twiml=formatted, to = to_num, from_ = from_num)
    print("Calling Phone Number: "+str(to_num))

# remove this to test function call:  
found_shiny_call()