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