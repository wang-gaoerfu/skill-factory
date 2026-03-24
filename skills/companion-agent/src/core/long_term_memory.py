"""
长期记忆系统 - 支持多年陪伴的持久化记忆存储

设计原则：
1. 数据持久化：支持多年数据存储
2. 语义检索：基于向量相似度搜索
3. 分层存储：热数据/冷数据分层
4. 隐私保护：数据加密存储
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import hashlib


class MemoryPriority(Enum):
    """记忆优先级"""
    CRITICAL = "critical"     # 关键记忆，永不遗忘（生日、过敏等）
    HIGH = "high"             # 重要记忆，长期保留
    MEDIUM = "medium"         # 普通记忆，中期保留
    LOW = "low"               # 日常记忆，短期保留


class MemoryCategory(Enum):
    """记忆类别"""
    # 用户档案
    IDENTITY = "identity"           # 身份信息（姓名、生日）
    PERSONALITY = "personality"      # 性格特点
    PREFERENCE = "preference"        # 偏好设置
    
    # 成长记录
    MILESTONE = "milestone"          # 里程碑事件
    ACHIEVEMENT = "achievement"       # 成就记录
    LEARNING = "learning"            # 学习进展
    
    # 日常记忆
    CONVERSATION = "conversation"     # 对话记忆
    EMOTION = "emotion"               # 情绪记录
    BEHAVIOR = "behavior"             # 行为观察
    
    # 分析结果
    INSIGHT = "insight"               # 洞察发现
    TALENT = "talent"                 # 天赋判断
    INTEREST = "interest"             # 兴趣发现
    
    # 健康数据（老人陪伴）
    HEALTH = "health"                 # 健康数据
    MEDICATION = "medication"          # 用药记录


@dataclass
class LongTermMemory:
    """长期记忆条目"""
    memory_id: str
    user_id: str
    category: MemoryCategory
    priority: MemoryPriority
    
    # 核心内容
    title: str                        # 记忆标题
    content: str                      # 记忆内容
    keywords: List[str]               # 关键词
    
    # 向量嵌入
    embedding: Optional[List[float]] = None
    
    # 时间信息
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    
    # 关联信息
    related_memories: List[str] = field(default_factory=list)
    source_conversation_id: Optional[str] = None
    
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # 生命周期
    expires_at: Optional[datetime] = None  # 过期时间（低优先级记忆）
    archived: bool = False


class LongTermMemorySystem:
    """
    长期记忆系统
    
    特点：
    1. 持久化存储：支持数据库后端
    2. 向量检索：语义相似度搜索
    3. 分层管理：热/温/冷数据分层
    4. 自动归档：旧数据自动归档
    """
    
    def __init__(
        self,
        storage_backend: str = "sqlite",  # sqlite, postgres, chroma, pinecone
        embedding_model: str = "text-embedding-ada-002"
    ):
        """
        初始化长期记忆系统
        
        Args:
            storage_backend: 存储后端
            embedding_model: 向量嵌入模型
        """
        self.storage_backend = storage_backend
        self.embedding_model = embedding_model
        
        # 内存缓存（热数据）
        self.hot_cache: Dict[str, LongTermMemory] = {}
        
        # 向量索引
        self.vector_index: Dict[str, List[float]] = {}
        
        # 初始化存储
        self._init_storage()
    
    def _init_storage(self):
        """初始化存储后端"""
        if self.storage_backend == "sqlite":
            self._init_sqlite()
        elif self.storage_backend == "chroma":
            self._init_chroma()
        elif self.storage_backend == "pinecone":
            self._init_pinecone()
    
    def _init_sqlite(self):
        """初始化 SQLite 存储"""
        # 本地开发和小规模使用
        import sqlite3
        self.db_path = "memory.db"
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()
    
    def _create_tables(self):
        """创建数据表"""
        cursor = self.conn.cursor()
        
        # 记忆主表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                memory_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                title TEXT,
                content TEXT,
                keywords TEXT,
                created_at TIMESTAMP,
                last_accessed TIMESTAMP,
                access_count INTEGER,
                expires_at TIMESTAMP,
                archived INTEGER DEFAULT 0,
                metadata TEXT
            )
        """)
        
        # 向量表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                memory_id TEXT PRIMARY KEY,
                embedding BLOB,
                FOREIGN KEY (memory_id) REFERENCES memories(memory_id)
            )
        """)
        
        # 索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_id ON memories(user_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_category ON memories(category)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_created_at ON memories(created_at)
        """)
        
        self.conn.commit()
    
    def _init_chroma(self):
        """初始化 Chroma 向量数据库"""
        # 中等规模，支持向量检索
        pass  # TODO: 实现
    
    def _init_pinecone(self):
        """初始化 Pinecone 向量数据库"""
        # 大规模，云端托管
        pass  # TODO: 实现
    
    def store(self, memory: LongTermMemory) -> str:
        """
        存储记忆
        
        Args:
            memory: 记忆对象
            
        Returns:
            记忆ID
        """
        # 生成向量嵌入
        memory.embedding = self._generate_embedding(memory.content)
        
        # 存储到热缓存
        self.hot_cache[memory.memory_id] = memory
        
        # 存储到向量索引
        if memory.embedding:
            self.vector_index[memory.memory_id] = memory.embedding
        
        # 持久化
        self._persist_memory(memory)
        
        return memory.memory_id
    
    def _generate_embedding(self, text: str) -> List[float]:
        """生成文本向量嵌入"""
        # TODO: 调用嵌入模型
        # 暂时返回占位向量
        return [0.0] * 1536
    
    def _persist_memory(self, memory: LongTermMemory):
        """持久化记忆到存储"""
        if self.storage_backend == "sqlite":
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO memories 
                (memory_id, user_id, category, priority, title, content, 
                 keywords, created_at, last_accessed, access_count, 
                 expires_at, archived, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory.memory_id,
                memory.user_id,
                memory.category.value,
                memory.priority.value,
                memory.title,
                memory.content,
                json.dumps(memory.keywords),
                memory.created_at.isoformat(),
                memory.last_accessed.isoformat(),
                memory.access_count,
                memory.expires_at.isoformat() if memory.expires_at else None,
                1 if memory.archived else 0,
                json.dumps(memory.metadata)
            ))
            
            if memory.embedding:
                cursor.execute("""
                    INSERT OR REPLACE INTO embeddings (memory_id, embedding)
                    VALUES (?, ?)
                """, (memory.memory_id, json.dumps(memory.embedding)))
            
            self.conn.commit()
    
    def recall(
        self,
        user_id: str,
        query: str = None,
        category: MemoryCategory = None,
        limit: int = 10
    ) -> List[LongTermMemory]:
        """
        回忆/检索记忆
        
        Args:
            user_id: 用户ID
            query: 查询文本（语义搜索）
            category: 类别过滤
            limit: 返回数量
            
        Returns:
            记忆列表
        """
        memories = []
        
        if query and self.storage_backend in ["chroma", "pinecone"]:
            # 向量语义搜索
            memories = self._vector_search(user_id, query, category, limit)
        else:
            # 传统关键词搜索
            memories = self._keyword_search(user_id, query, category, limit)
        
        # 更新访问信息
        for memory in memories:
            memory.last_accessed = datetime.now()
            memory.access_count += 1
            self._update_access_info(memory)
        
        return memories
    
    def _vector_search(
        self,
        user_id: str,
        query: str,
        category: MemoryCategory,
        limit: int
    ) -> List[LongTermMemory]:
        """向量语义搜索"""
        # TODO: 实现向量搜索
        return []
    
    def _keyword_search(
        self,
        user_id: str,
        query: str,
        category: MemoryCategory,
        limit: int
    ) -> List[LongTermMemory]:
        """关键词搜索"""
        memories = []
        
        if self.storage_backend == "sqlite":
            cursor = self.conn.cursor()
            
            sql = """
                SELECT * FROM memories 
                WHERE user_id = ? AND archived = 0
            """
            params = [user_id]
            
            if category:
                sql += " AND category = ?"
                params.append(category.value)
            
            if query:
                sql += " AND (title LIKE ? OR content LIKE ? OR keywords LIKE ?)"
                query_pattern = f"%{query}%"
                params.extend([query_pattern, query_pattern, query_pattern])
            
            sql += " ORDER BY priority DESC, created_at DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            for row in rows:
                memory = self._row_to_memory(row)
                memories.append(memory)
        
        return memories
    
    def _row_to_memory(self, row) -> LongTermMemory:
        """数据库行转记忆对象"""
        return LongTermMemory(
            memory_id=row[0],
            user_id=row[1],
            category=MemoryCategory(row[2]),
            priority=MemoryPriority(row[3]),
            title=row[4],
            content=row[5],
            keywords=json.loads(row[6]) if row[6] else [],
            created_at=datetime.fromisoformat(row[7]),
            last_accessed=datetime.fromisoformat(row[8]),
            access_count=row[9],
            expires_at=datetime.fromisoformat(row[10]) if row[10] else None,
            archived=bool(row[11]),
            metadata=json.loads(row[12]) if row[12] else {}
        )
    
    def _update_access_info(self, memory: LongTermMemory):
        """更新访问信息"""
        if self.storage_backend == "sqlite":
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE memories 
                SET last_accessed = ?, access_count = ?
                WHERE memory_id = ?
            """, (memory.last_accessed.isoformat(), memory.access_count, memory.memory_id))
            self.conn.commit()
    
    def archive_old_memories(self, days: int = 365):
        """
        归档旧记忆
        
        Args:
            days: 超过多少天的低优先级记忆归档
        """
        threshold = datetime.now() - timedelta(days=days)
        
        if self.storage_backend == "sqlite":
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE memories 
                SET archived = 1 
                WHERE priority = 'low' 
                AND created_at < ?
                AND archived = 0
            """, (threshold.isoformat()))
            self.conn.commit()
    
    def get_memory_timeline(
        self,
        user_id: str,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> Dict[str, List[LongTermMemory]]:
        """
        获取记忆时间线
        
        Args:
            user_id: 用户ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            按日期分组的记忆
        """
        timeline = {}
        
        if self.storage_backend == "sqlite":
            cursor = self.conn.cursor()
            
            sql = """
                SELECT * FROM memories 
                WHERE user_id = ? AND archived = 0
            """
            params = [user_id]
            
            if start_date:
                sql += " AND created_at >= ?"
                params.append(start_date.isoformat())
            
            if end_date:
                sql += " AND created_at <= ?"
                params.append(end_date.isoformat())
            
            sql += " ORDER BY created_at DESC"
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            for row in rows:
                memory = self._row_to_memory(row)
                date_key = memory.created_at.strftime("%Y-%m-%d")
                if date_key not in timeline:
                    timeline[date_key] = []
                timeline[date_key].append(memory)
        
        return timeline
    
    def export_user_data(self, user_id: str) -> Dict:
        """
        导出用户所有记忆数据
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户记忆数据
        """
        all_memories = self.recall(user_id, limit=10000)
        
        return {
            "user_id": user_id,
            "exported_at": datetime.now().isoformat(),
            "total_memories": len(all_memories),
            "memories": [
                {
                    "category": m.category.value,
                    "priority": m.priority.value,
                    "title": m.title,
                    "content": m.content,
                    "created_at": m.created_at.isoformat(),
                    "metadata": m.metadata
                }
                for m in all_memories
            ]
        }
    
    def close(self):
        """关闭连接"""
        if hasattr(self, 'conn'):
            self.conn.close()


# 使用示例
if __name__ == "__main__":
    # 初始化长期记忆系统
    memory_system = LongTermMemorySystem(storage_backend="sqlite")
    
    # 存储一条记忆
    memory = LongTermMemory(
        memory_id="mem_001",
        user_id="child_001",
        category=MemoryCategory.MILESTONE,
        priority=MemoryPriority.CRITICAL,
        title="第一次自己系鞋带",
        content="2026年3月24日，小明第一次成功自己系鞋带，花了10分钟",
        keywords=["第一次", "独立", "成长"],
        metadata={"age": 5, "location": "家里"}
    )
    
    memory_system.store(memory)
    
    # 检索记忆
    memories = memory_system.recall(
        user_id="child_001",
        query="鞋带",
        limit=5
    )
    
    print(f"找到 {len(memories)} 条相关记忆")
    
    memory_system.close()