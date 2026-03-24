---
name: companion-agent
description: 可定制化的陪伴型智能体框架，支持儿童教育陪伴、老人陪伴等多场景
metadata:
  {
    "openclaw":
      {
        "emoji": "🤝",
        "homepage": "https://github.com/wang-gaoerfu/skill-factory/tree/main/skills/companion-agent"
      }
  }
---

# 陪伴型智能体

一个可定制化的陪伴型智能体框架，支持多场景适配。

## 产品演进路线

1. **阶段1**：儿童教育陪伴（优先）
2. **阶段2**：老人陪伴
3. **阶段3**：单身男女陪伴
4. **阶段4**：心理陪伴

## 核心特性

- **前端配置界面**：用户可选择目标用户、陪伴价值、角色性格
- **统一硬件接入**：提供智能家居接入接口
- **纯软件技能**：无需绑定硬件载体

## 文档

- [市场调研报告](./research/market-research.md)
- [竞品分析](./research/competitor-analysis.md)
- [整体架构设计](./design/architecture.md)
- [阶段1：儿童教育陪伴](./design/phase1-kids-education.md)
- [阶段2：老人陪伴](./design/phase2-elderly-care.md)

## 目录结构

```
companion-agent/
├── SKILL.md                    # 技能定义
├── README.md                   # 项目说明
├── docs/                       # 文档（即将迁移到项目根目录）
│   ├── research/               # 调研文档
│   └── design/                 # 设计文档
├── src/                        # 源代码
│   ├── core/                   # 核心模块
│   │   ├── persona_engine.py   # 性格引擎
│   │   ├── memory_system.py    # 记忆系统
│   │   └── dialog_engine.py    # 对话引擎
│   ├── capabilities/           # 能力模块
│   ├── adapters/               # 适配器
│   └── utils/                  # 工具函数
├── config/                     # 配置文件
│   └── personas/               # 角色配置
└── tests/                      # 测试
```

## 开发状态

🚧 规划阶段，尚未开始实现