# Skill Factory 🛠️

A comprehensive guide for developing OpenClaw skills. OpenClaw skills extend your AI assistant with new capabilities.

## What is a Skill?

A skill is a directory containing a `SKILL.md` file that provides instructions and tool definitions to the LLM, optionally including scripts and resources.

## Documentation

| Document | Description |
|----------|-------------|
| [SKILL_DEVELOPMENT_GUIDE.md](./SKILL_DEVELOPMENT_GUIDE.md) | Complete skill development tutorial |
| [templates/](./templates/) | SKILL.md templates for different use cases |
| [examples/](./examples/) | Example skills to learn from |

## Quick Start

### 1. Create a Skill Directory

```bash
mkdir -p ~/.openclaw/workspace/skills/my-skill
```

### 2. Create SKILL.md

```markdown
---
name: my-skill
description: A brief description of what this skill does
---

# My Skill

Instructions for the AI agent on how to use this skill...
```

### 3. Refresh Skills

Ask your agent to "refresh skills" or restart the gateway.

## Skill Locations

Skills are loaded from three places (in order of precedence):

1. **Workspace skills**: `<workspace>/skills/` (highest priority)
2. **Managed skills**: `~/.openclaw/skills/`
3. **Bundled skills**: Shipped with OpenClaw installation

## Resources

- [Official Documentation](https://docs.openclaw.ai/tools/skills)
- [ClawHub - Skill Registry](https://clawhub.com)
- [AgentSkills Spec](https://agentskills.io)

## Contributing

Feel free to contribute your own skills or improvements to this guide.

## License

MIT