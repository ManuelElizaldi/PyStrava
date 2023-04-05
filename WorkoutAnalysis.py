# Packages required for this project:
import requests
import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
import gspread_dataframe as gd
import pygsheets
from datetime import date
import webbrowser
import Functions

# Importing credentials for Strava's API
from Credentials import StravaCredentials

# Setting up parameters for write_to_gsheet function
service_file_path = r'C:\Users\Manuel Elizaldi\Desktop\Learning-Testing\Workout-Analysis-API\Credentials\pacific-castle-303123-909a5ddcda92.json'
spreadsheet_id = '1pomkAzlndHBl_czERrwKkoZFUkJRGFjyhRTeoWA6CS4'

# From the StravaCredentials file we are importing we declare the necessary credentials to make API calls.
data = StravaCredentials.data
webbrowser.open(f"https://www.strava.com/oauth/authorize?client_id={data['client_id']}&response_type=code&redirect_uri=http://localhost/&approval_prompt=force&scope=profile:read_all,activity:read_all")
code = input("From the web broswer enter the code:")

# Creating date variable
today = date.today().strftime('%B/%d/%Y')

# Getting refresh token
token = requests.post(url= 'https://www.strava.com/api/v3/oauth/token',data=data).json()

# Accessing the token json to get refresh token and access token
refresh_token = token['refresh_token']
access_token = token['access_token']

# Setting up url and page
# This API request gives us the list of activities. 
# The table lacks certain details that we will get from another API request
page = 1
url = "https://www.strava.com/api/v3/activities"
access_token = token['access_token']
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
    activities = activities.append(r)
    
    page += 1