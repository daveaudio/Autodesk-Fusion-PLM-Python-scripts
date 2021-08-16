# This script is incomplete and not supported
# it is here for reference only for you to use
#
# Reason for the commitment... Autodesk has
# really bad documentation. I only wish I had
# this script a week ago it would have save me
# so much time... Good luck,your gonna need it!
#
# You will need to changE the:
# FLC_item_workspace = "x" to match the ITEMs directory
# of your FLC database. This can be found through the
# website URL address.


import requests
import os
import json

# https://{tenant}.autodeskplm360.net/workspace#workspaceid=22
# FLC_item_workspace = "<INSERT THE NUMBER OF THE DIRECTORY YOUR ITEMS ARE LOCATED AT>"
#
FLC_item_workspace = "22"



token_url = "https://developer.api.autodesk.com/authentication/v1/authenticate"

def get_token(client_id, client_secret):
    """ Retrieve and return an authentication token
    for this app's API key and secret."""

    print("Authenticating...")
    head = "Content-Type: application/x-www-form-urlencoded"
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': 'data:read'
    }
    r = requests.post(token_url, data=data)
    # print(r)
    if 200 == r.status_code:
        token = r.json()['access_token']
    else:
        token = None
    return token

def start_session(user_data):
    X_tenant = user_data[0]
    user_id = user_data[1]
    client_id = user_data[2]
    client_secret = user_data[3]
    token = get_token(client_id, client_secret)
    if len(token) == 0:
        print("Problem accessing the authentication server to obtain a token")
        exit(1)
    print("Token obtained= \n", token)
    print("Attempting to log into " + X_tenant + " server...")

    # log into the tenant and obtain a cookie
    url = "https://" + X_tenant + ".autodeskplm360.net/api/v3/users/@me"
    head = {"Authorization": "Bearer %s" % token, "Accept": "application/json", "X-user-id": user_id,
            "X-Tenant": X_tenant}
    TimeOut = 10
    print("Logging into PLM server '" + X_tenant + "'")
    print(u'Querying {0} ...'.format(url))
    r = requests.get(url, timeout=TimeOut, headers=head)
    if r == 'Fail':
        print("Problem accessing the " + X_tenant + " PLM server")
        exit(2)
    else:
        print("Session ready...")
    return [token, r.cookies]   # Return both the token and cookie for future use

# def request_data(X_tenant, path, api_key, X_user_id):
def get_data_cookie(X_tenant, path, cookie, TimeOut=10):
    host = "https://" + X_tenant + ".autodeskplm360.net"
    url = host + path
    head = {"Accept": "application/json"}
    #timeout = 10
    print(u'Querying {0} ...'.format(url))
    r = requests.get(url, timeout=TimeOut, headers=head, cookies=cookie)
    if r.status_code == 200:        # request succeeded
        response = r
    else:
        print("Request failed to " + url)
        print(r.status_code)
        response = 'Fail'
    return response

def get_data_token(X_tenant, path, token, X_user_id):
    host = "https://" + X_tenant + ".autodeskplm360.net"
    url = host + path
    head = {"Authorization": "Bearer %s" % token,
            "Accept": "application/json",
            'Content-Type': 'application/json',
            "X-user-id": user_id,
            "X-Tenant": X_tenant
            }
    TimeOut = 10
    print(u'Querying {0} ...'.format(url_request))
    r = requests.get(url_request, timeout=TimeOut, headers=head, cookies=cookie)
    if r.status_code == 200:        # request succeeded
        response = r
    else:
        print("Request failed to " + url)
        print(r.status_code)
        response = 'Fail'
    return response


def put_item_cookie(X_tenant, path, body, cookie):
    host = "https://" + X_tenant + ".autodeskplm360.net"
    url = host + path
    head = {"Accept": "application/json",
            "Content-Type": "application/json"
            }

    #key_value_pair = str(key_value_pair)
    #print(body)

#    r = requests.put(url, headers=head, data=json.dumps(body), cookies=cookie)
    #r = requests.put(url, headers=head, data=json.dumps(body), cookies=cookie)
    r = requests.put(url, headers=head, data=json.dumps(body), cookies=cookie)
    return r

def get_wadl(user_data):
    X_tenant = user_data[0]
    user_id = user_data[1]
    cookie = user_data[5]
    path = "/api/rest/application.wadl"
    host = "https://" + X_tenant + ".autodeskplm360.net"
    url_request = host + path
    print("Querying " + url_request)
    TimeOut=10
    r = requests.get(url_request, timeout=TimeOut, cookies=cookie)
    #xmlStr = str(r.content)
    xmldoc = xmltodict.parse(r.content)
    res = json.dumps(str(xmldoc), indent=2, sort_keys=True)
    #file = open("Schema_endpoints.json", "w")
    #file.write(res)
    #file.close()
    print(res)
    return r

def get_report(user_data, report_number):
    X_tenant = user_data[0]
    user_id = user_data[1]
    cookie = user_data[5]
    report_url = "/api/rest/v1/reports/" + str(report_number)
    Time_Out = 60
    res = get_data_cookie(X_tenant, report_url, cookie, Time_Out)
    r = json.loads(res.content)     # remove the cookie data and leave the good stuff
    return r

def get_classification(user_data, part_id):
    X_tenant = user_data[0]
    user_id = user_data[1]
    cookie = user_data[5]
    report_url = "/api/v3/workspaces/" + FLC_item_workspace + "items/" + str(part_id)
    res = get_data_cookie(X_tenant, report_url, cookie)
    r = json.loads(res.content)     # remove the cookie data and leave the good stuff
    return r

def get_attachments(user_data, part_id):
    # api/rest/v1/workspaces/{id}/items/{dmsID}/attachments
    X_tenant = user_data[0]
    user_id = user_data[1]
    cookie = user_data[5]
    #report_url = "/api/rest/v1/workspaces/" + FLC_item_workspace + "/items/" + str(part_id) +"/attachments"
    report_url = "/api/v3/workspaces/" + FLC_item_workspace + "/items/" + str(part_id) + "/attachments"
    res = get_data_cookie(X_tenant, report_url, cookie)
    r = json.loads(res.content)     # remove the cookie data and leave the good stuff
    return r

def get_key (path):
    path_split = path['__self__'].split("/")
    key = path_split[len(path_split)-1]
    return key

def change_item_detail(user_data, item_id, item_detail, new_value):
    X_tenant = user_data[0]
    #user_id = user_data[1]
    cookie = user_data[5]
    # Get current value
    path = "/api/rest/v1/workspaces/" + FLC_item_workspace + "/items/" + str(item_id)
    res = get_data_cookie(X_tenant, path, cookie)
    r = json.loads((res.content).decode('utf-8'))       # convert to JSON format
    # Check user details are in PLM data
    #all_details = r['sections'][0]['fields']       # for rest/V3

    # 'rest/v1' version
    curr_version = r['item']['details']['versionID']
    all_details = r['item']['metaFields']['entry']
    key_body = ()       # define a list
    continue_flag = False
    for i in all_details:
        # Build key : value pairs
        item_key = i['key']
        item_value = i['fieldData']['value']
        if item_key == item_detail:
            print("Found '" + item_detail + "' in PLM")
            key_body = key_body + ({"key": item_key, "value": new_value},)  # add to list
            found_entry = i
            continue_flag = True
        else:
            key_body = key_body + ({"key": item_key, "value": item_value},)  # add to list

    # check to see if the part has already had its items changed
    #if found_entry

    # When the item details are not found
    if continue_flag == False:
        print("<ERROR> Could not find " + item_detail + " in the PLM schema.")
        print("Available item details are:")
        for i in all_details:
            print("'" + i['key'] + "', ", end=" "),
        exit(0)

    body = {"versionID": curr_version,
                "metaFields":{ "entry": [i for i in key_body]} }
    print(body)
    print("Current entry:")
    print(found_entry['key'] + " = " + found_entry['fieldData']['value'])

    # update the item value
    res = put_item_cookie(X_tenant, path, body, cookie)
    print("Changing to:")
    print(found_entry['key'] + " = " + new_value)
    print(res)
    print(res.content)
    # Verify the change in PLM
    print("Checking the data on PLM :")
    res = get_data_cookie(X_tenant, path, cookie)
    r = json.loads((res.content).decode('utf-8'))       # convert to JSON format
    v1 = r['item']['metaFields']['entry']
    for i in v1:
        if i['key'] == item_detail:
            verify_value = i['fieldData']['value']
    if verify_value == new_value:
        print("Update suceeded!")
        res = "PASS"
    else:
        print("Update failed")
        res = "FAIL"
    return res

def list_workspaces(user_data):
    X_tenant = user_data[0]
    user_id = user_data[1]
    cookie = user_data[5]
    path = "/api/v3/workspaces/"
    res = get_data_cookie(X_tenant, path, cookie)
    r = (res.content).decode('utf-8')
    return r

def list_workspaces_v1(user_data):
    X_tenant = user_data[0]
    user_id = user_data[1]
    cookie = user_data[5]
    path = "/api/rest/v1/workspaces/"
    res = get_data_cookie(X_tenant, path, cookie)
    r = (res.content)       # return result as a
    #r = (res.content).decode('utf-8')   # return result as a string
    return r



#######################################################################
# The following scripts are currently under development



# Working from:
# https://forums.autodesk.com/t5/fusion-360-manage-forum/posting-an-attachment-to-the-fusion-lifecycle-api-using-a-web/td-p/8922502

def attach(X_tenant, path, api_key, X_user_id, fileName):
    #host = "https://" + X_tenant + ".autodeskplm360.net"
    #url_request = host + path
    #print(url_request)

    url_request = path

    head1 = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer %s" % api_key,
        "X-user-id": X_user_id,
        "X-Tenant": X_tenant
    }
    # Step 1 - add meta data
    body1 = {
        "fileName": fileName,
        "resourceName": "Photo_" + fileName,
        "description": fileName
    }
    # step 2 - send data
    #files = {'upload_file': open(fileName, 'rb')}
    files = open(fileName, 'rb')
    body2 = {
        'Content-Type': 'application/json',
        'Content - Disposition': 'form-data; name="itemDetail";filename = "' + fileName + '"',
        'upload_file': files

    }





    # step 3 - update data
    file_size = os.path.getsize(fileName)
    # OCTOPART_IMAGE1
    #15366
    data3 = {
        "Content - Disposition": '*; key=OCTOPART_IMAGE1; filename=' + fileName + ', size=' + str(file_size)
    }
    print(data3)
    data4 = {
        "Content - Disposition": "*;",
        "key": "OCTOPART_IMAGE1",
        "filename": fileName,
        "size": str(file_size)
    }

    requests.post(url_request, headers=head1, json=body1)
    requests.put(url_request, data=body2)
    r = requests.patch(url_request, data=data4)
    print(r)
    if r.status_code == 200:
        response = r
    else:
        response = 'Fail'
    return response






def attach_picture(user_data, item_id, picture):
    X_tenant = user_data[0]
    user_id = user_data[1]
    token = user_data[4]

    item_url = item_id  # remove this later back to just an item number
    #item_url = "/api/rest/v1/workspaces/"+FLC_item_workspace+"/items/" + str(item_id) + "/attachments"
    #/ api / v3 / workspaces /: wsId: / items /: itemId: / attachments
    #item_url = "/api/v3/workspaces/"+FLC_item_workspace+"/items/" + str(item_id) + "/attachments"
    print("Trying to:\nattach " + picture + "\nto " + item_url)
    attach(X_tenant, item_url, token, user_id, picture)
    # attach a file use



# to upload a web picture:
# '&lt;img src=&quot;https://sigma.octopart.com/68815859/image/Yageo-RC0402FR-074R7L.jpg&quot; style=&quot;height:180px;&quot;&gt;'

