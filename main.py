"""Main Module"""
import os
import requests
from twilio.rest import Client

# Open Weather API Endpoints, Parameters
API_KEY = os.environ.get("OWM_API_KEY")
API_ENDPOINT = f"https://api.openweathermap.org/data/2.5/onecall"
API_PARAMETERS = {
    "lat": 10.915731,
    "lon": 76.018570,
    "exclude": "current,minutely,daily",
    "appid": API_KEY
}

# Requesting weather data from open weather map
response = requests.get(url=API_ENDPOINT, params=API_PARAMETERS)
response.raise_for_status()
weather_data = response.json()
# Slicing json weather data to first 12 hours
hourly_data = weather_data["hourly"][0:12]

# Variable to track rain condition
will_rain = False
# Check if weather id falls below 700, which as per Open weather map is rain weather condition
for hour in hourly_data:
    weather_condition_id = hour["weather"][0]["id"]
    if weather_condition_id < 700:
        will_rain = True
        break

# Twilio API
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_no = os.environ["TWILIO_NO"]
user_no = os.environ["USER_NO"]

# Sending message if will rain= True
if will_rain:
    # Twilio library code for sending sms
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(body="Message from Rain sms alert app. It might rain🌧 today. Bring an Umbrella ☔",
                from_=twilio_no,
                to=user_no
                )

    # confirmation if message is sent
    print(message.status)
