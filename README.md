# Weather Forecast

A Python-based weather forecast application that provides 5-day weather forecasts using the OpenWeatherMap API with intelligent location selection and interactive user interface.

## Features

- **Smart Location Detection**: Automatically detects your current location using IP geolocation
- **Korean Language Detection**: Automatically prioritizes Korean locations when Korean characters are detected (e.g., "서울" → Seoul, South Korea)
- **Interactive Location Selection**: When multiple cities match your search, displays options with intelligent "best match" sorting
- **Intelligent Geocoding**: Uses OpenWeatherMap's geocoding API for accurate location matching
- **Enhanced Country Display**: Shows full country names (e.g., "South Korea", "United States") instead of codes
- **Multi-format Display**: Shows temperatures in both Fahrenheit and Celsius
- **5-Day Forecasts**: Provides detailed daily high/low temperatures and weather conditions
- **Multi-language Support**: Get forecasts in different languages
- **Flexible API Key Management**: Support for command line, environment file, or environment variable

## Quick Start

### Prerequisites

- Python 3.x
- Free API key from [OpenWeatherMap](https://openweathermap.org/api)

### Setup

1. **Get your API key**:
   - Sign up at [openweathermap.org](https://openweathermap.org/api)
   - Get your free API key

2. **Configure your API key** (choose one method):
   ```bash
   # Method 1: Add to ~/.env file (recommended)
   echo "OPENWEATHERMAP_API_KEY=your_api_key_here" >> ~/.env
   
   # Method 2: Set environment variable
   export OPENWEATHERMAP_API_KEY=your_api_key_here
   
   # Method 3: Use command line flag
   python3 forecast.py --api-key your_api_key_here
   ```

3. **Make script executable** (optional):
   ```bash
   chmod +x forecast.py
   ```

### Usage Examples

```bash
# Interactive mode - prompts for location
python3 forecast.py

# Specific location
python3 forecast.py "Los Angeles,CA,US"

# Different city (shows multiple options if ambiguous)
python3 forecast.py "Seoul"

# 3-day forecast
python3 forecast.py --days 3 "Seoul,KR"

# Korean language forecast
python3 forecast.py --lang ko "Seoul,KR"
```

## How It Works

When you search for a location, the application:

1. **Detects Your Location**: Uses IP geolocation to determine your current position
2. **Searches for Matches**: Queries OpenWeatherMap's geocoding API for your search term
3. **Sorts by Distance**: Orders results by proximity to your current location
4. **Presents Options**: Shows multiple matches when cities have the same name
5. **Fetches Forecast**: Retrieves 5-day weather data for the selected location
6. **Formats Display**: Shows daily highs/lows in both °F and °C

### Example Interactive Sessions

**English Location Search:**
```
$ python3 forecast.py
Enter location (or press Enter for current location): Los Angeles

Multiple Los Angeless found:
1. Los Angeles, California, United States (best match)
2. Los Angeles, Chiriquí, Panama
3. Los Angeles, Sucre, Colombia

Press Enter to choose the best match (1) or select other location (2-3): 

5-day forecast for Los Angeles, California, United States
========================================================

Monday, Aug 21     | High: 78°F (26°C) | Low: 65°F (18°C) | Clear Sky
Tuesday, Aug 22    | High: 80°F (27°C) | Low: 67°F (19°C) | Few Clouds
Wednesday, Aug 23  | High: 82°F (28°C) | Low: 68°F (20°C) | Scattered Clouds
Thursday, Aug 24   | High: 79°F (26°C) | Low: 66°F (19°C) | Light Rain
Friday, Aug 25     | High: 76°F (24°C) | Low: 64°F (18°C) | Partly Cloudy
```

**Korean Language Detection:**
```
$ python3 forecast.py "서울"

5-day forecast for Seoul, South Korea
======================================

Thursday, Aug 21 | High: 92°F (33°C) | Low: 79°F (26°C) | Few Clouds
Friday, Aug 22   | High: 92°F (33°C) | Low: 77°F (25°C) | Overcast Clouds
Saturday, Aug 23 | High: 94°F (34°C) | Low: 78°F (26°C) | Few Clouds
Sunday, Aug 24   | High: 88°F (31°C) | Low: 79°F (26°C) | Clear Sky
Monday, Aug 25   | High: 89°F (32°C) | Low: 75°F (24°C) | Light Rain
```

## API Information

- **Service**: OpenWeatherMap API
- **Free Tier Limits**: 60 calls/minute, 1,000,000 calls/month
- **APIs Used**: 
  - 5-day/3-hour forecast
  - Geocoding for location search
  - Reverse geocoding for coordinates
- **Default Units**: Imperial (Fahrenheit) with Celsius conversion

## Command Line Options

```
usage: forecast.py [-h] [--days DAYS] [--lang LANG] [--api-key API_KEY] [location]

positional arguments:
  location              Location (city,state,country format, e.g., "Los Angeles,CA,US")

optional arguments:
  -h, --help            show help message
  --days DAYS, -d DAYS  Number of days to forecast (default: 5)
  --lang LANG, -l LANG  Language code (e.g., en, fr, de, es, ru)
  --api-key API_KEY, -k API_KEY
                        OpenWeatherMap API key
```

## Author

**Thomas Chung**  
Created: August 21, 2025

## License

This project is open source and available under the MIT License.