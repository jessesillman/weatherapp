from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return data
        else:
            return None

    except Exception as e:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        api_key = os.getenv("API_KEY") # Ensure you have your API key in .env file
        weather_data = get_weather(api_key, city)
        return render_template('index.html', weather_data=weather_data)
    
    return render_template('index.html', weather_data=None)

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8081)), host='0.0.0.0', debug=True)
