import os
import time
import requests
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env if it exists (for local development)
load_dotenv()

# Configuration
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
CITY = os.getenv('CITY', 'Paris')
DB_HOST = os.getenv('DB_HOST', 'server')
DB_NAME = os.getenv('DB_NAME', 'weather_db')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASS = os.getenv('DB_PASS', 'password')
FETCH_INTERVAL = int(os.getenv('FETCH_INTERVAL', '600')) # Default 10 minutes

def get_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description']
        }
    except Exception as e:
        print(f"Error fetching data from OpenWeatherMap: {e}")
        return None

def save_to_db(data):
    max_retries = 5
    retry_delay = 5
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            cur = conn.cursor()
            query = """
                INSERT INTO weather_data (city, temperature, humidity, description)
                VALUES (%s, %s, %s, %s)
            """
            cur.execute(query, (data['city'], data['temperature'], data['humidity'], data['description']))
            conn.commit()
            cur.close()
            conn.close()
            print(f"Data saved to DB: {data}")
            return
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed to save data to DB: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Could not save data.")

def main():
    if not API_KEY:
        print("Error: OPENWEATHERMAP_API_KEY not found in environment variables.")
        return

    print("Starting Weather Client...")
    
    while True:
        weather_data = get_weather_data(API_KEY, CITY)
        if weather_data:
            save_to_db(weather_data)
        
        print(f"Waiting {FETCH_INTERVAL} seconds for next update...")
        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    main()
