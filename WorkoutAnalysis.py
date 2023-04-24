# Packages required for this project:
import requests
import pandas as pd
from datetime import date
import webbrowser
from Functions import *

# Importing credentials for Strava's API
from Credentials import StravaCredentials
import Functions

# Setting up parameters for write_to_gsheet function
# service_file_path = r'C:\Users\Manuel Elizaldi\Desktop\Learning-Testing\Workout-Analysis-API\Credentials\pacific-castle-303123-909a5ddcda92.json'
# spreadsheet_id = '1IyEEDEPNtLTigZGgQP0Rhq5_di1Bzit1ZBERn8zNsvE' # Currently setup for testing
service_file_path = r''
spreadsheet_id = '' # Currently setup for testing

# From the StravaCredentials file we are importing we declare the necessary credentials to make API calls.
data = StravaCredentials.data


if data == None:
    client_id = input('Input your Client ID:')
    client_secret = input('Input your Client Secret:')
    data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'code': data['code'],
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
general_table = GetWorkouts(access_token)
# Cleaning the general table
general_table = CleanGeneral_Table(general_table)
# Creating the activities breakdown table -> count of each workout type 
activities_breakdown = CreateActivitiesBreakdown(general_table)
# Creating the General Stats table
general_stats_df = CreateGeneralStatsdf(general_table)

# Creating the list of workout ids
all_workouts_list = list(general_table['id'])

# Testing:
all_workouts_list = all_workouts_list[0:20]

# Creating a json with the detailed view of all workouts
# This includes detailes like calories burned per workout and other variables that the general_table does not have
all_workouts_json = GetAllWorkouts(all_workouts_list,access_token)

# Cleaning the json and converting it into a dataframe. Also we create the workout's round details
all_workouts_df = CleanWorkoutJson(all_workouts_json)

# Creating additional dataframes for specific activities:
# Running type workouts
running_workouts_df = all_workouts_df.loc[all_workouts_df['workout_type'].isin(['Run','TrailRun'])]
# Biking type workouts
biking_workouts_df = all_workouts_df.loc[all_workouts_df['workout_type'].isin(['Ride','MountainBikeRide'])]
# Functional type workouts
functional_workouts_df = all_workouts_df.loc[all_workouts_df['workout_type'].isin(['Functional-Cardio Workout'])]

# Creating a dataframe with general statistics for all sports/workout types
all_workouts_desc = DescribeWorkoutdf(all_workouts_df)
running_workouts_desc = DescribeWorkoutdf(running_workouts_df)
biking_workouts_desc = DescribeWorkoutdf(biking_workouts_df)
functional_workouts_desc = DescribeWorkoutdf(functional_workouts_df)

print('Uploading data to google sheets.')
# Uploading the workout dataframe and the workout description df to google sheets
sheet_name = 'All_Workouts_Table'
WriteToGsheet(service_file_path,spreadsheet_id,sheet_name,all_workouts_df)

sheet_name = 'All_Workouts_Desc'
WriteToGsheet(service_file_path,spreadsheet_id,sheet_name,all_workouts_desc)

sheet_name = 'running_workouts_desc'
WriteToGsheet(service_file_path,spreadsheet_id,sheet_name,running_workouts_desc)

sheet_name = 'biking_workouts_desc'
WriteToGsheet(service_file_path,spreadsheet_id,sheet_name,running_workouts_desc)

sheet_name = 'functional_workouts_desc'
WriteToGsheet(service_file_path,spreadsheet_id,sheet_name,running_workouts_desc)

sheet_name = 'general_stats'
WriteToGsheet(service_file_path,spreadsheet_id,sheet_name,general_stats_df)

sheet_name = 'activities_breakdown'
WriteToGsheet(service_file_path,spreadsheet_id,sheet_name,activities_breakdown)