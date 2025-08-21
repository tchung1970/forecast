#!/usr/bin/env python3
# forecast.py
# by Thomas Chung
# on 2025-08-21
# 
# This script provides a weather forecast application that:
# 1. Accepts location input from user (command line or interactive prompt)
# 2. Uses IP geolocation to determine current location as fallback
# 3. Detects Korean characters in input and prioritizes Korean locations
# 4. Calls OpenWeatherMap API to get geocoding data for location matching
# 5. Presents multiple location options with intelligent "best match" sorting
# 6. Shows full country names instead of codes for better clarity
# 7. Fetches 5-day weather forecast data from OpenWeatherMap API
# 8. Displays formatted forecast with daily high/low temperatures in F and C
# 9. Supports multiple languages and configurable forecast duration
# 10. Handles API key from environment file or environment variable

"""
Weather forecast script using OpenWeatherMap API
"""

import argparse
import json
import math
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Optional


def load_env_file(env_path: str = "~/.env") -> dict:
    """Load environment variables from .env file"""
    env_vars = {}
    env_file = Path(env_path).expanduser()
    
    if env_file.exists():
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        # Remove quotes if present
                        value = value.strip('"\'')
                        env_vars[key.strip()] = value
        except Exception as e:
            print(f"Warning: Could not read {env_file}: {e}", file=sys.stderr)
    
    return env_vars


def get_current_location() -> str:
    """Get current location using IP geolocation"""
    try:
        # Use a free IP geolocation service
        with urllib.request.urlopen("http://ip-api.com/json/") as response:
            data = json.loads(response.read().decode('utf-8'))
            if data['status'] == 'success':
                city = data['city']
                region = data['regionName']
                country = data['countryCode']
                return f"{city},{region},{country}"
    except Exception:
        pass
    
    # Fallback to Los Angeles if geolocation fails
    return "Los Angeles,CA,US"


def get_current_coordinates() -> tuple:
    """Get current coordinates using IP geolocation"""
    try:
        # Use a free IP geolocation service
        with urllib.request.urlopen("http://ip-api.com/json/") as response:
            data = json.loads(response.read().decode('utf-8'))
            if data['status'] == 'success':
                return (data['lat'], data['lon'])
    except Exception:
        pass
    
    # Fallback to Los Angeles coordinates
    return (34.0522, -118.2437)


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates in kilometers using Haversine formula"""
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r


def has_korean_characters(text: str) -> bool:
    """Check if text contains Korean characters"""
    for char in text:
        if '\uac00' <= char <= '\ud7af':  # Hangul syllables
            return True
        if '\u3130' <= char <= '\u318f':  # Hangul compatibility jamo
            return True
        if '\ua960' <= char <= '\ua97f':  # Hangul jamo extended-A
            return True
        if '\ud7b0' <= char <= '\ud7ff':  # Hangul jamo extended-B
            return True
    return False


def smart_location_sort(geo_data: list, original_location: str, current_lat: float, current_lon: float) -> tuple:
    """Sort locations intelligently based on input language and distance"""
    # Calculate distances for all locations
    for loc in geo_data:
        loc['distance'] = calculate_distance(current_lat, current_lon, loc['lat'], loc['lon'])
    
    # Check if input contains Korean characters
    is_korean_input = has_korean_characters(original_location)
    if is_korean_input:
        # Only return Korean locations (country code 'KR')
        korean_locs = [loc for loc in geo_data if loc['country'] == 'KR']
        
        # Sort Korean locations by distance
        korean_locs.sort(key=lambda x: x['distance'])
        
        return korean_locs, is_korean_input
    else:
        # Default sorting by distance only
        geo_data.sort(key=lambda x: x['distance'])
        return geo_data, is_korean_input


def format_date_korean(dt: datetime) -> str:
    """Format date in Korean"""
    korean_days = {
        'Monday': '월요일',
        'Tuesday': '화요일', 
        'Wednesday': '수요일',
        'Thursday': '목요일',
        'Friday': '금요일',
        'Saturday': '토요일',
        'Sunday': '일요일'
    }
    
    korean_months = {
        'Jan': '1월', 'Feb': '2월', 'Mar': '3월', 'Apr': '4월',
        'May': '5월', 'Jun': '6월', 'Jul': '7월', 'Aug': '8월',
        'Sep': '9월', 'Oct': '10월', 'Nov': '11월', 'Dec': '12월'
    }
    
    day_name = dt.strftime('%A')
    month_abbr = dt.strftime('%b')
    day_num = dt.strftime('%d')
    
    korean_day = korean_days.get(day_name, day_name)
    korean_month = korean_months.get(month_abbr, month_abbr)
    
    return f"{korean_month} {day_num}일 {korean_day}"


def prompt_for_location() -> str:
    """Prompt user for location input"""
    try:
        current_loc = get_current_location()
        location = input(f"Enter location (or press Enter for current location): ").strip()
        if location:
            return location
        else:
            print(f"Using current location: {current_loc}")
            return current_loc
    except (KeyboardInterrupt, EOFError):
        current_loc = get_current_location()
        print(f"\nUsing current location: {current_loc}")
        return current_loc


def get_weather(location: str = None, days: int = 5, lang: str = "en", api_key: str = "demo_key", _original_location: str = None) -> str:
    """
    Fetch weather forecast from OpenWeatherMap API
    
    Args:
        location: Location to get weather for (city,state,country)
        days: Number of days to forecast (limited by API)
        lang: Language code for localization
        api_key: OpenWeatherMap API key
    
    Returns:
        Weather forecast as string
    """
    # Use provided API key
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    
    # Get location - prompt user if none provided
    if location is None:
        location = prompt_for_location()
    
    # First try to find the nearest location using geocoding
    original_location = location
    try:
        # Handle different location formats
        if ',' in location:
            # For "Los Angeles, CA" format, try "Los Angeles,CA,US"
            parts = [part.strip() for part in location.split(',')]
            if len(parts) == 2:
                # Assume US state if only 2 parts
                location = f"{parts[0]},{parts[1]},US"
        
        # Use geocoding to find nearest location
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={urllib.parse.quote(original_location)}&limit=5&appid={api_key}"
        with urllib.request.urlopen(geocoding_url) as geo_response:
            geo_data = json.loads(geo_response.read().decode('utf-8'))
            
        # Sort by distance from current location and use the nearest one
        if len(geo_data) > 1:
            current_lat, current_lon = get_current_coordinates()
            geo_data, is_korean_input = smart_location_sort(geo_data, original_location, current_lat, current_lon)
        else:
            is_korean_input = has_korean_characters(original_location)
            
        # Use coordinates of the nearest location
        nearest_loc = geo_data[0]
        params = {
                'lat': nearest_loc['lat'],
                'lon': nearest_loc['lon'],
                'appid': api_key,
                'units': 'imperial',
                'lang': lang
            }
    except Exception:
        # Fallback to original method
        params = {
            'q': location,
            'appid': api_key,
            'units': 'imperial',
            'lang': lang
        }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # Location not found, try geocoding search as fallback
            try:
                geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={urllib.parse.quote(location)}&limit=5&appid={api_key}"
                with urllib.request.urlopen(geocoding_url) as geo_response:
                    geo_data = json.loads(geo_response.read().decode('utf-8'))
                
                # Sort by distance from current location
                if len(geo_data) > 1:
                    current_lat, current_lon = get_current_coordinates()
                    geo_data, is_korean_input = smart_location_sort(geo_data, location, current_lat, current_lon)
                else:
                    is_korean_input = has_korean_characters(location)
                
                if not geo_data:
                    return f"Location '{location}' not found. Please try a more specific location (e.g., 'Los Angeles, CA' or 'London, UK')."
                
                # Show options if multiple found
                if len(geo_data) > 1:
                    print(f"\nMultiple locations found for '{location}':")
                    print()
                    for i, loc in enumerate(geo_data[:3], 1):
                        city = loc['name']
                        country_name = loc['country']
                        state = loc.get('state', '')
                        
                        if state and country_name == 'US':
                            loc_display = f"{city}, {state}"
                        elif state:
                            loc_display = f"{city}, {state}, {country_name}"
                        else:
                            loc_display = f"{city}, {country_name}"
                        
                        print(f"{i}. {loc_display}")
                    
                    print()
                    try:
                        if is_korean_input:
                            choice = input("Select location (1-3) or press Enter for #1: ").strip()
                        else:
                            choice = input("Select location (1-3) or press Enter for #1: ").strip()
                        if choice == '' or choice == '1':
                            selected_loc = geo_data[0]
                        elif choice == '2' and len(geo_data) > 1:
                            selected_loc = geo_data[1]
                        elif choice == '3' and len(geo_data) > 2:
                            selected_loc = geo_data[2]
                        else:
                            selected_loc = geo_data[0]  # Default to first
                    except (KeyboardInterrupt, EOFError, ValueError):
                        selected_loc = geo_data[0]
                else:
                    selected_loc = geo_data[0]
                
                # Use selected location coordinates to get weather
                lat, lon = selected_loc['lat'], selected_loc['lon']
                params = {
                    'lat': lat,
                    'lon': lon,
                    'appid': api_key,
                    'units': 'imperial',
                    'lang': lang
                }
                url = f"{base_url}?{urllib.parse.urlencode(params)}"
                with urllib.request.urlopen(url) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    
            except Exception as fallback_error:
                return f"Location '{location}' not found. Please try a more specific location (e.g., 'Los Angeles, CA' or 'London, UK')."
        else:
            raise Exception(f"HTTP Error {e.code}: {e.reason}")
    
    try:
        # Format the weather data - simple 5-day forecast
        city_name = data['city']['name']
        country = data['city']['country']
        coords = data['city']['coord']
        
        # Build location display with full country names
        country_names = {
            'US': 'United States',
            'CA': 'Canada', 
            'GB': 'United Kingdom',
            'FR': 'France',
            'DE': 'Germany',
            'JP': 'Japan',
            'KR': 'South Korea',
            'CN': 'China',
            'IN': 'India',
            'AU': 'Australia',
            'BR': 'Brazil',
            'MX': 'Mexico',
            'ES': 'Spain',
            'IT': 'Italy',
            'NL': 'Netherlands',
            'PA': 'Panama',
            'CO': 'Colombia',
            'SY': 'Syria',
            'PK': 'Pakistan',
            'RU': 'Russia',
            'UA': 'Ukraine',
            'PL': 'Poland',
            'TR': 'Turkey',
            'EG': 'Egypt',
            'SA': 'Saudi Arabia',
            'AE': 'United Arab Emirates',
            'IL': 'Israel',
            'IR': 'Iran',
            'IQ': 'Iraq',
            'JO': 'Jordan',
            'LB': 'Lebanon',
            'SG': 'Singapore',
            'TH': 'Thailand',
            'VN': 'Vietnam',
            'MY': 'Malaysia',
            'ID': 'Indonesia',
            'PH': 'Philippines',
            'BD': 'Bangladesh',
            'LK': 'Sri Lanka',
            'NP': 'Nepal',
            'MM': 'Myanmar',
            'KH': 'Cambodia',
            'LA': 'Laos',
            'MN': 'Mongolia',
            'KZ': 'Kazakhstan',
            'UZ': 'Uzbekistan',
            'KG': 'Kyrgyzstan',
            'TJ': 'Tajikistan',
            'TM': 'Turkmenistan',
            'AF': 'Afghanistan',
            'ZA': 'South Africa',
            'NG': 'Nigeria',
            'KE': 'Kenya',
            'ET': 'Ethiopia',
            'GH': 'Ghana',
            'TZ': 'Tanzania',
            'UG': 'Uganda',
            'MA': 'Morocco',
            'DZ': 'Algeria',
            'TN': 'Tunisia',
            'LY': 'Libya',
            'SD': 'Sudan',
            'AR': 'Argentina',
            'CL': 'Chile',
            'PE': 'Peru',
            'VE': 'Venezuela',
            'UY': 'Uruguay',
            'PY': 'Paraguay',
            'BO': 'Bolivia',
            'EC': 'Ecuador',
            'CR': 'Costa Rica',
            'GT': 'Guatemala',
            'HN': 'Honduras',
            'NI': 'Nicaragua',
            'SV': 'El Salvador',
            'BZ': 'Belize',
            'CU': 'Cuba',
            'JM': 'Jamaica',
            'HT': 'Haiti',
            'DO': 'Dominican Republic',
            'PR': 'Puerto Rico',
            'TT': 'Trinidad and Tobago'
        }
        
        country_full = country_names.get(country, country)
        
        # Try to get state/region info from the geocoding if available
        state_info = ""
        try:
            # Use the same geocoding call to get state information
            geocoding_url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={coords['lat']}&lon={coords['lon']}&limit=1&appid={api_key}"
            with urllib.request.urlopen(geocoding_url) as geo_response:
                geo_data = json.loads(geo_response.read().decode('utf-8'))
                if geo_data and 'state' in geo_data[0]:
                    state_info = f", {geo_data[0]['state']}"
        except:
            pass
        
        location_display = f"{city_name}{state_info}, {country_full}"
        coord_display = f"(Lat: {coords['lat']:.2f}, Lon: {coords['lon']:.2f})"
        
        # Show multiple location options if available (for locations that don't 404)
        search_location = _original_location or location
        try:
            # Get multiple location options using geocoding API  
            geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={urllib.parse.quote(search_location)}&limit=5&appid={api_key}"
            with urllib.request.urlopen(geocoding_url) as geo_response:
                geo_data = json.loads(geo_response.read().decode('utf-8'))
            
            # Sort by distance from current location
            if len(geo_data) > 1:
                current_lat, current_lon = get_current_coordinates()
                geo_data, is_korean_input = smart_location_sort(geo_data, search_location, current_lat, current_lon)
            else:
                is_korean_input = has_korean_characters(search_location)
                
            # Only show options if we have multiple locations AND the current result might not be the intended one
            if len(geo_data) > 1:
                print(f"\nMultiple {city_name}s found:")
                if is_korean_input:
                    print(f"1. {location_display}")
                else:
                    print(f"1. {location_display} (best match)")
                
                displayed_options = 1
                for i, loc in enumerate(geo_data[:3]):
                    city = loc['name']
                    country_code = loc['country']
                    state = loc.get('state', '')
                    
                    # Get full country name
                    country_full = country_names.get(country_code, country_code)
                    
                    # Format location display with full country names
                    if state:
                        loc_display = f"{city}, {state}, {country_full}"
                    else:
                        loc_display = f"{city}, {country_full}"
                    
                    # Skip if this is the same as current location
                    if abs(loc['lat'] - coords['lat']) > 0.1 or abs(loc['lon'] - coords['lon']) > 0.1:
                        print(f"{displayed_options + 1}. {loc_display}")
                        displayed_options += 1
                
                if displayed_options > 1:
                    print()
                    try:
                        if is_korean_input:
                            choice = input("Press Enter to choose option (1) or select other location (2-3): ").strip()
                        else:
                            choice = input("Press Enter to choose the best match (1) or select other location (2-3): ").strip()
                        if choice in ['2', '3']:
                            choice_idx = int(choice) - 2  # Adjust for skipped current location
                            if choice_idx < len(geo_data):
                                selected_loc = None
                                current_idx = 0
                                for loc in geo_data:
                                    if abs(loc['lat'] - coords['lat']) > 0.1 or abs(loc['lon'] - coords['lon']) > 0.1:
                                        if current_idx == choice_idx:
                                            selected_loc = loc
                                            break
                                        current_idx += 1
                                
                                if selected_loc:
                                    # Use the selected location's coordinates
                                    lat, lon = selected_loc['lat'], selected_loc['lon']
                                    params = {
                                        'lat': lat,
                                        'lon': lon,
                                        'appid': api_key,
                                        'units': 'imperial',
                                        'lang': lang
                                    }
                                    url = f"{base_url}?{urllib.parse.urlencode(params)}"
                                    # Re-fetch with correct coordinates
                                    with urllib.request.urlopen(url) as response:
                                        data = json.loads(response.read().decode('utf-8'))
                                    # Update the location info with selected choice
                                    city_name = data['city']['name']
                                    country = data['city']['country']
                                    coords = data['city']['coord']
                                    
                                    # Rebuild location display
                                    country_full = country_names.get(country, country)
                                    state_info = ""
                                    try:
                                        geocoding_url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={coords['lat']}&lon={coords['lon']}&limit=1&appid={api_key}"
                                        with urllib.request.urlopen(geocoding_url) as geo_response:
                                            geo_data_rev = json.loads(geo_response.read().decode('utf-8'))
                                            if geo_data_rev and 'state' in geo_data_rev[0]:
                                                state_info = f", {geo_data_rev[0]['state']}"
                                    except:
                                        pass
                                    location_display = f"{city_name}{state_info}, {country_full}"
                    except (KeyboardInterrupt, EOFError, ValueError):
                        pass  # Continue with current location
            
        except Exception:
            # If geocoding fails, just continue with original result
            pass
        
        # Format header and content based on language
        if lang == 'ko':
            forecast_text = f"\n{location_display} {days}일 일기예보\n"
            forecast_text += "=" * (len(location_display.encode('utf-8')) + len(str(days)) + 10) + "\n\n"
        else:
            forecast_text = f"\n{days}-day forecast for {location_display}\n"
            forecast_text += "=" * (len(location_display) + len(str(days)) + 20) + "\n\n"
        
        # Group forecasts by day and get daily highs/lows
        daily_forecasts = {}
        
        for item in data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            date_key = dt.strftime('%Y-%m-%d')
            
            # Format date based on language
            if lang == 'ko':
                date_str = format_date_korean(dt)
            else:
                date_str = dt.strftime('%A, %b %d')
            
            temp = item['main']['temp']
            desc = item['weather'][0]['description'].title()
            
            if date_key not in daily_forecasts:
                daily_forecasts[date_key] = {
                    'date_str': date_str,
                    'high': temp,
                    'low': temp,
                    'desc': desc
                }
            else:
                daily_forecasts[date_key]['high'] = max(daily_forecasts[date_key]['high'], temp)
                daily_forecasts[date_key]['low'] = min(daily_forecasts[date_key]['low'], temp)
        
        # Display up to requested number of days
        day_count = 0
        for date_key in sorted(daily_forecasts.keys()):
            if day_count >= days:
                break
                
            day = daily_forecasts[date_key]
            high_f = round(day['high'])
            low_f = round(day['low'])
            high_c = round((day['high'] - 32) * 5/9)
            low_c = round((day['low'] - 32) * 5/9)
            
            # Format output based on language
            if lang == 'ko':
                forecast_text += f"{day['date_str']:12} | 최고: {high_f:2}°F ({high_c:2}°C) | 최저: {low_f:2}°F ({low_c:2}°C) | {day['desc']}\n"
            else:
                forecast_text += f"{day['date_str']:15} | High: {high_f:2}°F ({high_c:2}°C) | Low: {low_f:2}°F ({low_c:2}°C) | {day['desc']}\n"
            day_count += 1
        
        return forecast_text
        
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return """OpenWeatherMap API key required.

Setup:
1. Get a free API key from openweathermap.org
2. Add it to ~/.env file:
   echo "OPENWEATHERMAP_API_KEY=your_api_key_here" >> ~/.env
3. Run the script again"""
        else:
            raise Exception(f"HTTP Error {e.code}: {e.reason}")
    except Exception as e:
        raise Exception(f"Error getting weather: {e}")




def main():
    """Main function to handle command line interface"""
    parser = argparse.ArgumentParser(
        description="Get weather forecast using OpenWeatherMap API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Prompts for location
  %(prog)s "Los Angeles,CA,US"          # Los Angeles weather  
  %(prog)s "Seoul,KR" --days 5          # Seoul 5-day forecast
  %(prog)s "Seoul,KR" --lang ko         # Seoul weather in Korean
        """)
    
    parser.add_argument(
        'location', 
        nargs='?', 
        default=None,
        help='Location (city,state,country format, e.g., "Los Angeles,CA,US") - prompts if not provided'
    )
    parser.add_argument(
        '--days', '-d',
        type=int,
        default=3,
        help='Number of days to forecast (default: 3, max: 5 due to API limit)'
    )
    parser.add_argument(
        '--lang', '-l',
        default='en',
        help='Language code (e.g., en, fr, de, es, ru)'
    )
    
    args = parser.parse_args()
    
    try:
        # Validate days parameter
        if args.days > 5:
            print("Sorry, the maximum forecast length is 5 days due to OpenWeatherMap API limitations.")
            sys.exit(1)
        
        if args.days < 1:
            print("Sorry, the minimum forecast length is 1 day.")
            sys.exit(1)
        
        # Load environment variables from ~/.env
        env_vars = load_env_file()
        
        # Get API key from environment file or environment variable
        api_key = (env_vars.get('OPENWEATHERMAP_API_KEY') or 
                  os.getenv('OPENWEATHERMAP_API_KEY') or 
                  "demo_key")
        
        weather = get_weather(args.location, args.days, args.lang, api_key, args.location)
        print(weather)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()