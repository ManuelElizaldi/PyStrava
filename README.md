<h1 align="center">
  <br>
  <a href=""><img src="https://github.com/ManuelElizaldi/PyStrava/blob/main/Images/ProjectLogo2.png" alt="PyStrava" width="400"></a>
  <br>
  PyStrava
  <br>
</h1>

# Table of Contents:
- [Currently working on](#currently-working-on)
- [New Features List](#new-features-)
- [Introduction & Project Desription](#introduction--project-desription)
    - [Project V. 1](#v-1)
    - [Project V. 2](#v-2)
- [Goals](#goals)
- [Technologies Used](#technologies-used)
- [Analysis & Dashboard](#analysis--dashboard)
    - [Sports Type Breakdown](#sports-type-breakdown)
    - [Descriptive Statistics](#descriptive-statistics) 
- [Level of Effort Score](#level-of-effort-score)
    - [How The Effort Score Is Calculated](#how-the-effort-score-is-calculated)
    - [Effort Analysis](#effort-analysis)
- [Machine Learning Model: Categorizing Workouts With K-Nearest Neighbor Algorithm](#machine-learning-model-categorizing-workout-level-of-effort-with-k-nearest-neighbor-algorithm)
    - [Why K Nearest Neighbor](#why-k-nearest-neighbor)
    - [Model](#model) 
- [How To Setup This Project](https://github.com/ManuelElizaldi/PyStrava/blob/main/Documentation/HowToSetUpProject.md)
    - [Strava API Access](https://github.com/ManuelElizaldi/PyStrava/blob/main/Documentation/HowToSetUpProject.md#strava---api-access)
    - [Google API Access](https://github.com/ManuelElizaldi/PyStrava/blob/main/Documentation/HowToSetUpProject.md#google-sheets-api)
    - [How to Use](https://github.com/ManuelElizaldi/PyStrava/blob/main/Documentation/HowToSetUpProject.md#how-to-use)
    - [Updating Your Data](https://github.com/ManuelElizaldi/PyStrava/blob/main/Documentation/HowToSetUpProject.md#updating-your-existing-data) 
    - [Copy This Dashboard Template](https://github.com/ManuelElizaldi/PyStrava/blob/main/Documentation/HowToSetUpProject.md#copy-this-dashboard-template)
- [Areas of Improvement](#areas-of-improvement)

<h3 align="center">
  <img src="https://img.shields.io/github/repo-size/ManuelElizaldi/PyStrava"/>
  <a href="https://manuelelizaldi.github.io/index.html" target="_blank" class="button"><img src="https://img.shields.io/website?up_message=Portfolio%20Website&url=https%3A%2F%2Fmanuelelizaldi.github.io%2Findex.html"/></a>
  <br>
</h3>

# Currently working on:
### V 2. of PyStrava, migrating database to PostgreSQL and creating a web app to showcase workout statistics 

# New Features ⚛️
- 08/02/2023 - Inside the Google Looker dashboard, for the biking and running pages, I added a score card that displays the total distance traveled for the selected date range. 
- 10/12/2023 - Added a pace column to the dataset and corresponding looker dashboard score cards.
- 10/12/2023 - Deployed an update Google Sheet database script.
- 10/19/2023 - Average speed, max speed, total elevation gain and distance scores now give 0 points when their values are = 0.
- 01/24/2024 - Added a file contaning the documentation for the functions used in the scripts. 

# Introduction & Project Desription
Back in 2020, during the pandemic, I promised myself to prioritize my physical health. To achieve this, I wanted to use technology. By maintaining a digital record of all my workouts, I compelled myself to stay disciplined and on track. I have been using my Garmin smartwatch and the Strava app to log all my activities. Since embarking on this journey, I have witnessed progress in my physical health, abilities, and mental well-being. I have accomplished goals that once seemed impossible, and I have gained self-belief, realizing that I am far more capable than I thought. Initially, running 10km was a struggle, but now I have completed Austin's Half Marathon, a 10km Spartan Race, an Ultra Marathon (50km) and Mexico City's 2023 Marathon.

Leveraging my programming and data analysis skills, I aim to explore other ways in which technology can improve my fitness journey. 

## V. 1
In this version, I utilize Strava API to download all my workouts, build an ETL pipeline to clean the data, and then upload it to a Google Sheet. This Google Sheet will serve as the foundation for a workout statistics dashboard.

Regarding the Machine Learning aspect of the project, I will utilize my workout data to train a Multi Label Classification Model that categorizes the level of effort for each activity.

## V. 2
Expanding upon V. 1, now I want to build a web app that can display the same statistics as the Google looker dashboard and also add new and improved insights like a workout tracker calendar. 
Additionally, build a PostgreSQL database for my workout data.

# Goals
## V. 1
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

## V. 2
Explain what the goal of v2 is here ******
![DataPipeline](/Images/DataPipelineV2.png)
# Technologies Used
## Programming Language
- Python 3.8.5
## Dashboard
- Google Looker Studio
## Packages
- Pandas 1.1.3
- numpy 1.22.4
- matplotlib 3.3.2
- Requests 2.28.2
- Pygsheets 2.0.6
- Scikit-Learn 1.2.2
- Gspread 5.7.2
- Webbrowser
## Relevant Documentation
- [Strava's API documentation](https://developers.strava.com/)
- [Pygsheets](https://pygsheets.readthedocs.io/en/stable/)
- [Requests](https://requests.readthedocs.io/en/latest/)
- [Gspread Authentication](https://docs.gspread.org/en/latest/oauth2.html#enable-api-access)
- [Google APIs](https://developers.google.com/docs/api/reference/rest)
- [PyStrava's Functions Documentation](https://github.com/ManuelElizaldi/PyStrava/blob/main/FunctionsDocumentation.md)
- [How To Setup This Project](https://github.com/ManuelElizaldi/PyStrava/blob/main/Documentation/HowToSetUpProject.md)

# Areas Of Improvement
These are some features I plan to implement over time. 
- Develop an Effort model that enables individuals to calculate their level of effort for each workout. It will be applicable to anyone, providing a tool for assessing effort and facilitating personal improvement.
- Add a pace metric for running workouts. ✔️
- To streamline the database updating process, it is essential to implement real-time reporting, eliminating the need to run the Update_GoogleSheet.py file manually every time we want to update our Google Sheet database. Use Kafka technology for this.
- In order to ensure regular updates, a feature should be created to automatically execute the Update_GoogleSheet.py file on a weekly basis.
- To enhance the machine learning model, I plan to leverage Garmin's API infrastructure, which provides valuable data such as [VO2 Max](https://www.healthline.com/health/vo2-max) and Sleep data.
- A key addition to this project would be the creation of a dashboard specifically designed for individual workout statistics. This would involve analyzing metrics like cadence and other aspects that are not currently covered.
- Considering the additional workout statistics available through Strava's premium membership, it would be beneficial to implement some of these features into the project. 
- Model can be further improved by creating ratios between variables, such as calories burned per 10 minutes during a workout. This can contribute to the development of a performance score, similar to the effort score.
- Exploring ways to track activities like bouldering, rugby or soccer is crucial to expand the scope of the project.
- Furthermore, the inclusion of tracking strength output would provide an additional dimension of information for the machine learning model.
- To enhance the model's effectiveness, gathering more data is essential. Therefore, increasing the number of workouts performed will greatly improve the model's performance.
- Add a desktop shortcut that when clicked, runs the PyStrava.py script.

# Analysis & Dashboard
The graphs and statistics you will see in this section were created in the [Google Looker Dashboard](https://lookerstudio.google.com/reporting/c8efd23d-4f39-42d1-a336-26aebac76fa5). Feel free to explore my data.

## Sports Type Breakdown
I started recording my workouts on May 20, 2020, and as of May 26, 2023, I have logged 703 different activities, encompassing various sports. Here is a breakdown of my activities:

![TypesOfSports](/Images/SportCount.png)

Among my recorded activities, Functional-Cardio Workout stands out as the most frequently performed, with 516 sessions. This activity involves kettlebell training, dynamic stretching, calisthenics, and weight lifting. The reason behind my prioritization of this activity is the convenience of having a home gym.

Following Functional-Cardio Workout, running takes second place with 76 workouts. Looking ahead, I plan to dedicate more attention to running and trail running due to upcoming races on my schedule.

Weight training secures the third position with 30 logged sessions. While weight training used to be one of my primary focuses, I have now shifted my focus towards [aerobic exercises](https://www.healthline.com/health/fitness-exercise/aerobic-exercise-examples#:~:text=It%20can%20include%20activities%20like,lungs%2C%20and%20circulatory%20system%20healthy).

Bike riding and swimming rank fourth and fifth, respectively. However, with my current objective of participating in a triathlon, I am determined to increase my activity count in these sports.

## Descriptive Statistics
As mentioned earlier, my primary focus revolves around functional training, running, swimming, and biking. Therefore, I would like to provide some descriptive statistics for these activities. However, please note that I need to log more swimming activities before I can create a comprehensive dashboard for it. 

### Functional Workouts:
![Functional Stats](/Images/FunctionalStats.png)

### Running:
Please note that running includes running and trail running activities. 
![Running Stats](/Images/RunningStats.png)

### Biking:
Please note that biking includes road biking and mountain biking.
![Biking Stats](/Images/BikingStats.png)

### Overall:
These statistics cover all the sports types referenced in the [Sports Type Subsection](#sport-type-breakdown)
![General Stats](/Images/GeneralStats.png)

### Some of the important conclusions from these statistics are:
- Running is the activity where I burn the most calories and have the highest average heart rate.
- Functional workouts and running result in the highest maximum heart rate.
- Biking workouts account for a greater average time spent.
- Currently, my running pace is 8.7 km/h, knowing this, I will aim to increase it to 9 km/h.

### Relationship Between Average Heart Rate and Distance
For my running workouts, I adhere to the philosophy of "run slow to run fast." Essentially, this approach entails running at a slow pace for 80% of the time and incorporating fast runs for the remaining 20%. How does this translate into specific numbers? Well, during my runs, I ensure that my heart rate does not exceed 155 beats per minute. This helps me stay within the [aerobic zone](https://www.whoop.com/thelocker/aerobic-heart-rate-zone/#:~:text=The%20aerobic%20heart%20rate%20zone%20is%20a%20heart%20rate%20between,person%20running%20next%20to%20you.), allowing my body to efficiently utilize oxygen. By following this technique, I am able to avoid the accumulation of hydrogen ions (commonly referred to as lactic acid) and can comfortably sustain my runs for a longer duration.

![Running_HeartRate_Distance_Relationship](/Images/Running-DistanceAvgHeartRate.png)

In this graph, we can observe that the majority of my running workouts fall within the average heart rate range of 145 to 160, this range is good, although I have to be careful not to go over 155 beats per minute. If you are intrested in reading more about the "run slow to run fast" philosophy, you can read this [article](https://marathonhandbook.com/run-slow-to-run-fast/).

### Monthly Average Laps for Functional Training
For my Functional Training, I follow a specific approach. I design a circuit comprising 4-6 exercises in each round and aim to complete a minimum of 3 rounds in each session. The primary focus is on finishing the rounds in the shortest amount of time possible. This training methodology is geared towards pushing myself into the [anaerobic zone](https://www.physio-pedia.com/Anaerobic_Exercise#:~:text=Anaerobic%20exercise%20is%20any%20activity,short%20length%20with%20high%20intensity.), where the workouts are short but intense. The exercises included in the circuit can vary, encompassing movements such as kettlebell swings, kettle bell snatches, squats, pull-ups, overhead presses, jumping exercises, sprints, rope jumping, weighted stretches and one of my personal favorites, burpees. By incorporating these dynamic exercises into my Functional Training, I can challenge my body and achieve optimal results.

![Average Monthly Laps for Functional Training](/Images/FunctionalTrainingLaps.png)

This graph illustrates the average number of rounds completed per month. Notably, October 2021 stands out as the month with the highest average number of laps, reaching 8.8. One significant observation is the upward trend in rounds per month, indicating an improvement in my fitness over time. Starting from September 2021, I have consistently surpassed the minimum threshold that I set for myself. Although there was a temporary decline in September 2022, my performance swiftly rebounded. This data highlights the progress I have made and underscores my dedication to maintaining a consistent level of physical activity.

# Level of Effort Score
## How The Effort Score Is Calculated
To calculate the effort score, we begin by creating bins based on the minimum, maximum, quartiles, and outliers of each variable. Within these bins, we assign points depending on the range in which a value falls. These points are determined subjectively, drawing from personal experience and perceived effort.

For instance, let's consider the average heart rate variable. We know that higher average heart rates indicate greater effort in the workout, so we establish the following point ranges:

![Average Heart Rate Box Plot](/Images/AverageHeartRateBoxPlot.png)

- 1 - 100: 5 points
- 100 - 130: 10 points
- 130 - 145: 15 points
- 145 - 155: 20 points
- 155 - 165: 30 points
- 165 - 170: 35 points
- Above 170: 40 points

For instance, if my average heart rate during a workout was 155, I would assign 30 points for that activity in a separate column. Each variable has its own column dedicated to storing the score for each workout in that particular variable.

In the case of the distance variable, it is important to make a distinction between sports. For instance, biking generally requires less effort compared to running. Therefore, we have programmed the model to effectively differentiate between different sports. By incorporating these considerations into the model, we can accurately assess the effort level associated with various activities, resulting in a deeper understanding of the overall effort required. Taking into account the specific demands and characteristics of each sport we can get a better picture of the overall effort involved.

![Distance Box Plot](/Images/RunningBikingBoxPlot.png)

After assigning a scoring system to each variable, we calculate the sum of each column and store it in the column labeled 'effort_score'. Here are the ranges to determine the level of effort:

- 0 - 100: No Effort
- 100 - 125: Low Effort
- 125 - 150: Medium Effort
- 150 or above: High Effort

## Effort Analysis
After assigning each workout with its corresponding level of effort, we can analyze the breakdown count for each sport type. Based on this analysis, I have made several observations:
- Functional training, contrary to my initial assumption, appears to be a medium effort workout rather than high effort.
- The majority of my runs are categorized as high effort.
- Biking shows a relatively balanced distribution across high, medium, and low effort levels.
- Surprisingly, hiking turned out to be a high effort activity, which makes sense considering factors such as elevation gain, time spent, distance covered, and calories burned. It turns out that walking can be an effective way to burn calories.
- Yoga, despite being categorized as requiring no effort in the current model, is an area of opportunity. From personal experience, I find yoga to be an activity that demands considerable effort. In the future, I would like to find a way to incorporate this insight into the model.
- Mountain biking is as a highly effective activity for pushing myself, with the majority of workouts falling into the high effort category.
- Most of my workouts fall in the high and medium effort levels.

![TypesOfSportsByEffort](/Images/WorkoutLevelOfEffortBySportType-.png)

The graph displayed below illustrates the correlation between calories and average heart rate, categorizing each workout with its corresponding label. This data strongly supports my initial hypothesis, which suggests that as heart rate increases, the body requires more energy (calories), indicating a higher level of effort.

![Relationship between calories and average heart rate](/Images/RelationshipBetweenAvgHeartRateCalories.png)

By analyzing this graph, it becomes evident that tracking heart rate can serve as a reliable indicator of the intensity and effectiveness of a workout in terms of caloric expenditure. This insight can be particularly valuable in designing personalized fitness programs and optimizing training routines to align with specific fitness goals.

# Machine Learning Model: Categorizing Workout Level of Effort with K-Nearest Neighbor Algorithm
## Why K Nearest Neighbor
I have chosen to use the K Nearest Neighbor (KNN) algorithm for this project. Here's a couple of reasons behind my decision:
Firstly, our dataset consists of a relatively small number of records (703). KNN is known to work well with smaller datasets, making it a suitable choice for our scenario. Additionally, I have identified the presence of a few outliers within our data. These outliers can potentially introduce noise and affect the overall performance of our model. However, KNN is robust against the influence of outliers as it makes predictions based on similarity. By considering the neighbors in proximity to a given data point, KNN can mitigate the impact of outliers and provide more reliable predictions. Moreover, the nature of KNN allows it to identify groups or clusters within the data. If there happens to be a group of outliers that share similar characteristics or patterns, KNN is more likely to recognize and assign them to the appropriate label.

## Model
This K Nearest Neighbors (KNN) model is designed for multi-label classification tasks. The labels in this model represent different effort levels: No Effort, Low Effort, Medium Effort, and High Effort. The model aims to predict the effort level of workouts based on the score columns we created for each variable/workotu metric.

###  Model Performance and Optimal Value of K
- During the cross-validation test, the model's performance scores were found to be more consistent when using a K value of 7 compared to 5 or 23. This suggests that a K value of 7 provides more stable and reliable predictions across different subsets of the data.
- Grid search, which systematically explored different hyperparameter settings, ranked K = 7 as the best choice for the model. This configuration achieved a score of 0.96, outperforming K = 5 and K = 23.
- The model demonstrated a good level of accuracy, achieving 86% correctness in classifying instances.
- The F1 score, a combined measure of precision and recall, was calculated to be 0.858, indicating a good balance between precision and recall.
- The precision score of 0.861 indicates the model's ability to correctly predict positive instances out of all instances predicted as positive.
- The recall score of 0.858 reflects the model's ability to identify and capture positive instances accurately.

### Consideration of Data Characteristics
- This KNN model is robust to outliers present in the data. Outliers with the same label tend to be clustered together, making the model effective in capturing and classifying high effort and no effort workouts, which are the most common outlier instances.
- Total amount of records: 703.
- 20% of the dataset was used for testing, while the remaining 80% was used for training.

### Confusion Matrix
![ConfussionMatrix](/Images/Effort_Score_Variables_Model.png)


### Classification Report
![Classification Report](/Images/ClassificationReport.png)

### Model Strengths and Weaknesses
**Strenghts:**
- The model demonstrates high accuracy in accurately labeling High and Medium effort workouts.
- Overall, the model achieves an accuracy rate of 86%, indicating its effectiveness in correctly classifying workout intensity levels.

**Weaknesses:**
- The model may not be as accurate in labeling low and no effort workouts compared to medium and high intensity ones, as there are fewer instances of the former in the dataset.
- As the dataset expands, it may be necessary to update or modify the model to maintain its effectiveness.
- It is worth considering investing time in exploring alternative distance metrics, as they may yield improvements in the model's performance.
- There is correlation between the Max Heart Rate and Average Heart Rate variables, as well as between the Max Speed and Average Speed variables. It might be necessary to evaluate and potentially drop some variables to avoid redundancy or multicollinearity in the dataset.

### Practical Applications
- With this model you can build a workout program, where you can use it to classify the intensity level and determine the number of high, medium, low, and no effort workouts within a specific time period.
- It helps you track your progress and ensures that you stay on track with your program. The model will provide insights on whether you are pushing yourself adequately.
- Additionally, this model can be used to identify signs of overtraining, helping you maintain a balanced and healthy training regimen.
