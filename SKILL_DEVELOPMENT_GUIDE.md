# OpenClaw Skill Development Guide

A comprehensive guide to creating custom skills for OpenClaw.

## Table of Contents

1. [What is a Skill?](#what-is-a-skill)
2. [Skill Architecture](#skill-architecture)
3. [SKILL.md Format](#skillmd-format)
4. [Step-by-Step Tutorial](#step-by-step-tutorial)
5. [Advanced Features](#advanced-features)
6. [Best Practices](#best-practices)
7. [Debugging & Testing](#debugging--testing)
8. [Publishing to ClawHub](#publishing-to-clawhub)

---

## What is a Skill?

A skill is a directory containing a `SKILL.md` file that provides instructions and tool definitions to the LLM. Skills are the primary way to extend OpenClaw's capabilities.

### Why Create Skills?

- **Encapsulate workflows**: Package complex multi-step processes
- **Add new tools**: Integrate external APIs and services
- **Customize behavior**: Tailor the AI to your specific needs
- **Share knowledge**: Distribute useful capabilities to others

---

## Skill Architecture

### Directory Structure

```
my-skill/
├── SKILL.md          # Required: Main skill definition
├── README.md         # Optional: Documentation
├── scripts/          # Optional: Helper scripts
│   └── helper.sh
├── templates/        # Optional: Template files
│   └── output.tmpl
└── resources/        # Optional: Static resources
    └── data.json
```

### Loading Locations

Skills are loaded from three places (in order of precedence):

| Location | Priority | Purpose |
|----------|----------|---------|
| `<workspace>/skills/` | Highest | User's personal skills |
| `~/.openclaw/skills/` | Medium | Shared skills for all agents |
| Bundled skills | Lowest | Pre-installed with OpenClaw |

---

## SKILL.md Format

### Basic Structure

```markdown
---
name: skill-name
description: A brief description of what this skill does
---

# Skill Title

Main instructions for the AI agent...
```

### YAML Frontmatter Fields

#### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique skill identifier (use lowercase with hyphens) |
| `description` | string | Brief description shown to users |

#### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `homepage` | string | URL for more information |
| `user-invocable` | boolean | Expose as slash command (default: true) |
| `disable-model-invocation` | boolean | Exclude from model prompt (default: false) |
| `command-dispatch` | string | Set to "tool" for direct tool dispatch |
| `command-tool` | string | Tool name for command dispatch |
| `metadata` | object | Additional configuration (see below) |

### Metadata Configuration

The `metadata.openclaw` field controls skill loading and requirements:

```markdown
---
name: my-api-skill
description: Integrates with an external API
metadata:
  {
    "openclaw":
      {
        "emoji": "🔌",
        "homepage": "https://example.com",
        "requires":
          {
            "bins": ["curl"],
            "env": ["API_KEY"],
            "config": ["myApi.enabled"]
          },
        "primaryEnv": "API_KEY"
      }
  }
---
```

#### Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `emoji` | string | Emoji shown in UI |
| `homepage` | string | URL shown as "Website" |
| `os` | array | Platform restriction: `["darwin", "linux", "win32"]` |
| `always` | boolean | Skip all gating checks |
| `requires.bins` | array | Required executables on PATH |
| `requires.env` | array | Required environment variables |
| `requires.config` | array | Required config paths in openclaw.json |
| `primaryEnv` | string | Main API key variable name |
| `install` | array | Installer specs for the skill |

---

## Step-by-Step Tutorial

### Example: Creating a Weather Skill

#### Step 1: Create the Directory

```bash
mkdir -p ~/.openclaw/workspace/skills/weather
```

#### Step 2: Create SKILL.md

```markdown
---
name: weather
description: Get current weather and forecasts for any location
metadata:
  {
    "openclaw":
      {
        "emoji": "🌤️",
        "requires": { "bins": ["curl"] }
      }
  }
---

# Weather Skill

Provides weather information for any location worldwide.

## Usage

When the user asks about weather:

1. Extract the location from the user's request
2. Use the `exec` tool to call the weather API:
   ```bash
   curl -s "https://wttr.in/{location}?format=j1"
   ```
3. Parse the JSON response
4. Present the weather information in a clear, readable format

## Example

User: "What's the weather in Tokyo?"

Response:
- Use `exec` to run: `curl -s "https://wttr.in/Tokyo?format=j1"`
- Parse and format the response
- Return: "Currently in Tokyo: 18°C, Partly cloudy..."
```

#### Step 3: Test the Skill

```bash
# Refresh skills
openclaw agent --message "What's the weather in Tokyo?"
```

---

## Advanced Features

### Using `{baseDir}`

Reference the skill's directory in your instructions:

```markdown
# Template Skill

Use the template at {baseDir}/templates/output.tmpl to format results.
```

### Custom Tools

Define tools the skill should use:

```markdown
---
name: my-tool-skill
description: A skill with custom tool usage
---

# Custom Tool Skill

Use the following tools:
- `exec` for running shell commands
- `browser` for web interactions
- `web_fetch` for fetching URLs

## Workflow

1. Use `web_fetch` to get the page content
2. Use `exec` to process the data
3. Return formatted results
```

### Environment Variables

Skills can require and use environment variables:

```markdown
---
name: api-skill
description: Integrates with an external API
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["MY_API_KEY"] },
        "primaryEnv": "MY_API_KEY"
      }
  }
---

# API Integration Skill

Use the `MY_API_KEY` environment variable for authentication.

When making API calls, include:
```bash
curl -H "Authorization: Bearer $MY_API_KEY" "https://api.example.com/data"
```
```

### Installer Specs

Define how users can install dependencies:

```markdown
metadata:
  {
    "openclaw":
      {
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "my-tool",
              "bins": ["my-tool"],
              "label": "Install my-tool (brew)"
            }
          ]
      }
  }
```

Installer types:
- `brew`: Homebrew package
- `node`: npm/pnpm/yarn package
- `go`: Go package
- `download`: Direct download

---

## Best Practices

### 1. Clear Instructions

Write instructions that tell the AI **what to do**, not how to be an AI:

```markdown
# Good
When the user asks for X:
1. Fetch data from Y
2. Parse the result
3. Format and return

# Bad
You are an AI assistant that helps with X...
```

### 2. Security First

- Validate user inputs before passing to shell commands
- Use `{baseDir}` for file paths instead of hardcoded paths
- Never expose sensitive credentials in instructions

### 3. Concise Descriptions

Keep descriptions short and informative:

```markdown
# Good
description: Generate AI images using DALL-E

# Bad
description: This skill allows you to generate amazing AI images using OpenAI's DALL-E API, which is a powerful image generation model...
```

### 4. Handle Errors

Include error handling in your instructions:

```markdown
## Error Handling

If the API call fails:
1. Check if the location is valid
2. Retry with a simplified location name
3. If still failing, inform the user and suggest alternatives
```

---

## Debugging & Testing

### Test Locally

```bash
# Test a skill directly
openclaw agent --message "use my weather skill for Tokyo"

# Check skill loading
openclaw agent --message "list available skills"
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Skill not loaded | Check file is named `SKILL.md` (case-sensitive) |
| Tool not available | Verify tool is in `requires.bins` |
| Env var missing | Add to `requires.env` and configure in openclaw.json |
| Permission denied | Check script is executable: `chmod +x script.sh` |

### View Loaded Skills

Ask your agent: "What skills do you have available?"

---

## Publishing to ClawHub

### 1. Prepare Your Skill

Ensure your skill:
- Has a complete `SKILL.md`
- Includes a `README.md` with usage examples
- Has been tested locally

### 2. Create a Git Repository

```bash
cd my-skill
git init
git add .
git commit -m "Initial commit"
```

### 3. Publish to ClawHub

```bash
clawhub publish my-skill
```

Or submit via [https://clawhub.com](https://clawhub.com)

---

## Examples

See the [examples/](./examples/) directory for complete skill examples:

- `weather/` - Simple API integration
- `image-gen/` - AI image generation
- `data-processing/` - Complex multi-step workflow

---

## Resources

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Registry](https://clawhub.com)
- [AgentSkills Specification](https://agentskills.io)
- [GitHub Discussions](https://github.com/openclaw/openclaw/discussions)