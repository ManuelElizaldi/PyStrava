<h1 align="center">
  <br>
  #WORK IN PROGRESS :no_entry:
  <br>
 </h1>
 
<h1 align="center">
  <br>
  <a href=""><img src="https://github.com/ManuelElizaldi/PyStrava/blob/main/Images/ProjectLogo2.png" alt="PyStrava" width="400"></a>
  <br>
  PyStrava
  <br>
</h1>

<h3 align="center">
  <br>
  :star: Star this project on GitHub — it motivates me a lot!
  <br>
</h3>

# Workout-Analysis
# Table of Contents:
- [Introduction](#introduction)
- [Goals](#goals)
- [Technologies Used](#technologies-used)
- [Project Setup](#project-setup)
- [Project Desription](#project-description)

## Introduction
During the pandemic I promised myself to set my physical health as one of my priorities. To do that, I wanted to use technology to help me achieve my goals by having a digital record of all the workouts I've done in order to force myself to stay disciplined and on track. I've been using my Garmin smartwatch and Strava's app to keep a log of all my acitivites. In this project one of my objectives is to use the statistical tools I've learned through out my career and build a dashboard where I can visualize my progress.  

Since starting this journey I have seen progress in physical health, physical abilities and mental health. I have reached goals that never seemed possible and started to believe in myself. I have discovered that I am much more capable of what I initially thought. When I first started working out consistently running 10km was miserable, now I have completed [Austin's Half Marathon](https://youraustinmarathon.com/), a [10km Spartan Race](https://www.spartan.com/) and I am registered for Austin's 2024 Maratho and an Ultra Marathon (50km) in July 2023. For this reason I am also gonna write a section about my philosophy of traning in hopes that someone looking to better their health feels inspired by this project and can chase that better version of themselves that is out there waiting to be found.

## Goals
As I have stated before, I wanted to use techonology to help me reach my goals, therefore I built a Python script that pulls data from Strava's server, cleans it and then uploads it to Google Sheets. With the output file I can produce a dashboard in Google Looker Studio where I can find all my workout statistics. With this dashboard I want to understand which type of physical activities r

Likewise, I want to build a machine learning model that can classify 3 types of workouts: 
  1) Low Effort 
  2) Medium Effort 
  3) High Effort

## Technologies Used
### Programming Language
- Python 3.8.5
### Dashboard
- Google Looker Studio
### Packages
- Pandas 1.1.3
- Requests 2.28.2
- Pygsheets 2.0.6
### Relevant Documentation
- [Strava's API documentation](https://developers.strava.com/)
- [Pygsheets](https://pygsheets.readthedocs.io/en/stable/)
- [Requests](https://requests.readthedocs.io/en/latest/)

## Project Setup
### Strava - API access
In order to use any of the scripts in this project there are a couple of steps that need to be done. First you have to create an account in [Strava](https://www.strava.com/), then you have to start an App in the My App menu inside your profile. Once this step is done you will be given a Client ID and Client Secret which are used to access the API through the python script. Also, you have to change the privacy setting in your profile, which can be found in the menu: Privacy Controls, here you have to set the 'Who Can See' settings for Profile Page and Activities to 'Everyone' to be able to pull the workout data through the API. Here's an image of how it should look:

<img src="https://raw.githubusercontent.com/ManuelElizaldi/Workout-Analysis-API/main/Images/PrivacySettings.png"/>

After those steps are done, before you use any of the API calls to pull data, we have to open the following link to get our authorization code. Here I use the package [Webbrowser](https://docs.python.org/3/library/webbrowser.html) to open this page directly from the script but you can do it manually too, just note that this code will expire. Change the ```{client_id}``` with your own and open the link: 
``` python
https://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri=http://localhost/&approval_prompt=force&scope=profile:read_all,activity:read_all
```
When you open the page you will see this window, click on authorize.

![AuthorizationStep1](Images/StravaAuthorizationStep1.png)

After you authorize, you will see the following page, don't panic, this is what we want. Save the code (red box) in your script. Now you have all the necessary information and authorizations to use Strava's API.

![AuthorizationStep2](Images/StravaAuthorizationStep2.png)

Make sure to declare your data variable in your script or declare it in a config.py file and import it to your main script. Your data dictionary should look like this:

``` python
data = {
'client_id': 'xxxx',
'client_secret':'xxxx',
'code': 'xxxx',
'grant_type':'authorization_code'
}
```

This dictionary holds the required credentials to run any Strava API.

### Google Sheets API 
In order to use the package Pygsheets to uplaod data to Google Drive from our python script, we first need to create a project in the [Google Developers Console](https://console.cloud.google.com/projectselector2/apis/dashboard?pli=1&supportedpurview=project&authuser=1). In the box labeled “Search for APIs and Services”, search for “Google Drive API” and enable it, then in the box labeled “Search for APIs and Services”, search for “Google Sheets API” and enable it. 

After the API is enabled, we have to get a Google service account, which is an account intended for non-human users, i.e. our python script. These are the steps to getting a service account:

1. In the "API & Services", go to "Credentials".
2. Choose "Create Credentials".
3. Click on "Service account key".
4. Answer all the questions and then click on "Create" and "Done".
5. Click "Manage service accounts" in the "Service accounts section".
6. Press on ⋮ near recently created service account and select “Manage keys” and then click on “ADD KEY > Create new key”
7. Select the JSON option and press "Continue".

The resulting file will look something like this:
``` python
{
  "type": "service_account",
  "project_id": "pacific-castle-303123",
  "private_key_id": "xxx",
  "private_key": "xxx",
  "client_email": "manuel-elizaldi@pacific-castle-303123.iam.gserviceaccount.com",
  "client_id": "118237617576468519006",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/manuel-elizaldi%40pacific-castle-303123.iam.gserviceaccount.com"
}
``` 
Make sure to add the path to the json file like so in the script:

```python 
service_file_path = r'\GoogleCredentials.json'
```

From this Json, grab the ```"client_email"``` and share your Google sheet with it just like you would share it with somone else.

And also declare the sheet id which you can get from the link of the Google Sheet you created to store the data from this project:

![GoogleSheetId](/Images/GoogleSheetId.jpg)

After all this steps are done, now you can run the WorkoutAnalysis.py file and extract all your workouts from Strava! 

If these instructions were not clear I suggest you read through these articles: 
- [Gspread Authentication](https://docs.gspread.org/en/latest/oauth2.html#enable-api-access)
- [Strava's API documentation](https://developers.strava.com/)

------------------------------------------------------------------
## Project Desription

I started recording since 05-20-2020 and as of 03-26-2023 I'v logged over 600 different workouts, consisting of different types of physical exercises
As of 2-11-2023 I have logged over 600 activities consisting of different types of physical exercises. I started recording my workouts in order to keep me on track of my goals.  to determine some basic questions like, how consistent have I been, 

when I first created my [Strava](https://www.strava.com/dashboard) account. At first, this data was gathered using my cellphone, linking Samsung's Health App to Strava, but then I switched to a [Garming Pheonix 6](https://www.garmin.com/en-US/p/702902) smart watch. This allowed me to get more metrics like heart rate, which I use to calculate the approximate calories I burn in a workout

### Analysis 
### Dashboard
