---
name: api-integration-template
description: Template for skills that integrate with external APIs
metadata:
  {
    "openclaw":
      {
        "emoji": "🔌",
        "requires":
          {
            "bins": ["curl"],
            "env": ["API_KEY"]
          },
        "primaryEnv": "API_KEY"
      }
  }
---

# API Integration Skill

Integrates with [Service Name] API to [do something useful].

## Configuration

This skill requires an API key. Configure it in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "api-integration-template": {
        "enabled": true,
        "env": {
          "API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

## Usage

When the user wants to [use this skill]:

1. Prepare the API request:
   ```bash
   curl -s -H "Authorization: Bearer $API_KEY" \
     "https://api.example.com/endpoint?param=value"
   ```

2. Parse the JSON response

3. Format and present the results

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/endpoint` | GET | Description |

## Error Handling

- **401 Unauthorized**: Check API key is valid
- **429 Rate Limited**: Wait and retry
- **500 Server Error**: Inform user and suggest trying later

## Rate Limits

This API has the following limits:
- X requests per minute
- Y requests per day