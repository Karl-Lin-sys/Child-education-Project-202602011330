"""
感情分析モジュール
テキストと音声から感情を認識・分析
"""
import random
from datetime import datetime
from typing import Dict, List, Optional
from models import EmotionType, EmotionState


class EmotionAnalyzer:
    """感情分析エンジン"""
    
    # 感情キーワード辞書
    EMOTION_KEYWORDS = {
        EmotionType.HAPPY: [
            "うれしい", "たのしい", "嬉しい", "楽しい", "わーい", "やった",
            "すごい", "大好き", "ありがとう", "最高", "いいね"
        ],
        EmotionType.SAD: [
            "かなしい", "悲しい", "さみしい", "寂しい", "つらい", "辛い",
            "泣きたい", "いやだ", "こまった", "困った"
        ],
        EmotionType.ANGRY: [
            "むかつく", "いらいら", "怒り", "ふざけるな", "やめて",
            "きらい", "嫌い", "ひどい", "ずるい"
        ],
        EmotionType.SURPRISED: [
            "びっくり", "驚いた", "えっ", "すごい", "まさか",
            "本当", "うそ", "信じられない"
        ],
        EmotionType.FEARFUL: [
            "こわい", "怖い", "不安", "心配", "どうしよう",
            "できない", "無理", "やだ"
        ],
        EmotionType.EXCITED: [
            "わくわく", "ドキドキ", "早く", "待ちきれない",
            "すごく楽しみ", "興奮"
        ],
        EmotionType.CALM: [
            "大丈夫", "落ち着いて", "ゆっくり", "のんびり",
            "穏やか", "平和"
        ]
    }
    
    # 感情に対応する顔文字
    EMOTION_EMOJIS = {
        EmotionType.HAPPY: "😊",
        EmotionType.SAD: "😢",
        EmotionType.ANGRY: "😠",
        EmotionType.SURPRISED: "😲",
        EmotionType.FEARFUL: "😨",
        EmotionType.NEUTRAL: "😐",
        EmotionType.EXCITED: "🤩",
        EmotionType.CALM: "😌"
    }
    
    def __init__(self):
        pass
    
    def analyze_text(self, text: str) -> EmotionState:
        """テキストから感情を分析"""
        text_lower = text.lower()
        
        # 各感情のスコアを計算
        emotion_scores = {}
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        # 最も高いスコアの感情を取得
        if emotion_scores:
            primary = max(emotion_scores, key=emotion_scores.get)
            max_score = emotion_scores[primary]
            confidence = min(0.9, 0.3 + max_score * 0.2)
        else:
            primary = EmotionType.NEUTRAL
            confidence = 0.5
        
        # 二次感情を計算
        secondary = {}
        for emotion, score in emotion_scores.items():
            if emotion != primary:
                secondary[emotion.value] = min(0.8, score * 0.15)
        
        # 感情価（ポジティブ/ネガティブ）を計算
        valence = self._calculate_valence(primary, emotion_scores)
        
        # 覚醒度を計算
        arousal = self._calculate_arousal(primary)
        
        return EmotionState(
            timestamp=datetime.now(),
            primary_emotion=primary,
            confidence=confidence,
            secondary_emotions=secondary,
            valence=valence,
            arousal=arousal
        )
    
    def _calculate_valence(
        self, 
        primary: EmotionType, 
        scores: Dict
    ) -> float:
        """感情価を計算（-1: ネガティブ、+1: ポジティブ）"""
        valence_map = {
            EmotionType.HAPPY: 0.8,
            EmotionType.SAD: -0.7,
            EmotionType.ANGRY: -0.6,
            EmotionType.SURPRISED: 0.2,
            EmotionType.FEARFUL: -0.5,
            EmotionType.NEUTRAL: 0.0,
            EmotionType.EXCITED: 0.7,
            EmotionType.CALM: 0.3
        }
        return valence_map.get(primary, 0.0)
    
    def _calculate_arousal(self, emotion: EmotionType) -> float:
        """覚醒度を計算（0: 低い、1: 高い）"""
        arousal_map = {
            EmotionType.HAPPY: 0.6,
            EmotionType.SAD: 0.3,
            EmotionType.ANGRY: 0.9,
            EmotionType.SURPRISED: 0.8,
            EmotionType.FEARFUL: 0.7,
            EmotionType.NEUTRAL: 0.4,
            EmotionType.EXCITED: 0.95,
            EmotionType.CALM: 0.2
        }
        return arousal_map.get(emotion, 0.5)
    
    def get_emoji(self, emotion: EmotionType) -> str:
        """感情に対応する絵文字を取得"""
        return self.EMOTION_EMOJIS.get(emotion, "😐")
    
    def get_emotion_feedback(self, state: EmotionState) -> str:
        """感情状態に基づくフィードバックを生成"""
        feedback_templates = {
            EmotionType.HAPPY: [
                "とても楽しそうですね！",
                "嬉しい気持ちが伝わってきます！",
                "その笑顔、すてきです！"
            ],
            EmotionType.SAD: [
                "悲しい気持ちになっているのかな？",
                "つらいときは話してくれてありがとう",
                "一緒にゆっくり考えようね"
            ],
            EmotionType.ANGRY: [
                "怒っている気持ち、わかるよ",
                "深呼吸してみようか",
                "どうしてそう感じたか教えてくれる？"
            ],
            EmotionType.SURPRISED: [
                "びっくりしたね！",
                "予想外だったかな？",
                "驚きの発見だね！"
            ],
            EmotionType.FEARFUL: [
                "心配しなくても大丈夫だよ",
                "一緒にいるから安心してね",
                "怖いときは言ってね"
            ],
            EmotionType.EXCITED: [
                "わくわくするね！",
                "その気持ち、とっても素敵！",
                "楽しみだね！"
            ],
            EmotionType.CALM: [
                "落ち着いていてすごいね",
                "リラックスできているね",
                "穏やかな気持ちだね"
            ],
            EmotionType.NEUTRAL: [
                "どんな気持ち？",
                "何か考えていることある？",
                "話してくれてありがとう"
            ]
        }
        
        templates = feedback_templates.get(state.primary_emotion, [""])
        return random.choice(templates)
    
    def calculate_emotional_stability(
        self, 
        emotion_timeline: List[EmotionState]
    ) -> float:
        """感情の安定度を計算（0-100）"""
        if len(emotion_timeline) < 2:
            return 50.0
        
        # 感情の変動を計算
        valence_changes = []
        arousal_changes = []
        
        for i in range(1, len(emotion_timeline)):
            prev = emotion_timeline[i-1]
            curr = emotion_timeline[i]
            valence_changes.append(abs(curr.valence - prev.valence))
            arousal_changes.append(abs(curr.arousal - prev.arousal))
        
        avg_valence_change = sum(valence_changes) / len(valence_changes)
        avg_arousal_change = sum(arousal_changes) / len(arousal_changes)
        
        # 変動が少ないほど安定度が高い
        stability = 100 - (avg_valence_change + avg_arousal_change) * 50
        return max(0, min(100, stability))
