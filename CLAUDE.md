# Weather Forecast

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based weather forecast application that uses the OpenWeatherMap API to provide weather information. The main script is `forecast.py` which provides a command-line interface for getting weather forecasts (3 days default, up to 5 days maximum).

## Development Commands

```bash
# Setup: Add your API key to ~/.env file
echo "OPENWEATHERMAP_API_KEY=your_api_key_here" >> ~/.env

# Run the weather forecast script (prompts for location)
python forecast.py

# Get weather for a specific location
python forecast.py "Los Angeles,CA,US"

# Get multi-day forecast (3 days default, 5 days maximum)
python forecast.py --days 3 "Seoul,KR"

# Get weather in Korean
python forecast.py --lang ko "Seoul,KR"
```

## Architecture Overview

- **forecast.py**: Main script containing weather fetching functionality and CLI interface
- Uses Python's built-in `urllib` for HTTP requests to OpenWeatherMap API
- Command-line argument parsing with `argparse`
- Supports city,state,country location format with intelligent geocoding
- Interactive location selection when multiple matches found
- IP geolocation fallback for current location detection
- **Korean language detection**: Automatically prioritizes Korean locations when Korean characters are detected
- **Smart location sorting**: Prioritizes search term relevance over geographic distance for better location matching
- **Enhanced country name display**: Shows full country names instead of codes for better clarity
- **Auto-Korean localization**: Korean cities automatically use Korean formatting (names, dates, weather descriptions)
- **Celsius-first display**: Korean formatting shows Celsius first, then Fahrenheit
- Error handling for network requests and invalid inputs
- Clean text-based output format with both Fahrenheit and Celsius
- **Consistent formatting**: All vertical separators are perfectly aligned for clean output display
- Configurable forecast length with 3-day default and 5-day maximum

## API Integration

The application integrates with OpenWeatherMap API:
- Base URL: http://api.openweathermap.org/data/2.5/forecast
- Requires free API key from openweathermap.org 
- Free plan limits: 60 API calls/minute, 1,000,000 calls/month, 5-day forecast maximum
- Includes: Current weather API, 3-hour forecast for 5 days API, Weather Maps, Air Pollution API, Geocoding API
- API key can be provided via:
  - ~/.env file: `OPENWEATHERMAP_API_KEY=your_key`
  - Environment variable: `OPENWEATHERMAP_API_KEY`
- Supports location-based queries in "city,state,country" format
- Uses geocoding API for intelligent location matching and disambiguation
- Reverse geocoding for coordinate-based lookups
- Configurable forecast duration (up to 5 days maximum due to API limitation)
- Multi-language support (English and Korean)
- Temperature units: Fahrenheit first for English (92°F (33°C)), Celsius first for Korean (33°C (92°F))
- Korean weather descriptions: Automatic translation of weather conditions (Clear Sky → 맑음)