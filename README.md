# Skill Factory 🛠️

OpenClaw 技能开发工厂，包含开发指南、模板、示例和实际技能项目。

## 目录结构

```
skill-factory/
├── README.md                           # 本文件
├── SKILL_DEVELOPMENT_GUIDE.md          # 技能开发教程（英文）
├── SKILL_DEVELOPMENT_GUIDE_CN.md       # 技能开发教程（中文）
├── templates/                          # SKILL.md 模板
├── examples/                           # 示例技能
│   ├── weather/
│   ├── image-gen/
│   └── data-processing/
└── skills/                             # 实际技能项目
    └── companion-agent/                # 陪伴型智能体
        ├── SKILL.md                    # 技能定义
        ├── src/                        # 源代码
        ├── config/                     # 配置
        └── docs/                       # 项目文档
```

## 技能项目

### 陪伴型智能体 (companion-agent)

一个可定制化的陪伴型智能体框架，支持多场景：

- **阶段1**：儿童教育陪伴（优先）
- **阶段2**：老人陪伴
- **阶段3**：单身男女陪伴
- **阶段4**：心理陪伴

详见 [skills/companion-agent/](./skills/companion-agent/)

## 开发指南

| 文档 | 说明 |
|------|------|
| [SKILL_DEVELOPMENT_GUIDE.md](./SKILL_DEVELOPMENT_GUIDE.md) | 完整的技能开发教程（英文） |
| [SKILL_DEVELOPMENT_GUIDE_CN.md](./SKILL_DEVELOPMENT_GUIDE_CN.md) | 完整的技能开发教程（中文） |
| [templates/](./templates/) | 不同场景的 SKILL.md 模板 |
| [examples/](./examples/) | 示例技能供学习参考 |

## 快速开始

### 1. 创建技能目录

```bash
mkdir -p skills/my-skill
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

## 资源链接

- [OpenClaw 官方文档](https://docs.openclaw.ai/tools/skills)
- [ClawHub 技能市场](https://clawhub.com)
- [AgentSkills 规范](https://agentskills.io)

## 贡献

欢迎贡献你自己的技能或改进本指南。

## 许可证

MIT