# Packages required for this project:
import requests
import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
import gspread_dataframe as gd
import pygsheets
from datetime import date
import webbrowser
from Functions import *

# Importing credentials for Strava's API
from Credentials import StravaCredentials
import Functions

# Setting up parameters for write_to_gsheet function
service_file_path = r'C:\Users\Manuel Elizaldi\Desktop\Learning-Testing\Workout-Analysis-API\Credentials\pacific-castle-303123-909a5ddcda92.json'
spreadsheet_id = '1pomkAzlndHBl_czERrwKkoZFUkJRGFjyhRTeoWA6CS4'

# From the StravaCredentials file we are importing we declare the necessary credentials to make API calls.
data = StravaCredentials.data

# Creating date variable
today = date.today().strftime('%B/%d/%Y')

# Accessing the token json to get refresh token and access token
access_token = GetToken(data)

# Getting all workouts general table, from this table we get the list of workout ids
general_table = GetWorkouts(access_token)
# Creating the list of workout ids
all_workouts_list = list(general_table['id'])

# Creating a json with the detailed view of all workouts
# This includes detailes like calories burned per workout and other variables that the general_table does not have
all_workouts_json = GetAllWorkouts(all_workouts_list,access_token)

# Cleaning the json and converting it into a dataframe. Also we create the workout's round details
all_workouts_df = CleanWorkoutJson(all_workouts_json)

# Creating a dataframe with general statistics 
all_workouts_desc = DescribeWorkoutdf(all_workouts_df)

# Uploading the workout dataframe and the workout description df to google sheets
sheet_name = 'All_Workouts_Table'
WriteToGsheet(service_file_path,spreadsheet_id,sheet_name,all_workouts_df)

sheet_name = 'All_Workouts_Desc'
WriteToGsheet(service_file_path,spreadsheet_id,sheet_name,all_workouts_desc)