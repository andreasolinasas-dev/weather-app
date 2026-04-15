"""
Weather Application - Main Flask Application
A beautiful weather web application to check weather conditions for any city worldwide.
"""

from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import requests
import os
import math
import hashlib
import unicodedata
from datetime import datetime, timedelta
from datetime import timezone
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'weather-app-secret-key-2024')

# Search history storage (in-memory for simplicity, could use database)
search_history = []
MAX_HISTORY = 10

# OpenWeatherMap API Configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5"
SUPPORTED_LANGUAGES = {'it', 'en', 'fr', 'es'}
DEFAULT_LANGUAGE = 'it'
BACKGROUND_CACHE_TTL_SECONDS = 12 * 60 * 60
background_photo_cache = {}

CITY_POSTCARD_QUERIES = {
    'sydney,au': ['sydney opera house', 'sydney harbour bridge', 'sydney harbour skyline', 'sydney australia skyline'],
    'tokyo,jp': ['tokyo skyline', 'shibuya crossing tokyo', 'tokyo tower', 'tokyo japan city lights'],
    'berlin,de': ['berlin brandenburg gate', 'berlin tv tower', 'berlin skyline', 'berlin germany architecture'],
    'madrid,es': ['madrid plaza mayor', 'madrid royal palace', 'madrid gran via', 'madrid skyline'],
    'new york,us': ['new york skyline', 'statue of liberty', 'brooklyn bridge', 'central park new york'],
    'paris,fr': ['paris eiffel tower', 'paris seine', 'paris louvre', 'paris skyline'],
    'london,gb': ['london tower bridge', 'london big ben', 'london thames skyline', 'london uk cityscape'],
    'turin,it': ['turin mole antonelliana', 'turin piazza castello', 'turin italy skyline', 'turin city center'],
    'venice,it': ['venice canal gondola', 'venice rialto bridge', 'venice st mark square', 'venice lagoon'],
    'florence,it': ['florence duomo', 'florence ponte vecchio', 'florence skyline', 'florence italy old town'],
    'rome,it': ['rome colosseum', 'rome vatican', 'rome pantheon', 'rome skyline'],
    'milan,it': ['milan duomo', 'milan galleria vittorio emanuele', 'milan skyline', 'milan city center'],
    'naples,it': ['naples vesuvius', 'naples bay', 'naples historic center', 'naples waterfront'],
    'cagliari,it': ['cagliari harbor', 'cagliari italy coastline', 'cagliari bastion', 'cagliari sardinia skyline'],
    'nuuk,gl': ['nuuk greenland harbor', 'nuuk greenland colorful houses', 'nuuk greenland fjord', 'nuuk greenland skyline'],
    'sisimiut,gl': ['sisimiut greenland harbor', 'sisimiut colorful houses', 'sisimiut greenland coast', 'sisimiut fjord'],
    'ilulissat,gl': ['ilulissat greenland icefjord', 'ilulissat iceberg', 'ilulissat greenland coast', 'ilulissat arctic landscape'],
    'aasiaat,gl': ['aasiaat greenland harbor', 'aasiaat colorful houses', 'aasiaat arctic coast', 'aasiaat greenland town'],
    'qaqortoq,gl': ['qaqortoq greenland colorful houses', 'qaqortoq harbor', 'qaqortoq greenland coast', 'qaqortoq arctic town'],
    'maniitsoq,gl': ['maniitsoq greenland harbor', 'maniitsoq fjord', 'maniitsoq arctic coast', 'maniitsoq colorful houses'],
    'tasiilaq,gl': ['tasiilaq greenland mountains', 'tasiilaq harbor', 'tasiilaq fjord', 'tasiilaq arctic town'],
    'paamiut,gl': ['paamiut greenland coast', 'paamiut harbor', 'paamiut colorful houses', 'paamiut fjord'],
    'narsaq,gl': ['narsaq greenland fjord', 'narsaq greenland village', 'narsaq harbor', 'narsaq arctic landscape'],
    'uummannaq,gl': ['uummannaq greenland iceberg', 'uummannaq harbor', 'uummannaq fjord', 'uummannaq arctic town']
}

def normalize_language(lang):
    """Return a supported OpenWeather/UI language code."""
    """Return a supported OpenWeather/UI language code."""
    if not lang:
        return DEFAULT_LANGUAGE
    lang = str(lang).lower().strip()
    return lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE


def normalize_photo_key(value):
    """Normalize city labels so postcard queries match reliably."""
    text = str(value or '').strip()
    for prefix in ('Comune di ', 'City of ', 'Municipality of '):
        if text.lower().startswith(prefix.lower()):
            text = text[len(prefix):]
            break

    text = unicodedata.normalize('NFD', text)
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    return ' '.join(text.split()).lower()


def utc_to_local_datetime(timestamp, timezone_offset_seconds=0):
    """Convert a UTC timestamp to a city-local datetime using a fixed offset."""
    return datetime.fromtimestamp(timestamp + int(timezone_offset_seconds or 0), tz=timezone.utc).replace(tzinfo=None)


def format_local_datetime(timestamp, timezone_offset_seconds=0, fmt='%Y-%m-%d %H:%M'):
    """Format a UTC timestamp as local city time."""
    return utc_to_local_datetime(timestamp, timezone_offset_seconds).strftime(fmt)


def parse_time_string(time_text):
    """Parse a HH:MM or HH:MM:SS string into minutes since midnight."""
    if not time_text:
        return None
    parts = str(time_text).split(':')
    try:
        hour = int(parts[0])
        minute = int(parts[1]) if len(parts) > 1 else 0
        return hour * 60 + minute
    except (TypeError, ValueError, IndexError):
        return None


def get_city_postcard_queries(city_name, country_code=None):
    """Return postcard-style search queries for a city."""
    key = normalize_photo_key(f"{city_name},{country_code}" if country_code else city_name)
    if key in CITY_POSTCARD_QUERIES:
        return CITY_POSTCARD_QUERIES[key]

    city_key = normalize_photo_key(city_name)
    if city_key in CITY_POSTCARD_QUERIES:
        return CITY_POSTCARD_QUERIES[city_key]

    city_label = ' '.join(str(city_name or '').split())
    if country_code:
        return [
            f"{city_label} skyline",
            f"{city_label} cityscape",
            f"{city_label} landmark",
            f"{city_label} travel"
        ]

    return [
        f"{city_label} skyline",
        f"{city_label} cityscape",
        f"{city_label} landmark",
        f"{city_label} travel"
    ]


def read_background_photo_cache(cache_key):
    entry = background_photo_cache.get(cache_key)
    if not entry:
        return None

    stored_at = entry.get('stored_at')
    if not stored_at:
        return None

    if (datetime.utcnow() - stored_at).total_seconds() > BACKGROUND_CACHE_TTL_SECONDS:
        background_photo_cache.pop(cache_key, None)
        return None

    return entry.get('payload')


def write_background_photo_cache(cache_key, payload):
    background_photo_cache[cache_key] = {
        'stored_at': datetime.utcnow(),
        'payload': payload
    }


def fetch_unsplash_photo(query, lang=DEFAULT_LANGUAGE):
    """Fetch a single postcard-style photo from LoremFlickr (free alternative)."""
    try:
        # Use query as keyword for LoremFlickr
        image_url = f"https://loremflickr.com/1600/900/{query.replace(' ', ',')}"
        
        return {
            'source': 'loremflickr',
            'image_url': image_url,
            'photo_url': f"https://loremflickr.com/search/{query.replace(' ', ',')}",
            'photographer': 'LoremFlickr',
            'photographer_url': 'https://loremflickr.com',
            'query': query
        }
    except Exception:
        return None
        return None


def get_city_background_photo(city_name, country_code=None, lang=DEFAULT_LANGUAGE):
    """Get a real-time postcard-style background photo for a city."""
    cache_key = normalize_photo_key(f"{city_name},{country_code}" if country_code else city_name)
    cached = read_background_photo_cache(cache_key)
    if cached:
        return cached

    for query in get_city_postcard_queries(city_name, country_code):
        result = fetch_unsplash_photo(query, lang=lang)
        if result:
            write_background_photo_cache(cache_key, result)
            return result

    return None

def validate_city_name(city_name):
    """
    Validate city name input for weather search.
    
    Performs comprehensive validation on city name input to ensure it's a valid
    location for weather API requests. Checks for empty input, invalid characters,
    numeric-only input, minimum length, and common invalid patterns.
    
    Args:
        city_name (str): The city name to validate
        
    Returns:
        tuple: A tuple containing:
            - bool: True if valid, False if invalid
            - str: Error message if invalid, or the cleaned city name if valid
            
    Examples:
        >>> validate_city_name("Rome")
        (True, "Rome")
        
        >>> validate_city_name("...")
        (False, "Invalid city name: contains only punctuation")
        
        >>> validate_city_name("123")
        (False, "Invalid city name: contains only numbers")
        
        >>> validate_city_name("test")
        (False, "Invalid city name")
    """
    if not city_name or not city_name.strip():
        return False, "City name cannot be empty"
    
    # Remove extra whitespace
    city_name = city_name.strip()
    
    # Check for invalid characters (only dots, numbers, or special chars)
    if all(c in '.-,;:!?\'"()[]{}' for c in city_name):
        return False, "Invalid city name: contains only punctuation"
    
    # Check if it's just numbers
    if city_name.replace(' ', '').isdigit():
        return False, "Invalid city name: contains only numbers"
    
    # Check minimum length
    if len(city_name) < 2:
        return False, "City name too short"
    
    # Check for common invalid patterns
    invalid_patterns = ['test', 'asdf', 'qwerty', 'xxx', '123', 'abc']
    if city_name.lower() in invalid_patterns:
        return False, "Invalid city name"
    
    return True, city_name

def get_weather_data(city_name, country_code=None, lang=DEFAULT_LANGUAGE):
    """
    Fetch current weather data from OpenWeatherMap API.
    
    Retrieves comprehensive weather information for a specified city, including
    temperature, humidity, wind speed, pressure, visibility, and more. The function
    validates the city name, makes an API request, and handles various error conditions.
    
    Args:
        city_name (str): The name of the city to fetch weather for
        country_code (str, optional): ISO 3166-1 alpha-2 country code to disambiguate
            cities with the same name (e.g., "US" for United States, "IT" for Italy)
        
    Returns:
        dict: A dictionary containing either:
            - Weather data with keys: 'coord', 'weather', 'base', 'main', 'visibility',
              'wind', 'clouds', 'dt', 'sys', 'timezone', 'id', 'name', 'cod'
            - Error data with 'error' key describing the issue
            
    Raises:
        No exceptions are raised; errors are returned as dictionaries with 'error' key.
        
    Examples:
        >>> # Basic usage
        >>> weather = get_weather_data("Rome")
        >>> print(weather['name'], weather['main']['temp'])
        Rome 22.5
        
        >>> # With country code
        >>> weather = get_weather_data("Paris", "FR")
        >>> print(weather['name'])
        Paris
        
        >>> # Error handling
        >>> result = get_weather_data("...")
        >>> print(result)
        {'error': 'Invalid city name: contains only punctuation'}
        
        >>> # City not found
        >>> result = get_weather_data("NonExistentCity")
        >>> print(result)
        {'error': 'City "NonExistentCity" not found. Please check the spelling and try again.'}
        
    Note:
        - Requires a valid OpenWeatherMap API key set in environment variables
        - API calls have a 10-second timeout
        - Temperature is returned in Celsius (metric units)
        - The function validates city names to prevent invalid API requests
    """
    try:
        # Validate city name
        is_valid, result = validate_city_name(city_name)
        if not is_valid:
            return {'error': result}
        
        city_name = result
        
        # Build query
        query = city_name
        if country_code:
            query = f"{city_name},{country_code}"
        
        # Make API request
        url = f"{BASE_URL}/weather"
        params = {
            'q': query,
            'appid': API_KEY,
            'units': 'metric',  # Celsius
            'lang': normalize_language(lang)
        }
        
        # Debug: Log the request
        print(f"🔍 Making API request for: {query}")
        print(f"🔗 Request URL: {url}")
        print(f"🔑 API Key: {API_KEY[:10]}..." if API_KEY else "🔑 API Key: NOT SET")
        
        response = requests.get(url, params=params, timeout=10)
        
        # Check for 404 - city not found
        if response.status_code == 404:
            return {'error': f'City "{city_name}" not found. Please check the spelling and try again.'}
        
        # Check for 401 - unauthorized
        if response.status_code == 401:
            return {'error': 'API authentication failed. Please check your OpenWeatherMap API key.'}
        
        response.raise_for_status()
        data = response.json()
        
        # Verify the returned city matches the requested one only when no country code is provided.
        # Some cities use localized names (for example, Turin/Torino), so we trust the API
        # more when the country is already disambiguated.
        if not country_code:
            returned_city = data.get('name', '').lower()
            requested_city = city_name.lower()
            
            if requested_city not in returned_city and returned_city not in requested_city:
                if not (returned_city.startswith(requested_city[:3]) or requested_city.startswith(returned_city[:3])):
                    return {'error': f'City "{city_name}" not found. Did you mean {data.get("name", "a different location")}?'}
        
        return data
    
    except requests.exceptions.HTTPError as e:
        if 'response' in locals() and response.status_code == 404:
            return {'error': f'City "{city_name}" not found. Please check the spelling and try again.'}
        elif 'response' in locals() and response.status_code == 401:
            return {'error': 'API authentication failed. Please check your OpenWeatherMap API key.'}
        else:
            return {'error': f'API returned error: {str(e)}'}
    except requests.exceptions.RequestException as e:
        return {'error': f"Failed to fetch weather data: {str(e)}"}
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}

def get_weather_by_coordinates(lat, lon, lang=DEFAULT_LANGUAGE):
    """Fetch weather data by geographic coordinates"""
    try:
        url = f"{BASE_URL}/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY,
            'units': 'metric',
            'lang': normalize_language(lang)
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {'error': f"Failed to fetch weather data: {str(e)}"}

def get_forecast_data(city_name, lang=DEFAULT_LANGUAGE):
    """Fetch 5-day weather forecast"""
    try:
        url = f"{BASE_URL}/forecast"
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric',
            'cnt': 40,  # 5 days * 8 intervals per day
            'lang': normalize_language(lang)
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {'error': f"Failed to fetch forecast data: {str(e)}"}

def geocode_location(query):
    """Geocode a location name to coordinates using Nominatim"""
    try:
        geolocator = Nominatim(user_agent="weather_app_v1")
        location = geolocator.geocode(query, timeout=10)
        if location:
            return {
                'lat': location.latitude,
                'lon': location.longitude,
                'address': location.address
            }
        return None
    except (GeocoderTimedOut, GeocoderServiceError):
        return None

def format_weather_data(data):
    """Format weather data for display"""
    if 'error' in data:
        return None
    
    weather = data['weather'][0]
    main = data['main']
    wind = data.get('wind', {})
    clouds = data.get('clouds', {}).get('all', 0)
    visibility = data.get('visibility', 0) / 1000  # Convert to km
    pressure = main.get('pressure', 0)
    humidity = main.get('humidity', 0)
    timezone_offset = data.get('timezone', 0)
    
    # Convert timestamp to datetime
    sunrise = format_local_datetime(data['sys']['sunrise'], timezone_offset, '%H:%M')
    sunset = format_local_datetime(data['sys']['sunset'], timezone_offset, '%H:%M')
    local_timestamp = format_local_datetime(data['dt'], timezone_offset, '%Y-%m-%d %H:%M')
    
    return {
        'city': data['name'],
        'country': data['sys']['country'],
        'timezone_offset': timezone_offset,
        'temperature': round(main['temp'], 1),
        'feels_like': round(main['feels_like'], 1),
        'temp_min': round(main['temp_min'], 1),
        'temp_max': round(main['temp_max'], 1),
        'weather_main': weather['main'],
        'weather_description': weather['description'],
        'weather_icon': weather['icon'],
        'wind_speed': wind.get('speed', 0),
        'wind_direction': wind.get('deg', 0),
        'clouds': clouds,
        'visibility': round(visibility, 1),
        'pressure': pressure,
        'humidity': humidity,
        'sunrise': sunrise,
        'sunset': sunset,
        'timestamp': local_timestamp,
        'sunrise_unix': data['sys']['sunrise'],
        'sunset_unix': data['sys']['sunset'],
        'timestamp_unix': data['dt']
    }

def format_forecast_data(data):
    """Format forecast data for display"""
    if 'error' in data:
        return None
    
    forecasts = []
    daily_forecasts = {}
    timezone_offset = data.get('city', {}).get('timezone', 0)

    for item in data['list']:
        if 'dt' in item:
            local_dt = utc_to_local_datetime(item['dt'], timezone_offset)
        elif 'dt_txt' in item:
            local_dt = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
        else:
            continue
        date_key = local_dt.strftime('%Y-%m-%d')
        weather = item['weather'][0]
        main = item['main']

        if date_key not in daily_forecasts:
            daily_forecasts[date_key] = {
                'date': date_key,
                'temperature': round(main['temp'], 1),
                'temp_min': round(main['temp_min'], 1),
                'temp_max': round(main['temp_max'], 1),
                'weather': weather['main'],
                'description': weather['description'],
                'icon': weather['icon'],
                'humidity': main['humidity'],
                'wind_speed': item.get('wind', {}).get('speed', 0),
                'best_score': abs(local_dt.hour - 12),
                'local_time': local_dt.strftime('%H:%M')
            }
            continue

        forecast = daily_forecasts[date_key]
        forecast['temp_min'] = min(forecast['temp_min'], round(main['temp_min'], 1))
        forecast['temp_max'] = max(forecast['temp_max'], round(main['temp_max'], 1))

        score = abs(local_dt.hour - 12)
        if score < forecast['best_score']:
            forecast.update({
                'temperature': round(main['temp'], 1),
                'weather': weather['main'],
                'description': weather['description'],
                'icon': weather['icon'],
                'humidity': main['humidity'],
                'wind_speed': item.get('wind', {}).get('speed', 0),
                'best_score': score,
                'local_time': local_dt.strftime('%H:%M')
            })
    
    for item in sorted(daily_forecasts.values(), key=lambda forecast: forecast['date']):
        item.pop('best_score', None)
        forecasts.append(item)

    return forecasts

def add_to_history(city_name, country_code=None):
    """Add city to search history"""
    global search_history
    
    # Create a unique key for the search
    search_key = f"{city_name}{f',{country_code}' if country_code else ''}"
    
    # Remove if already exists
    search_history = [item for item in search_history if item['key'] != search_key]
    
    # Add to beginning
    search_history.insert(0, {
        'key': search_key,
        'city': city_name,
        'country': country_code,
        'display': f"{city_name}{f',{country_code}' if country_code else ''}",
        'timestamp': datetime.now().isoformat()
    })
    
    # Keep only last MAX_HISTORY items
    search_history = search_history[:MAX_HISTORY]

def get_search_history():
    """Get search history"""
    return search_history

def calculate_moon_phase(date):
    """Calculate moon phase for a given date"""
    # Simple moon phase calculation
    # Moon cycle is approximately 29.53 days
    reference_date = datetime(2000, 1, 6, 18, 14)  # New moon reference
    days_since_reference = (date - reference_date).days
    moon_age = days_since_reference % 29.53
    
    if moon_age < 1.84:
        return "New Moon", "🌑"
    elif moon_age < 5.53:
        return "Waxing Crescent", "🌒"
    elif moon_age < 9.22:
        return "First Quarter", "🌓"
    elif moon_age < 12.91:
        return "Waxing Gibbous", "🌔"
    elif moon_age < 16.60:
        return "Full Moon", "🌕"
    elif moon_age < 20.29:
        return "Waning Gibbous", "🌖"
    elif moon_age < 23.98:
        return "Last Quarter", "🌗"
    else:
        return "Waning Crescent", "🌘"

def get_moon_info(lat, lon):
    """Get moon phase and information"""
    try:
        # Get current moon phase
        current_phase, emoji = calculate_moon_phase(datetime.now())
        
        # Calculate next full moon
        reference_date = datetime(2000, 1, 6, 18, 14)
        days_since_reference = (datetime.now() - reference_date).days
        moon_age = days_since_reference % 29.53
        
        days_to_full_moon = (14.765 - moon_age) % 29.53
        next_full_moon = datetime.now() + timedelta(days=days_to_full_moon)
        
        # Calculate moonrise/moonset (approximate)
        # This is a simplified calculation
        moonrise_hour = (18 + int(moon_age * 0.8)) % 24
        moonset_hour = (6 + int(moon_age * 0.8)) % 24
        
        return {
            'phase': current_phase,
            'emoji': emoji,
            'illumination': round((moon_age / 29.53) * 100, 1),
            'next_full_moon': next_full_moon.strftime('%Y-%m-%d'),
            'moonrise': f"{moonrise_hour:02d}:00",
            'moonset': f"{moonset_hour:02d}:00",
            'age_days': round(moon_age, 1)
        }
    except Exception as e:
        return {'error': f"Failed to calculate moon info: {str(e)}"}

def get_astronomical_info(lat, lon):
    """Get astronomical information"""
    try:
        # Get moon info
        moon_info = get_moon_info(lat, lon)
        
        # Get sun info (simplified)
        # In a real application, you'd use a proper astronomical library
        return {
            'moon': moon_info,
            'sunrise': '06:30',  # Would be calculated based on coordinates
            'sunset': '18:45',   # Would be calculated based on coordinates
            'daylight_hours': '12h 15m'
        }
    except Exception as e:
        return {'error': f"Failed to get astronomical info: {str(e)}"}

def get_fun_weather_facts(weather_data):
    """Generate fun facts based on weather data"""
    if 'error' in weather_data:
        return []
    
    facts = []
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data.get('wind', {}).get('speed', 0)
    weather_main = weather_data['weather'][0]['main']
    
    # Temperature facts
    if temp > 30:
        facts.append("🔥 It's hot! Perfect day for ice cream and swimming!")
    elif temp < 0:
        facts.append("❄️ Brrr! Time to bundle up and enjoy some hot chocolate!")
    elif temp > 20:
        facts.append("☀️ Lovely weather! Great day to be outdoors!")
    
    # Weather condition facts
    if weather_main == 'Clear':
        facts.append("☀️ Clear skies! Perfect for stargazing tonight!")
    elif weather_main == 'Clouds':
        facts.append("☁️ Cloudy day! Great time for indoor activities!")
    elif weather_main == 'Rain':
        facts.append("🌧️ Rainy day! Perfect for reading a book with a warm drink!")
    elif weather_main == 'Snow':
        facts.append("❄️ Snow day! Time to build a snowman!")
    
    # Humidity facts
    if humidity > 80:
        facts.append("💧 High humidity! Your hair might be extra curly today!")
    elif humidity < 30:
        facts.append("🌵 Low humidity! Don't forget to stay hydrated!")
    
    # Wind facts
    if wind_speed > 15:
        facts.append("💨 Windy day! Hold onto your hats!")
    
    # Fun general facts
    facts.append(f"🌍 Did you know? The current temperature is {temp}°C!")
    facts.append(f"💨 Wind is blowing at {wind_speed} m/s from the {get_wind_direction(weather_data.get('wind', {}).get('deg', 0))}!")
    
    return facts[:3]  # Limit to 3 facts

def get_wind_direction(degrees):
    """Convert wind degrees to cardinal direction"""
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 
                  'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    if degrees is None:
        return 'N/A'
    index = round(degrees / 22.5) % 16
    return directions[index]

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/weather', methods=['GET'])
def api_weather():
    """API endpoint for current weather"""
    city = request.args.get('city')
    country = request.args.get('country')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    lang = request.args.get('lang', DEFAULT_LANGUAGE)
    
    if not city and not (lat and lon):
        return jsonify({'error': 'Please provide a city name or coordinates'}), 400
    
    if lat and lon:
        data = get_weather_by_coordinates(lat, lon, lang=lang)
    else:
        data = get_weather_data(city, country, lang=lang)
    
    if 'error' in data:
        return jsonify(data), 500
    
    formatted_data = format_weather_data(data)
    return jsonify(formatted_data)

@app.route('/api/forecast', methods=['GET'])
def api_forecast():
    """API endpoint for weather forecast"""
    city = request.args.get('city')
    lang = request.args.get('lang', DEFAULT_LANGUAGE)
    
    if not city:
        return jsonify({'error': 'Please provide a city name'}), 400
    
    data = get_forecast_data(city, lang=lang)
    
    if 'error' in data:
        return jsonify(data), 500
    
    formatted_data = format_forecast_data(data)
    return jsonify(formatted_data)

@app.route('/api/geocode', methods=['GET'])
def api_geocode():
    """API endpoint for geocoding"""
    query = request.args.get('q')
    
    if not query:
        return jsonify({'error': 'Please provide a query'}), 400
    
    result = geocode_location(query)
    
    if result:
        return jsonify(result)
    
    return jsonify({'error': 'Location not found'}), 404

@app.route('/api/popular-cities', methods=['GET'])
def api_popular_cities():
    """API endpoint for popular cities"""
    popular_cities = [
        {'name': 'Rome', 'country': 'IT', 'display': 'Rome, Italy'},
        {'name': 'Milan', 'country': 'IT', 'display': 'Milan, Italy'},
        {'name': 'Naples', 'country': 'IT', 'display': 'Naples, Italy'},
        {'name': 'Florence', 'country': 'IT', 'display': 'Florence, Italy'},
        {'name': 'Venice', 'country': 'IT', 'display': 'Venice, Italy'},
        {'name': 'Turin', 'country': 'IT', 'display': 'Turin, Italy'},
        {'name': 'London', 'country': 'GB', 'display': 'London, UK'},
        {'name': 'Paris', 'country': 'FR', 'display': 'Paris, France'},
        {'name': 'Berlin', 'country': 'DE', 'display': 'Berlin, Germany'},
        {'name': 'Madrid', 'country': 'ES', 'display': 'Madrid, Spain'},
        {'name': 'New York', 'country': 'US', 'display': 'New York, USA'},
        {'name': 'Tokyo', 'country': 'JP', 'display': 'Tokyo, Japan'},
        {'name': 'Sydney', 'country': 'AU', 'display': 'Sydney, Australia'},
        {'name': 'Dubai', 'country': 'AE', 'display': 'Dubai, UAE'},
        {'name': 'Moscow', 'country': 'RU', 'display': 'Moscow, Russia'},
        {'name': 'Beijing', 'country': 'CN', 'display': 'Beijing, China'}
    ]
    return jsonify(popular_cities)

@app.route('/api/history', methods=['GET'])
def api_history():
    """API endpoint for search history"""
    return jsonify(search_history)

@app.route('/api/history', methods=['POST'])
def api_add_history():
    """API endpoint to add to search history"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    city = data.get('city')
    country = data.get('country')
    
    if not city:
        return jsonify({'error': 'City name is required'}), 400
    
    add_to_history(city, country)
    return jsonify({'success': True, 'history': search_history})

@app.route('/api/history', methods=['DELETE'])
def api_clear_history():
    """API endpoint to clear search history"""
    global search_history
    search_history = []
    return jsonify({'success': True})

@app.route('/api/moon', methods=['GET'])
def api_moon():
    """API endpoint for moon phase information"""
    lat = request.args.get('lat', 41.9028)  # Default: Rome
    lon = request.args.get('lon', 12.4964)
    
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({'error': 'Invalid coordinates'}), 400
    
    moon_info = get_moon_info(lat, lon)
    return jsonify(moon_info)

@app.route('/api/astronomy', methods=['GET'])
def api_astronomy():
    """API endpoint for astronomical information"""
    lat = request.args.get('lat', 41.9028)
    lon = request.args.get('lon', 12.4964)
    
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({'error': 'Invalid coordinates'}), 400
    
    astro_info = get_astronomical_info(lat, lon)
    return jsonify(astro_info)

@app.route('/api/fun-facts', methods=['GET'])
def api_fun_facts():
    """API endpoint for fun weather facts"""
    city = request.args.get('city')
    country = request.args.get('country')
    lang = request.args.get('lang', DEFAULT_LANGUAGE)
    
    if not city:
        return jsonify({'error': 'City name is required'}), 400
    
    weather_data = get_weather_data(city, country, lang=lang)
    
    if 'error' in weather_data:
        return jsonify(weather_data), 500
    
    facts = get_fun_weather_facts(weather_data)
    return jsonify({'facts': facts, 'city': weather_data['name']})


@app.route('/api/background-photo', methods=['GET'])
def api_background_photo():
    """API endpoint for postcard-style city background photos."""
    city = request.args.get('city')
    country = request.args.get('country')
    lang = request.args.get('lang', DEFAULT_LANGUAGE)

    if not city:
        return jsonify({'error': 'City name is required'}), 400

    photo = get_city_background_photo(city, country, lang=lang)
    if not photo:
        return jsonify({'error': 'Background photo not available'}), 503

    return jsonify(photo)

if __name__ == '__main__':
    # Check if API key is set
    if not API_KEY or API_KEY == 'your_api_key_here':
        print("\n" + "="*60)
        print("WARNING: OpenWeatherMap API key is not configured!")
        print("="*60)
        print("\nTo use this application, you need to:")
        print("1. Get a free API key from: https://openweathermap.org/api")
        print("2. Create a .env file in this directory")
        print("3. Add your API key: OPENWEATHER_API_KEY=your_actual_key")
        print("\nYou can copy .env.example and modify it.")
        print("="*60 + "\n")
    
    print("\n🌤️  Weather Application starting...")
    print("📍 Access the app at: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
