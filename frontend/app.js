/**
 * メインアプリケーション - VRコミュニケーションプラットフォーム
 */
const API_BASE = 'http://localhost:5000/api';

let currentSession = null;
let currentScenario = null;

// ナビゲーション
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        switchSection(e.currentTarget.dataset.section);
    });
});

function switchSection(sectionId) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

    document.getElementById(sectionId)?.classList.add('active');
    document.querySelector(`[data-section="${sectionId}"]`)?.classList.add('active');

    const titles = {
        home: ['ホーム', 'VRでコミュニケーションを楽しく学ぼう！'],
        scenarios: ['シナリオ', '練習したいシナリオを選んでね'],
        'vr-room': ['VRルーム', '仮想空間でコミュニケーション体験'],
        chat: ['AIチャット', 'AIパートナーと自由にお話しよう'],
        progress: ['進捗', 'これまでの成長を確認しよう']
    };

    document.getElementById('pageTitle').textContent = titles[sectionId]?.[0] || '';
    document.getElementById('pageDescription').textContent = titles[sectionId]?.[1] || '';
}

// API呼び出し
async function fetchAPI(endpoint, options = {}) {
    try {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        return await res.json();
    } catch (e) {
        console.error('API Error:', e);
        return null;
    }
}

// ホーム読み込み
async function loadHome() {
    // スキル一覧
    const skills = await fetchAPI('/skills');
    if (skills?.skills) {
        document.getElementById('skillsGrid').innerHTML = skills.skills
            .map(s => `<span class="skill-tag">${s.name}</span>`).join('');
    }

    // 感情一覧
    const emotions = await fetchAPI('/emotions');
    if (emotions?.emotions) {
        document.getElementById('emotionsGrid').innerHTML = emotions.emotions
            .map(e => `<span class="emotion-tag" title="${e.name}">${e.emoji}</span>`).join('');
    }
}

// シナリオ読み込み
async function loadScenarios() {
    // カテゴリ
    const cats = await fetchAPI('/scenarios/categories');
    if (cats?.categories) {
        const select = document.getElementById('categoryFilter');
        select.innerHTML = '<option value="">すべて</option>' +
            cats.categories.map(c => `<option value="${c.name}">${c.name}</option>`).join('');
    }

    // シナリオ
    const filter = document.getElementById('categoryFilter').value;
    const endpoint = filter ? `/scenarios?category=${encodeURIComponent(filter)}` : '/scenarios';
    const data = await fetchAPI(endpoint);

    const grid = document.getElementById('scenariosGrid');
    if (!data?.scenarios?.length) {
        grid.innerHTML = '<p>シナリオがありません</p>';
        return;
    }

    grid.innerHTML = data.scenarios.map(s => `
        <div class="scenario-card" onclick="selectScenario('${s.id}')">
            <div class="scenario-header">
                <span class="scenario-title">${s.title}</span>
                <span class="scenario-category">${s.category}</span>
            </div>
            <p class="scenario-description">${s.description}</p>
            <div class="scenario-meta">
                <span class="difficulty-stars">${'★'.repeat(s.difficulty)}${'☆'.repeat(5 - s.difficulty)}</span>
                <span>⏱️ ${s.duration_minutes}分</span>
                <span>${s.environment?.icon || '🏠'} ${s.environment?.name || ''}</span>
            </div>
        </div>
    `).join('');
}

document.getElementById('categoryFilter')?.addEventListener('change', loadScenarios);

// シナリオ選択
async function selectScenario(scenarioId) {
    const data = await fetchAPI(`/scenarios/${scenarioId}`);
    if (!data) return;

    currentScenario = data;

    // セッション開始
    const session = await fetchAPI('/sessions', {
        method: 'POST',
        body: JSON.stringify({ scenario_id: scenarioId })
    });

    if (session) {
        currentSession = session;
    }

    // VRルームに切り替え
    switchSection('vr-room');

    // VRシーン初期化
    initVRScene();
    loadScenarioToVR(currentScenario);

    // UI更新
    document.getElementById('vrControls').style.display = 'block';
    document.getElementById('sceneInfo').innerHTML = `
        <strong>${data.title}</strong><br>
        <span style="color: var(--text-muted)">${data.description}</span>
    `;

    // 初期ダイアログ表示
    if (data.dialogues?.length) {
        showDialogue(data.dialogues);
    }
}

function showDialogue(dialogues) {
    const box = document.getElementById('dialogueBox');
    let html = '';

    dialogues.forEach(d => {
        if (d.speaker === 'system') {
            html += `<p style="color: var(--accent)">${d.text}</p>`;
        } else if (d.speaker === 'ai') {
            const char = d.character || 'AI';
            html += `<p><strong>${char}:</strong> 「${d.text}」</p>`;
        } else if (d.speaker === 'prompt') {
            html += `<p style="color: var(--accent-yellow)">💡 ${d.text}</p>`;
        }
    });

    box.innerHTML = html;
}

// VRメッセージ送信
async function sendVRMessage() {
    const input = document.getElementById('vrInput');
    const message = input.value.trim();
    if (!message || !currentSession) return;

    input.value = '';
    const ageGroup = document.getElementById('ageGroupSelect').value;

    const response = await fetchAPI(`/sessions/${currentSession.session_id}/chat`, {
        method: 'POST',
        body: JSON.stringify({ message, age_group: ageGroup })
    });

    if (response) {
        const box = document.getElementById('dialogueBox');
        box.innerHTML += `
            <p><strong>あなた:</strong> 「${message}」</p>
            <p><strong>AI:</strong> 「${response.response}」</p>
            ${response.teaching_point ? `<p style="color: var(--accent-green)">💡 ${response.teaching_point}</p>` : ''}
        `;
        box.scrollTop = box.scrollHeight;
    }
}

document.getElementById('vrInput')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendVRMessage();
});

// AIチャット
async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message) return;

    input.value = '';
    const ageGroup = document.getElementById('ageGroupSelect').value;
    const container = document.getElementById('chatMessages');

    // ユーザーメッセージ追加
    container.innerHTML += `<div class="message child">${message}</div>`;

    // セッションがなければ作成
    if (!currentSession) {
        const session = await fetchAPI('/sessions', {
            method: 'POST',
            body: JSON.stringify({})
        });
        if (session) currentSession = session;
    }

    // API呼び出し
    const response = await fetchAPI(`/sessions/${currentSession.session_id}/chat`, {
        method: 'POST',
        body: JSON.stringify({ message, age_group: ageGroup })
    });

    if (response) {
        container.innerHTML += `<div class="message ai">${response.response}</div>`;
        document.getElementById('currentEmotion').textContent = response.emotion?.emoji || '😊';
        container.scrollTop = container.scrollHeight;
    }
}

document.getElementById('chatInput')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendChatMessage();
});

// ヘルスチェック
async function checkHealth() {
    const status = document.getElementById('apiStatus');
    try {
        const res = await fetch(`${API_BASE}/health`);
        if (res.ok) {
            status.className = 'api-status connected';
            status.innerHTML = '<span class="status-dot"></span><span>接続中</span>';
        } else throw new Error();
    } catch {
        status.className = 'api-status';
        status.innerHTML = '<span class="status-dot"></span><span>未接続</span>';
    }
}

// 初期化
checkHealth();
loadHome();
loadScenarios();
