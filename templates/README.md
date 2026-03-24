# Skill Templates

This directory contains SKILL.md templates for different skill types.

## Available Templates

| Template | File | Use Case |
|----------|------|----------|
| Basic Skill | `basic-skill.md` | Simple skills without external dependencies |
| API Integration | `api-integration.md` | Skills that call external APIs |
| Script-Based | `script-skill.md` | Skills with helper scripts |

## How to Use

1. Copy the appropriate template to your skill directory:
   ```bash
   cp templates/basic-skill.md ~/.openclaw/workspace/skills/my-skill/SKILL.md
   ```

2. Edit the file and customize:
   - `name`: Your skill's unique identifier
   - `description`: What your skill does
   - Instructions in the body

3. Test your skill:
   ```bash
   openclaw agent --message "test my new skill"
   ```

## Template Contents

Each template includes:

- **YAML frontmatter**: Metadata and configuration
- **Usage section**: How the skill should be invoked
- **Example**: Sample interaction
- **Error handling**: What to do when things go wrong