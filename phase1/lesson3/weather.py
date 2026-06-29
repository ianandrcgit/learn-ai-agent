import requests
import os
from dotenv import load_dotenv

# Load secret keys from .env file
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

if not API_KEY:
    raise RuntimeError("Missing WEATHER_API_KEY in .env or environment variables")

def get_weather(city: str) -> None:
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            print(f"\n=== Weather in {city} ===")
            print(f"Temperature : {data['main']['temp']}°C")
            print(f"Feels like  : {data['main']['feels_like']}°C")
            print(f"Condition   : {data['weather'][0]['description']}")
            print(f"Humidity    : {data['main']['humidity']}%")
        else:
            print(f"Error {response.status_code}: {data.get('message', 'Unknown error')}")

    except Exception as e:
        print(f"Something went wrong: {e}")

# Run
get_weather("Bangalore")
get_weather("London")
get_weather("Hubli")