"""
记忆系统 - 存储用户信息、对话历史、成长记录
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MemoryType(Enum):
    """记忆类型"""
    USER_PROFILE = "user_profile"       # 用户档案
    CONVERSATION = "conversation"        # 对话记忆
    GROWTH_RECORD = "growth_record"      # 成长记录
    HEALTH_DATA = "health_data"          # 健康数据


@dataclass
class Memory:
    """记忆条目"""
    memory_id: str
    user_id: str
    memory_type: MemoryType
    content: str
    importance: str = "medium"  # high, medium, low
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MemorySystem:
    """
    记忆系统
    
    负责：
    - 用户档案管理
    - 对话历史记录
    - 成长记录跟踪
    - 健康数据存储
    """
    
    def __init__(self, storage_backend: str = "local"):
        """
        初始化记忆系统
        
        Args:
            storage_backend: 存储后端 (local, vector_db, etc.)
        """
        self.storage_backend = storage_backend
        self.memories: Dict[str, Memory] = {}
        self.user_profiles: Dict[str, Dict] = {}
        self.conversation_history: Dict[str, List[Memory]] = {}
        
    def save_memory(self, memory: Memory) -> str:
        """
        保存记忆
        
        Args:
            memory: 记忆对象
            
        Returns:
            记忆ID
        """
        self.memories[memory.memory_id] = memory
        
        # 按用户组织对话历史
        if memory.memory_type == MemoryType.CONVERSATION:
            if memory.user_id not in self.conversation_history:
                self.conversation_history[memory.user_id] = []
            self.conversation_history[memory.user_id].append(memory)
        
        return memory.memory_id
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """
        获取用户档案
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户档案字典
        """
        return self.user_profiles.get(user_id)
    
    def update_user_profile(self, user_id: str, profile_data: Dict) -> None:
        """
        更新用户档案
        
        Args:
            user_id: 用户ID
            profile_data: 档案数据
        """
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}
        self.user_profiles[user_id].update(profile_data)
    
    def get_conversation_history(
        self, 
        user_id: str, 
        limit: int = 10
    ) -> List[Memory]:
        """
        获取对话历史
        
        Args:
            user_id: 用户ID
            limit: 返回条数限制
            
        Returns:
            对话记忆列表
        """
        history = self.conversation_history.get(user_id, [])
        return history[-limit:] if history else []
    
    def get_growth_records(
        self, 
        user_id: str,
        record_type: Optional[str] = None
    ) -> List[Memory]:
        """
        获取成长记录
        
        Args:
            user_id: 用户ID
            record_type: 记录类型过滤
            
        Returns:
            成长记录列表
        """
        records = [
            m for m in self.memories.values()
            if m.user_id == user_id 
            and m.memory_type == MemoryType.GROWTH_RECORD
        ]
        
        if record_type:
            records = [r for r in records if r.metadata.get('record_type') == record_type]
        
        return sorted(records, key=lambda x: x.created_at, reverse=True)
    
    def search_memories(
        self, 
        query: str, 
        user_id: Optional[str] = None,
        memory_type: Optional[MemoryType] = None
    ) -> List[Memory]:
        """
        搜索记忆
        
        Args:
            query: 搜索关键词
            user_id: 用户ID过滤
            memory_type: 记忆类型过滤
            
        Returns:
            匹配的记忆列表
        """
        # TODO: 实现向量搜索
        results = []
        for memory in self.memories.values():
            if user_id and memory.user_id != user_id:
                continue
            if memory_type and memory.memory_type != memory_type:
                continue
            if query.lower() in memory.content.lower():
                results.append(memory)
        return results