# Packages required for this project:
import requests
import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
import gspread_dataframe as gd
import pygsheets
from datetime import date
import webbrowser

# Importing credentials for Strava's API
from Credentials import StravaCredentials

# From the StravaCredentials file we are importing 
data = StravaCredentials.data
webbrowser.open(f"https://www.strava.com/oauth/authorize?client_id={data['client_id']}&response_type=code&redirect_uri=http://localhost/&approval_prompt=force&scope=profile:read_all,activity:read_all")
data['code'] = input("From the web broswer enter the code:")