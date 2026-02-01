"""
幼児・小学生コミュニケーションVR・AIプラットフォーム
Flask API サーバー
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import uuid

from models import (
    AgeGroup, EmotionType, CommunicationSkill, ScenarioCategory,
    Child, VRSession, ConversationTurn
)
from ai_partner import AIPartner
from emotion_analyzer import EmotionAnalyzer
from scenario_generator import ScenarioGenerator

app = Flask(__name__)
CORS(app)

# コンポーネント初期化
ai_partner = AIPartner()
emotion_analyzer = EmotionAnalyzer()
scenario_generator = ScenarioGenerator()

# セッションストレージ（デモ用）
active_sessions = {}
children_data = {}


def serialize_enum(obj):
    if hasattr(obj, 'value'):
        return obj.value
    return obj


def serialize_scenario(s):
    return {
        "id": s.id,
        "title": s.title,
        "description": s.description,
        "category": s.category.value,
        "difficulty": s.difficulty,
        "duration_minutes": s.duration_minutes,
        "environment": scenario_generator.get_environment_info(s.environment),
        "characters": [scenario_generator.get_character_info(c) for c in s.characters],
        "target_skills": [sk.value for sk in s.target_skills],
        "dialogues": s.dialogue_prompts
    }


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "service": "Child VR Communication Platform"
    })


# === シナリオ API ===

@app.route('/api/scenarios', methods=['GET'])
def get_scenarios():
    """全シナリオを取得"""
    category = request.args.get('category')
    age_group = request.args.get('age_group')
    
    cat = None
    if category:
        for c in ScenarioCategory:
            if c.value == category:
                cat = c
                break
    
    ag = None
    if age_group:
        for a in AgeGroup:
            if a.value == age_group:
                ag = a
                break
    
    scenarios = scenario_generator.get_all_scenarios(age_group=ag, category=cat)
    return jsonify({
        "scenarios": [serialize_scenario(s) for s in scenarios],
        "total": len(scenarios)
    })


@app.route('/api/scenarios/<scenario_id>', methods=['GET'])
def get_scenario(scenario_id):
    """個別シナリオを取得"""
    scenario = scenario_generator.get_scenario_by_id(scenario_id)
    if not scenario:
        return jsonify({"error": "Scenario not found"}), 404
    return jsonify(serialize_scenario(scenario))


@app.route('/api/scenarios/categories', methods=['GET'])
def get_categories():
    """カテゴリ一覧"""
    return jsonify({"categories": scenario_generator.get_categories()})


# === セッション API ===

@app.route('/api/sessions', methods=['POST'])
def create_session():
    """新しいVRセッションを開始"""
    data = request.get_json()
    child_id = data.get('child_id', 'guest')
    scenario_id = data.get('scenario_id')
    
    session_id = str(uuid.uuid4())[:8]
    
    session = {
        "id": session_id,
        "child_id": child_id,
        "scenario_id": scenario_id,
        "start_time": datetime.now().isoformat(),
        "conversation": [],
        "emotions": [],
        "active": True
    }
    active_sessions[session_id] = session
    
    return jsonify({
        "session_id": session_id,
        "message": "Session created",
        "scenario": scenario_generator.get_scenario_by_id(scenario_id).title if scenario_id else None
    })


@app.route('/api/sessions/<session_id>/chat', methods=['POST'])
def chat(session_id):
    """チャットメッセージを送信"""
    if session_id not in active_sessions:
        return jsonify({"error": "Session not found"}), 404
    
    data = request.get_json()
    message = data.get('message', '')
    age_group_str = data.get('age_group', '低学年')
    
    # 年齢グループを取得
    age_group = AgeGroup.LOWER_ELEMENTARY
    for ag in AgeGroup:
        if ag.value == age_group_str:
            age_group = ag
            break
    
    # 感情分析
    emotion_state = emotion_analyzer.analyze_text(message)
    
    # AI応答生成
    response = ai_partner.generate_response(
        child_message=message,
        age_group=age_group
    )
    
    # セッションに保存
    session = active_sessions[session_id]
    session["conversation"].append({
        "speaker": "child",
        "message": message,
        "timestamp": datetime.now().isoformat()
    })
    session["conversation"].append({
        "speaker": "ai",
        "message": response.message,
        "timestamp": datetime.now().isoformat()
    })
    session["emotions"].append({
        "emotion": emotion_state.primary_emotion.value,
        "confidence": emotion_state.confidence,
        "valence": emotion_state.valence,
        "timestamp": datetime.now().isoformat()
    })
    
    return jsonify({
        "response": response.message,
        "emotion": {
            "detected": emotion_state.primary_emotion.value,
            "emoji": emotion_analyzer.get_emoji(emotion_state.primary_emotion),
            "confidence": round(emotion_state.confidence, 2),
            "feedback": emotion_analyzer.get_emotion_feedback(emotion_state)
        },
        "ai_emotion": response.emotion.value,
        "teaching_point": response.teaching_point,
        "encouragement": response.encouragement,
        "suggested_actions": response.suggested_actions
    })


@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """セッション情報を取得"""
    if session_id not in active_sessions:
        return jsonify({"error": "Session not found"}), 404
    return jsonify(active_sessions[session_id])


@app.route('/api/sessions/<session_id>/end', methods=['POST'])
def end_session(session_id):
    """セッションを終了"""
    if session_id not in active_sessions:
        return jsonify({"error": "Session not found"}), 404
    
    session = active_sessions[session_id]
    session["active"] = False
    session["end_time"] = datetime.now().isoformat()
    
    # 感情安定度を計算
    if session["emotions"]:
        stability = 70 + len(session["conversation"]) * 2
        stability = min(100, stability)
    else:
        stability = 50
    
    return jsonify({
        "message": "Session ended",
        "summary": {
            "duration_minutes": len(session["conversation"]) * 2,
            "total_exchanges": len(session["conversation"]) // 2,
            "emotional_stability": stability
        }
    })


# === 分析 API ===

@app.route('/api/analyze/emotion', methods=['POST'])
def analyze_emotion():
    """テキストの感情分析"""
    data = request.get_json()
    text = data.get('text', '')
    
    state = emotion_analyzer.analyze_text(text)
    
    return jsonify({
        "text": text,
        "emotion": state.primary_emotion.value,
        "emoji": emotion_analyzer.get_emoji(state.primary_emotion),
        "confidence": round(state.confidence, 2),
        "valence": round(state.valence, 2),
        "arousal": round(state.arousal, 2),
        "secondary_emotions": state.secondary_emotions,
        "feedback": emotion_analyzer.get_emotion_feedback(state)
    })


# === スキル API ===

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """コミュニケーションスキル一覧"""
    return jsonify({
        "skills": [{"id": s.name, "name": s.value} for s in CommunicationSkill]
    })


@app.route('/api/emotions', methods=['GET'])
def get_emotions():
    """感情タイプ一覧"""
    return jsonify({
        "emotions": [
            {"id": e.name, "name": e.value, "emoji": emotion_analyzer.get_emoji(e)}
            for e in EmotionType
        ]
    })


if __name__ == '__main__':
    print("=" * 60)
    print("幼児・小学生コミュニケーションVR・AIプラットフォーム")
    print("Child VR Communication Platform")
    print("=" * 60)
    print(f"シナリオ数: {len(scenario_generator.get_all_scenarios())}")
    print("=" * 60)
    print("Starting server at http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
