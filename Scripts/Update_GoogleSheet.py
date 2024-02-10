
import requests
import pandas as pd
import numpy as np
import pygsheets
import datetime
from datetime import date
import json
import webbrowser
from time import sleep
import gspread
from oauth2client.service_account import ServiceAccountCredentials


from Functions import *
# Importing credentials for Strava's API
from Credentials.StravaCredentials import data

# Importing credentials to get access token
data = StravaCredentials.data

# Getting Strava acccess token
access_token = GetToken(data)

# Getting an updated list of activities
activities = retrieve_activities(access_token)
# Creating list to compare against not updated list
updated_workouts = list(activities['id'])

# Setting up parameters for gspread - updating google sheet
service_file_path = r'C:\Users\Manuel Elizaldi\Desktop\Learning-Testing\PyStrava\Credentials\pacific-castle-303123-909a5ddcda92.json'
spreadsheet_id = '1pomkAzlndHBl_czERrwKkoZFUkJRGFjyhRTeoWA6CS4'

# My scope determines what we want to do with the google api
myscope = ['https://spreadsheets.google.com/feeds', 
            'https://www.googleapis.com/auth/drive']

# Authentication
mycred = ServiceAccountCredentials.from_json_keyfile_name(service_file_path,myscope) # type: ignore
client = gspread.authorize(mycred)

# Opening and reading the All_Workouts_Table <- this will contain our not updated list of workouts
mysheet = client.open('workout-data').sheet1
list_of_row = mysheet.get_all_records()

# Parsing json into a dataframe
all_workouts_df = pd.json_normalize(list_of_row)

# Creating a list of ids
not_updated_workouts = list(all_workouts_df['activity_id'])

# How many new workouts will be added to Google Sheet
print('Adding',len(updated_workouts) - len(not_updated_workouts),'workouts to Google Sheet')

# Creating a list containing the missing workouts
missing_workouts = list(set(updated_workouts).difference(not_updated_workouts))

# Calling function to extract missing workouts
missing_workouts_json = GetAllWorkouts(missing_workouts,access_token)

# Parsing workout json
missing_workouts_df = CleanWorkoutJson(missing_workouts_json)

# Creating the score columns
missing_workouts_df = CreateScoreColumns(missing_workouts_df)

# Using concat to join both updated and not updated dataframes
all_workouts_df_updated = pd.concat([all_workouts_df, missing_workouts_df])

# Sorting by date
all_workouts_df_updated['start_date'] = pd.to_datetime(all_workouts_df_updated['start_date'])
all_workouts_df_updated = all_workouts_df_updated.sort_values(by=['start_date'], ascending=False)

# Uploading to Google Sheet
sheet_name = 'All_Workouts_Table'
WriteToGsheet(service_file_path,spreadsheet_id,sheet_name,all_workouts_df_updated)