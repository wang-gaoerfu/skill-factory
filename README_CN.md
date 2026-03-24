# Skill Factory 技能工厂 🛠️

OpenClaw 技能开发完整指南。OpenClaw 技能为你的 AI 助手扩展新能力。

## 什么是 Skill？

Skill 是一个包含 `SKILL.md` 文件的目录，该文件为 LLM 提供指令和工具定义，可选包含脚本和资源。

## 文档导航

| 文档 | 说明 |
|------|------|
| [SKILL_DEVELOPMENT_GUIDE_CN.md](./SKILL_DEVELOPMENT_GUIDE_CN.md) | 完整的技能开发教程 |
| [templates/](./templates/) | 不同场景的 SKILL.md 模板 |
| [examples/](./examples/) | 示例技能供学习参考 |

## 快速开始

### 1. 创建技能目录

```bash
mkdir -p ~/.openclaw/workspace/skills/my-skill
```

### 2. 创建 SKILL.md

```markdown
---
name: my-skill
description: 简要描述这个技能的功能
---

# 我的技能

给 AI 智能体的使用说明...
```

### 3. 刷新技能

让你的智能体"刷新技能"或重启 Gateway。

## 技能存放位置

技能从三个位置加载（按优先级排序）：

1. **工作区技能**：`<workspace>/skills/`（最高优先级）
2. **托管技能**：`~/.openclaw/skills/`
3. **内置技能**：随 OpenClaw 安装包提供

## 资源链接

- [官方文档](https://docs.openclaw.ai/tools/skills)
- [ClawHub - 技能市场](https://clawhub.com)
- [AgentSkills 规范](https://agentskills.io)

## 贡献

欢迎贡献你自己的技能或改进本指南。

## 许可证

MIT