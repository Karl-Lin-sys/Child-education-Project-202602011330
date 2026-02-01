"""
データモデル定義
幼児・小学生コミュニケーションVR・AIプラットフォーム
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


class AgeGroup(Enum):
    """年齢グループ"""
    INFANT = "幼児"  # 3-5歳
    LOWER_ELEMENTARY = "低学年"  # 6-8歳
    UPPER_ELEMENTARY = "高学年"  # 9-12歳


class EmotionType(Enum):
    """感情タイプ"""
    HAPPY = "喜び"
    SAD = "悲しみ"
    ANGRY = "怒り"
    SURPRISED = "驚き"
    FEARFUL = "恐れ"
    NEUTRAL = "普通"
    EXCITED = "興奮"
    CALM = "穏やか"


class ScenarioCategory(Enum):
    """VRシナリオカテゴリ"""
    GREETING = "あいさつ"
    SHARING = "共有・分かち合い"
    CONFLICT = "問題解決"
    COOPERATION = "協力"
    EMPATHY = "思いやり"
    SELF_EXPRESSION = "自己表現"
    LISTENING = "傾聴"
    ASKING_HELP = "助けを求める"


class CommunicationSkill(Enum):
    """コミュニケーションスキル"""
    VERBAL = "言語表現"
    NONVERBAL = "非言語表現"
    ACTIVE_LISTENING = "傾聴力"
    EMPATHY = "共感力"
    CONFLICT_RESOLUTION = "問題解決力"
    SELF_REGULATION = "感情調整力"
    SOCIAL_AWARENESS = "社会的認識"
    ASSERTIVENESS = "主張力"


@dataclass
class Child:
    """子どもデータモデル"""
    id: str
    name: str
    age: int
    age_group: AgeGroup
    avatar_id: str = "default"
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class VRScenario:
    """VRシナリオ"""
    id: str
    title: str
    description: str
    category: ScenarioCategory
    target_age_group: AgeGroup
    difficulty: int  # 1-5
    target_skills: List[CommunicationSkill]
    duration_minutes: int
    environment: str  # "classroom", "playground", "home", etc.
    characters: List[str]
    dialogue_prompts: List[Dict]


@dataclass
class EmotionState:
    """感情状態"""
    timestamp: datetime
    primary_emotion: EmotionType
    confidence: float  # 0-1
    secondary_emotions: Dict[str, float] = field(default_factory=dict)
    valence: float = 0.0  # -1 to 1 (negative to positive)
    arousal: float = 0.0  # 0 to 1 (calm to excited)


@dataclass
class ConversationTurn:
    """会話ターン"""
    turn_id: int
    speaker: str  # "child" or "ai"
    message: str
    timestamp: datetime
    emotion: Optional[EmotionState] = None
    skill_indicators: List[CommunicationSkill] = field(default_factory=list)


@dataclass
class VRSession:
    """VRセッション"""
    id: str
    child_id: str
    scenario_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    conversation_history: List[ConversationTurn] = field(default_factory=list)
    emotion_timeline: List[EmotionState] = field(default_factory=list)
    skill_scores: Dict[str, float] = field(default_factory=dict)
    completed: bool = False


@dataclass
class ProgressReport:
    """進捗レポート"""
    child_id: str
    report_date: datetime
    sessions_completed: int
    total_practice_minutes: int
    skill_progress: Dict[str, float]
    emotion_stability: float
    strengths: List[str]
    areas_to_improve: List[str]
    recommendations: List[str]


@dataclass
class AIResponse:
    """AIパートナーの応答"""
    message: str
    emotion: EmotionType
    suggested_actions: List[str]
    teaching_point: Optional[str] = None
    encouragement: Optional[str] = None
