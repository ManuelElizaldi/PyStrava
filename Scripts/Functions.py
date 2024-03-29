import requests
import pandas as pd
import numpy as np
import pygsheets
import time
from time import sleep 
import datetime
from datetime import date
import gspread

# Setting up parameters for write_to_gsheet function
service_file_path = r'C:\Users\USER\Desktop\Learning\PyStrava\Credentials\pacific-castle-303123-909a5ddcda92.json'
spreadsheet_id = '1pomkAzlndHBl_czERrwKkoZFUkJRGFjyhRTeoWA6CS4'

# Creating function that returns the access token that is used in the other api calls
def GetToken(data):
    token = requests.post(url = 'https://www.strava.com/api/v3/oauth/token',data=data).json()
    access_token = token['access_token']
    
    return access_token

# Define a function to retrieve activities from Strava API
def retrieve_activities(access_token):
    url = "https://www.strava.com/api/v3/activities"
    activities = pd.DataFrame()
    page = 1
    while True:
        # Get page of activities from Strava
        print('Getting page number:', page)
        r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
        
        # Check for rate limit exceeded error
        if r.status_code != 200:
            print('Error:',r.status_code, 'stopping extraction')
            break
    
        else:
            r = r.json()
            print(f'Extraction of page {page} complete')
            
            # if no results then exit loop
            if (not r):
                print('Extraction done')
                break
            r = pd.json_normalize(r)
            
            # Adding the new table to the data frame that is storing all the data
            activities = pd.concat([activities, r])
            page += 1

    try:
        # Clean up the dataframe
        clean_activities = activities[['id',
            'name',
            'distance',
            'elapsed_time',
            'total_elevation_gain',
            'sport_type',
            'start_date',
            'achievement_count',
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
        return clean_activities
    except:
        ('Error occurred during extraction')



# Function that cleans the output from the function GetWorkouts()
def CleanGeneral_Table(general_table):
    print('Cleaning General Table')
    general_table['aprox_calories_burned'] = round((general_table['workout_time_sec']/60) * ((0.6309*general_table['average_heartrate']) + (0.1988*80) + (0.2017*26 - 55.0969)) / 4.184,0)

    # from meters to kilometers
    general_table['distance'] = round(general_table['distance']/1000,2)

    # from seconds to minutes
    general_table['workout_time_min'] = round(general_table['workout_time_sec']/60,2)

    # Fix start_date column into the correct format
    general_table["start_date"] = pd.to_datetime(general_table['start_date']).dt.date

    # Changing name of workout type => Workout
    general_table['sport_type'] = general_table['sport_type'].replace({'Workout':'Functional-Cardio Workout'})
    
    # Chaning from m/s to km/h
    general_table['max_speed'] = general_table['max_speed'] * 3.6
    general_table['average_speed'] = general_table['average_speed'] * 3.6
    return general_table

# This function will create a dataframe/pivot table with the count of every sport type
# Function is not gonna work, we need to fix line 110, append becomes concat now -> activities_breakdown.append(pd.Series(new.....
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
    most_recent_workout = max(general_table['start_date'])
    average_workout_duration = round(general_table['workout_time_min'].mean(), 2)
    aprox_average_calories_burned_per_workout = round(general_table['aprox_calories_burned'].mean(), 0)
    average_distance_ran = round(running_activities['distance'].mean(), 0)
    average_biking_distance = round(biking_activities['distance'].mean(), 0)

    # Creating dataframe from general statistics variables
    # Create the DataFrame
    general_stats_df = pd.DataFrame({
    'First Workout' : first_recorded_workout,
    'Most Recent Workout' : most_recent_workout,
    'Average Workout Duration in Minutes' : average_workout_duration,
    'Approximate Average Calories Burned Per Workout' : aprox_average_calories_burned_per_workout,
    'Average Distance Ran in Kilometers' : average_distance_ran,
    'Average Biking Distance in Kilometers' : average_biking_distance
    },index=['Info'])

    # Transposing dataframe, setting new index and column
    general_stats_df = general_stats_df.T
    general_stats_df = general_stats_df.reset_index()
    general_stats_df = general_stats_df.rename(columns = {'index' : 'Info', 'Info' : 'Data'})
    print(f'First recorded workout: {first_recorded_workout}')
    print(f'Most recent workout: {most_recent_workout}')
    return general_stats_df


# This function uses the workouts ids from the general_table to extract a table with all the workouts info that was not present in the general table
# The API limit is 100 calls per 15 minutes, this function is designed to waits 15 minutes when it reaches the API limit 
# It will also tell you the time that it will take to finish the extraction
def GetAllWorkouts(workout_list, access_token):
    workout_info = []
    workout_num = 1
    rate_limit = 100
    time_interval = 900  # 15 minutes = 900 seconds
    
    # Getting time that it will take to finish extraction
    wait_time = ((len(workout_list) / 100) * 900) / 60 
    hours = wait_time / 60
    
    # Separating the whole and fractional part of hours
    whole_hours = int(hours)
    fractional_hours = (hours - whole_hours) * 60 
    
    # Perform iterations while respecting the rate limit
    #  {whole_hours:02} : {int(fractional_hours):02} hours or 
    print(f'Extracting all workouts, due to the API rate limit, this will take {wait_time} minutes.')
    for i in workout_list:
        print('Extracting workout:', workout_num)
        req = requests.get(url = f'https://www.strava.com/api/v3/activities/{i}?access_token='+access_token)
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
            print(f'Reached rate limit of {rate_limit} requests. Sleeping for {int(time_interval / 60)} minutes.')
            time.sleep(time_interval)

    return workout_info


# This function will parse the workout json, grab the relevant columns, clean the units and create a lap counter for the final dataframe
def CleanWorkoutJson(workout_json):
    # parsing json
    df = pd.json_normalize(workout_json)
    # Formatting distance to km 
    df['distance'] = round(df['distance']/1000,2)
    # Formatting workout time to actual minutes
    df['workout_time_min'] = round(df['moving_time']/60,2)
    df['workout_time_min'] = round(df['workout_time_min'] - (df['workout_time_min'] % 1) + (((df['workout_time_min'] % 1) * 60) / 100), 2)
    # Date in the right format
    df["start_date"] = pd.to_datetime(df['start_date']).dt.date
    # Formatting speed to km/h
    df['average_speed'] = df['average_speed'] * 3.6
    df['max_speed'] = df['max_speed'] * 3.6
    df = df.rename(columns = {'id' : 'activity_id', 'average_speed' : 'average_speed_km/h', 'max_speed' : 'max_speed_km/h'})
    df['sport_type'] = df['sport_type'].replace({'Workout' : 'Functional-Cardio Workout'})
    # Creating the start and end latitude and longitude
    df['start_lat'], df['start_long'] = zip(*df['start_latlng'].apply(lambda x: (x[0], x[1]) if x else (None, None)))
    df['end_lat'], df['end_long'] = zip(*df['end_latlng'].apply(lambda x: (x[0], x[1]) if x else (None, None)))
    
    #Getting the columns we want
    df = df[['activity_id',
                'name',
                'start_date',
                'sport_type',
                'distance',
                'workout_time_min',
                'calories',
                'total_elevation_gain',
                'start_lat',
                'start_long',
                'end_lat',
                'end_long',
                'average_speed_km/h',
                'max_speed_km/h',
                'average_temp',
                'average_heartrate',
                'max_heartrate']]

    # Now working on laps data frame, we create 2, 1 for lap avg time and lap counter
    workout_laps = pd.json_normalize(workout_json, 'laps')
    workout_laps = workout_laps[['activity.id', 'name', 'moving_time', 'distance', 'average_heartrate', 'max_heartrate', 'average_speed', 'max_speed']]
    workout_laps = workout_laps.rename(columns={'activity.id' : 'activity_id',
                                                    'name' : 'lap',
                                                    'moving_time' : 'lap_time_min',
                                                    'distance' : 'lap_distance',
                                                    'average_heartrate' : 'lap_average_heartrate',
                                                    'max_heartrate' : 'lap_max_heartrate_km/h',
                                                    'average_speed' : 'lap_average_speed_km/h',
                                                    'max_speed' : 'lap_max_speed'})
    # Formatting lap time to actual minutes
    workout_laps['lap_time_min'] = round(workout_laps['lap_time_min'] / 60,2)
    workout_laps['lap_time_min'] = round(workout_laps['lap_time_min'] - (workout_laps['lap_time_min']%1) + (((workout_laps['lap_time_min'] % 1) * 60) / 100), 2)
    
    # Distance to km
    workout_laps['lap_distance'] = round(workout_laps['lap_distance']/ 1000, 2)
    # Getting the average lap time for each workout
    avg_lap_time = workout_laps.pivot_table(index = ['activity_id'],values = 'lap_time_min', aggfunc = 'mean')
    avg_lap_time = avg_lap_time.reset_index()
    
    # renaming columns
    avg_lap_time = avg_lap_time.rename(columns = {'lap_time_min' : 'avg_lap_time'})
    
    # Gettting lap counter from the workout_laps dataframe
    lap_counter = workout_laps['activity_id'].value_counts().rename_axis('activity_id').reset_index(name='lap_count')
    
    # mergin avg_lap_time and lap_counter dataframes
    lap_stats = avg_lap_time.merge(lap_counter,on='activity_id')
    
    # merging lap stats(avg time and counter) to workout dataframe
    merged = df.merge(lap_stats, on = 'activity_id')
    # Rounding the avg lap time column
    merged[['avg_lap_time']] = round(merged[['avg_lap_time']],2)
    # setting lap counter column to numeric - don't know exactly why 
    merged['lap_count'] = pd.to_numeric(merged['lap_count'])
    # Getting the pace column
    merged['pace'] = round((merged['workout_time_min'] / merged['distance']) - ((merged['workout_time_min'] / merged['distance'])%1) + ((((merged['workout_time_min'] / merged['distance'])%1)*60)/100),2)
    # When getting the pace, some workouts wont have pace, so we replace Nans with 0. 
    merged[['pace']] = merged[['pace']].fillna(0)
    return merged

def CleanLapsJson(workout_json):
    # parsing json
    df = pd.json_normalize(workout_json, 'laps')
    df = df[['activity.id',
            'id',
            'lap_index',
            'moving_time',
            'distance',
            'average_speed',
            'max_speed',
            'split',
            'start_index',
            'end_index',
            'total_elevation_gain',
            'average_heartrate',
            'max_heartrate'
            ]]

    # removed columns temporarily: 'average_cadence', 'pace_zone'
    # renaming laps id
    df = df.rename(columns={'activity.id' : 'activity_id',
                            'id' : 'lap_id',
                            'moving_time' : 'lap_time_min',
                            'distance' : 'lap_distance',
                            'average_heartrate' : 'lap_avg_heartrate',
                            'max_heartrate' : 'lap_max_heartrate_km/h',
                            'average_speed' : 'lap_avg_speed_km/h',
                            'max_speed' : 'lap_max_speed_km/h',
                            'total_elevation_gain' : 'lap_total_elevation_gain',
                            'average_cadence' : 'avg_cadence'})

    # Formatting lap distance to km
    df['lap_distance'] = round(df['lap_distance']/1000,2)

    # Formatting lap time to minutes
    df['lap_time_min'] = round(df['lap_time_min']/60,2)
    df['lap_time_min'] = round(df['lap_time_min'] - (df['lap_time_min']%1) + (((df['lap_time_min'] % 1) * 60) / 100),2)

    # Formatting lap start index to minutes
    df['start_index'] = round(df['start_index']/60,2)
    df['start_index'] = round(df['start_index'] - (df['start_index']%1) + (((df['start_index'] % 1) * 60) / 100),2)
    
    # Formatting lap end index to minutes
    df['end_index'] = round(df['end_index']/60,2)
    df['end_index'] = round(df['end_index'] - (df['end_index']%1) + (((df['end_index'] % 1) * 60) / 100),2)   
    
    # Formatting speed to km/h
    df['lap_avg_speed_km/h'] = df['lap_avg_speed_km/h'] * 3.6
    df['lap_max_speed_km/h'] = df['lap_max_speed_km/h'] * 3.6
    
    return df

# Breaking down workout_df to all different tables - laps table is = to laps_df
def DivideTables(workout_df):    
    activity = workout_df[['activity_id',
                        'start_date',
                        'sport_type',
                        'effort_score_label']]

    activity_name = workout_df[['activity_id',
                                'name']]

    activity_coordinates = workout_df[['activity_id',
                                    'start_lat',
                                    'start_long',
                                    'end_lat',
                                    'end_long']]

    activity_details = workout_df[['activity_id',
                                'workout_time_min',
                                'calories',
                                'average_heartrate',
                                'avg_lap_time',
                                'total_elevation_gain',
                                'max_heartrate',
                                'distance',
                                'average_speed_km/h',
                                'max_speed_km/h',
                                'average_temp',
                                'pace',
                                'lap_count']]

    activity_scores = workout_df[['activity_id',
                                'distance_score',
                                'workout_time_score',
                                'calorie_score',
                                'total_elevation_gain_score',
                                'average_heartrate_score',
                                'max_heartrate_score',
                                'avg_lap_time_score',
                                'lap_count_score',
                                'avg_speed_score',
                                'max_speed_score',
                                'pace_score',
                                'effort_score',
                                'effort_score_rank']]
    
    return activity, activity_name, activity_coordinates, activity_details, activity_scores

# This function creates the score columns used to build the k nearest neighbors model 
# points are marked with comments
def CreateScoreColumns(df):
    pace_conditions = [
    (df['pace'] == 0), # 0 
    (df['sport_type'].isin(['Run'])) & (df['pace'] <= 2), # 30
    (df['sport_type'].isin(['Run'])) & (df['pace'] >= 5) & (df['pace'] < 6), #25
    (df['sport_type'].isin(['Run'])) & (df['pace'] >= 6) & (df['pace'] < 7), #20
    (df['sport_type'].isin(['Run'])) & (df['pace'] >= 7) & (df['pace'] < 10), #10
    (df['sport_type'].isin(['Run'])) & (df['pace'] > 10), #5
    (df['sport_type'].isin(['TrailRun'])) & (df['pace'] <= 5), #35
    (df['sport_type'].isin(['TrailRun'])) & (df['pace'] >= 5) & (df['pace'] < 6), #30
    (df['sport_type'].isin(['TrailRun'])) & (df['pace'] >= 6) & (df['pace'] < 7.3), #25
    (df['sport_type'].isin(['TrailRun'])) & (df['pace'] >= 7.3) & (df['pace'] < 10), #20
    (df['sport_type'].isin(['TrailRun'])) & (df['pace'] >= 10) & (df['pace'] < 13),#15
    (df['sport_type'].isin(['TrailRun'])) & (df['pace'] > 13), #5
    (df['sport_type'].isin(['Hike'])) & (df['pace'] <= 12.3), #5
    (df['sport_type'].isin(['Hike'])) & (df['pace'] >= 12.3) & (df['pace'] < 13), #4
    (df['sport_type'].isin(['Hike'])) & (df['pace'] >= 13) & (df['pace'] < 14), #3
    (df['sport_type'].isin(['Hike'])) & (df['pace'] >= 14) & (df['pace'] < 15.5), #2
    (df['sport_type'].isin(['Hike'])) & (df['pace'] > 15.5), #1
    (df['sport_type'].isin(['Swim'])) & (df['pace'] <= 43), #25
    (df['sport_type'].isin(['Swim'])) & (df['pace'] >= 43) & (df['pace'] < 49), #20
    (df['sport_type'].isin(['Swim'])) & (df['pace'] >= 49) & (df['pace'] < 55), #15
    (df['sport_type'].isin(['Swim'])) & (df['pace'] > 55), #10
    (df['sport_type'].isin(['AlpineSki'])) & (df['pace'] >= 2) & (df['pace'] < 2.3), #20
    (df['sport_type'].isin(['AlpineSki'])) & (df['pace'] >= 2.5) & (df['pace'] < 2.7), #15
    (df['sport_type'].isin(['AlpineSki'])) & (df['pace'] >= 2.7) & (df['pace'] < 3), #10
    (df['sport_type'].isin(['AlpineSki'])) & (df['pace'] > 3),#5
    (df['sport_type'].isin(['Ride'])) & (df['pace'] <= 3), # 30
    (df['sport_type'].isin(['Ride'])) & (df['pace'] >= 3) & (df['pace'] < 4), # 25
    (df['sport_type'].isin(['Ride'])) & (df['pace'] >= 4) & (df['pace'] < 4.60), # 20
    (df['sport_type'].isin(['Ride'])) & (df['pace'] >= 4.60) & (df['pace'] < 6.21), #15
    (df['sport_type'].isin(['Ride'])) & (df['pace'] > 6.21), # 5
    (df['sport_type'].isin(['MountainBikeRide'])) & (df['pace'] <= 4), #30
    (df['sport_type'].isin(['MountainBikeRide'])) & (df['pace'] >= 4) & (df['pace'] < 4.3), #25
    (df['sport_type'].isin(['MountainBikeRide'])) & (df['pace'] >= 4.3) & (df['pace'] < 4.5), #20
    (df['sport_type'].isin(['MountainBikeRide'])) & (df['pace'] >= 4.5) & (df['pace'] < 6), #15
    (df['sport_type'].isin(['MountainBikeRide'])) & (df['pace'] > 6) #10
    ] 

    pace_conditions_values = [0, 30, 25, 20, 10, 5, #Run 
                          35, 30, 25, 20, 15, 5, # TrailRun
                          5, 4, 3, 2, 1, #Hike
                          25, 20, 15, 10, #Swim
                          20, 15, 10, 5, #Ski
                          30, 25, 20, 15, 5, #Ride
                          30, 25, 20, 15, 10 #MountainBikeRide
                          ] 

    df['pace_score'] = np.select(pace_conditions, pace_conditions_values)
        
    distance_conditions = [
        (df['distance'] == 0), # 1
        (df['sport_type'].isin(['Run', 'TrailRun'])) & (df['distance'] >= 0) & (df['distance'] < 5), # 5
        (df['sport_type'].isin(['Run', 'TrailRun'])) & (df['distance'] >= 5) & (df['distance'] < 10), # 10 
        (df['sport_type'].isin(['Run', 'TrailRun'])) & (df['distance'] >= 10) & (df['distance'] < 13), # 25 
        (df['sport_type'].isin(['Run', 'TrailRun'])) & (df['distance'] >= 13), # 30
        (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['distance'] >= 1) & (df['distance'] < 5), # 5
        (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['distance'] >= 5) & (df['distance'] < 8.5), # 10
        (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['distance'] >= 8.5) & (df['distance'] < 12), # 15
        (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['distance'] >= 12) & (df['distance'] < 15), # 20
        (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['distance'] >= 15), # 25
        (df['sport_type'].isin(['AlpineSki']) & (df['distance'] >= 10) & (df['distance'] < 15)), # 10
        (df['sport_type'].isin(['AlpineSki']) & (df['distance'] >= 15) & (df['distance'] < 20)), # 15
        (df['sport_type'].isin(['AlpineSki']) & (df['distance'] >= 20)), # 20
        (df['sport_type'].isin(['Swim'])) & (df['distance'] >= 0.10) & (df['distance'] < 0.20), # 10
        (df['sport_type'].isin(['Swim'])) & (df['distance'] >= 0.20) & (df['distance'] < 0.30), # 15
        (df['sport_type'].isin(['Swim'])) & (df['distance'] >= 0.30) & (df['distance'] < 0.35), # 20
        (df['sport_type'].isin(['Swim'])) & (df['distance'] >= 0.35) & (df['distance'] < 0.40), # 25
        (df['sport_type'].isin(['Swim'])) & (df['distance'] >= 0.40), # 30
        (df['distance'] > 0.5) & (df['distance'] < 1), # 1
        (df['distance'] > 1) & (df['distance'] < 2), # 2
        (df['distance'] > 2) & (df['distance'] < 3), # 3
        (df['distance'] > 3) & (df['distance'] < 4), # 4
        (df['distance'] > 4) # 5
        ]

    distance_conditions_values = [0, 5, 10, 25, 30, # running
                                5, 10, 15, 20, 25, # biking
                                10, 15, 20, # skiing
                                10, 15, 20, 25, 30, # swimming
                                1, 2, 3, 4, 5 # special activitie 
                                ]

    # applying conditions and values
    df['distance_score'] = np.select(distance_conditions, distance_conditions_values)

    workout_time_condition = [
        (df['workout_time_min'] >= 2) & (df['workout_time_min'] < 10),
        (df['workout_time_min'] >= 10) & (df['workout_time_min'] < 15),
        (df['workout_time_min'] >= 15) & (df['workout_time_min'] < 20),
        (df['workout_time_min'] >= 20) & (df['workout_time_min'] < 25),
        (df['workout_time_min'] >= 25) & (df['workout_time_min'] < 30),
        (df['workout_time_min'] >= 20) & (df['workout_time_min'] < 35),
        (df['workout_time_min'] >= 35) & (df['workout_time_min'] < 40),
        (df['workout_time_min'] >= 40) & (df['workout_time_min'] < 45),
        (df['workout_time_min'] >= 45) & (df['workout_time_min'] < 50),
        (df['workout_time_min'] >= 55) & (df['workout_time_min'] < 60),
        (df['workout_time_min'] >= 60)
    ]

    workout_time_values = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

    # applying the conditions and values to the dataframe
    df['workout_time_score'] = np.select(workout_time_condition, workout_time_values)

    # building calories conditions and values
    calories_conditions = [(df['calories'] >= 0) & (df['calories'] < 100), # 5
                        (df['calories'] >= 100) & (df['calories'] < 200), # 15
                        (df['calories'] >= 200) & (df['calories'] < 300), # 25
                        (df['calories'] >= 300) & (df['calories'] < 400), # 35
                        (df['calories'] >= 400) & (df['calories'] < 500), # 40
                        (df['calories'] >= 500) & (df['calories'] < 600), # 50
                        (df['calories'] >= 600) & (df['calories'] < 700), # 60
                        (df['calories'] >= 700) & (df['calories'] < 800), # 70
                        (df['calories'] >= 800) & (df['calories'] < 900), # 80
                        (df['calories'] >= 900) & (df['calories'] < 1000), # 90
                        (df['calories'] >= 1000) # 100
                        ] 

    calories_values = [5, 15, 25, 35, 40, 50, 60, 70, 80, 90, 100]

    df['calorie_score'] = np.select(calories_conditions, calories_values)


    # Building elevation conditions and values
    elevation_conditions = [(df['total_elevation_gain'] == 0),
                            (df['total_elevation_gain'] >= 1) & (df['total_elevation_gain'] < 100),
                            (df['total_elevation_gain'] >=100) & (df['total_elevation_gain'] < 200),
                            (df['total_elevation_gain'] >= 200) & (df['total_elevation_gain'] < 300),
                            (df['total_elevation_gain'] >= 300) & (df['total_elevation_gain'] < 400),
                            (df['total_elevation_gain'] >= 400) & (df['total_elevation_gain'] < 500),
                            (df['total_elevation_gain'] > 500)]

    elevation_values = [0,5,10,15,20,25,30]


    df['total_elevation_gain_score'] = np.select(elevation_conditions, elevation_values)


    # replacing some of the Nans with 1 
    df['average_heartrate'] = df['average_heartrate'].fillna(1)
    # building average heartrate conditions and values
    avg_heartrate_conditions = [
                                (df['average_heartrate'] > 0) & (df['average_heartrate'] < 100),
                                (df['average_heartrate'] >= 100) & (df['average_heartrate'] < 130),
                                (df['average_heartrate'] >= 130) & (df['average_heartrate'] < 145),
                                (df['average_heartrate'] >= 145) & (df['average_heartrate'] < 155),
                                (df['average_heartrate'] >= 155) & (df['average_heartrate'] < 165),
                                (df['average_heartrate'] >= 165) & (df['average_heartrate'] < 170),
                                (df['average_heartrate'] >= 170)
                                ]

    avg_heartrate_values = [5, 10, 15, 20, 30, 35, 40]

    df['average_heartrate_score'] = np.select(avg_heartrate_conditions, avg_heartrate_values)

    # replacing some of the Nans with 1 
    df['max_heartrate'] = df['max_heartrate'].fillna(1)

    # building max heartrate conditions and values
    max_heartrate_conditions = [
        (df['max_heartrate'] >= 0) & (df['max_heartrate'] < 80),
        (df['max_heartrate'] >= 80) & (df['max_heartrate'] < 130),
        (df['max_heartrate'] >= 130) & (df['max_heartrate'] < 165),
        (df['max_heartrate'] >= 165) & (df['max_heartrate'] < 175),
        (df['max_heartrate'] >= 175) & (df['max_heartrate'] < 185),
        (df['max_heartrate'] >= 180)
    ]

    max_heartrate_values = [5, 10, 15, 25, 30, 35]

    df['max_heartrate_score'] = np.select(max_heartrate_conditions, max_heartrate_values)


    # avg time per lap conditions and values
    avg_lap_time_conditions = [
                                (df['avg_lap_time'] >= 0) & (df['avg_lap_time'] < 5),
                                (df['avg_lap_time'] >= 5) & (df['avg_lap_time'] < 10),
                                (df['avg_lap_time'] >= 10) & (df['avg_lap_time'] < 20),
                                (df['avg_lap_time'] >= 20) & (df['avg_lap_time'] < 30),
                                (df['avg_lap_time'] >= 30)
                                ]


    avg_lap_time_values = [1, 5, 10, 15, 20]


    df['avg_lap_time_score'] = np.select(avg_lap_time_conditions, avg_lap_time_values)


    # lap count conditions and values
    lap_count_conditions = [(df['lap_count'] >= 0) & (df['lap_count'] < 3),
                            (df['lap_count'] >= 3) & (df['lap_count'] < 4),
                            (df['lap_count'] >= 4) & (df['lap_count'] < 5),
                            (df['lap_count'] >= 5) & (df['lap_count'] < 6),
                            (df['lap_count'] >= 6)
                            ]

    lap_count_values = [5, 10, 20, 25, 35]

    df['lap_count_score'] = np.select(lap_count_conditions, lap_count_values)

    # average speed conditions and values
    avg_speed_conditions = [
                            (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['average_speed_km/h'] >= 0) & (df['average_speed_km/h'] < 6), #5 
                            (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['average_speed_km/h'] >= 6) & (df['average_speed_km/h'] < 12),#10
                            (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['average_speed_km/h'] >= 12) & (df['average_speed_km/h'] < 14),#15
                            (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['average_speed_km/h'] >= 14) & (df['average_speed_km/h'] < 18),#20
                            (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['average_speed_km/h'] >= 18),#25
                            (df['average_speed_km/h'] == 0), #1
                            (df['average_speed_km/h'] >= 0) & (df['average_speed_km/h'] < 5), # 5
                            (df['average_speed_km/h'] >= 5) & (df['average_speed_km/h'] < 7), # 10
                            (df['average_speed_km/h'] >= 7) & (df['average_speed_km/h'] < 9), # 15
                            (df['average_speed_km/h'] >= 9) & (df['average_speed_km/h'] < 10), # 25 
                            (df['average_speed_km/h'] >= 10) & (df['average_speed_km/h'] < 11), # 30
                            (df['average_speed_km/h'] >= 11) , # 35
    ]
    avg_speed_values = [5,10,15,20,25,0,5,10,15,25,30,35]


    df['avg_speed_score'] = np.select(avg_speed_conditions, avg_speed_values)


    # max speed conditions and values
    max_speed_conditions = [ (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['max_speed_km/h'] >= 0) & (df['max_speed_km/h'] < 15), # 5
                            (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['max_speed_km/h'] >= 15) & (df['max_speed_km/h'] < 20),# 10
                            (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['max_speed_km/h'] >= 20) & (df['max_speed_km/h'] < 25),# 15
                            (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['max_speed_km/h'] >= 25) & (df['max_speed_km/h'] < 30),# 20
                            (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['max_speed_km/h'] >= 30) & (df['max_speed_km/h'] < 35),# 25
                            (df['sport_type'].isin(['Ride', 'MountainBikeRide'])) & (df['max_speed_km/h'] >= 35),# 30
                            (df['max_speed_km/h'] == 0), # 1
                            (df['max_speed_km/h'] >= 0) & (df['max_speed_km/h'] < 5),# 5
                            (df['max_speed_km/h'] >= 5) & (df['max_speed_km/h'] < 10), # 10
                            (df['max_speed_km/h'] >= 10) & (df['max_speed_km/h'] < 15), # 15
                            (df['max_speed_km/h'] >= 15) & (df['max_speed_km/h'] < 20),# 20
                            (df['max_speed_km/h'] >= 25) & (df['max_speed_km/h'] < 30),# 25
                            (df['max_speed_km/h'] >= 30) & (df['max_speed_km/h'] < 35),# 30 
                            (df['max_speed_km/h'] >= 35)# 35
                            ]

    max_speed_values = [5, 10, 15, 20, 25, 30, 0, 5, 10, 15, 20, 25, 30, 35]


    df['max_speed_score'] = np.select(max_speed_conditions, max_speed_values)


    # Getting effort score for each workout
    df['effort_score'] = df['distance_score'] + df['workout_time_score'] + df['calorie_score'] + df['total_elevation_gain_score'] + df['average_heartrate_score'] + df['max_heartrate_score'] + df['avg_lap_time_score'] +df['lap_count_score'] + df['avg_speed_score'] +df['max_speed_score'] + df['pace_score']


    # creating low, medium and high effort scores column depending on the total amount of points
    score_conditions = [(df['effort_score'] >= 0) & (df['effort_score'] < 100),
                        (df['effort_score'] >= 100) & (df['effort_score'] < 125),
                        (df['effort_score'] >= 125) & (df['effort_score'] < 150),
                        (df['effort_score'] >= 150)]

    score_values = ['No Effort','Low Effort','Medium Effort','High Effort']


    df['effort_score_label'] = np.select(score_conditions, score_values)


    score_rank_conditions = [(df['effort_score_label'] == 'No Effort'),
                            (df['effort_score_label'] == 'Low Effort'),
                            (df['effort_score_label'] == 'Medium Effort'),
                            (df['effort_score_label'] == 'High Effort')]

    score_rank_values = ['1','2','3','4']
    df['effort_score_rank'] = np.select(score_rank_conditions, score_rank_values)
    
    return df

# Creating function that generates the effort counter table by workout
def EffortLevelBreakdown(df):
    effort_counter_table = pd.pivot_table(df, values = 'activity_id',index = ['sport_type'], columns=['effort_score_label'], aggfunc = 'count').fillna('-')
    effort_counter_table = effort_counter_table.reset_index() 
    return effort_counter_table

# This function gives us a general description of the list of workouts
def DescribeWorkoutdf(workout_df):
    # Convert 'start_date' column to datetime.date data type
    workout_df['start_date'] = pd.to_datetime(workout_df['start_date']).dt.date
    
    # Create variables to hold values
    first_workout = min(workout_df['start_date'], default = datetime.date.min)
    last_workout = max(workout_df['start_date'], default = datetime.date.min)
    avg_workout_duration = round(workout_df['workout_time_min'].mean(),2)
    avg_calories_burned_per_workout = workout_df['calories'].mean()
    avg_distance = round(workout_df['distance'].mean(),0)
    avg_heart_rate = round(workout_df['average_heartrate'].mean(),0)
    avg_max_heart_rate = round(workout_df['max_heartrate'].mean(),0)
    avg_speed = round(workout_df['average_speed_km/h'].mean(),0) * 3.6
    avg_max_speed = round(workout_df['max_speed_km/h'].mean(),0) * 3.6
    workout_counter = len(workout_df)
    avg_laps = round(workout_df['lap_count'].mean(),0)

    # Creating dataframe from general statistics variables
    # Create the DataFrame
    grl_stats_df = pd.DataFrame({
        'First Recorded Workout:' : first_workout,
        'Most Recent Workout': last_workout,
        'Average Workout Duration in Minutes' : avg_workout_duration,
        'Average Calories Burned Per Workout' : avg_calories_burned_per_workout,
        'Average Distance in Kilometers' : avg_distance,
        'Average Heart Rate' : avg_heart_rate,
        'Average Max Hear Rate' : avg_max_heart_rate,
        'Average Speed km/h' : avg_speed,
        'Average Max Speed km/h' : avg_max_speed,
        'Number of Workouts:' : workout_counter,
        'Average Number of Laps' : avg_laps
    },index = ['Info'])

    # Transposing dataframe, setting new index and column
    grl_stats_df = grl_stats_df.T
    grl_stats_df = grl_stats_df.reset_index()
    grl_stats_df = grl_stats_df.rename(columns={'index' : 'Info', 'Info' : 'Data'})
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
    wks_write.clear('A1', None, '*')
    wks_write.set_dataframe(data_df, (0, 0), encoding = 'utf-8', fit = True)
    wks_write.frozen_rows = 1
    

def UpdateGoogleSheet(access_token, service_file_path,  clean_activities, all_workouts_df):
    # Setting up gspread authentications
    mycred = ServiceAccountCredentials.from_json_keyfile_name(service_file_path,myscope) # type: ignore
    client = gspread.authorize(mycred)
    
    # Extracting data 
    mysheet = client.open('workout-data').sheet1
    list_of_row = mysheet.get_all_records()
    
    # Making dataframe from data we extracted
    all_workouts_df = pd.DataFrame(list_of_row)
    
    # From the general table extract ids to be updated
    updated_ids = list(clean_activities['id'])
    # Getting the current ids, not updated 
    not_updated_workouts = list(all_workouts_df['activity_id'])
    print('Adding',len(updated_ids) - len(not_updated_workouts), 'new workouts.')
    # Comparing both id lists and getting a subset of the ones that are missing
    missing_workouts = list(set(updated_ids).difference(not_updated_workouts))
    
    # Extracting missing workouts and formatting json
    missing_workouts_json = GetAllWorkouts(missing_workouts,access_token)
    missing_workouts_df = CleanWorkoutJson(missing_workouts_json)
    
    # Applying model values
    missing_workouts_df = CreateScoreColumns(missing_workouts_df)
    
    # concat results
    all_workouts_df = pd.concat([all_workouts_df, missing_workouts_df])
    
    return all_workouts_df