# Importing libraries
import requests
import pandas as pd
import numpy as np
from datetime import date
from time import sleep
from sqlalchemy import create_engine
import pandas.io.sql as sqlio
# Functions contains all the PyStrava functions 
from Functions import *
# Importing credentials for Strava's API
import sys
sys.path.extend([
    r'C:\Users\Usuario\Desktop\Learning-Testing\PyStrava',
    r'C:\Users\Usuario\Desktop\Learning-Testing\PyStrava\Scripts'
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

# Getting Strava acccess token
access_token = GetToken(data)

# Getting an updated list of activities
activities = retrieve_activities(access_token)

# Creating list to compare against not updated list
updated_workouts = list(activities['id'])

# Opening and reading the All_Workouts_Table <- this will contain our not updated list of workouts
cur = conn.cursor()
query = "select activity_id from activity"

# Parsing json into a dataframe
all_workouts_df = sqlio.read_sql_query(query, conn)

# Creating a list of ids
not_updated_workouts = list(all_workouts_df['activity_id'])

# How many new workouts will be added to database
print('Adding',len(updated_workouts) - len(not_updated_workouts),'workouts to Database')

# Creating a list containing the missing workouts
missing_workouts = list(set(updated_workouts).difference(not_updated_workouts))

# Calling function to extract missing workouts
missing_workouts_json = GetAllWorkouts(missing_workouts,access_token)

# Parsing workout json
missing_workouts_df = CleanWorkoutJson(missing_workouts_json)

# Creating laps table
laps_df = CleanLapsJson(missing_workouts_json)

# Creating the score columns
missing_workouts_df = CreateScoreColumns(missing_workouts_df)

# Using concat to join both updated and not updated dataframes
all_workouts_df_updated = pd.concat([all_workouts_df, missing_workouts_df])

# Sorting by date
all_workouts_df_updated['start_date'] = pd.to_datetime(all_workouts_df_updated['start_date'])
all_workouts_df_updated = all_workouts_df_updated.sort_values(by=['start_date'], ascending=False)

# Dividing all_workouts_df to multiple tables to then upload to database
activity, activity_name, activity_coordinates, activity_details, activity_scores = DivideTables(all_workouts_df)

# Sending data to Postgresql
activity.to_sql('activity', engine, if_exists='replace', index=False)
activity_name.to_sql('activity_name', engine, if_exists='replace', index=False)
activity_coordinates.to_sql('activity_coordinates', engine, if_exists='replace', index=False)
activity_details.to_sql('activity_details', engine, if_exists='replace', index=False)
activity_scores.to_sql('activity_scores', engine, if_exists='replace', index=False)
laps_df.to_sql('laps', engine, if_exists='replace', index=False)

# closing sql database connections
engine.dispose()
cur.close()
conn.close()