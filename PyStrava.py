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
service_file_path = r'C:\Users\Manuel Elizaldi\Desktop\Learning-Testing\PyStrava\Credentials\pacific-castle-303123-909a5ddcda92.json'
spreadsheet_id = '1IyEEDEPNtLTigZGgQP0Rhq5_di1Bzit1ZBERn8zNsvE' # Currently setup for testing
#service_file_path = r''
#spreadsheet_id = '' # Currently setup for testing

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
print('Generating Genearl Table.')

# This API request gives us the general list of activities. 
# The table lacks certain details that we will get from another API request 
page = 1
url = "https://www.strava.com/api/v3/activities"
#access_token = token['access_token']
#access_token = token
# Create the dataframe ready for the API call to store your activity data
activities = pd.DataFrame()
while True:
    # get page of activities from Strava
    print('Getting page number:',page)
    r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
    r = r.json()
    print(f'Extraction of page {page} Complete')
    # if no results then exit loop
    if (not r):
        print('Extration Done')
        break
    r = pd.json_normalize(r)
    activities = activities.append(r) # type: ignore
    
    page += 1

    clean_activities = activities[['id',
    'name',
    'distance',
    'elapsed_time',
    'total_elevation_gain',
    'sport_type',
    'start_date','achievement_count',
    'athlete_count',
    'start_latlng',
    'end_latlng',
    'average_speed',
    'max_speed',
    'average_temp',
    'average_heartrate',
    'max_heartrate',
    'average_cadence',
    'elev_high',
    'elev_low']]

general_table = clean_activities.copy()
general_table = general_table.rename(columns={'elapsed_time':'workout_time_sec'})
general_table.to_csv(r'C:\Users\Manuel Elizaldi\Desktop\Learning-Testing\PyStrava\Outputs\test.csv')
print('General Table created successfully.')

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
print('Extracting all workouts.')
all_workouts_json = GetAllWorkouts(all_workouts_list,access_token)

# Cleaning the json and converting it into a dataframe. Also we create the workout's round details
all_workouts_df = CleanWorkoutJson(all_workouts_json)
all_workouts_df.to_csv(r'C:\Users\Manuel Elizaldi\Desktop\Learning-Testing\PyStrava\Outputs\test.csv')
# Creating additional dataframes for specific activities:
# Running type workouts
running_workouts_df = all_workouts_df.loc[all_workouts_df['sport_type'].isin(['Run','TrailRun'])]
# Biking type workouts
biking_workouts_df = all_workouts_df.loc[all_workouts_df['sport_type'].isin(['Ride','MountainBikeRide'])]
# Functional type workouts
functional_workouts_df = all_workouts_df.loc[all_workouts_df['sport_type'].isin(['Functional-Cardio Workout'])]

# Creating a dataframe with general statistics for all sports/workout types
print('Creating description of workouts.')
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