# GetToken
This function will give you the access token requiered to use strava's API.

The argument 'data' contains the following information:

```
        data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type':'authorization_code'
    }
```
   - clinet_id, client_secret are obtained from the project page inside strava. 
   - code is obtained when authoricing access to the app through this website: 'https://www.strava.com/api/v3/oauth/token'.
   - grant_type is just the type of authorization.

# retrieve_activities
This function will give us the table from which we can extract the workout ids from. This table does not contain all the information we need.

   - In the PyStrava.py script this function is used to generate the 'general_table'

# CleanGeneral_Table
This function will clean the 