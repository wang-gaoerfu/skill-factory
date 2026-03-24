---
name: script-skill-template
description: Template for skills that use helper scripts
metadata:
  {
    "openclaw":
      {
        "emoji": "📜",
        "requires": { "bins": ["bash"] }
      }
  }
---

# Script-Based Skill

This skill uses helper scripts in the `scripts/` directory.

## Directory Structure

```
script-skill/
├── SKILL.md
├── scripts/
│   ├── helper.sh
│   └── processor.py
└── README.md
```

## Usage

When the user requests [action]:

1. Use the `exec` tool to run the helper script:
   ```bash
   bash {baseDir}/scripts/helper.sh --param "value"
   ```

2. Process the output

3. Return formatted results

## Scripts

### helper.sh

Main processing script.

```bash
#!/bin/bash
# Helper script for [purpose]

PARAM="$1"

# Do something useful
echo "Processing: $PARAM"
```

## Security Notes

- Always validate user input before passing to scripts
- Use quotes around variables to prevent injection
- Sanitize file paths and arguments