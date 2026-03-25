# 整体架构设计

**版本**：v0.1  
**日期**：2026-03-24

---

## 一、系统概览

### 1.1 设计目标

做一个**可定制化的陪伴型智能体框架**，核心特性：

- **前端配置界面**：用户可选择目标用户、陪伴价值、角色性格
- **统一硬件接入**：提供智能家居接入渠道
- **纯软件技能**：无需绑定硬件载体
- **多场景适配**：儿童教育 / 老人陪伴 / 单身陪伴 / 心理陪伴

### 1.2 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户层 (User Layer)                       │
├─────────────────────────────────────────────────────────────────┤
│  Web配置界面  │  移动端  │  语音交互  │  消息平台(飞书/微信等)   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     应用层 (Application Layer)                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ 儿童教育陪伴 │  │  老人陪伴    │  │  单身陪伴    │  ...      │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      核心层 (Core Layer)                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │ 性格引擎   │ │ 记忆系统   │ │ 对话引擎   │ │ 分析引擎   │   │
│  │ Persona    │ │ Memory     │ │ Dialog     │ │ Analysis   │   │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │
│  ┌────────────┐ ┌────────────┐                                 │
│  │ 任务调度   │ │ 报告生成   │                                 │
│  │ Scheduler  │ │ Reporter   │                                 │
│  └────────────┘ └────────────┘                                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     能力层 (Capability Layer)                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │ 语音能力   │ │ 知识库     │ │ 日程管理   │ │ 健康监护   │   │
│  │ Voice      │ │ Knowledge  │ │ Calendar   │ │ Health     │   │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     接入层 (Integration Layer)                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │ 智能家居   │ │ 消息平台   │ │ 第三方API  │ │ 硬件设备   │   │
│  │ SmartHome  │ │ Messaging  │ │ APIs       │ │ Devices    │   │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、核心模块设计

### 2.1 性格引擎 (Persona Engine)

负责管理Agent的性格、说话风格、行为模式。

```
性格配置结构：
{
  "name": "小萌",
  "age": "7岁",
  "personality": ["活泼", "好奇心强", "爱问问题"],
  "speaking_style": "童趣、鼓励性、简单易懂",
  "interests": ["科学", "故事", "画画"],
  "values": ["诚实", "勇敢", "友爱"]
}
```

**功能**：
- 性格配置存储
- 对话风格调整
- 角色切换支持

### 2.2 记忆系统 (Memory System)

负责存储用户信息、对话历史、成长记录。**支持多年陪伴的长期记忆**。

#### 短期记忆 vs 长期记忆

```
记忆系统架构：
├── 短期记忆 (MemorySystem)
│   ├── 最近N轮对话
│   ├── 当前会话上下文
│   └── 临时工作记忆
│
└── 长期记忆 (LongTermMemorySystem) ⭐ 核心
    ├── 持久化存储
    ├── 向量语义检索
    └── 分层生命周期管理
```

#### 长期记忆分类

```
记忆类别：
├── 身份档案（永不遗忘）
│   ├── identity: 姓名、生日、过敏史
│   ├── personality: 性格特点
│   └── preference: 偏好设置
│
├── 成长记录（长期保留）
│   ├── milestone: 里程碑事件（第一次...）
│   ├── achievement: 成就记录
│   └── learning: 学习进展
│
├── 对话记忆（中期保留）
│   ├── conversation: 重要对话
│   ├── emotion: 情绪记录
│   └── behavior: 行为观察
│
├── 洞察分析（长期保留）
│   ├── insight: 洞察发现
│   ├── talent: 天赋判断
│   └── interest: 兴趣发现
│
└── 健康数据（老人陪伴）
    ├── health: 健康数据
    └── medication: 用药记录
```

#### 记忆优先级

| 优先级 | 保留策略 | 示例 |
|--------|----------|------|
| CRITICAL | 永久保留 | 生日、过敏史、重大成就 |
| HIGH | 长期保留（5年+） | 天赋判断、性格分析 |
| MEDIUM | 中期保留（1-3年） | 学习记录、兴趣变化 |
| LOW | 短期保留（1年内） | 日常对话、临时信息 |

#### 存储后端

| 后端 | 适用场景 | 特点 |
|------|----------|------|
| SQLite | 本地开发、小规模 | 零配置、单文件 |
| PostgreSQL | 中等规模 | 关系型、ACID |
| Chroma | 中等规模 | 向量检索、本地部署 |
| Pinecone | 大规模、云端 | 云托管、高可用 |

#### 关键功能

```python
# 存储记忆
memory = LongTermMemory(
    memory_id="mem_001",
    user_id="child_001",
    category=MemoryCategory.MILESTONE,
    priority=MemoryPriority.CRITICAL,
    title="第一次自己系鞋带",
    content="2026年3月24日，小明第一次成功自己系鞋带",
    keywords=["第一次", "独立", "成长"]
)
memory_system.store(memory)

# 语义检索
memories = memory_system.recall(
    user_id="child_001",
    query="他有什么成长里程碑？",
    limit=10
)

# 时间线查看
timeline = memory_system.get_memory_timeline(
    user_id="child_001",
    start_date="2024-01-01",
    end_date="2026-12-31"
)

# 数据导出（隐私保护）
data = memory_system.export_user_data(user_id="child_001")
```

#### 数据生命周期管理

```
记忆生命周期：
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  创建   │ ──▶ │  活跃   │ ──▶ │  归档   │ ──▶ │  清理   │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │               │               │               │
   首次记录       频繁访问        低优先级         过期删除
                  access_count    旧数据归档       用户请求
```

#### 隐私保护

- 数据加密存储
- 用户可导出自己的数据
- 用户可请求删除所有数据
- 符合 GDPR 等隐私法规

### 2.3 对话引擎 (Dialog Engine)

负责自然语言理解和生成。

**功能**：
- 意图识别
- 上下文管理
- 情感分析
- 多轮对话

### 2.4 分析引擎 (Analysis Engine)

负责从对话和行为中提取洞察，分析用户各方面情况，生成带依据的报告。

```
分析类型：
├── 性格分析 (Personality)
│   ├── 外向/内向判断
│   ├── 情绪稳定性
│   └── 社交倾向
├── 天赋判断 (Talent)
│   ├── 逻辑思维
│   ├── 创造力
│   ├── 语言表达
│   ├── 数学能力
│   ├── 艺术感知
│   └── 运动协调
├── 心理状况 (Psychological)
│   ├── 情绪状态
│   ├── 压力水平
│   └── 心理健康预警
├── 兴趣发现 (Interest)
│   ├── 兴趣领域识别
│   ├── 兴趣深度评估
│   └── 兴趣发展趋势
├── 优缺点分析 (Strength & Weakness)
│   ├── 优点发现
│   ├── 缺点识别
│   └── 改进建议
└── 行为模式 (Behavior Pattern)
    ├── 学习习惯
    ├── 社交模式
    └── 时间管理
```

**核心能力**：
- 从对话中提取分析证据
- 基于证据生成带依据的结论
- 计算分析置信度
- 生成结构化报告

**报告生成**：
- 日报/周报/月报
- 专项分析报告
- 家长可查看的完整报告

### 2.5 任务调度 (Scheduler)

负责定时任务、提醒、主动关怀。

**功能**：
- 日程提醒
- 主动问候
- 健康打卡
- 学习计划

---

## 三、能力层设计

### 3.1 语音能力 (Voice)

```
语音能力模块：
├── 语音识别 (STT)
│   ├── ElevenLabs Scribe
│   ├── Whisper
│   └── 讯飞语音
├── 语音合成 (TTS)
│   ├── ElevenLabs
│   ├── Azure TTS
│   └── 科大讯飞
└── 语音交互
    ├── 唤醒词检测
    └── 实时对话
```

### 3.2 知识库 (Knowledge)

```
知识库模块：
├── 儿童教育知识库
│   ├── 学科知识（语数外等）
│   ├── 百科知识
│   └── 故事资源库
├── 健康知识库
│   ├── 养生知识
│   ├── 疾病常识
│   └── 用药提醒
└── 通用知识库
    ├── 天气查询
    ├── 新闻资讯
    └── 生活常识
```

### 3.3 日程管理 (Calendar)

```
日程管理模块：
├── 日程创建
├── 提醒通知
├── 日程查询
└── 日程冲突检测
```

### 3.4 健康监护 (Health)

```
健康监护模块：
├── 健康数据采集
│   ├── 穿戴设备接入
│   └── 手动录入
├── 健康分析
│   ├── 趋势分析
│   └── 异常预警
└── 健康提醒
    ├── 吃药提醒
    ├── 运动提醒
    └── 作息提醒
```

---

## 四、接入层设计

### 4.1 智能家居接入

```
智能家居接入方案：
├── Home Assistant（优先）
│   ├── 支持设备最多（1000+）
│   ├── 本地部署
│   └── API完善
├── 品牌直连
│   ├── 小米米家
│   ├── 华为智选
│   ├── 涂鸦智能
│   └── Apple HomeKit
└── 统一抽象层
    ├── 设备发现
    ├── 状态查询
    └── 控制指令
```

### 4.2 消息平台接入

```
消息平台支持：
├── 飞书（当前）
├── 微信公众号
├── 企业微信
├── 钉钉
└── QQ
```

---

## 五、数据模型

### 5.1 用户模型

```json
{
  "user_id": "string",
  "profile": {
    "name": "string",
    "age": "number",
    "avatar": "string",
    "interests": ["string"],
    "personality": ["string"]
  },
  "settings": {
    "persona_id": "string",
    "voice_enabled": true,
    "language": "zh-CN"
  },
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### 5.2 会话模型

```json
{
  "session_id": "string",
  "user_id": "string",
  "messages": [
    {
      "role": "user|assistant",
      "content": "string",
      "timestamp": "timestamp",
      "emotion": "string"
    }
  ],
  "context": {
    "current_topic": "string",
    "pending_tasks": ["string"]
  }
}
```

### 5.3 记忆模型

```json
{
  "memory_id": "string",
  "user_id": "string",
  "type": "profile|conversation|growth",
  "content": "string",
  "importance": "high|medium|low",
  "tags": ["string"],
  "created_at": "timestamp",
  "last_accessed": "timestamp"
}
```

### 5.4 分析结果模型

```json
{
  "result_id": "string",
  "user_id": "string",
  "analysis_type": "talent|personality|psychological|interest|strength_weakness",
  "dimension": "string",
  "conclusion": "string",
  "confidence": "high|medium|low",
  "evidence_list": [
    {
      "evidence_id": "string",
      "evidence_type": "conversation|behavior|test",
      "content": "string",
      "timestamp": "timestamp",
      "context": "string",
      "relevance_score": 0.0
    }
  ],
  "suggestions": ["string"],
  "created_at": "timestamp"
}
```

### 5.5 分析报告模型

```json
{
  "report_id": "string",
  "user_id": "string",
  "report_type": "daily|weekly|monthly|special",
  "period_start": "timestamp",
  "period_end": "timestamp",
  "summary": "string",
  "results": ["AnalysisResult"],
  "overall_assessment": "string",
  "recommendations": ["string"],
  "generated_at": "timestamp"
}
```

---

## 六、技术选型

### 6.1 存储后端：SQLite + Chroma

**阶段1采用 SQLite + Chroma 组合方案**：

| 数据库 | 用途 | 原因 |
|--------|------|------|
| **SQLite** | 结构化数据 | 用户档案、记忆元数据、分析结果 |
| **Chroma** | 向量数据 | 语义检索、相似度搜索 |

**选择理由**：

| 优势 | 说明 |
|------|------|
| 零配置 | SQLite 单文件，Chroma 本地目录，开箱即用 |
| 易备份 | 复制文件就能备份 |
| 易迁移 | 后期可平滑迁移到 PostgreSQL + Pinecone |
| 开发快 | Python 原生支持，不需要额外服务 |
| 成本低 | 无需云服务费用 |

**数据分工**：

```
SQLite 存储结构化数据：
├── 用户档案（user_profiles）
├── 记忆元数据（memories: memory_id, title, category, priority）
├── 分析结果（analysis_results）
└── 报告记录（reports）

Chroma 存储向量数据：
├── 记忆内容的向量嵌入
├── 语义检索支持
└── 相似记忆推荐
```

**数据目录结构**：

```
~/.openclaw/data/
└── companion-agent/
    ├── memories.db        # SQLite 数据库
    └── chroma/            # Chroma 向量数据库
        ├── chroma.sqlite3
        └── ...
```

### 6.2 技术演进路线

```
阶段1（当前）: SQLite + Chroma
    │
    │ • 用户量 < 1000
    │ • 单机部署
    │ • 本地开发验证
    │
    ▼
阶段2: PostgreSQL + Chroma
    │
    │ • 用户量 1000-10000
    │ • 需要关系型数据库高级功能
    │ • 多实例部署
    │
    ▼
阶段3: PostgreSQL + Pinecone
    │
    │ • 用户量 > 10000
    │ • 需要云端托管
    │ • 高可用、自动扩展
```

### 6.3 其他技术选型（待定）

| 层级 | 技术 | 候选方案 |
|------|------|----------|
| 前端 | Web配置界面 | React / Vue |
| 后端 | OpenClaw Skill | TypeScript / Python |
| 结构化存储 | SQLite ✅ | SQLite → PostgreSQL |
| 向量存储 | Chroma ✅ | Chroma → Pinecone |
| LLM | 大语言模型 | GPT-4 / Claude / 国产模型 |
| 语音 | TTS/STT | ElevenLabs / Azure / 讯飞 |
| 智能家居 | Home Assistant | Python API |

---

## 七、开发计划

### 阶段1：儿童教育陪伴（优先）

见 [phase1-kids-education.md](./phase1-kids-education.md)

### 阶段2：老人陪伴

见 [phase2-elderly-care.md](./phase2-elderly-care.md)

---

## 八、成长型智能体设计 ⭐ 核心特性

### 8.1 设计理念

**核心理念：智能体跟着孩子一起"长大"**

传统智能体是静态的，但孩子的成长是动态的。我们的智能体必须具备"成长能力"：

| 维度 | 传统智能体 | 成长型智能体 |
|------|------------|--------------|
| 知识库 | 固定不变 | 根据年龄自动升级 |
| 记忆库 | 短期/无 | 长期积累，完整成长轨迹 |
| 角色年龄 | 固定 | 跟着孩子一起增长 |
| 对话风格 | 统一 | 从童趣→成熟，适应认知发展 |
| 陪伴深度 | 浅层 | 深度了解，因材施教 |

### 8.2 知识库分层演进

知识库根据孩子年龄阶段自动切换内容深度和表达方式：

| 年龄段 | 阶段名称 | 知识库内容 | 对话风格 | 典型表达 |
|--------|----------|------------|----------|----------|
| **3-6岁** | 启蒙期 | 基础认知、简单故事、生活常识、颜色形状 | 童趣、短句、多鼓励、拟人化 | "哇！好棒呀！~" |
| **6-9岁** | 探索期 | 小学知识、百科入门、兴趣培养、简单逻辑 | 引导式、启发思考、好奇探索 | "你觉得是为什么呢？" |
| **9-12岁** | 成长期 | 小学高年级、深度探索、思维训练、价值观引导 | 讨论式、培养逻辑、尊重观点 | "我同意你的观点，但..." |
| **12岁+** | 成熟期 | 初中知识、复杂话题、独立思考、人生规划 | 朋友式、平等对话、深度交流 | "你怎么看这件事？" |

**知识库自动切换机制**：

```python
class KnowledgeBaseManager:
    def get_knowledge_tier(self, child_age: int) -> KnowledgeTier:
        """根据年龄返回对应的知识库层级"""
        if child_age < 6:
            return KnowledgeTier.ENLIGHTENMENT  # 启蒙期
        elif child_age < 9:
            return KnowledgeTier.EXPLORATION   # 探索期
        elif child_age < 12:
            return KnowledgeTier.GROWTH        # 成长期
        else:
            return KnowledgeTier.MATURITY      # 成熟期
```

### 8.3 记忆库分层演进

记忆库采用**多层生命周期管理**，确保关键信息永不丢失：

```
记忆层次结构：
├── 核心档案层（永久保留）
│   ├── 身份信息：姓名、生日、血型、过敏史
│   ├── 性格画像：核心性格特点、长期稳定
│   ├── 天赋判断：发现的天赋潜能
│   └── 重大里程碑：第一次说话、第一次上学等
│
├── 成长轨迹层（长期保留，5年+）
│   ├── 学习历程：各学科进步曲线
│   ├── 兴趣演变：兴趣爱好的变化轨迹
│   ├── 能力发展：各项能力的发展记录
│   └── 重要事件：获奖、比赛、特殊经历
│
├── 行为洞察层（中期保留，1-3年）
│   ├── 行为模式：学习习惯、社交模式
│   ├── 情绪记录：情绪变化趋势
│   ├── 对话摘要：重要对话的内容摘要
│   └── 分析结论：各类分析的结果
│
├── 日常互动层（短期保留，1年内）
│   ├── 日常对话：聊天记录
│   ├── 临时任务：待办事项、提醒
│   └── 即时情绪：当前情绪状态
│
└── 历史档案层（可导出、可删除）
    └── 完整历史：所有数据的备份
```

**记忆优先级与保留策略**：

| 优先级 | 保留时长 | 内容类型 | 示例 |
|--------|----------|----------|------|
| **PERMANENT** | 永久 | 核心档案 | 生日、天赋判断、重大成就 |
| **LONG** | 5年+ | 成长轨迹 | 学习曲线、兴趣演变 |
| **MEDIUM** | 1-3年 | 行为洞察 | 分析结论、情绪记录 |
| **SHORT** | 1年内 | 日常互动 | 日常对话、临时任务 |
| **ARCHIVE** | 按需 | 历史档案 | 完整历史备份 |

### 8.4 角色成长机制

智能体的角色属性随孩子年龄同步增长：

```json
{
  "child_profile": {
    "child_id": "child_001",
    "name": "小明",
    "birth_date": "2019-03-15",
    "current_age": 7
  },
  "persona_config": {
    "persona_id": "xiaomeng",
    "base_name": "小萌",
    "base_age": 7,
    "growth_mode": "sync_with_child",
    "current_age": 7,
    "last_birthday_update": "2026-03-15"
  }
}
```

**角色成长触发时机**：
1. 孩子生日 → 自动升级
2. 家长手动调整 → 确认后升级
3. 学期切换 → 提示升级

**角色成长时自动更新**：
- [ ] 知识库层级
- [ ] 对话风格模板
- [ ] 角色年龄显示
- [ ] 能力模块配置
- [ ] 分析算法参数

### 8.5 陪伴深度演进

随着陪伴时间增长，智能体对孩子的了解越来越深：

| 陪伴时长 | 了解深度 | 典型能力 |
|----------|----------|----------|
| **1个月内** | 初步认识 | 知道名字、年龄、基本喜好 |
| **1-3个月** | 逐渐熟悉 | 了解兴趣、学习习惯、性格特点 |
| **3-6个月** | 深入了解 | 发现天赋、识别情绪模式、预测需求 |
| **6个月-1年** | 熟悉伙伴 | 完整成长轨迹、因材施教、主动关怀 |
| **1年以上** | 深度陪伴 | 了解孩子的全部，像老朋友一样 |

**陪伴深度可视化**：

```
小明与小萌的陪伴深度
─────────────────────────────
陪伴时长：1年3个月
了解深度：★★★★☆ (85%)

已了解的内容：
✅ 性格特点：外向、好奇心强、爱问问题
✅ 学习风格：视觉学习型、注意力集中时间约20分钟
✅ 兴趣爱好：画画★★★★、科学★★★☆、数学★★☆☆
✅ 天赋潜能：创造力★★★★、语言表达★★★★、逻辑思维★★★☆
✅ 情绪模式：压力敏感型、需要鼓励支持
✅ 成长轨迹：完整记录156个里程碑事件

待深入了解：
○ 社交模式（数据不足）
○ 价值观形成（年龄尚小）
```

### 8.6 数据连续性保证

**问题**：孩子从3岁用到12岁，数据如何保证不丢失？

**解决方案**：

```
数据连续性保障机制：
├── 多重备份
│   ├── 本地实时备份
│   ├── 云端定期备份
│   └── 家长可导出
├── 版本管理
│   ├── 知识库版本标记
│   ├── 记忆版本追踪
│   └── 配置版本回滚
├── 迁移支持
│   ├── 设备迁移工具
│   ├── 账号迁移工具
│   └── 数据导入导出
└── 隐私保护
    ├── 数据加密存储
    ├── 家长完全控制
    └── 符合儿童隐私法规
```

### 8.7 成长型智能体的技术实现

**核心组件**：

```python
class GrowthEngine:
    """成长型智能体引擎"""
    
    def __init__(self, child_id: str):
        self.child_id = child_id
        self.child_profile = self.load_child_profile()
        self.persona = self.load_persona()
        self.knowledge_base = self.get_knowledge_tier()
        self.memory_system = self.get_memory_system()
    
    def get_knowledge_tier(self) -> KnowledgeTier:
        """根据年龄获取知识库层级"""
        age = self.child_profile.age
        if age < 6:
            return KnowledgeTier.ENLIGHTENMENT
        elif age < 9:
            return KnowledgeTier.EXPLORATION
        elif age < 12:
            return KnowledgeTier.GROWTH
        else:
            return KnowledgeTier.MATURITY
    
    def get_dialog_style(self) -> DialogStyle:
        """根据年龄获取对话风格"""
        tier = self.get_knowledge_tier()
        styles = {
            KnowledgeTier.ENLIGHTENMENT: DialogStyle.CHILDISH,
            KnowledgeTier.EXPLORATION: DialogStyle.GUIDING,
            KnowledgeTier.GROWTH: DialogStyle.DISCUSSING,
            KnowledgeTier.MATURITY: DialogStyle.FRIENDLY
        }
        return styles[tier]
    
    def check_growth_trigger(self) -> bool:
        """检查是否需要触发成长升级"""
        # 孩子生日检查
        if self.is_birthday():
            return True
        # 学期切换检查
        if self.is_semester_change():
            return True
        return False
    
    def perform_growth_upgrade(self):
        """执行成长升级"""
        old_tier = self.get_knowledge_tier()
        self.persona.current_age = self.child_profile.age
        new_tier = self.get_knowledge_tier()
        
        if old_tier != new_tier:
            self.notify_growth_upgrade(old_tier, new_tier)
            self.archive_old_tier_data(old_tier)
            self.initialize_new_tier_data(new_tier)
```

---

## 九、待讨论问题

1. **LLM选择**：用哪个模型？国产还是OpenAI？
2. **语音方案**：用哪家TTS/STT？
3. **数据存储**：用户数据如何存储？隐私保护？
4. **商业化**：免费还是付费？如何变现？
5. **硬件接入优先级**：先支持哪些智能家居品牌？
6. **成长升级通知**：孩子生日时如何优雅地通知升级？
7. **跨年龄段数据迁移**：如何平滑过渡知识库层级？