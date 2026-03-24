# OpenClaw 技能开发指南

创建 OpenClaw 自定义技能的完整指南。

## 目录

1. [什么是 Skill？](#什么是-skill)
2. [技能架构](#技能架构)
3. [SKILL.md 格式详解](#skillmd-格式详解)
4. [分步教程](#分步教程)
5. [高级功能](#高级功能)
6. [最佳实践](#最佳实践)
7. [调试与测试](#调试与测试)
8. [发布到 ClawHub](#发布到-clawhub)

---

## 什么是 Skill？

Skill 是一个包含 `SKILL.md` 文件的目录，该文件为 LLM 提供指令和工具定义。技能是扩展 OpenClaw 能力的主要方式。

### 为什么要创建技能？

- **封装工作流**：打包复杂的多步骤流程
- **添加新工具**：集成外部 API 和服务
- **定制行为**：让 AI 适应你的特定需求
- **分享知识**：向他人分发有用的功能

---

## 技能架构

### 目录结构

```
my-skill/
├── SKILL.md          # 必需：技能主定义文件
├── README.md         # 可选：文档说明
├── scripts/          # 可选：辅助脚本
│   └── helper.sh
├── templates/        # 可选：模板文件
│   └── output.tmpl
└── resources/        # 可选：静态资源
    └── data.json
```

### 加载位置

技能从三个位置加载（按优先级排序）：

| 位置 | 优先级 | 用途 |
|------|--------|------|
| `<workspace>/skills/` | 最高 | 用户的个人技能 |
| `~/.openclaw/skills/` | 中等 | 所有智能体共享的技能 |
| 内置技能 | 最低 | 随 OpenClaw 预装 |

---

## SKILL.md 格式详解

### 基本结构

```markdown
---
name: skill-name
description: 简要描述这个技能的功能
---

# 技能标题

给 AI 智能体的主要指令...
```

### YAML Frontmatter 字段

#### 必需字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 唯一的技能标识符（使用小写加连字符） |
| `description` | string | 显示给用户的简要描述 |

#### 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `homepage` | string | 更多信息的 URL |
| `user-invocable` | boolean | 作为斜杠命令暴露（默认：true） |
| `disable-model-invocation` | boolean | 从模型提示中排除（默认：false） |
| `command-dispatch` | string | 设为 "tool" 直接调度到工具 |
| `command-tool` | string | 命令调度的工具名称 |
| `metadata` | object | 附加配置（见下方） |

### Metadata 配置

`metadata.openclaw` 字段控制技能加载和要求：

```markdown
---
name: my-api-skill
description: 集成外部 API
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

#### Metadata 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `emoji` | string | UI 中显示的表情符号 |
| `homepage` | string | 显示为"网站"的 URL |
| `os` | array | 平台限制：`["darwin", "linux", "win32"]` |
| `always` | boolean | 跳过所有门禁检查 |
| `requires.bins` | array | PATH 中必需的可执行文件 |
| `requires.env` | array | 必需的环境变量 |
| `requires.config` | array | openclaw.json 中必需的配置路径 |
| `primaryEnv` | string | 主要 API 密钥变量名 |
| `install` | array | 技能安装器规格 |

---

## 分步教程

### 示例：创建天气技能

#### 步骤 1：创建目录

```bash
mkdir -p ~/.openclaw/workspace/skills/weather
```

#### 步骤 2：创建 SKILL.md

```markdown
---
name: weather
description: 获取任意地点的当前天气和预报
metadata:
  {
    "openclaw":
      {
        "emoji": "🌤️",
        "requires": { "bins": ["curl"] }
      }
  }
---

# 天气技能

提供全球任意地点的天气信息。

## 使用方法

当用户询问天气时：

1. 从用户请求中提取地点
2. 使用 `exec` 工具调用天气 API：
   ```bash
   curl -s "https://wttr.in/{location}?format=j1"
   ```
3. 解析 JSON 响应
4. 以清晰可读的格式呈现天气信息

## 示例

用户："东京天气怎么样？"

响应：
- 使用 `exec` 运行：`curl -s "https://wttr.in/Tokyo?format=j1"`
- 解析并格式化响应
- 返回："东京当前：18°C，多云..."
```

#### 步骤 3：测试技能

```bash
# 刷新技能
openclaw agent --message "东京天气怎么样？"
```

---

## 高级功能

### 使用 `{baseDir}`

在指令中引用技能目录：

```markdown
# 模板技能

使用 {baseDir}/templates/output.tmpl 的模板来格式化结果。
```

### 自定义工具

定义技能应使用的工具：

```markdown
---
name: my-tool-skill
description: 使用自定义工具的技能
---

# 自定义工具技能

使用以下工具：
- `exec` 运行 shell 命令
- `browser` 进行网页交互
- `web_fetch` 获取 URL

## 工作流程

1. 使用 `web_fetch` 获取页面内容
2. 使用 `exec` 处理数据
3. 返回格式化结果
```

### 环境变量

技能可以要求和使用环境变量：

```markdown
---
name: api-skill
description: 集成外部 API
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["MY_API_KEY"] },
        "primaryEnv": "MY_API_KEY"
      }
  }
---

# API 集成技能

使用 `MY_API_KEY` 环境变量进行认证。

调用 API 时包含：
```bash
curl -H "Authorization: Bearer $MY_API_KEY" "https://api.example.com/data"
```
```

### 安装器规格

定义用户如何安装依赖：

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
              "label": "安装 my-tool (brew)"
            }
          ]
      }
  }
```

安装器类型：
- `brew`: Homebrew 包
- `node`: npm/pnpm/yarn 包
- `go`: Go 包
- `download`: 直接下载

---

## 最佳实践

### 1. 清晰的指令

写指令要告诉 AI **做什么**，而不是如何成为 AI：

```markdown
# 好的写法
当用户请求 X 时：
1. 从 Y 获取数据
2. 解析结果
3. 格式化并返回

# 不好的写法
你是一个帮助 X 的 AI 助手...
```

### 2. 安全第一

- 在传递给 shell 命令前验证用户输入
- 使用 `{baseDir}` 代替硬编码路径
- 永远不要在指令中暴露敏感凭据

### 3. 简洁的描述

保持描述简短且信息丰富：

```markdown
# 好的写法
description: 使用 DALL-E 生成 AI 图像

# 不好的写法
description: 这个技能允许你使用 OpenAI 的 DALL-E API 生成令人惊叹的 AI 图像，这是一个强大的图像生成模型...
```

### 4. 错误处理

在指令中包含错误处理：

```markdown
## 错误处理

如果 API 调用失败：
1. 检查地点是否有效
2. 尝试使用简化的地点名称重试
3. 如果仍然失败，通知用户并建议替代方案
```

---

## 调试与测试

### 本地测试

```bash
# 直接测试技能
openclaw agent --message "使用我的天气技能查询东京"

# 检查技能加载
openclaw agent --message "列出可用的技能"
```

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 技能未加载 | 检查文件名是否为 `SKILL.md`（区分大小写） |
| 工具不可用 | 验证工具在 `requires.bins` 中 |
| 环境变量缺失 | 添加到 `requires.env` 并在 openclaw.json 中配置 |
| 权限被拒绝 | 检查脚本是否可执行：`chmod +x script.sh` |

### 查看已加载的技能

询问你的智能体："你有哪些可用的技能？"

---

## 发布到 ClawHub

### 1. 准备你的技能

确保你的技能：
- 有完整的 `SKILL.md`
- 包含 `README.md` 和使用示例
- 已在本地测试

### 2. 创建 Git 仓库

```bash
cd my-skill
git init
git add .
git commit -m "初始提交"
```

### 3. 发布到 ClawHub

```bash
clawhub publish my-skill
```

或通过 [https://clawhub.com](https://clawhub.com) 提交

---

## 示例

查看 [examples/](./examples/) 目录获取完整的技能示例：

- `weather/` - 简单的 API 集成
- `image-gen/` - AI 图像生成
- `data-processing/` - 复杂的多步骤工作流

---

## 资源链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [ClawHub 技能市场](https://clawhub.com)
- [AgentSkills 规范](https://agentskills.io)
- [GitHub 讨论](https://github.com/openclaw/openclaw/discussions)