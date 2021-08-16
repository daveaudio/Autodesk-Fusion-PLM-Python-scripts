# Autodesk-Fusion-PLM-API-Python-scripts
Python scripts for accessing data from Autodesk's Fusion lifecycle (PLM) system

You should already have the Fusion lifecycle database setup and have web browser access

Step 1 - Get yourself registered here:

https://forge.autodesk.com/

Step 2 - Make an "app" and get the following information:
* CLIENT ID

* CLIENT SECRET

This will be used to obtain a session token from the authorisation server.
The session token will enable access to your Fusion PLM tenent it will only be accessible by you.

Step 3 - write some gosh darn Python!

It is recommended to use the start code from the "my_DB.py" as it already has everything you need to get started quickly.

"import PLM" will give access to the scripts.

Access the scripts from your python program with the following:

`reply = PLM.start_session(user_data)`

  Where "user_data" is defined as tuple containing:
  
    `user_data[0] = Tenant` #(use the name without the extra "https://'{tenant}'.autodeskplm360.net" stuff)

    `user_data[1] = eMail address` # used by the tenant to log you into the system
    
    `user_data[2] = Client ID` # from the Forge website
    
    `user_data[3] = Client secret` # from the Forge website
    
  Description:
  
    This will request the session token, and also obtain a session cookie for all subsequent requests The reply from this function gives:
      
        `reply[0] = session token`
        
        `reply[1] = session cookie`
        
   It is recommended to add both of these session Ids back into the user_data as it is used for the rest functions.
   
   `user_data = user_data + (reply[0],)  # Session Token now in user_data[4]`
   
   `user_data = user_data + (reply[1],)  # Session Cookie now in user_data[5]`
   
   There is probably a better way to handle this, but... well... meh!

***

![git](https://user-images.githubusercontent.com/21262744/129590612-90c55312-1e7c-4573-9dad-4faed9bfd271.png)   

To get access to your parts in the database you will need to change the following line to match your database schema:

For instance my schema has the "ITEMS and BOMs" at workspace number 22.

My URL gives: "https://{tenant}.autodeskplm360.net/workspace#workspaceid=22". Which means I change this to:

`FLC_item_workspace = "22"`

You should be able to find the workspace through the website address... get use to this, you are going to use it a lot with this API.

***

Here is a list of the other options:

`reply = PLM.get_wadl(user_data)` # gets a list of all the commands available in your PLM system

`reply = PLM.list_workspaces(user_data)`  # Lists all the workspaces in your schema. Uses API version 3

`reply = PLM.list_workspaces_v1(user_data)` # List all the workspaces in your schema. Uses API version 1

`reply = PLM.get_report(user_data, report_number)` # returns a report already setup on the PLM system

`reply = PLM.get_classification(user_data, part_id)` # returns all the information for a part. Requires the database part_ID of the part not the part name

`reply = PLM.change_item_detail(user_data, item_id, item_detail, new_value)` # edits the part with new information


***

Under development:

`reply = PLM.attach()`  # Attach a file to a part

`reply = PLM.attach_picture()`  # Attach a picture to a part - (file or web)

