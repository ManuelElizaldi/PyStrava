# Packages required for this project:
import requests
import pandas as pd
from datetime import date
import webbrowser
import json
# Functions contains all the PyStrava functions 
from Functions import *
# Importing credentials for Strava's API
import sys
sys.path.append(r'C:\Users\Manuel Elizaldi\Desktop\Learning-Testing\PyStrava\Credentials')
sys.path.append(r'C:\Users\Usuario\Desktop\Learning-Testing\PyStrava')
import StravaCredentials
# Setting up parameters for write_to_gsheet function
service_file_path = r'C:\Users\Manuel Elizaldi\Desktop\Learning-Testing\PyStrava\Credentials\pacific-castle-303123-909a5ddcda92.json'
# spreadsheet_id = '1IyEEDEPNtLTigZGgQP0Rhq5_di1Bzit1ZBERn8zNsvE' # Currently setup for testing
# use this spreadsheet id to find google sheets file 
spreadsheet_id = '1pomkAzlndHBl_czERrwKkoZFUkJRGFjyhRTeoWA6CS4' # spreadsheet connected to dashboard in looker 

# From the StravaCredentials file we are importing we declare the necessary credentials to make API calls.
try:
    data = StravaCredentials.data
except:
    if data == None:
        client_id = input('Input your Client ID:')
        client_secret = input('Input your Client Secret:')
        webbrowser.open(f"https://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri=http://localhost/&approval_prompt=force&scope=profile:read_all,activity:read_all")
        code = input("From the web broswer enter the code:")
        data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type':'authorization_code'
    }

# Creating date variable
today = date.today().strftime('%B/%d/%Y')

# Accessing the token json to get refresh token and access token
# Getting refresh and access token
token = requests.post(url= 'https://www.strava.com/api/v3/oauth/token',data=data).json()

# Accessing the token json to get refresh token and access token
refresh_token = token['refresh_token']
access_token = token['access_token']

# Getting all workouts general table, from this table we get the list of workout ids
print('Generating General Table.')

# This API request gives us the general list of activities. 
# The table lacks certain details that we will get from another API request 
activities = retrieve_activities(access_token)
general_table = activities.copy()
general_table = general_table.rename(columns={'elapsed_time':'workout_time_sec'})
#general_table.to_csv(r'C:\Users\Manuel Elizaldi\Desktop\Learning\PyStrava\Outputs\test.csv')
print('General Table created successfully.')

# Cleaning the general table
general_table = CleanGeneral_Table(general_table)

# Creating the list of workout ids
all_workouts_list = list(general_table['id'])

# Testing:
# all_workouts_list = list(general_table['id'][0:150])

# Testing:
all_workouts_list = all_workouts_list[0:150]

# Creating a json with the detailed view of all workouts
# This includes detailes like calories burned per workout and other variables that the general_table does not have
print('Extracting all workouts.')
all_workouts_json = GetAllWorkouts(all_workouts_list,access_token)

# Saving json as checkpoint
# with open(r'C:\Users\Usuario\Desktop\Learning-Testing\PyStrava\Outputs\test_all_workouts.json', 'w') as json_file:
#     json.dump(all_workouts_json, json_file)

# Cleaning the json and converting it into a dataframe. Also we create the workout's round details
all_workouts_df = CleanWorkoutJson(all_workouts_json)

# Creating effort score columns
print('Calculating level of effort columns.')
all_workouts_df = CreateScoreColumns(all_workouts_df)

# saving dataframe
all_workouts_df.to_csv(r'C:\Users\Usuario\Desktop\Learning-Testing\PyStrava\Outputs\all_workouts_df.csv')

# # Creating a dataframe with general statistics for all sports/workout types
print('Creating description of workouts.')
all_workouts_desc = DescribeWorkoutdf(all_workouts_df)

# Generating the table that shows how many workouts for each effort level 
all_workouts_effort_table = EffortLevelBreakdown(all_workouts_df)

print('Uploading data to google sheets.')
# Uploading the workout dataframe and the workout description df to google sheets
# Change the sheet name to the name in your own google sheet
sheet_name = 'All_Workouts_Table'
WriteToGsheet(service_file_path,spreadsheet_id,sheet_name,all_workouts_df)

sheet_name = 'All_Workouts_Desc_Table'
WriteToGsheet(service_file_path,spreadsheet_id,sheet_name,all_workouts_desc)