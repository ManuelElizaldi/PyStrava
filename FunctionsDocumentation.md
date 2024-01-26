# GetToken
This function retrieves the access token.

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
This function will output the table from which we can extract the workout IDs. The only argument requiered is the access token.

   - In the PyStrava.py script this function is used to generate the dataframe 'general_table'

# CleanGeneral_Table
This function will clean the 'general_table', the following actions are taken:
   - Calculate the approximate calories burned.
   - Converts distance to kilometers.
   - Turns time from ms to minutes.
   - Formats dates.
   - In the sport_type, changes the value 'Workout' to 'Functional-Cardio Workout'

# CreateActivitiesBreakdown
This table provides a breakdown of workout counts for each sport, along with the total of workouts recorded up to the current date.

# CreateGeneralStatsdf
The argument requiered for this table is the 'general_table' generated from the function 'retrieve_activities'

This function will create a pivot table containing the following information about the activities:
  - Date of the first recorded workout.
  - Date of the last recorded workout.
  - Average workout duration in minutes.
  - Approximate average calories burned per workout.
  - Average distance ran.
  - Average distance biked.

# GetAllWorkouts
The argumetns requiered for this function are:
   - List of workout ids you want to extract
      - Normally we use the entire list of workouts ids from the general table 
   - Access token

This function will 