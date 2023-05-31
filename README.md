<h1 align="center">
  <br>
  <a href=""><img src="https://github.com/ManuelElizaldi/PyStrava/blob/main/Images/ProjectLogo2.png" alt="PyStrava" width="400"></a>
  <br>
  PyStrava
  <br>
</h1>

<h3 align="center">
  <br>
  :star: Star this project on GitHub — it motivates me a lot and you will stay up to date on the project!
  <br>
  <br>
  <img src="https://img.shields.io/github/repo-size/ManuelElizaldi/PyStrava"/>
  <a href="https://manuelelizaldi.github.io/index.html" target="_blank" class="button"><img src="https://img.shields.io/website?up_message=Portfolio%20Website&url=https%3A%2F%2Fmanuelelizaldi.github.io%2Findex.html"/></a>
  <br>
</h3>

# Workout-Analysis
# Table of Contents:
- [Introduction & Project Desription](#introduction--project-desription)
- [Goals](#goals)
- [Technologies Used](#technologies-used)
- [Project Setup](#project-setup)
    - [Strava API Access](#strava---api-access)
    - [Google API Access](#google-sheets-api)
    - [How to Use](#how-to-use)
    - [Updating Your Data](#updating-your-existing-data) 
- [Analysis & Dashboard](#analysis-)
    - [Descriptive Statistics](#descriptive-statistics) 
- [Areas of Improvement](#areas-of-improvement)

## Introduction & Project Desription

Back in 2020, during the pandemic, I promised myself to prioritize my physical health. To achieve this, I wanted to use technology. By maintaining a digital record of all my workouts, I compelled myself to stay disciplined and on track. I have been using my Garmin smartwatch and the Strava app to log all my activities. Since embarking on this journey, I have witnessed progress in my physical health, abilities, and mental well-being. I have accomplished goals that once seemed impossible, and I have gained self-belief, realizing that I am far more capable than I thought. Initially, running 10km was a struggle, but now I have completed Austin's Half Marathon, a 10km Spartan Race, and I have plans to participate in an Ultra Marathon (50km) in July 2023. Additionally, I am registered for Austin's 2024 Marathon.

Leveraging my programming and data analysis skills, I aim to explore other ways in which technology can improve my fitness journey. In this project, I utilize Strava API to download all my workouts, build an ETL pipeline to clean the data, and then upload it to a Google Sheet. This Google Sheet will serve as the foundation for a workout statistics dashboard.

Regarding the Machine Learning aspect of the project, I will utilize my workout data to train a Multi Label Classification Model that categorizes the level of effort for each activity.

## Goals
1. Build a python script that extracts all my workout data from Strava.
2. Clean and prepare data to be uploaded to Google Drive.
3. Build a dashboard containing workout metrics in Google Looker.
4. Train a K-Nearest Neighbors model to classify my workouts in 4 different categories:
    - No Effort
    - Low Effort 
    - Medium Effort 
    - High Effort

The data pipeline for this project looks like this:
![DataPipeline](/Images/DataPipeline.png)

## Technologies Used
### Programming Language
- Python 3.8.5
### Dashboard
- Google Looker Studio
### Packages
- Pandas 1.1.3
- numpy 1.22.4
- matplotlib 3.3.2
- Requests 2.28.2
- Pygsheets 2.0.6
- Scikit-Learn 1.2.2
- Gspread 5.7.2
- Webbrowser
### Relevant Documentation
- [Strava's API documentation](https://developers.strava.com/)
- [Pygsheets](https://pygsheets.readthedocs.io/en/stable/)
- [Requests](https://requests.readthedocs.io/en/latest/)
- [Gspread Authentication](https://docs.gspread.org/en/latest/oauth2.html#enable-api-access)

## Project Setup
Before you can use the [PyStrava Notebook](https://github.com/ManuelElizaldi/PyStrava/blob/main/PyStrava_Notebook.ipynb) or the [PyStrava Script](https://github.com/ManuelElizaldi/PyStrava/blob/main/PyStrava.py) you need to follow these instructions: 

### Strava - API access
Before we can start using Strava's API we first need to complete a couple of steps to gain access:

1. If you haven't already, create an account in [Strava](https://www.strava.com/)
2. Head to your Profile Settings and then click on “Privacy Controls” and set “Profile Page” and “Activities” to Everyone, like this:

<img src="https://raw.githubusercontent.com/ManuelElizaldi/Workout-Analysis-API/main/Images/PrivacySettings.png"/>

3. Create a Strava application inside this link: [Create a Strava Application](https://www.strava.com/settings/api)
4. You can answer all the questions however you want, just make sure the “Authorization Callback Domain” field is set to “localhost”. Like so:

![Strava Application Fields](Images/StravaApplicationFields.png)

After those steps are done, before you use any of the API calls to pull data, we need to get our authorization code, which we get by opening the following link:

``` python
https://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri=http://localhost/&approval_prompt=force&scope=profile:read_all,activity:read_all
```

In the [PyStrava Notebook](https://github.com/ManuelElizaldi/PyStrava/blob/main/PyStrava_Notebook.ipynb) and the [PyStrava Script](https://github.com/ManuelElizaldi/PyStrava/blob/main/PyStrava.py) I use the package [Webbrowser](https://docs.python.org/3/library/webbrowser.html) to open this page directly from the script but you can do it manually too. This code will expire, so if you are not getting access you might need to run it again. Change the ```{client_id}``` with your own and you shuold be able to access the authorization window. 

When you open the page you will see this window, click on authorize.

![AuthorizationStep1](Images/StravaAuthorizationStep1.png)

After you authorize, you will see the following page, don't panic, this is what we want. Save the code (red box) in your script. Now you have all the necessary information and authorizations to use Strava's API. While the script is running, make sure you don't close this window.

![AuthorizationStep2](Images/StravaAuthorizationStep2.png)

Make sure to declare your data dictionary-variable in your script or declare it in a config.py file and import it to your main script. Your data dictionary should look like this:

``` python
data = {
'client_id': 'xxxx',
'client_secret':'xxxx',
'code': 'xxxx',
'grant_type':'authorization_code'
}
```

This dictionary holds the required credentials to run any Strava API.

If these instructions were not clear I suggest you read through this page: 
- [Strava's API documentation](https://developers.strava.com/)

### Google Sheets API 
In order to use the package Pygsheets to uplaod data to Google Drive and Gspread to download it from our python script, we first need to create a project in the [Google Developers Console](https://console.cloud.google.com/projectselector2/apis/dashboard?pli=1&supportedpurview=project&authuser=1). In the box labeled “Search for APIs and Services”, search for “Google Drive API” and enable it, then in the box labeled “Search for APIs and Services”, search for “Google Sheets API” and enable it. 

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
Or add it to your Config.py file. I used the path option. 

From this Json, grab the ```"client_email"``` and share your Google sheet with it just like you would share it with somone else.

And also declare the sheet id which you can get from the link of the Google Sheet you created to store the data from this project:

![GoogleSheetId](/Images/GoogleSheetId.jpg)
```
spreadsheet_id = '1pomkAzlndHBl_czERrwKkoZFUkJRGFjyhRTeoWA6CS4'
```

After all this steps are done, now you can run the [PyStrava Notebook](https://github.com/ManuelElizaldi/PyStrava/blob/main/PyStrava_Notebook.ipynb) and the [PyStrava Script](https://github.com/ManuelElizaldi/PyStrava/blob/main/PyStrava.py) to extract all your workouts from Strava and upload them to Google Drive! 

If these instructions were not clear I suggest you read through this article: 
- [Gspread Authentication](https://docs.gspread.org/en/latest/oauth2.html#enable-api-access)

### How to use
In order for the [PyStrava Script](https://github.com/ManuelElizaldi/PyStrava/blob/main/PyStrava.py) to work, we need to make sure we create 3 tabs inside the Google Sheet file that will hold our data. If you don't want to modify the script, make sure you create the following tabs with the same syntax:

- All_Workouts_Table
- All_Workouts_Desc_Table
- Activities_Breakdown

If these tabs don't exist or are misspelled you will get an error.
After running the script you should see all your data inside the file.

### Updating your existing data
If you already have data in your Google Sheet and you just want to add new workouts, you can run the [Update Google Sheet](https://github.com/ManuelElizaldi/PyStrava/blob/main/Update_GoogleSheet.py). This will add any new workouts.

------------------------------------------------------------------

## Analysis & Dashboard
I started recording my workouts on May 20, 2020, and as of May 18, 2023, I have logged 695 different activities, encompassing various sports. Here is a breakdown of my activities:

![TypesOfSports](/Images/SportCount.png)

Among my recorded activities, Functional-Cardio Workout stands out as the most frequently performed, with 512 sessions. This comprehensive activity involves kettlebell training, dynamic stretching, calisthenics, and weight lifting. The reason behind my prioritization of this activity is the convenience of having a home gym.

Following Functional-Cardio Workout, running takes second place with 73 workouts. Looking ahead, I plan to dedicate more attention to running and trail running due to upcoming races on my schedule.

Weight training secures the third position with 30 logged sessions. While weight training used to be one of my primary focuses, I have now shifted my focus towards [aerobic exercises](https://www.healthline.com/health/fitness-exercise/aerobic-exercise-examples#:~:text=It%20can%20include%20activities%20like,lungs%2C%20and%20circulatory%20system%20healthy).

Bike riding and swimming rank fourth and fifth, respectively. However, with my current objective of participating in a triathlon, I am determined to increase my activity count in these sports.

### Descriptive Statistics
As mentioned earlier, my primary focus revolves around functional training, running, swimming, and biking. Therefore, I would like to provide some descriptive statistics for these activities. However, please note that I need to log more swimming activities before I can create a comprehensive dashboard for it. 

#### Functional Workouts:
![Functional Stats](/Images/FunctionalStats.png)

#### Running:
Please note that running includes running and trail running activities. 
![Running Stats](/Images/RunningStats.png)

#### Biking:
Please note that biking includes road biking and mountain biking.
![Biking Stats](/Images/BikingStats.png)

#### Overall:
![General Stats](/Images/GeneralStats.png)

#### Relationship Between Average Heart Rate and Distance
![](/Images/Running-DistanceAvgHeartRate.png)

### Level of Effort 
#### How it works: 



![ConfussionMatrix](/Images/ConfussionMatrix-white.png)
![WorkoutEffortCounter](/Images/WorkoutLevelOfEffortDistribution.png)


![TypesOfSportsByEffort](/Images/WorkoutLevelOfEffortBySportType.png)

### Copy this dashboard template 
If you want to use this dashboard as a template for your own analysis, follow these steps. 
1. Open the [Dashboard](https://lookerstudio.google.com/reporting/c8efd23d-4f39-42d1-a336-26aebac76fa5), and on the  ⋮  button, click "Make a copy".
2. Click on Create a Data Source 

![Copy This Report Window](/Images/CopyThisReport.png)

4. Click Google Sheets from the Google Connectors and select the Google Sheet you created for this project.

After these steps are done, you will have a copy of this dashboard inside your Google Looker. 

## Areas Of Improvement
These are some features I plan to implement over time. 
- To streamline the database updating process, it is essential to implement real-time reporting, eliminating the need to run the Update_GoogleSheet.py file manually every time we want to update our Google Sheet database. 
- In order to ensure regular updates, a feature should be created to automatically execute the Update_GoogleSheet.py file on a weekly basis.
- To enhance the machine learning model, I plan to leverage Garmin's API infrastructure, which provides valuable data such as [VO2 Max](https://www.healthline.com/health/vo2-max) and Sleep data.
- A key addition to this project would be the creation of a dashboard specifically designed for individual workout statistics. This would involve analyzing metrics like cadence and other aspects that are not currently covered.
- Considering the additional workout statistics available through Strava's premium membership, it would be beneficial to implement some of these features into the project. 
- The effort score model can be further improved by creating ratios between variables, such as calories burned per 10 minutes during a workout. This can contribute to the development of a performance score, similar to the effort score.
- Exploring ways to track activities like bouldering, rugby or soccer is crucial to expand the scope of the project.
- Furthermore, the inclusion of tracking strength output would provide an additional dimension of information for the machine learning model.
- To enhance the model's effectiveness, gathering more data is essential. Therefore, increasing the number of workouts performed will greatly improve the model's performance.
