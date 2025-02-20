import os
import requests
import json
import schedule
import time
import sys

API_KEY = os.getenv("WEATHER_API_KEY")
if not API_KEY:
    raise ValueError("API Key not found. Set WEATHER_API_KEY as an environment variable.")

CITIES = ["New York", "London", "Tokyo"]
LOG_FILE = "/app/data/weather_log.json"
REPORT_FILE = "/app/data/weather_report.txt"

class WeatherFetcher:
    """Fetch and store weather data"""

    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_weather(self, city):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                return {
                    "city": city,
                    "weather": data["weather"][0]["description"],
                    "temperature": data["main"]["temp"]
                }
            else:
                print(f"Failed to retrieve data for {city}: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching weather for {city}: {e}")
            return None

    def save_to_file(self, data):
        try:
            with open(LOG_FILE, "a") as file:
                json.dump(data, file, indent=4)
                file.write("\n")
            print(f"Data saved to {LOG_FILE}")

            # Generate weather report
            report_content = "\n".join([f"{entry['city']}: {entry['weather']}, {entry['temperature']}°C" for entry in data])

            with open(REPORT_FILE, "w") as report_file:
                report_file.write(report_content)

            print(f"✅ Weather report successfully written to {REPORT_FILE}", flush=True)
        except Exception as e:
            print(f"Error saving data: {e}")

def main():
    weather_fetcher = WeatherFetcher(API_KEY)
    weather_data = []

    for city in CITIES:
        data = weather_fetcher.fetch_weather(city)
        if data:
            weather_data.append(data)

    if weather_data:
        weather_fetcher.save_to_file(weather_data)

main()

schedule.every(1).hour.do(main)

print("Scheduled to fetch weather data every hour...", flush=True)

while True:
    schedule.run_pending()
    time.sleep(60)

