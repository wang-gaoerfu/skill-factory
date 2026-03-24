"""
分析引擎 - 分析用户各方面情况，生成洞察报告
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AnalysisType(Enum):
    """分析类型"""
    PERSONALITY = "personality"           # 性格分析
    TALENT = "talent"                     # 天赋判断
    PSYCHOLOGICAL = "psychological"       # 心理状况
    LEARNING_STYLE = "learning_style"     # 学习风格
    INTEREST = "interest"                 # 兴趣发现
    STRENGTH_WEAKNESS = "strength_weakness"  # 优缺点分析
    BEHAVIOR_PATTERN = "behavior_pattern" # 行为模式


class ConfidenceLevel(Enum):
    """置信度级别"""
    HIGH = "high"         # 高置信度（多次观察）
    MEDIUM = "medium"     # 中等置信度
    LOW = "low"           # 低置信度（初步判断）


@dataclass
class AnalysisEvidence:
    """分析依据"""
    evidence_id: str
    evidence_type: str           # conversation, behavior, test, etc.
    content: str                 # 具体内容
    timestamp: datetime          # 时间
    context: str                 # 上下文
    relevance_score: float = 0.0 # 相关度评分


@dataclass
class AnalysisResult:
    """分析结果"""
    result_id: str
    analysis_type: AnalysisType
    dimension: str               # 分析维度
    conclusion: str              # 结论
    confidence: ConfidenceLevel  # 置信度
    evidence_list: List[AnalysisEvidence]  # 依据列表
    suggestions: List[str]        # 建议
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalysisReport:
    """分析报告"""
    report_id: str
    user_id: str
    report_type: str             # daily, weekly, monthly, special
    period_start: datetime
    period_end: datetime
    summary: str                 # 总体概述
    results: List[AnalysisResult]  # 各项分析结果
    overall_assessment: str      # 综合评估
    recommendations: List[str]   # 整体建议
    generated_at: datetime = field(default_factory=datetime.now)


class AnalysisEngine:
    """
    分析引擎
    
    负责：
    - 从对话和行为中提取洞察
    - 分析性格、天赋、心理状况
    - 发现优点和缺点
    - 生成带依据的分析报告
    """
    
    def __init__(self, memory_system=None):
        """
        初始化分析引擎
        
        Args:
            memory_system: 记忆系统引用
        """
        self.memory_system = memory_system
        self.analysis_results: Dict[str, List[AnalysisResult]] = {}
        self.reports: Dict[str, AnalysisReport] = {}
        
        # 分析规则配置
        self.analysis_rules = {
            "talent_keywords": {
                "逻辑思维": ["为什么", "怎么回事", "原来是这样"],
                "创造力": ["如果", "想象", "自己设计"],
                "语言表达": ["我觉得", "我认为", "可以这样说"],
                "数学能力": ["算一下", "多少", "数学"],
                "艺术感知": ["颜色", "好看", "画", "音乐"],
                "运动协调": ["跑", "跳", "运动", "球"],
            },
            "emotion_indicators": {
                "开心": ["太棒了", "好开心", "哈哈"],
                "焦虑": ["担心", "害怕", "紧张"],
                "沮丧": ["我不会", "太难了", "我不行"],
                "兴奋": ["太好了", "终于", "等不及"],
            },
            "behavior_patterns": {
                "主动学习": "主动提问、探索新知识",
                "被动学习": "需要引导才学习",
                "坚持性强": "遇到困难不放弃",
                "容易放弃": "遇到困难就退缩",
                "好奇心强": "频繁提问、探索",
            }
        }
    
    def analyze_from_conversation(
        self, 
        user_id: str,
        conversation_history: List[Dict],
        analysis_type: AnalysisType
    ) -> AnalysisResult:
        """
        从对话历史中分析
        
        Args:
            user_id: 用户ID
            conversation_history: 对话历史
            analysis_type: 分析类型
            
        Returns:
            分析结果
        """
        evidence_list = []
        findings = {}
        
        # 遍历对话，提取证据
        for msg in conversation_history:
            content = msg.get("content", "")
            
            # 根据分析类型提取不同证据
            if analysis_type == AnalysisType.TALENT:
                evidence = self._extract_talent_evidence(content, msg)
                if evidence:
                    evidence_list.append(evidence)
                    self._update_findings(findings, evidence)
            
            elif analysis_type == AnalysisType.PSYCHOLOGICAL:
                evidence = self._extract_psychological_evidence(content, msg)
                if evidence:
                    evidence_list.append(evidence)
            
            elif analysis_type == AnalysisType.INTEREST:
                evidence = self._extract_interest_evidence(content, msg)
                if evidence:
                    evidence_list.append(evidence)
        
        # 生成分析结论
        conclusion = self._generate_conclusion(findings, analysis_type)
        confidence = self._calculate_confidence(evidence_list)
        suggestions = self._generate_suggestions(conclusion, analysis_type)
        
        result = AnalysisResult(
            result_id=f"{user_id}_{analysis_type.value}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            analysis_type=analysis_type,
            dimension=self._get_dimension(analysis_type),
            conclusion=conclusion,
            confidence=confidence,
            evidence_list=evidence_list,
            suggestions=suggestions
        )
        
        # 存储结果
        if user_id not in self.analysis_results:
            self.analysis_results[user_id] = []
        self.analysis_results[user_id].append(result)
        
        return result
    
    def _extract_talent_evidence(self, content: str, msg: Dict) -> Optional[AnalysisEvidence]:
        """提取天赋相关证据"""
        for talent, keywords in self.analysis_rules["talent_keywords"].items():
            for keyword in keywords:
                if keyword in content:
                    return AnalysisEvidence(
                        evidence_id=f"ev_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                        evidence_type="conversation",
                        content=content,
                        timestamp=msg.get("timestamp", datetime.now()),
                        context=f"发现 {talent} 倾向：使用了关键词 '{keyword}'",
                        relevance_score=0.8
                    )
        return None
    
    def _extract_psychological_evidence(self, content: str, msg: Dict) -> Optional[AnalysisEvidence]:
        """提取心理状况证据"""
        for emotion, indicators in self.analysis_rules["emotion_indicators"].items():
            for indicator in indicators:
                if indicator in content:
                    return AnalysisEvidence(
                        evidence_id=f"ev_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                        evidence_type="emotion",
                        content=content,
                        timestamp=msg.get("timestamp", datetime.now()),
                        context=f"检测到情绪：{emotion}，关键词：'{indicator}'",
                        relevance_score=0.7
                    )
        return None
    
    def _extract_interest_evidence(self, content: str, msg: Dict) -> Optional[AnalysisEvidence]:
        """提取兴趣相关证据"""
        interest_keywords = ["喜欢", "感兴趣", "好玩", "有趣", "想学", "想看"]
        for keyword in interest_keywords:
            if keyword in content:
                # 提取感兴趣的对象
                return AnalysisEvidence(
                    evidence_id=f"ev_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                    evidence_type="interest",
                    content=content,
                    timestamp=msg.get("timestamp", datetime.now()),
                    context=f"发现兴趣点",
                    relevance_score=0.9
                )
        return None
    
    def _update_findings(self, findings: Dict, evidence: AnalysisEvidence):
        """更新发现"""
        # TODO: 实现更复杂的发现聚合逻辑
        pass
    
    def _generate_conclusion(self, findings: Dict, analysis_type: AnalysisType) -> str:
        """生成结论"""
        # TODO: 基于 findings 生成结构化结论
        return "分析进行中..."
    
    def _calculate_confidence(self, evidence_list: List[AnalysisEvidence]) -> ConfidenceLevel:
        """计算置信度"""
        if len(evidence_list) >= 5:
            return ConfidenceLevel.HIGH
        elif len(evidence_list) >= 2:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW
    
    def _generate_suggestions(self, conclusion: str, analysis_type: AnalysisType) -> List[str]:
        """生成建议"""
        # TODO: 基于结论生成具体建议
        return []
    
    def _get_dimension(self, analysis_type: AnalysisType) -> str:
        """获取分析维度名称"""
        dimension_map = {
            AnalysisType.PERSONALITY: "性格特点",
            AnalysisType.TALENT: "天赋潜能",
            AnalysisType.PSYCHOLOGICAL: "心理状况",
            AnalysisType.LEARNING_STYLE: "学习风格",
            AnalysisType.INTEREST: "兴趣爱好",
            AnalysisType.STRENGTH_WEAKNESS: "优缺点",
            AnalysisType.BEHAVIOR_PATTERN: "行为模式",
        }
        return dimension_map.get(analysis_type, "综合分析")
    
    def generate_report(
        self,
        user_id: str,
        report_type: str = "weekly",
        period_start: datetime = None,
        period_end: datetime = None
    ) -> AnalysisReport:
        """
        生成分析报告
        
        Args:
            user_id: 用户ID
            report_type: 报告类型
            period_start: 分析开始时间
            period_end: 分析结束时间
            
        Returns:
            分析报告
        """
        if period_end is None:
            period_end = datetime.now()
        if period_start is None:
            # 默认分析最近一周
            from datetime import timedelta
            period_start = period_end - timedelta(days=7)
        
        # 获取该时间段的分析结果
        results = [
            r for r in self.analysis_results.get(user_id, [])
            if period_start <= r.created_at <= period_end
        ]
        
        # 生成综合评估
        overall_assessment = self._generate_overall_assessment(results)
        
        # 生成整体建议
        recommendations = self._generate_recommendations(results)
        
        # 生成概述
        summary = self._generate_summary(results)
        
        report = AnalysisReport(
            report_id=f"report_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            user_id=user_id,
            report_type=report_type,
            period_start=period_start,
            period_end=period_end,
            summary=summary,
            results=results,
            overall_assessment=overall_assessment,
            recommendations=recommendations
        )
        
        self.reports[report.report_id] = report
        return report
    
    def _generate_overall_assessment(self, results: List[AnalysisResult]) -> str:
        """生成综合评估"""
        # TODO: 实现综合评估逻辑
        return "综合评估生成中..."
    
    def _generate_recommendations(self, results: List[AnalysisResult]) -> List[str]:
        """生成整体建议"""
        recommendations = []
        for result in results:
            recommendations.extend(result.suggestions)
        return list(set(recommendations))  # 去重
    
    def _generate_summary(self, results: List[AnalysisResult]) -> str:
        """生成概述"""
        # TODO: 实现概述生成逻辑
        return "分析概述生成中..."
    
    def get_user_analysis_history(
        self, 
        user_id: str,
        analysis_type: Optional[AnalysisType] = None
    ) -> List[AnalysisResult]:
        """
        获取用户分析历史
        
        Args:
            user_id: 用户ID
            analysis_type: 分析类型过滤
            
        Returns:
            分析结果列表
        """
        results = self.analysis_results.get(user_id, [])
        if analysis_type:
            results = [r for r in results if r.analysis_type == analysis_type]
        return sorted(results, key=lambda x: x.created_at, reverse=True)