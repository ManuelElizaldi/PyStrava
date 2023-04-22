import requests
import pandas as pd
import pygsheets
import time
from time import sleep 
from datetime import date

# Setting up parameters for write_to_gsheet function
service_file_path = r'C:\Users\Manuel Elizaldi\Desktop\Learning-Testing\Workout-Analysis-API\Credentials\pacific-castle-303123-909a5ddcda92.json'
spreadsheet_id = '1pomkAzlndHBl_czERrwKkoZFUkJRGFjyhRTeoWA6CS4'

# Creating function that returns the access token that is used in the other api calls
def GetToken(data):
    token = requests.post(url= 'https://www.strava.com/api/v3/oauth/token',data=data).json()
    access_token = token['access_token']
    
    return access_token

# Function that returns the general list of activities. This list lacks certain details that we can get from another api call
def GetWorkouts(access_token):    
    page = 1
    url = "https://www.strava.com/api/v3/activities"
    # Create the dataframe ready for the API call to store your activity data
    activities = pd.DataFrame()
    print('Extracting worokouts for general table.')
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
        
        clean_activities = clean_activities.rename(columns={'elapsed_time':'workout_time_sec'})
        
        return clean_activities

# Function that cleans the output from the function GetWorkouts()
def CleanGeneral_Table(general_table):
    print('Cleaning General Table')
    general_table['aprox_calories_burned'] = round((general_table['workout_time_sec']/60) * ((0.6309*general_table['average_heartrate']) + (0.1988*80) + (0.2017*26 - 55.0969)) / 4.184,0)

    # from meters to kilometers
    general_table[['distance']] = round(general_table['distance']/1000,2)

    # from seconds to minutes
    general_table['workout_time_min'] = round(general_table['workout_time_sec']/60,2)

    # Fix start_date column into the correct format
    general_table[["start_date"]] = pd.to_datetime(general_table['start_date']).dt.date

    # Changing name of workout type => Workout
    general_table['sport_type'] = general_table['sport_type'].replace({'Workout':'Functional-Cardio Workout'})
    
    return general_table

# This function will create a dataframe/pivot table with the count of every sport type
def CreateActivitiesBreakdown(general_table):
    print('Creating Activities Breakdown table')
    today = date.today().strftime('%B/%d/%Y')
    # Variables for activities breakdown dataframe 
    today_msg = f'Total workouts as of {today}'
    total_workouts = len(general_table)

    # Breakdown of workout types:
    new = [today_msg,total_workouts]
    activities_breakdown = general_table['sport_type'].value_counts().rename_axis('Sport').reset_index(name='Count')
    activities_breakdown = activities_breakdown.append(pd.Series(new, index=['Sport','Count']), ignore_index=True)
    return activities_breakdown

def CreateGeneralStatsdf(general_table):
    print('Creating the Genearl Statistics table.')
    # Creating additional dataframes for specific activities:
    # Running type workouts
    running_activities = general_table.loc[general_table['sport_type'].isin(['Run','TrailRun'])]

    # Biking type workouts
    biking_activities = general_table.loc[general_table['sport_type'].isin(['Ride','MountainBikeRide'])]

    # Functional type workouts
    functional_activities = general_table.loc[general_table['sport_type'].isin(['Functional-Cardio Workout'])]
    first_recorded_workout = min(general_table['start_date'])
    most_recent_workout=max(general_table['start_date'])
    average_workout_duration=round(general_table['workout_time_min'].mean(),2)
    aprox_average_calories_burned_per_workout=round(general_table['aprox_calories_burned'].mean(),0)
    average_distance_ran=round(running_activities['distance'].mean(),0)
    average_biking_distance=round(biking_activities['distance'].mean(),0)

    # Creating dataframe from general statistics variables
    # Create the DataFrame
    general_stats_df = pd.DataFrame({
    'First Workout':first_recorded_workout,
    'Most Recent Workout': most_recent_workout,
    'Average Workout Duration in Minutes':average_workout_duration,
    'Approximate Average Calories Burned Per Workout':aprox_average_calories_burned_per_workout,
    'Average Distance Ran in Kilometers':average_distance_ran,
    'Average Biking Distance in Kilometers':average_biking_distance
    },index=['Info'])

    # Transposing dataframe, setting new index and column
    # general_stats_df = general_stats_df.T
    # general_stats_df = general_stats_df.reset_index()
    # general_stats_df = general_stats_df.rename(columns={'index':'Info','Info':'Data'})
    print(f'First recorded workout: {first_recorded_workout}')
    print(f'Most recent workout: {most_recent_workout}')
    return general_stats_df
    
# Get detailed view of workouts function:
# This function will get the data for each workout, if it reaches the API request limit it will stop the process
# The API rate limit allows us to do 100 requests for each 15 mintues. To prvent passing this limit we only grab -
# - the most recent 100 workouts from each list.
def GetWorkoutData(workout_list):
    workout_info = []
    workout_num = 1
    if len(workout_list)>100:
        print('This workout list is too large, reducing to the 100 most recent workouts.')
        workout_list = workout_list[:100]
        for i in workout_list:
            print('Extracting workout:', workout_num)
            req = requests.get(url = f'https://www.strava.com/api/v3/activities/{i}?access_token='+access_token)
            if req.status_code == 200:
                req = req.json()
                workout_info.append(req)
                workout_num += 1
            else:
                print('Error in authorization or API limit exceeded, stopping extraction')
                break
    else:
        for i in workout_list:
            print('Extracting workout:',workout_num)
            req = requests.get(url = f'https://www.strava.com/api/v3/activities/{i}?access_token='+access_token)
            if req.status_code == 200:
                req = req.json()
                workout_info.append(req)
                workout_num += 1
            else:
                print('Error in authorization or API limit exceeded, stopping extraction')
                break
    return workout_info


# This function is very similar to the GetWorkoutData() but it has a built in timer that waits 15 minutes when it reaches the API limit 
def GetAllWorkouts(workout_list, access_token):
    workout_info = []
    workout_num = 1
    rate_limit = 100
    time_interval = 900  # 15 minutes = 900 seconds
    wait_time = ((len(workout_list)/100) * 900)/60

    print(f'Extracting all workouts, due to the API rate limit, this will take {wait_time} minutes to run.')
    for i in workout_list:
        print('Extracting workout:', workout_num)
        req = requests.get(url=f'https://www.strava.com/api/v3/activities/{i}?access_token='+access_token)
        if req.status_code == 200:
            req = req.json()
            workout_info.append(req)
            workout_num += 1
        elif req.status_code == 429 and 'message' in req.json() and req.json()['message'] == 'Rate Limit Exceeded':
            # If rate limit exceeded error is received, wait for 15 minutes before continuing
            print('Rate limit exceeded. Waiting for 15 minutes...')
            time.sleep(time_interval)
        else:
            print('Error occurred during API request:', req.status_code, req.json())
            break

        # Pause after every 100 iterations and wait for 15 minutes
        if workout_num % rate_limit == 0:
            print(f'Reached rate limit of {rate_limit} requests. Sleeping for {int(time_interval/60)} minutes.')
            time.sleep(time_interval)

    return workout_info

# This function will parse the workout json, grab the relevant columns, clean the units and create a lap counter for the final dataframe
def CleanWorkoutJson(workout_json):
    df = pd.json_normalize(workout_json)
    df[['distance']] = round(df['distance']/1000,2)
    df['workout_time_min'] = round(df['elapsed_time']/60,2)
    df[["start_date"]] = pd.to_datetime(df['start_date']).dt.date
    df = df.rename(columns={'id':'activity_id'})
    df = df[['activity_id',
               'name',
               'start_date',
               'sport_type',
               'distance',
               'workout_time_min',
               'calories',
               'total_elevation_gain',
               'start_latlng',
               'end_latlng',
               'average_speed',
               'max_speed',
               'average_temp',
               'average_heartrate',
               'max_heartrate']]
    
    workout_laps = pd.json_normalize(workout_json,'laps')
    workout_laps = workout_laps[['activity.id','name','elapsed_time','distance','average_heartrate','max_heartrate','average_speed','max_speed']]
    workout_laps = workout_laps.rename(columns={'activity.id':'activity_id',
                                                'name':'lap',
                                                'elapsed_time':'lap_elapsed_time_min',
                                                'distance':'lap_distance',
                                                'average_heartrate':'lap_average_heartrate',
                                                'max_heartrate':'lap_max_heartrate',
                                                'average_speed':'lap_average_speed',
                                                'max_speed':'lap_max_speed'})
    workout_laps['lap_elapsed_time_min'] = round(workout_laps['lap_elapsed_time_min']/60,2)
    workout_laps['lap_distance'] = round(workout_laps['lap_distance']/1000,2)

    avg_time_per_lap = workout_laps.groupby('activity_id').mean()
    avg_time_per_lap = avg_time_per_lap.reset_index()
    avg_time_per_lap = avg_time_per_lap[['activity_id','lap_elapsed_time_min']]
    avg_time_per_lap = avg_time_per_lap.rename(columns={'lap_elapsed_time_min':'avg_time_per_lap'})    
    
    lap_counter = workout_laps['activity_id'].value_counts().rename_axis('activity_id').reset_index(name='lap_count')
    
    lap_stats = avg_time_per_lap.merge(lap_counter,on='activity_id')
    
    merged = df.merge(lap_stats, on = 'activity_id')
    merged['lap_count'] = pd.to_numeric(merged['lap_count'])
    return merged

# This function gives us a general description of the list of workouts
def DescribeWorkoutdf(workout_df):
    first_workout = min(workout_df['start_date'], default="EMPTY")
    last_workout=max(workout_df['start_date'], default="EMPTY")
    avg_workout_duration=round(workout_df['workout_time_min'].mean(),2)
    avg_calories_burned_per_workout=workout_df['calories'].mean()
    avg_distance=round(workout_df['distance'].mean(),0)
    workout_counter = len(workout_df)
    avg_laps = round(workout_df['lap_count'].mean(),0)

    # Creating dataframe from general statistics variables
    # Create the DataFrame
    grl_stats_df = pd.DataFrame({
        'First Recorded Workout:':first_workout,
        'Most Recent Workout': last_workout,
        'Average Workout Duration in Minutes':avg_workout_duration,
        'Average Calories Burned Per Workout':avg_calories_burned_per_workout,
        'Average Distance in Kilometers':avg_distance,
        'Number of Workouts:': workout_counter,
        'Average Number of Laps':avg_laps
    },index=['Info'])

    # Transposing dataframe, setting new index and column
    # grl_stats_df = grl_stats_df.T
    # grl_stats_df = grl_stats_df.reset_index()
    # grl_stats_df = grl_stats_df.rename(columns={'index':'Info','Info':'Data'})
    return grl_stats_df

# This function uses gspread and pygsheets modules to upload data to google sheets
def WriteToGsheet(service_file_path, spreadsheet_id, sheet_name, data_df):
    """
    this function takes data_df and writes it under spreadsheet_id
    and sheet_name using your credentials under service_file_path
    """
    gc = pygsheets.authorize(service_file=service_file_path)
    sh = gc.open_by_key(spreadsheet_id)
    try:
        sh.add_worksheet(sheet_name)
    except:
        pass
    wks_write = sh.worksheet_by_title(sheet_name)
    wks_write.clear('A1',None,'*')
    wks_write.set_dataframe(data_df, (1,1), encoding='utf-8', fit=True)
    wks_write.frozen_rows = 1