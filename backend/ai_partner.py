"""
AIコミュニケーションパートナー
子どもとの対話を行うAIエンジン
"""
import random
from datetime import datetime
from typing import List, Dict, Optional
from models import (
    EmotionType, EmotionState, AIResponse, 
    CommunicationSkill, AgeGroup, ConversationTurn
)
from emotion_analyzer import EmotionAnalyzer


class AIPartner:
    """AIコミュニケーションパートナー"""
    
    # 年齢別の話し方調整
    LANGUAGE_STYLES = {
        AgeGroup.INFANT: {
            "complexity": "simple",
            "sentence_length": "short",
            "vocabulary": "basic"
        },
        AgeGroup.LOWER_ELEMENTARY: {
            "complexity": "moderate", 
            "sentence_length": "medium",
            "vocabulary": "expanding"
        },
        AgeGroup.UPPER_ELEMENTARY: {
            "complexity": "advanced",
            "sentence_length": "varied",
            "vocabulary": "rich"
        }
    }
    
    # 会話パターン
    RESPONSE_TEMPLATES = {
        "greeting": {
            AgeGroup.INFANT: [
                "こんにちは！きょうもなかよくあそぼうね！",
                "やあ！げんきかな？",
                "おはよう！いっしょにたのしもうね！"
            ],
            AgeGroup.LOWER_ELEMENTARY: [
                "こんにちは！今日は何をしたい？",
                "やあ！元気だった？",
                "会えてうれしいな！"
            ],
            AgeGroup.UPPER_ELEMENTARY: [
                "こんにちは！調子はどう？",
                "やあ、今日も頑張ろうね！",
                "元気そうで良かった！"
            ]
        },
        "encouragement": {
            AgeGroup.INFANT: [
                "すごいすごい！",
                "じょうずだね！",
                "がんばったね！"
            ],
            AgeGroup.LOWER_ELEMENTARY: [
                "とても上手だね！",
                "その調子！頑張ってるね！",
                "すごい！できたね！"
            ],
            AgeGroup.UPPER_ELEMENTARY: [
                "素晴らしい！よく考えたね！",
                "その発想、いいね！",
                "成長しているのが分かるよ！"
            ]
        },
        "clarification": {
            AgeGroup.INFANT: [
                "もういちどおしえて？",
                "なあに？",
                "どうしたの？"
            ],
            AgeGroup.LOWER_ELEMENTARY: [
                "もう少し教えてくれる？",
                "どういうこと？",
                "それはどうして？"
            ],
            AgeGroup.UPPER_ELEMENTARY: [
                "もう少し詳しく聞かせて",
                "具体的にはどういうこと？",
                "なぜそう思ったの？"
            ]
        }
    }
    
    # コミュニケーションスキル教育ポイント
    TEACHING_POINTS = {
        CommunicationSkill.VERBAL: [
            "自分の気持ちを言葉で伝えてみよう",
            "相手にわかりやすく話してみよう",
            "「〜したい」「〜と思う」を使ってみよう"
        ],
        CommunicationSkill.ACTIVE_LISTENING: [
            "相手の話をしっかり聞こうね",
            "うなずきながら聞いてみよう",
            "相手が話し終わるまで待とうね"
        ],
        CommunicationSkill.EMPATHY: [
            "相手はどんな気持ちかな？",
            "自分だったらどう感じる？",
            "相手の立場で考えてみよう"
        ],
        CommunicationSkill.CONFLICT_RESOLUTION: [
            "お互いの気持ちを話し合おう",
            "一緒に解決方法を考えよう",
            "「ごめんね」と「いいよ」を大切に"
        ]
    }
    
    def __init__(self):
        self.emotion_analyzer = EmotionAnalyzer()
        self.conversation_history: List[ConversationTurn] = []
    
    def generate_response(
        self,
        child_message: str,
        age_group: AgeGroup,
        scenario_context: Optional[str] = None,
        target_skill: Optional[CommunicationSkill] = None
    ) -> AIResponse:
        """子どもの発言に対する応答を生成"""
        
        # 感情分析
        emotion_state = self.emotion_analyzer.analyze_text(child_message)
        
        # 応答を構築
        response_parts = []
        
        # 1. 感情への共感
        empathy = self._generate_empathy(emotion_state, age_group)
        if empathy:
            response_parts.append(empathy)
        
        # 2. メイン応答
        main_response = self._generate_main_response(
            child_message, age_group, scenario_context
        )
        response_parts.append(main_response)
        
        # 3. スキル教育（オプション）
        teaching = None
        if target_skill:
            teaching = self._get_teaching_point(target_skill)
        
        # 4. 励まし
        encouragement = self._get_encouragement(age_group, emotion_state)
        
        # 提案アクションを生成
        actions = self._suggest_actions(emotion_state, target_skill)
        
        return AIResponse(
            message=" ".join(response_parts),
            emotion=self._determine_ai_emotion(emotion_state),
            suggested_actions=actions,
            teaching_point=teaching,
            encouragement=encouragement
        )
    
    def _generate_empathy(
        self, 
        state: EmotionState, 
        age_group: AgeGroup
    ) -> str:
        """共感の言葉を生成"""
        return self.emotion_analyzer.get_emotion_feedback(state)
    
    def _generate_main_response(
        self,
        message: str,
        age_group: AgeGroup,
        context: Optional[str]
    ) -> str:
        """メイン応答を生成"""
        
        # キーワードベースの応答
        message_lower = message.lower()
        
        # 質問への応答
        if "?" in message or "？" in message or "なに" in message:
            if "気持ち" in message or "きもち" in message:
                return "気持ちを考えるのは大切だね。どんな気持ちか、一緒に考えてみよう！"
            elif "どうして" in message or "なぜ" in message:
                return "いい質問だね！理由を考えることはとても大切だよ。"
            else:
                templates = self.RESPONSE_TEMPLATES["clarification"][age_group]
                return random.choice(templates)
        
        # あいさつへの応答
        greetings = ["こんにちは", "おはよう", "やあ", "ハロー", "hello", "hi"]
        if any(g in message_lower for g in greetings):
            templates = self.RESPONSE_TEMPLATES["greeting"][age_group]
            return random.choice(templates)
        
        # 一般的な応答
        general_responses = {
            AgeGroup.INFANT: [
                "そうなんだね！",
                "おしえてくれてありがとう！",
                "いいね！"
            ],
            AgeGroup.LOWER_ELEMENTARY: [
                "なるほど！教えてくれてありがとう！",
                "そうだったんだね！",
                "面白い考えだね！"
            ],
            AgeGroup.UPPER_ELEMENTARY: [
                "興味深いね！もっと聞かせて。",
                "素敵な考え方だね！",
                "よく考えているね！"
            ]
        }
        return random.choice(general_responses[age_group])
    
    def _get_teaching_point(self, skill: CommunicationSkill) -> str:
        """スキルに関する教育ポイントを取得"""
        points = self.TEACHING_POINTS.get(skill, [])
        return random.choice(points) if points else ""
    
    def _get_encouragement(
        self, 
        age_group: AgeGroup, 
        state: EmotionState
    ) -> str:
        """励ましの言葉を取得"""
        if state.valence < 0:
            # ネガティブな感情の場合
            encouragements = [
                "一緒に頑張ろうね！",
                "大丈夫、きっとうまくいくよ！",
                "いつでも応援しているよ！"
            ]
        else:
            templates = self.RESPONSE_TEMPLATES["encouragement"][age_group]
            encouragements = templates
        
        return random.choice(encouragements)
    
    def _suggest_actions(
        self,
        state: EmotionState,
        skill: Optional[CommunicationSkill]
    ) -> List[str]:
        """提案アクションを生成"""
        actions = []
        
        # 感情に基づくアクション
        if state.arousal > 0.7:
            actions.append("深呼吸をしてみよう")
        
        if state.valence < -0.3:
            actions.append("気持ちを言葉にしてみよう")
        
        # スキルに基づくアクション
        if skill == CommunicationSkill.ACTIVE_LISTENING:
            actions.append("相手の目を見て聞いてみよう")
        elif skill == CommunicationSkill.EMPATHY:
            actions.append("相手の気持ちを想像してみよう")
        elif skill == CommunicationSkill.VERBAL:
            actions.append("「私は〜と思います」で話してみよう")
        
        return actions[:3]  # 最大3つ
    
    def _determine_ai_emotion(self, child_state: EmotionState) -> EmotionType:
        """AI側の感情を決定"""
        # 子どもの感情に寄り添いながらポジティブを維持
        if child_state.valence < -0.3:
            return EmotionType.CALM  # 落ち着いた対応
        elif child_state.primary_emotion == EmotionType.EXCITED:
            return EmotionType.HAPPY  # 一緒に喜ぶ
        else:
            return EmotionType.HAPPY  # 基本は明るく
