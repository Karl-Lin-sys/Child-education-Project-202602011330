"""
VRシナリオ生成エンジン
コミュニケーション練習用のVRシナリオを生成
"""
import random
from typing import List, Dict
from models import (
    VRScenario, ScenarioCategory, AgeGroup, 
    CommunicationSkill
)


class ScenarioGenerator:
    """VRシナリオ生成エンジン"""
    
    # 環境設定
    ENVIRONMENTS = {
        "classroom": {"name": "教室", "icon": "🏫"},
        "playground": {"name": "公園", "icon": "🏞️"},
        "home": {"name": "おうち", "icon": "🏠"},
        "library": {"name": "図書館", "icon": "📚"},
        "store": {"name": "お店", "icon": "🏪"}
    }
    
    # キャラクター
    CHARACTERS = {
        "friend_boy": {"name": "たける", "type": "友達", "emoji": "👦"},
        "friend_girl": {"name": "さくら", "type": "友達", "emoji": "👧"},
        "teacher": {"name": "やまだ先生", "type": "先生", "emoji": "👨‍🏫"},
        "parent": {"name": "ママ", "type": "親", "emoji": "👩"},
        "stranger": {"name": "知らない人", "type": "他人", "emoji": "🧑"}
    }
    
    # プリセットシナリオ
    PRESET_SCENARIOS = [
        {
            "title": "あいさつをしよう",
            "category": ScenarioCategory.GREETING,
            "description": "朝、教室で友達に会ったときのあいさつの練習をしよう",
            "environment": "classroom",
            "characters": ["friend_boy", "friend_girl"],
            "skills": [CommunicationSkill.VERBAL, CommunicationSkill.SOCIAL_AWARENESS],
            "difficulty": 1,
            "duration": 5,
            "dialogues": [
                {"speaker": "system", "text": "朝、教室に入ると、友達のたけるくんがいます。"},
                {"speaker": "ai", "text": "おはよう！", "character": "friend_boy"},
                {"speaker": "prompt", "text": "あいさつを返してみよう！"}
            ]
        },
        {
            "title": "おもちゃを貸してあげよう",
            "category": ScenarioCategory.SHARING,
            "description": "友達がおもちゃを使いたがっているとき、どうする？",
            "environment": "playground",
            "characters": ["friend_girl"],
            "skills": [CommunicationSkill.EMPATHY, CommunicationSkill.VERBAL],
            "difficulty": 2,
            "duration": 10,
            "dialogues": [
                {"speaker": "system", "text": "公園で遊んでいると、さくらちゃんがボールを見ています。"},
                {"speaker": "ai", "text": "そのボール、かして...？", "character": "friend_girl"},
                {"speaker": "prompt", "text": "さくらちゃんにどう答える？"}
            ]
        },
        {
            "title": "ケンカを仲直り",
            "category": ScenarioCategory.CONFLICT,
            "description": "友達とケンカしてしまった！仲直りの方法を考えよう",
            "environment": "classroom",
            "characters": ["friend_boy"],
            "skills": [CommunicationSkill.CONFLICT_RESOLUTION, CommunicationSkill.SELF_REGULATION],
            "difficulty": 3,
            "duration": 15,
            "dialogues": [
                {"speaker": "system", "text": "さっき、たけるくんとおもちゃの取り合いでケンカしちゃった..."},
                {"speaker": "ai", "text": "...", "character": "friend_boy", "emotion": "sad"},
                {"speaker": "prompt", "text": "たけるくんに話しかけてみよう。なんて言う？"}
            ]
        },
        {
            "title": "一緒に遊ぼう",
            "category": ScenarioCategory.COOPERATION,
            "description": "友達を遊びに誘ってみよう",
            "environment": "playground",
            "characters": ["friend_boy", "friend_girl"],
            "skills": [CommunicationSkill.VERBAL, CommunicationSkill.ASSERTIVENESS],
            "difficulty": 2,
            "duration": 10,
            "dialogues": [
                {"speaker": "system", "text": "公園に行くと、友達が二人います。"},
                {"speaker": "prompt", "text": "一緒に遊ぼうって誘ってみよう！"}
            ]
        },
        {
            "title": "困っている子を助けよう",
            "category": ScenarioCategory.EMPATHY,
            "description": "泣いている友達がいる。どうしたらいい？",
            "environment": "classroom",
            "characters": ["friend_girl"],
            "skills": [CommunicationSkill.EMPATHY, CommunicationSkill.ACTIVE_LISTENING],
            "difficulty": 3,
            "duration": 15,
            "dialogues": [
                {"speaker": "system", "text": "教室で、さくらちゃんが泣いています。"},
                {"speaker": "ai", "text": "うぅ...", "character": "friend_girl", "emotion": "sad"},
                {"speaker": "prompt", "text": "さくらちゃんに声をかけてみよう"}
            ]
        },
        {
            "title": "自己紹介をしよう",
            "category": ScenarioCategory.SELF_EXPRESSION,
            "description": "新しい友達に自分のことを紹介してみよう",
            "environment": "classroom",
            "characters": ["friend_boy"],
            "skills": [CommunicationSkill.VERBAL, CommunicationSkill.SELF_REGULATION],
            "difficulty": 2,
            "duration": 10,
            "dialogues": [
                {"speaker": "system", "text": "新しいお友達が転校してきました。"},
                {"speaker": "ai", "text": "はじめまして！きみの名前は？", "character": "friend_boy"},
                {"speaker": "prompt", "text": "自己紹介してみよう！"}
            ]
        },
        {
            "title": "お話を聞こう",
            "category": ScenarioCategory.LISTENING,
            "description": "友達の話を最後まで聞いてみよう",
            "environment": "playground",
            "characters": ["friend_girl"],
            "skills": [CommunicationSkill.ACTIVE_LISTENING, CommunicationSkill.EMPATHY],
            "difficulty": 2,
            "duration": 10,
            "dialogues": [
                {"speaker": "system", "text": "さくらちゃんが話したそうにしています。"},
                {"speaker": "ai", "text": "ねえねえ、きのうね...", "character": "friend_girl"},
                {"speaker": "prompt", "text": "さくらちゃんの話を聞いてみよう"}
            ]
        },
        {
            "title": "助けを求めよう",
            "category": ScenarioCategory.ASKING_HELP,
            "description": "困ったとき、大人に助けを求める練習をしよう",
            "environment": "classroom",
            "characters": ["teacher"],
            "skills": [CommunicationSkill.VERBAL, CommunicationSkill.ASSERTIVENESS],
            "difficulty": 2,
            "duration": 10,
            "dialogues": [
                {"speaker": "system", "text": "教室で靴ひもがほどけちゃった。自分でできない..."},
                {"speaker": "prompt", "text": "先生に助けを求めてみよう。なんて言う？"}
            ]
        }
    ]
    
    def __init__(self):
        self.scenario_id_counter = 1
    
    def get_all_scenarios(
        self, 
        age_group: AgeGroup = None, 
        category: ScenarioCategory = None
    ) -> List[VRScenario]:
        """全シナリオを取得"""
        scenarios = []
        
        for preset in self.PRESET_SCENARIOS:
            scenario = self._create_scenario_from_preset(preset)
            
            # フィルタリング
            if age_group and scenario.difficulty > self._get_max_difficulty(age_group):
                continue
            if category and scenario.category != category:
                continue
            
            scenarios.append(scenario)
        
        return scenarios
    
    def get_scenario_by_id(self, scenario_id: str) -> VRScenario:
        """IDでシナリオを取得"""
        for preset in self.PRESET_SCENARIOS:
            scenario = self._create_scenario_from_preset(preset)
            if scenario.id == scenario_id:
                return scenario
        return None
    
    def _create_scenario_from_preset(self, preset: Dict) -> VRScenario:
        """プリセットからシナリオオブジェクトを作成"""
        scenario_id = f"SCN{self.PRESET_SCENARIOS.index(preset)+1:04d}"
        
        return VRScenario(
            id=scenario_id,
            title=preset["title"],
            description=preset["description"],
            category=preset["category"],
            target_age_group=AgeGroup.LOWER_ELEMENTARY,  # デフォルト
            difficulty=preset["difficulty"],
            target_skills=preset["skills"],
            duration_minutes=preset["duration"],
            environment=preset["environment"],
            characters=preset["characters"],
            dialogue_prompts=preset["dialogues"]
        )
    
    def _get_max_difficulty(self, age_group: AgeGroup) -> int:
        """年齢に応じた最大難易度を取得"""
        difficulty_map = {
            AgeGroup.INFANT: 2,
            AgeGroup.LOWER_ELEMENTARY: 3,
            AgeGroup.UPPER_ELEMENTARY: 5
        }
        return difficulty_map.get(age_group, 3)
    
    def get_environment_info(self, env_key: str) -> Dict:
        """環境情報を取得"""
        return self.ENVIRONMENTS.get(env_key, {})
    
    def get_character_info(self, char_key: str) -> Dict:
        """キャラクター情報を取得"""
        return self.CHARACTERS.get(char_key, {})
    
    def get_recommended_scenarios(
        self, 
        skills_to_improve: List[CommunicationSkill],
        age_group: AgeGroup
    ) -> List[VRScenario]:
        """改善すべきスキルに基づいた推薦シナリオ"""
        all_scenarios = self.get_all_scenarios(age_group=age_group)
        
        # スキルマッチングでソート
        scored = []
        for scenario in all_scenarios:
            match_count = len(set(scenario.target_skills) & set(skills_to_improve))
            scored.append((scenario, match_count))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in scored[:5]]
    
    def get_categories(self) -> List[Dict]:
        """カテゴリ一覧を取得"""
        return [
            {"id": cat.name, "name": cat.value}
            for cat in ScenarioCategory
        ]
