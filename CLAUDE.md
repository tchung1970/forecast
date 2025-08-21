# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based weather forecast application that uses the OpenWeatherMap API to provide weather information. The main script is `forecast.py` which provides a command-line interface for getting weather forecasts.

## Development Commands

```bash
# Setup: Add your API key to ~/.env file
echo "OPENWEATHERMAP_API_KEY=your_api_key_here" >> ~/.env

# Run the weather forecast script (prompts for location)
python3 forecast.py

# Get weather for a specific location
python3 forecast.py "New York,NY,US"

# Get multi-day forecast
python3 forecast.py --days 3 "London,GB"

# Get weather in a different language
python3 forecast.py --lang fr "Paris,FR"

# Override API key via command line
python3 forecast.py --api-key YOUR_KEY

# Make script executable
chmod +x forecast.py
```

## Architecture Overview

- **forecast.py**: Main script containing weather fetching functionality and CLI interface
- Uses Python's built-in `urllib` for HTTP requests to OpenWeatherMap API
- Command-line argument parsing with `argparse`
- Supports city,state,country location format
- Error handling for network requests and invalid inputs
- Clean text-based output format

## API Integration

The application integrates with OpenWeatherMap API:
- Base URL: http://api.openweathermap.org/data/2.5/forecast
- Requires free API key from openweathermap.org 
- Free plan limits: 60 API calls/minute, 1,000,000 calls/month
- Includes: Current weather API, 3-hour forecast for 5 days API, Weather Maps, Air Pollution API, Geocoding API
- API key can be provided via:
  - Command line: `--api-key YOUR_KEY`
  - ~/.env file: `OPENWEATHERMAP_API_KEY=your_key`
  - Environment variable: `OPENWEATHERMAP_API_KEY`
- Supports location-based queries in "city,state,country" format
- Configurable forecast duration (up to 5 days)
- Multi-language support
- Imperial units (Fahrenheit) by default