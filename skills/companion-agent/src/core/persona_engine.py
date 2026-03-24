"""
性格引擎 - 管理 Agent 的性格、说话风格、行为模式
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class PersonaConfig:
    """角色配置"""
    persona_id: str
    name: str
    age: Optional[int] = None
    personality: List[str] = None
    speaking_style: Dict = None
    values: List[str] = None
    catchphrases: List[str] = None
    response_rules: List[str] = None

    def __post_init__(self):
        if self.personality is None:
            self.personality = []
        if self.speaking_style is None:
            self.speaking_style = {}
        if self.values is None:
            self.values = []
        if self.catchphrases is None:
            self.catchphrases = []
        if self.response_rules is None:
            self.response_rules = []


class PersonaEngine:
    """
    性格引擎
    
    负责：
    - 加载和管理角色配置
    - 根据角色调整对话风格
    - 支持多角色切换
    """
    
    def __init__(self, config_dir: str = None):
        """
        初始化性格引擎
        
        Args:
            config_dir: 角色配置文件目录
        """
        self.config_dir = config_dir
        self.personas: Dict[str, PersonaConfig] = {}
        self.current_persona: Optional[PersonaConfig] = None
        
    def load_persona(self, persona_id: str) -> PersonaConfig:
        """
        加载指定角色配置
        
        Args:
            persona_id: 角色ID
            
        Returns:
            角色配置对象
        """
        # TODO: 从配置文件加载
        pass
    
    def set_persona(self, persona_id: str) -> bool:
        """
        设置当前使用的角色
        
        Args:
            persona_id: 角色ID
            
        Returns:
            是否设置成功
        """
        if persona_id in self.personas:
            self.current_persona = self.personas[persona_id]
            return True
        return False
    
    def get_system_prompt(self) -> str:
        """
        根据当前角色生成系统提示词
        
        Returns:
            系统提示词
        """
        if not self.current_persona:
            return ""
        
        persona = self.current_persona
        prompt_parts = [
            f"你的名字是{persona.name}。",
        ]
        
        if persona.age:
            prompt_parts.append(f"你{persona.age}岁。")
        
        if persona.personality:
            prompt_parts.append(f"你的性格特点：{', '.join(personality)}。")
        
        if persona.speaking_style:
            tone = persona.speaking_style.get('tone', '')
            if tone:
                prompt_parts.append(f"你的说话风格是{tone}。")
        
        return " ".join(prompt_parts)
    
    def format_response(self, content: str) -> str:
        """
        根据角色风格格式化回复内容
        
        Args:
            content: 原始回复内容
            
        Returns:
            格式化后的内容
        """
        # TODO: 实现风格转换
        return content