import json
import os
import pandas as pd
import requests
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")  # todo: joint intent classification and slot filling classification for getting time, only for report
# atist dataset?
candidate_label_current_time = ['current time',
                                'general question']  # todo: if general, then only gpt3 output, else gpt3/weather/heartrate

user_mock_data = pd.read_csv('mock_healthcare.csv')

url = "https://api.ambeedata.com/latest/by-city"
querystring = {"city": "Zurich"}  # location could be changed by Juli
headers = {
    'x-api-key': os.getenv('weather_api_key'),
    'Content-type': "application/json"
}


# question = input("Please enter your question below: ")
def get_question_type(question):
    zero_shot_classify = classifier(question, candidate_label_current_time)

    # todo: find the optimal parameter for this by experimentation
    activity_type = zero_shot_classify['labels'][0]
    return activity_type


def current_response():
    # condition that checks the user data itself
    if user_mock_data.average_sleep_week_hr[0] < 5:
        health_data_response = f'Sleep Placeholder message filled by Juli'
    elif user_mock_data.sleep_last_night_hr[0] < 5:
        health_data_response = f'Sleep Placeholder message filled by Juli'
    elif user_mock_data.avg_hearrate_yesterday_bpm[0] > 90:
        health_data_response = f'Sleep Placeholder message filled by Juli'
    elif user_mock_data['oxygen saturation'][0] < 93:
        health_data_response = f'Sleep Placeholder message filled by Juli'

    # condition that checks the current weather and then returns an additional response
    full_response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(full_response.text)

    AQI = response['stations'][0]['AQI']
    AQI_info = response['stations'][0]['aqiInfo']['category']
    print(AQI, AQI_info)

    if AQI < 50:
        weather_response = f'Placeholder for good aqi by Juli.'
    elif 50 < AQI < 100:
        weather_response = f'Air quality Index is moderate, decide what to do Juli placeholder'
    elif 101 < AQI < 150:
        weather_response = f'Air quality is Unhealthy for sensitive group. Placeholder for Juli'
    elif AQI > 150:
        weather_response = f'Unhealthy. Placeholder for Juli'

    return f'Hey, so I checked your health data, and {health_data_response}. Also, since you are going outside,' \
           f'I thought you should know {weather_response}'
