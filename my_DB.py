#!/usr/bin/env python3
import PLM

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ENTER YOUR DETAILS HERE:
tenant = "abcdefghijklmnop"     # name of your tenant without the extra info "https://'{tenant}'.autodeskplm360.net"

# Forge Authentication server 'APP' details
client_id = "AbCdEfG12345678"
client_secret = "A1b2C3Dkajsfhalshitdf"

# USER DETAILS
user_id = "me@myemailaddress.com"

# Don't forget to change the <FLC_item_workspace = ""> pointer in the PLM.py file to point to your parts workspace!

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Collect all the user data together
user_data = (tenant, user_id, client_id, client_secret)
# Start a PLM session
reply = PLM.start_session(user_data)
token = reply[0]
cookie = reply[1]

if len(token) == 0:
    print("No reply from Authentication server...")
    exit(0)
user_data = user_data + (token,)  # adding the token to the user data for future queries
user_data = user_data + (cookie,)
# Run your stuff here >>>>



# report_number = 12
# res = PLM.get_report(user_data, report_number)
# print(res)

