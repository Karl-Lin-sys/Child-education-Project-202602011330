# 幼児・小学生コミュニケーションVR・AIデザインプラットフォーム
# Child VR Communication Platform

VRとAIを活用して、子どものコミュニケーション能力を育成するプラットフォーム

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-green)
![Three.js](https://img.shields.io/badge/Three.js-r128-orange)

## 🎮 概要

幼児・小学生（3〜12歳）のコミュニケーション能力を、VR環境とAIパートナーを通じて楽しく育成するプラットフォームです。

### 主な機能

- **🥽 VRシナリオシミュレーター** - 様々な社会的場面をVR環境で体験
- **🤖 AIコミュニケーションパートナー** - 対話型AIとの会話練習
- **😊 感情認識システム** - テキストから感情を分析しフィードバック
- **📊 学習進捗分析** - コミュニケーション能力の成長を可視化

## 🏗️ プロジェクト構造

```
child_vr_communication/
├── backend/
│   ├── app.py              # Flask API
│   ├── ai_partner.py       # AIパートナー
│   ├── emotion_analyzer.py # 感情分析
│   ├── scenario_generator.py # シナリオ生成
│   └── models.py           # データモデル
├── frontend/
│   ├── index.html          # メインUI
│   ├── styles.css          # スタイル
│   ├── app.js              # アプリロジック
│   └── vr-scene.js         # Three.js VR
├── README.md
└── requirements.txt
```

## 🚀 セットアップ

```bash
# クローン
git clone https://github.com/I-PingLin/Child-education-Project-202602011330.git
cd Child-education-Project-202602011330

# インストール
pip install -r requirements.txt

# 起動
cd backend
python app.py
```

ブラウザで `frontend/index.html` を開いてください。

## 📡 API エンドポイント

| エンドポイント | 説明 |
|---------------|------|
| `/api/scenarios` | シナリオ一覧 |
| `/api/sessions` | セッション管理 |
| `/api/sessions/<id>/chat` | AIチャット |
| `/api/analyze/emotion` | 感情分析 |
| `/api/skills` | スキル一覧 |

## 🎬 シナリオ例

- あいさつをしよう
- おもちゃを貸してあげよう
- ケンカを仲直り
- 困っている子を助けよう
- 自己紹介をしよう

## 💡 スキル領域

| スキル | 説明 |
|-------|------|
| 言語表現 | 自分の気持ちを言葉で伝える |
| 傾聴力 | 相手の話をしっかり聞く |
| 共感力 | 相手の気持ちを理解する |
| 問題解決力 | トラブルを解決する |
| 感情調整力 | 自分の感情をコントロール |

## 👨‍💻 作者

I-Ping Lin

## 📝 ライセンス

MIT License
