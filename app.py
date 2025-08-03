

import os
from flask import Flask, render_template, request, jsonify
import requests
import geocoder

app = Flask(__name__)

API_KEY = 'd0bf3784701b405bae55bb19d5627926'  # Use your actual API key


def get_location():
    g = geocoder.ip('me')
    if g.ok:
        return g.city
    return None


def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={city}"
        f"&appid={API_KEY}&units=metric"
    )
    response = requests.get(url)
    try:
        data = response.json()
        if response.status_code != 200:
            return {'error': data.get('message', 'Error retrieving weather.')}
        return {
            'weather': data['weather'][0]['description'].title(),
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind': data['wind']['speed'],
            'icon': data['weather'][0]['icon']
        }
    except Exception:
        return {'error': 'Invalid response from server.'}


@app.route('/')
def index():
    auto_city = get_location()
    return render_template('index.html', auto_city=auto_city)


@app.route('/weather')
def weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'No city provided.'})
    data = get_weather(city)
    return jsonify(data)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
