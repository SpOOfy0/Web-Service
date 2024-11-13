from flask import Flask, request, render_template
import json
import urllib.parse
from urllib.request import urlopen
from contextlib import closing

app = Flask(__name__)

API_KEY = '9f3b38b6c9d172d064ea2ac1187530a88e9e5be836f2f4936b3b1f0b43392ae6'

def get_city_insee(city_name):
    """Fetch the INSEE code of the city from the API."""
    try:
        city_name_encoded = urllib.parse.quote(city_name)
        url = f'https://api.meteo-concept.com/api/location/cities?token={API_KEY}&search={city_name_encoded}'
        
        with closing(urlopen(url)) as f:
            data = json.loads(f.read())
            if data['cities']:
                return data['cities'][0]['insee']
            else:
                return None
    except Exception as e:
        return None

def get_weather_forecast(insee_code):
    """Fetch the weather forecast using the INSEE code."""
    try:
        url = f'https://api.meteo-concept.com/api/forecast/daily/0?token={API_KEY}&insee={insee_code}'
        
        with closing(urlopen(url)) as f:
            decoded = json.loads(f.read())
            city = decoded.get('city', {})
            forecast = decoded.get('forecast', {})
            
            if city and forecast:
                return {
                    'city': city.get('name', 'N/A'),
                    'precipitation_today': forecast.get('rr10', 'N/A'),
                    'max_precipitation': forecast.get('rr1', 'N/A')
                }
            else:
                return None
    except Exception as e:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_info = None
    if request.method == 'POST':
        city_name = request.form.get('city')
        insee_code = get_city_insee(city_name)
        if insee_code:
            weather_info = get_weather_forecast(insee_code)
        else:
            weather_info = {'error': 'City not found. Please try again.'}
    
    return render_template('index.html', weather_info=weather_info)

if __name__ == '__main__':
    app.run(debug=True)
