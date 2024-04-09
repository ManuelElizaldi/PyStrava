# Importing libraries
import pandas as pd
from datetime import date
from sqlalchemy import create_engine
import pandas.io.sql as sqlio
import psycopg2
import json
import sys
sys.path.extend([
    r'C:\Users\Usuario\OneDrive\Desktop\Learning-Testing\PyStrava',
    r'C:\Users\Usuario\OneDrive\Desktop\Learning-Testing\PyStrava\Scripts'
])
from Functions import *
from StravaCredentials import *

# Creating connection to database and creating engine to upload data
db_url = f'postgresql://{username}:{pwd}@{hostname}:{port_id}/{database}'
engine = create_engine(db_url)

conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)

# Creating date variable
today = date.today().strftime('%Y-%m-%d')

# Getting secret code
webbrowser.open(f"https://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri=http://localhost/&approval_prompt=force&scope=profile:read_all,activity:read_all")
code = input("From the web broswer enter the code:")
data['code'] = code

# Getting Strava acccess token
access_token = GetToken(data)

# Getting an updated list of activities
# activities df - this does not include workout details
updated_workouts = retrieve_activities(access_token)

# Creating list to compare against not updated list
updated_workouts_list = list(updated_workouts['id'])

# Creating a cursor and also quering the database to get the current list of workouts from activity table
cur = conn.cursor()
query = "select activity_id from activity"

# Turning query into dataframe - all activities
not_updated_workouts = sqlio.read_sql_query(query, conn)
print('Extracting data from SQL database.')

# Creating a list of ids from the list of activity ids
not_updated_workouts_list = list(not_updated_workouts['activity_id'])

# How many new workouts will be added to database
print('Adding',len(updated_workouts_list) - len(not_updated_workouts_list),'workouts to Database.')

# Creating a list containing the missing workouts
# missing workouts = workouts to be added 
missing_workouts = list(set(updated_workouts_list).difference(not_updated_workouts_list))

# Calling function to extract missing workouts
missing_workouts_json = GetAllWorkouts(missing_workouts, access_token)

# Saving json as checkpoint
with open(r'C:\Users\Usuario\OneDrive\Desktop\Learning-Testing\PyStrava\Outputs\{}-Updated.json'.format(today), 'w') as json_file:
    json.dump(missing_workouts_json, json_file)

# Parsing workout json
missing_workouts_df = CleanWorkoutJson(missing_workouts_json)

# Parsing workout json to create laps table
laps_df = CleanLapsJson(missing_workouts_json)

# Creating the score columns from the workout json 
missing_workouts_df = CreateScoreColumns(missing_workouts_df)

# Using concat to join both updated and not updated dataframes
# all_workouts_df_updated = pd.concat([not_updated_workouts, missing_workouts_df])


# Dividing all_workouts_df to multiple tables to then upload to database
activity, activity_name, activity_coordinates, activity_details, activity_scores = DivideTables(missing_workouts_df)

# Sending data to Postgresql
print('Uploading data to database.')

activity.to_sql('activity', engine, if_exists='append', index=False)
activity_name.to_sql('activity_name', engine, if_exists='append', index=False)
activity_coordinates.to_sql('activity_coordinates', engine, if_exists='append', index=False)
activity_details.to_sql('activity_details', engine, if_exists='append', index=False)
activity_scores.to_sql('activity_scores', engine, if_exists='append', index=False)
laps_df.to_sql('laps', engine, if_exists='append', index=False)

print('Database updated.')

# closing sql database connections
engine.dispose()
cur.close()
conn.close()
print('Connections closed.')