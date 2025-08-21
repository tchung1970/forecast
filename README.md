# Weather Forecast

A Python-based weather forecast application that provides weather forecasts using the OpenWeatherMap API with intelligent location selection and interactive user interface.

## Features

- **Smart Location Detection**: Automatically detects your current location using IP geolocation
- **Korean Language Detection**: Automatically prioritizes Korean locations when Korean characters are detected (e.g., "서울" → Seoul, South Korea)
- **Interactive Location Selection**: When multiple cities match your search, displays options with intelligent search relevance prioritization
- **Intelligent Geocoding**: Uses OpenWeatherMap's geocoding API for accurate location matching
- **Enhanced Country Display**: Shows full country names (e.g., "South Korea", "United States") instead of codes
- **Multi-format Display**: Shows temperatures in both Fahrenheit and Celsius with perfectly aligned output formatting
- **Multi-Day Forecasts**: Provides detailed daily high/low temperatures and weather conditions (3 days default, up to 5 days maximum)
- **Multi-language Support**: Get forecasts in English and Korean
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
   ```

### Usage Examples

```bash
# Interactive mode - prompts for location
python forecast.py

# Specific location
python forecast.py "Los Angeles,CA,US"

# Different city (shows multiple options if ambiguous)
python forecast.py "Seoul"

# 3-day forecast (default)
python forecast.py --days 3 "Seoul,KR"

# Korean language forecast
python forecast.py --lang ko "Seoul,KR"
```

## How It Works

When you search for a location, the application:

1. **Detects Your Location**: Uses IP geolocation to determine your current position
2. **Searches for Matches**: Queries OpenWeatherMap's geocoding API for your search term
3. **Sorts by Relevance**: Prioritizes exact matches and search term relevance over geographic distance
4. **Presents Options**: Shows multiple matches when cities have the same name
5. **Fetches Forecast**: Retrieves weather data for the selected location (3 days default, up to 5 days)
6. **Formats Display**: Shows daily highs/lows in both °F and °C with perfectly aligned columns

### Example Interactive Sessions

**English Location Search:**
```
$ python forecast.py
Enter location (or press Enter for current location): Los Angeles

Multiple Los Angeless found:
1. Los Angeles, California, United States (best match)
2. Los Angeles, Chiriquí, Panama
3. Los Angeles, Sucre, Colombia

Press Enter to choose the best match (1) or select other location (2-3): 

3-day forecast for Los Angeles, California, United States
=========================================================

Thursday, Aug 21 | High:  94°F (35°C) | Low:  77°F (25°C) | Clear Sky
Friday, Aug 22   | High:  95°F (35°C) | Low:  78°F (26°C) | Overcast Clouds
Saturday, Aug 23 | High:  90°F (32°C) | Low:  78°F (25°C) | Clear Sky
```

**Korean Language Detection:**
```
$ python forecast.py "서울"

서울, 대한민국 3일 일기예보
===========================

8월 21일 목요일   | 최고: 33°C (92°F) | 최저: 26°C (78°F) | 맑음
8월 22일 금요일   | 최고: 33°C (92°F) | 최저: 25°C (77°F) | 흐림
8월 23일 토요일   | 최고: 34°C (94°F) | 최저: 26°C (78°F) | 구름 조금
```

**Korean Language Explicit:**
```
$ python forecast.py --lang ko "Seoul,KR"

서울, 대한민국 3일 일기예보
===========================

8월 21일 목요일   | 최고: 33°C (92°F) | 최저: 26°C (78°F) | 맑음
8월 22일 금요일   | 최고: 33°C (92°F) | 최저: 25°C (77°F) | 흐림
8월 23일 토요일   | 최고: 34°C (94°F) | 최저: 26°C (78°F) | 구름 조금
```

## API Information

- **Service**: OpenWeatherMap API
- **Free Tier Limits**: 60 calls/minute, 1,000,000 calls/month, 5-day forecast maximum
- **APIs Used**: 
  - 5-day/3-hour forecast (limited to 5 days maximum)
  - Geocoding for location search
  - Reverse geocoding for coordinates
- **Default Units**: Imperial (Fahrenheit) with Celsius conversion

## Command Line Options

```
usage: forecast.py [-h] [--days DAYS] [--lang LANG] [location]

positional arguments:
  location              Location (city,state,country format, e.g., "Los Angeles,CA,US")

optional arguments:
  -h, --help            show help message
  --days DAYS, -d DAYS  Number of days to forecast (default: 3, max: 5 due to API limit)
  --lang LANG, -l LANG  Language code (en for English, ko for Korean)
```

## Author

**Thomas Chung**  
Created: August 21, 2025

## License

This project is open source and available under the MIT License.