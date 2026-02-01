/**
 * VRシーン描画 - Three.js
 */
class VRSceneManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.characters = {};
        this.environment = null;
        this.isInitialized = false;
    }

    init() {
        if (this.isInitialized || !this.container) return;

        // Three.jsシーン初期化
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1a2e);

        // カメラ設定
        const width = this.container.clientWidth;
        const height = this.container.clientHeight || 400;
        this.camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        this.camera.position.set(0, 1.5, 5);

        // レンダラー設定
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(width, height);
        this.container.innerHTML = '';
        this.container.appendChild(this.renderer.domElement);

        // ライティング
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(5, 10, 5);
        this.scene.add(directionalLight);

        // 床
        const floorGeometry = new THREE.PlaneGeometry(20, 20);
        const floorMaterial = new THREE.MeshStandardMaterial({
            color: 0x2d3347,
            roughness: 0.8
        });
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        floor.rotation.x = -Math.PI / 2;
        this.scene.add(floor);

        this.isInitialized = true;
        this.animate();
    }

    loadEnvironment(envType) {
        // 環境オブジェクトをクリア
        if (this.environment) {
            this.scene.remove(this.environment);
        }

        this.environment = new THREE.Group();

        const colors = {
            classroom: 0x4a5568,
            playground: 0x48bb78,
            home: 0xed8936,
            library: 0x805ad5,
            store: 0x38b2ac
        };

        const color = colors[envType] || 0x4a5568;

        // 簡易的な壁を作成
        const wallMaterial = new THREE.MeshStandardMaterial({ color: color, side: THREE.DoubleSide });

        // 後ろの壁
        const backWall = new THREE.Mesh(new THREE.PlaneGeometry(20, 8), wallMaterial);
        backWall.position.set(0, 4, -10);
        this.environment.add(backWall);

        // 左の壁
        const leftWall = new THREE.Mesh(new THREE.PlaneGeometry(20, 8), wallMaterial);
        leftWall.rotation.y = Math.PI / 2;
        leftWall.position.set(-10, 4, 0);
        this.environment.add(leftWall);

        // 右の壁
        const rightWall = new THREE.Mesh(new THREE.PlaneGeometry(20, 8), wallMaterial);
        rightWall.rotation.y = -Math.PI / 2;
        rightWall.position.set(10, 4, 0);
        this.environment.add(rightWall);

        this.scene.add(this.environment);
    }

    addCharacter(id, name, position = { x: 0, y: 0, z: 0 }) {
        // シンプルなキャラクター表現
        const group = new THREE.Group();

        // 体
        const bodyGeo = new THREE.CylinderGeometry(0.3, 0.4, 1, 16);
        const bodyMat = new THREE.MeshStandardMaterial({ color: 0x6366f1 });
        const body = new THREE.Mesh(bodyGeo, bodyMat);
        body.position.y = 0.5;
        group.add(body);

        // 頭
        const headGeo = new THREE.SphereGeometry(0.3, 16, 16);
        const headMat = new THREE.MeshStandardMaterial({ color: 0xfcd34d });
        const head = new THREE.Mesh(headGeo, headMat);
        head.position.y = 1.3;
        group.add(head);

        group.position.set(position.x, position.y, position.z);
        this.characters[id] = group;
        this.scene.add(group);
    }

    removeCharacter(id) {
        if (this.characters[id]) {
            this.scene.remove(this.characters[id]);
            delete this.characters[id];
        }
    }

    clearCharacters() {
        for (const id in this.characters) {
            this.scene.remove(this.characters[id]);
        }
        this.characters = {};
    }

    animate() {
        if (!this.isInitialized) return;

        requestAnimationFrame(() => this.animate());

        // キャラクターをゆらゆら動かす
        for (const id in this.characters) {
            const char = this.characters[id];
            char.rotation.y = Math.sin(Date.now() * 0.001) * 0.1;
        }

        this.renderer.render(this.scene, this.camera);
    }

    resize() {
        if (!this.isInitialized) return;

        const width = this.container.clientWidth;
        const height = this.container.clientHeight;

        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    destroy() {
        if (this.renderer) {
            this.renderer.dispose();
        }
        this.isInitialized = false;
    }
}

// グローバルインスタンス
let vrScene = null;

function initVRScene() {
    if (!vrScene) {
        vrScene = new VRSceneManager('vrViewport');
    }
    vrScene.init();
}

function loadScenarioToVR(scenario) {
    if (!vrScene || !vrScene.isInitialized) {
        initVRScene();
    }

    vrScene.clearCharacters();
    vrScene.loadEnvironment(scenario.environment?.name || 'classroom');

    // キャラクターを配置
    if (scenario.characters) {
        scenario.characters.forEach((char, index) => {
            const x = (index - scenario.characters.length / 2) * 2;
            vrScene.addCharacter(char.name, char.name, { x: x, y: 0, z: -2 });
        });
    }
}

window.addEventListener('resize', () => {
    if (vrScene) vrScene.resize();
});
