import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

# --- WEATHER ---
def get_weather(city: str) -> None:
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            print(f"\n=== Weather in {city} ===")
            print(f"Temperature : {data['main']['temp']}°C")
            print(f"Condition   : {data['weather'][0]['description']}")
            print(f"Humidity    : {data['main']['humidity']}%")
        else:
            print(f"Error: {data['message']}")
    except Exception as e:
        print(f"Something went wrong: {e}")


# --- CURRENCY CONVERTER ---
def convert_currency(amount: float, rate: float) -> None:
    result = round(amount * rate, 2)
    print(f"\nConverted Amount: ₹{result}")


# --- UNIT CONVERTER ---
def convert_units(value: float, unit: str) -> None:
    if unit == "kg":
        print(f"\n{value} kg = {round(value * 2.205, 2)} lbs")
    elif unit == "km":
        print(f"\n{value} km = {round(value * 0.621, 2)} miles")
    else:
        print("Unknown unit. Try kg or km.")


# --- MAIN MENU ---
def main():
    print("\n============================")
    print("   Personal AI Assistant")
    print("============================")

    while True:
        print("\nWhat do you want to do?")
        print("1. Check Weather")
        print("2. Convert Currency (USD to INR)")
        print("3. Convert Units")
        print("4. Quit")

        choice = input("\nEnter choice (1/2/3/4): ").strip()

        if choice == "1":
            city = input("Enter city name: ").strip()
            get_weather(city)

        elif choice == "2":
            try:
                amount = float(input("Enter amount in USD: "))
                convert_currency(amount, 83.5)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "3":
            try:
                value = float(input("Enter value: "))
                unit = input("Enter unit (kg/km): ").strip().lower()
                convert_units(value, unit)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            print("\nGoodbye! Keep building. 🚀")
            break

        else:
            print("Invalid choice. Enter 1, 2, 3 or 4.")


# RUN
main()