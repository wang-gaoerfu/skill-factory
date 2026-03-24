---
name: weather
description: Get current weather and forecasts for any location worldwide
metadata:
  {
    "openclaw":
      {
        "emoji": "🌤️",
        "homepage": "https://wttr.in",
        "requires": { "bins": ["curl"] }
      }
  }
---

# Weather Skill

Provides weather information for any location worldwide using the wttr.in API.

## Usage

When the user asks about weather, follow these steps:

### Current Weather

1. Extract the location from the user's request
2. Use the `exec` tool to fetch weather data:
   ```bash
   curl -s "https://wttr.in/{location}?format=j1"
   ```
3. Parse the JSON response for:
   - Temperature (current, feels like)
   - Weather condition
   - Humidity
   - Wind speed and direction
4. Present the information in a clear format

### Forecast

For multi-day forecasts:
```bash
curl -s "https://wttr.in/{location}?format=j1&lang=en"
```

## Example Output

User: "What's the weather in Tokyo?"

Response:
```
🌤️ Tokyo Weather

Current: 18°C (feels like 16°C)
Condition: Partly cloudy
Humidity: 65%
Wind: 12 km/h NW

Today: High 22°C, Low 14°C
```

## Supported Locations

- City names: "Tokyo", "New York"
- Airport codes: "JFK", "LHR"
- Coordinates: "35.68,139.69"
- IP-based: Leave empty for current location

## Error Handling

- **Unknown location**: Suggest checking spelling or using a nearby city
- **API error**: Retry once, then inform user
- **No data**: Inform user the service is temporarily unavailable