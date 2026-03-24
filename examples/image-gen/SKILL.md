---
name: image-generation
description: Generate AI images using various providers
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "env": ["OPENAI_API_KEY"] },
        "primaryEnv": "OPENAI_API_KEY"
      }
  }
---

# Image Generation Skill

Generate AI images using OpenAI's DALL-E or other providers.

## Configuration

Set your API key in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "image-generation": {
        "enabled": true,
        "env": {
          "OPENAI_API_KEY": "sk-your-key-here"
        }
      }
    }
  }
}
```

## Usage

When the user wants to generate an image:

### DALL-E 3

```bash
curl -s https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "dall-e-3",
    "prompt": "{user prompt}",
    "size": "1024x1024",
    "quality": "standard",
    "n": 1
  }'
```

### Image Sizes

| Size | Aspect Ratio | Use Case |
|------|--------------|----------|
| 1024x1024 | Square | Portraits, icons |
| 1792x1024 | Landscape | Banners, covers |
| 1024x1792 | Portrait | Phone wallpapers |

### Prompt Enhancement

Help improve user prompts:
1. Add style if not specified (photorealistic, illustration, etc.)
2. Include lighting and composition hints
3. Keep prompts under 4000 characters

## Example

User: "Generate a sunset over mountains"

Enhanced prompt: "A photorealistic sunset over snow-capped mountains, golden hour lighting, dramatic clouds, wide angle view, 8k quality"

## Output

- Extract the `url` from the response
- Present the image URL to the user
- Optionally download and save locally

## Rate Limits

- DALL-E 3: ~5 images per minute
- Consider caching for repeated requests