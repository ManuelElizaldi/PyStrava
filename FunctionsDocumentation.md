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

   - In the PyStrava.py script this function is used to generate the dataframe 'general_table'.
   - Also, from the output of this function we obtain the list of workout ids that is used on the 'GetAllWorkouts' function. 

# CleanGeneral_Table
The argument requiered for this function is the 'general_table' table generated from the function 'retrieve_activities'.

This function will clean the 'general_table', the following actions are taken:
   - Calculate the approximate calories burned.
   - Converts distance to kilometers.
   - Turns time from ms to minutes.
   - Formats dates.
   - In the sport_type, changes the value 'Workout' to 'Functional-Cardio Workout'

# CreateActivitiesBreakdown
The argument requiered for this function is the 'general_table' table generated from the function 'retrieve_activities'.

This table provides a breakdown of workout counts for each sport, along with the total of workouts recorded up to the current date.

# CreateGeneralStatsdf
The argument requiered for this table is the 'general_table' generated from the function 'retrieve_activities'.

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
      - Normally we use the entire list of workouts ids from the 'general_table' table.
   - Access token

This function will output a json with all the workouts and the details that are not present in the 'general_table' table. This information can be used to build dashboards and statistical models.

# CleanWorkoutJson
This function will clean the json output from the function 'GetAllWorkouts'. The following actions will be performed:
   - Convert distance to kilometers. 
   - Change name of column moving_time to workout_time_min.
   - Convert time from seconds to minutes. 
   - Format date.
   - Converts distance from meters to kilometers.
   - Format longitude and latitude. 
   - Filters out columns not being used in the script. 
   - Extract the laps for each workout and performes formatting calculations. Laps then are added as a column to the output table. 

# CreateScoreColumns
This function takes the DataFrame ('df') table output from the 'CleanWorkoutJson' function as an argument. It calculates the effort scores based on each workout's metrics.

# EffortLevelBreakdown
This function takes the 'df' table as an argument and generates a detailed breakdown description of the workouts. It includes various pieces of information, such as:
   - First workout recorded
   - Last workout recorded
   - Average workout duration in minutes
   - Average calories burned
   - Average distance ran
   - Average heartrate 
   - Average speed
   - Average max speed
   - Count of total workouts recorded
   - Average laps per workout