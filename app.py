from flask import Flask, request, jsonify
from flask_limiter import Limiter 
from flask_limiter.util import get_remote_address
import os, requests, redis, json
from dotenv import load_dotenv

app = Flask(__name__)
'''
App routing means mapping the urls to a specific function that will handle the logic for that URL
'''
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.route("/weather")
def weather():
    load_dotenv(dotenv_path=".env")
    api_key = os.getenv("API_KEY")
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Please provide a city name"}), 400
    city = city.strip().lower()
    redis_key = f"weather:{city}"
    cached_weather = redis_client.get(redis_key)

    if cached_weather is None:
        print(f"Could not retrieve {city} weather information, from IEX cloud API")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            return jsonify({"error":f"HTTP error: {http_err}"}), 503
        except requests.exceptions.RequestException as req_err:
            return jsonify({"error": "Network error or request failed"}),503
        except requests.exceptions.ReadTimeout as time_err:
            return jsonify({"error":"Request timed out"}),503

        data = response.json()
        if data["cod"] == 200:
            result = weather_info(data)
            emoji = get_weather_emoji(result['weather_id'])
            weather_data = ({
                "city": city,
                "temperature": f"{result['temperature']:.0f}°C",
                "emoji": emoji,
                "description": result['description']
            })
            redis_client.set(redis_key, json.dumps(weather_data),ex=43200)
            return jsonify(weather_data)
        else:
            return jsonify({"error":"City not found"}),404
    else:
        print(f"Found {city} weather information in cache, serving from redis")
        cached_weather = json.loads(cached_weather)
        return jsonify(cached_weather)

def weather_info(data): 
    temperature_k = data["main"]["temp"]
    temperature_c = temperature_k - 273.15
    temperature_f = (temperature_k * 9/5) - 459.67
    weather_id = data["weather"][0]["id"]
    weather_description = data["weather"][0]["description"]
    return{
        "temperature": temperature_c,
        "weather_id": weather_id,
        "description": weather_description 
    }
def get_weather_emoji(weather_id):
    if 200 <= weather_id <= 232:
        return "⛈"
    elif 300 <= weather_id <= 321:
        return "🌦"
    elif 500 <= weather_id <= 531:
        return "🌧"
    elif 600 <= weather_id <= 622:
        return "❄"
    elif 701 <= weather_id <= 741:
        return "🌫"
    elif weather_id == 762:
        return "🌋"
    elif weather_id == 771:
        return "💨"
    elif weather_id == 781:
        return "🌪"
    elif weather_id == 800:
        return "☀"
    elif 801 <= weather_id <= 804:
        return "☁"
    else:
        return ""
    

limiter = Limiter(key_func=get_remote_address,app=app,default_limits=["20 per minute"])

'''
Rate limiting by the remote_address of the request
A default rate limit of 20 request per minute applied to all routes.
The slow route having an explicit rate limit decorator will bypass the default rate limit and only allow 1 request per minute.
The medium route inherits the default limits and adds on a decorated limit of 1 request per second.
'''
@app.route("/slow")
@limiter.limit("1 per minute")
def slow():
    return ":("


@app.route("/medium")
@limiter.limit("1 per second", override_defaults=False)
def medium():
    return ":|"


@app.route("/fast")
def fast():
    return ":)"



if __name__ == "__main__":
    app.run(debug=True)
