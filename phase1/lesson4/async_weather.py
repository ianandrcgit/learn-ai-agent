import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

# ASYNC FUNCTION — note the "async def"
async def get_weather(session, city: str) -> None:
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        async with session.get(url, params=params) as response:
            data = await response.json()

            if response.status == 200:
                print(f"\n=== Weather in {city} ===")
                print(f"Temperature : {data['main']['temp']}°C")
                print(f"Condition   : {data['weather'][0]['description']}")
                print(f"Humidity    : {data['main']['humidity']}%")
            else:
                print(f"Error for {city}: {data['message']}")

    except Exception as e:
        print(f"Something went wrong for {city}: {e}")


# MAIN ASYNC FUNCTION — runs everything together
async def main():
    cities = ["Bangalore", "London", "Tokyo", "New York", "Hubballi"]

    async with aiohttp.ClientSession() as session:
        tasks = [get_weather(session, city) for city in cities]
        await asyncio.gather(*tasks)


# RUN
asyncio.run(main())