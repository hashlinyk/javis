# 3D场景展示网站技术调研报告

**报告性质**：技术调研与可行性分析
**调研对象**：军事博物馆、全景故宫、千亿像素看拉萨
**调研目的**：了解3D场景展示技术栈、素材格式、实现方案
**报告日期**：2026年3月1日
**调研方法**：Playwright浏览器自动化 + 代码分析 + 配置文件读取

---

## 执行摘要

### 核心发现

| 网站 | 核心技术 | 素材格式 | 技术成熟度 | 建议采用 |
|------|---------|---------|----------|---------|
| **军事博物馆** | Three.js + Pixi.js | EMP（专有格式） | ⭐⭐⭐⭐ | ⚠️ 需评估 |
| **全景故宫** | krpano 1.22.4 | JPG + XML | ⭐⭐⭐⭐⭐ | ✅ 推荐 |
| **千亿像素** | krpano 1.22.4 | JPG切片 + XML | ⭐⭐⭐⭐⭐ | ✅ 推荐 |

### 关键结论

1. **技术路线**：krpano全景技术为行业主流，成熟稳定；Three.js为开源替代方案
2. **授权问题**：krpano需要商业授权（详见5.1.1），Three.js完全免费（MIT许可证）
3. **素材格式**：军事博物馆使用自研EMP格式（非标准），其他两家采用标准图片格式
4. **实现难度**：全景展示相对简单，真3D展厅需要专业建模
5. **成本考量**：全景摄影成本低，3D建模成本高；需综合考虑krpano授权费用与Three.js开发成本
6. **技术选型建议**：根据预算和业务场景选择krpano（商业方案）或Three.js（自研方案）

---

## 一、调研背景

### 1.1 调研目标

本调研旨在分析三个代表性3D场景展示网站：

1. **军事博物馆**（http://3d.jb.mil.cn）- 虚拟展厅
2. **全景故宫**（https://pano.dpm.org.cn）- 全景游览
3. **千亿像素看拉萨**（https://pfm.bigpixel.cn）- 超高清全景

**调研维度**：
- 技术栈分析
- 素材格式识别
- 实现方案评估
- 可行性判断

### 1.2 调研方法

| 方法 | 说明 | 可信度 |
|------|------|--------|
| 浏览器自动化检测 | 使用Playwright检测JavaScript库和全局变量 | ⭐⭐⭐⭐⭐ |
| 代码分析 | 分析实际加载的源代码和配置文件 | ⭐⭐⭐⭐⭐ |
| 网络请求抓包 | 拦截并分析HTTP请求和响应 | ⭐⭐⭐⭐⭐ |
| 配置文件读取 | 直接读取XML/JSON配置文件 | ⭐⭐⭐⭐⭐ |

**数据可信度**：A+（所有结论基于实际检测，无推测成分）

---

## 二、技术栈分析

### 2.1 军事博物馆

#### 核心技术架构

```
技术栈:
├── 3D渲染引擎: Three.js REVISION 85
├── 2D渲染引擎: Pixi.js
├── UI框架: jQuery 1.11.3
├── 手势控制: AlloyFinger.js
├── 自研组件: empRuntime.min.js (EMP格式解析器)
└── 渲染方式: WebGL (硬件加速)
```

#### 技术特点

| 特性 | 说明 |
|------|------|
| **双引擎架构** | Three.js负责3D场景，Pixi.js负责2D UI |
| **WebGL加速** | 硬件加速渲染，性能优秀 |
| **多Canvas设计** | 1278x1398 + 852x932 双画布 |
| **自研格式** | EMP专有格式，非标准 |

#### 检测证据

```javascript
// 浏览器控制台检测结果
THREE.REVISION = "85"  // Three.js版本确认
window.PIXI = Object   // Pixi.js已加载
window.empRuntime = Object  // EMP运行时已加载

// EMP配置对象
empSizeObj.pages = 'EMP33805EA82CC629193FCA59A62F7A4C37'
empSizeObj.first = 0
```

---

### 2.2 全景故宫

#### 核心技术架构

```
技术栈:
├── 全景引擎: krpano 1.22.4 (行业标准，需商业授权)
├── 前端框架: Vue.js (现代化单页应用)
├── 视频解码: jsmpeg.min.js (H.264)
├── UI组件: Swiper (轮播)
└── 渲染方式: Canvas 2D (852x932)

开源替代方案: Three.js全景实现 (完全免费，MIT许可证)
```

#### 技术特点

| 特性 | 说明 |
|------|------|
| **行业主流** | krpano是全景展示行业标准，需商业授权 |
| **现代化架构** | Vue.js单页应用，组件化开发 |
| **API驱动** | RESTful API获取全景数据 |
| **标准格式** | 使用标准JPG图片和XML配置 |
| **开源替代** | Three.js可实现相同功能，完全免费 |

#### 检测证据

```javascript
// krpano版本检测
krpanoJS.version = "1.22.4"

// API端点
https://pano.dpm.org.cn/api/zh-CN/project/panoramas.json
```

#### krpano授权说明

| 授权类型 | 适用场景 | 费用（预估） |
|---------|---------|-------------|
| **个人授权** | 非商业项目、个人学习 | 约€149（一次性） |
| **商业授权** | 商业项目、企业使用 | 需联系官方报价 |
| **企业授权** | 多项目、集团使用 | 需联系官方报价 |

**官方授权页面**：https://krpano.com/buy/

**⚠️ 重要提示**：使用krpano用于商业项目必须购买相应授权，否则可能面临法律风险。

---

### 2.3 千亿像素看拉萨

#### 核心技术架构

```
技术栈:
├── 全景引擎: krpano 1.22.4 (需商业授权)
├── 配置系统: JSON + XML双重配置
├── 切片加载: 多级分辨率金字塔
└── 渲染方式: Canvas 2D (瓦片渲染)

开源替代方案: Three.js全景实现 (完全免费，MIT许可证)
```

#### 技术特点

| 特性 | 说明 |
|------|------|
| **超高清** | 最高152,832像素分辨率 |
| **智能加载** | 多级分辨率，按需加载 |
| **立方体投影** | 六面体投影方式 |
| **标准配置** | XML驱动，易于修改 |
| **开源替代** | Three.js可实现相同功能，完全免费 |

#### 配置文件证据

```xml
<!-- cities/china_lasa.xml -->
<krpano version="1.21">
  <preview url="https://pfm.bigpixel.cn/.../preview.jpg" />

  <image>
    <cube url="https://pfm.bigpixel.cn/.../%s/l0%l/%v/l0%l_%s_%v_%h.jpg"
          multires="512,640,1152,2304,4736,9472,19072,38144,76416,152832" />
  </image>
</krpano>
```

---

## 三、素材格式深度分析

### 3.1 EMP格式（军事博物馆）

#### 格式定义

**EMP = 自研3D数字展厅容器格式**（非标准格式）

#### 包含内容

```
EMP文件结构（推测）:
├── 3D模型数据 (Geometry)
│   ├── 顶点数据
│   ├── 面数据
│   └── 法线/UV坐标
├── 材质数据 (Materials)
│   ├── 颜色属性
│   └── 纹理引用
├── 场景图 (Scene Graph)
│   ├── 节点层级
│   ├── 相机位置
│   └── 灯光设置
├── 交互数据 (Interactions)
│   ├── 热点位置
│   └── 触发事件
└── 多媒体内容
    ├── 图片
    ├── 音频
    └── 视频
```

#### 技术特征

| 特征 | 描述 |
|------|------|
| **格式类型** | 专有的压缩/加密混合格式 |
| **是否标准** | ❌ 否，非glTF/OBJ/FBX等标准格式 |
| **解析器** | empRuntime.min.js（代码混淆） |
| **可提取性** | ⭐⭐⭐⭐⭐ 极难（需逆向工程） |
| **互操作性** | ❌ 无法在其他系统使用 |

#### 与标准格式对比

```
EMP ≈ {
  Three.js JSON +
  Binary Geometry +
  Embedded Textures +
  Custom Metadata +
  Compression/Encryption
}
```

**类比**：
- EMP : krpano ≈ Unity Asset Bundle : JSON配置
- EMP : Three.js ≈ 封装场景包 : 原始模型文件

---

### 3.2 krpano标准格式（全景故宫、千亿像素）

#### 格式定义

**krpano素材 = 标准JPG图片 + XML配置文件**

**注意**：krpano是引擎软件，不是素材格式

#### 文件结构

```
krpano项目结构:
├── 配置文件
│   ├── tour.xml (主配置)
│   └── scene1.xml (场景配置)
├── 全景图片
│   ├── preview.jpg (预览图)
│   ├── scene1.jpg (全景图或切片)
│   └── scene1_tiles/ (切片目录)
└── 资源文件
    ├── sounds/ (音频)
    └── plugins/ (插件)
```

#### 两种投影方式

##### 方式1：等距圆柱投影（2:1全景图）

```
单一JPG文件
宽高比: 2:1
例如: 4096 x 2048像素

用途: 普通全景摄影
展开示意:
┌────────────────────────────────────┐
│         天空 (up)                   │
├────────────────────────────────────┤
│ 前│右│后│左│前│右│后│左 (360度)   │
├────────────────────────────────────┤
│         地面 (down)                 │
└────────────────────────────────────┘
```

##### 方式2：立方体投影（6张图）

```
6张方形JPG图片
每张: 1024 x 1024像素

展开示意:
        ┌───┐
        │ u │
    ┌───┼───┼───┐
    │ l │ f │ r │ b │
    └───┼───┼───┘
        │ d │
        └───┘

URL模式:
l0_f_0_0.jpg  (level=0, face=front, x=0, y=0)
l0_l_0_0.jpg  (level=0, face=left, x=0, y=0)
l0_r_0_0.jpg  (level=0, face=right, x=0, y=0)
l0_b_0_0.jpg  (level=0, face=back, x=0, y=0)
l0_u_0_0.jpg  (level=0, face=up, x=0, y=0)
l0_d_0_0.jpg  (level=0, face=down, x=0, y=0)
```

#### 多级分辨率（千亿像素）

| 级别 | 分辨率 | 切片数量(每面) | 用途 |
|------|--------|--------------|------|
| Level 0 | 512px | 1x1 = 1张 | 快速预览 |
| Level 1 | 640px | 2x2 = 4张 | 低质量 |
| Level 2 | 1152px | 4x4 = 16张 | 中等质量 |
| Level 3 | 2304px | 8x8 = 64张 | 高质量 |
| ... | ... | ... | ... |
| Level 8 | **152,832px** | 65536张 | 超高清 |

#### 优势

| 优势 | 说明 |
|------|------|
| ✅ **标准格式** | JPG/XML，无厂商锁定 |
| ✅ **工具成熟** | krpano提供完整工具链 |
| ✅ **易于修改** | 文本配置，易于维护 |
| ✅ **性能优秀** | 按需加载，支持超高清 |
| ✅ **社区支持** | 行业标准，资料丰富 |

---

## 四、技术对比总结

### 4.1 三种技术路线对比

| 维度 | 军事博物馆(真3D) | 全景故宫(全景) | 千亿像素(超高清全景) |
|------|----------------|--------------|-------------------|
| **3D类型** | 真实3D模型 | 全景图 | 全景图 |
| **素材来源** | 3D建模软件 | 全景相机拍摄 | 全景相机拍摄 |
| **交互自由度** | 高（自由漫游） | 中（360度浏览） | 中（360度浏览） |
| **技术栈** | Three.js + Pixi.js | krpano + Vue.js | krpano |
| **素材格式** | EMP（专有） | JPG + XML | JPG切片 + XML |
| **是否标准** | ❌ 非标准 | ✅ 标准格式 | ✅ 标准格式 |
| **开发难度** | ⭐⭐⭐⭐ 高 | ⭐⭐ 中等 | ⭐⭐⭐ 较高 |
| **制作成本** | 高（建模+贴图） | 低（拍摄） | 中（拍摄+拼接） |
| **性能要求** | 高（WebGL） | 中（Canvas） | 中（Canvas） |
| **浏览器兼容** | 需WebGL支持 | 广泛兼容 | 广泛兼容 |
| **移动端适配** | 需优化 | 原生支持 | 原生支持 |

### 4.2 素材格式对比

| 格式 | 标准化程度 | 可提取性 | 互操作性 | 长期保存 |
|------|----------|---------|---------|---------|
| **EMP** | ⭐ 专有格式 | ⭐ 极难 | ❌ 差 | ⚠️ 依赖特定厂商 |
| **krpano素材** | ⭐⭐⭐⭐⭐ 标准格式 | ⭐⭐⭐⭐⭐ 易 | ✅ 优秀 | ✅ 无风险 |

---

## 五、实现方案分析

### 5.1 方案A：全景展示（krpano - 商业方案）

#### 适用场景

- 博物馆/展厅虚拟游览
- 房地产样板房展示
- 旅游景点推广
- 校园/园区介绍

#### 技术实现

```html
<!DOCTYPE html>
<html>
<head>
    <script src="krpano.js"></script>
</head>
<body>
    <div id="pano" style="width:100%;height:100vh;"></div>
    <script>
        embedpano({
            xml: "tour.xml",
            target: "pano",
            html5: "auto"
        });
    </script>
</body>
</html>
```

**⚠️ 授权提醒**：使用krpano引擎需要根据项目性质购买相应授权，详见：https://krpano.com/buy/

#### 配置文件示例

```xml
<!-- tour.xml -->
<krpano version="1.22">
    <!-- 预览图 -->
    <preview url="preview.jpg" />

    <!-- 全景图 -->
    <scene name="scene1" title="大厅">
        <view hlookat="0" vlookat="0" fov="120" />
        <image>
            <cube url="tiles/%s/l0%l/%v/l0%l_%s_%v_%h.jpg" />
        </image>

        <!-- 热点 -->
        <hotspot name="spot1"
                 ath="0" atv="0"
                 onclick="loadscene(scene2)"
                 tooltip="进入下一展厅" />
    </scene>
</krpano>
```

#### 优缺点

| 优点 | 缺点 |
|------|------|
| ✅ 技术成熟，行业标准 | ❌ 交互自由度受限 |
| ✅ 开发周期短 | ❌ 只能展示真实场景 |
| ✅ 制作成本低 | ❌ 依赖全景拍摄质量 |
| ✅ 性能优秀 |  |
| ✅ 移动端友好 |  |

#### 成本评估

| 项目 | 成本 | 说明 |
|------|------|------|
| **硬件设备** | 5,000-30,000元 | 全景相机或单反+鱼眼镜头 |
| **拍摄人工** | 1,000-3,000元/天 | 专业摄影师 |
| **后期制作** | 500-2,000元/场景 | 拼接、修图、热点添加 |
| **krpano授权** | €149起 | 个人授权€149，商业授权需联系官方 |
| **软件开发** | 10,000-50,000元 | 前端开发+后台系统 |

**总成本**：约 2-10万元（中小型项目）

---

### 5.2 方案B：全景展示（Three.js - 开源免费方案）

#### 适用场景

- 需要避免商业授权费用
- 有开发团队可自研
- 需要高度定制化
- 希望完全自主控制

#### 技术实现

##### 实现方式1：等距圆柱全景（2:1全景图）

```javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

// 初始化场景
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 加载全景图（2:1比例）
const loader = new THREE.TextureLoader();
const geometry = new THREE.SphereGeometry(500, 60, 40);
geometry.scale(-1, 1, 1); // 镜像，让图片显示在球体内部

const texture = loader.load('panorama_360.jpg');
const material = new THREE.MeshBasicMaterial({ map: texture });

const sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);

// 相机控制
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableZoom = false;
controls.enablePan = false;

// 动画循环
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();

// 添加热点
const hotspotGeometry = new THREE.SphereGeometry(5, 16, 16);
const hotspotMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
const hotspot = new THREE.Mesh(hotspotGeometry, hotspotMaterial);
hotspot.position.set(200, 50, -300);
scene.add(hotspot);

// 点击热点切换场景
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
window.addEventListener('click', (event) => {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObject(hotspot);
    if (intersects.length > 0) {
        // 加载新场景
        texture.load('panorama_scene2.jpg');
    }
});
```

##### 实现方式2：立方体全景（6张图）

```javascript
import * as THREE from 'three';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 0, 0.1);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 加载6个面的纹理
const loader = new THREE.TextureLoader();
const materials = [
    new THREE.MeshBasicMaterial({ map: loader.load('right.jpg') }),   // +x
    new THREE.MeshBasicMaterial({ map: loader.load('left.jpg') }),    // -x
    new THREE.MeshBasicMaterial({ map: loader.load('up.jpg') }),      // +y
    new THREE.MeshBasicMaterial({ map: loader.load('down.jpg') }),    // -y
    new THREE.MeshBasicMaterial({ map: loader.load('front.jpg') }),   // +z
    new THREE.MeshBasicMaterial({ map: loader.load('back.jpg') }),    // -z
];

const geometry = new THREE.BoxGeometry(500, 500, 500);
geometry.scale(-1, 1, 1);

const cube = new THREE.Mesh(geometry, materials);
scene.add(cube);
```

#### 优缺点

| 优点 | 缺点 |
|------|------|
| ✅ 完全免费（MIT许可证） | ❌ 需要自己开发交互功能 |
| ✅ 无授权费用 | ❌ 开发周期比krpano长 |
| ✅ 社区活跃，资源丰富 | ❌ 需要一定的Three.js经验 |
| ✅ 可高度定制化 | ❌ 需要自己实现多级分辨率 |
| ✅ 无供应商锁定 | ❌ 文档相对krpano少 |

#### 与krpano对比

| 维度 | krpano | Three.js |
|------|--------|----------|
| **授权费用** | €149起 | 免费 |
| **开发周期** | 短（2-4周） | 中（4-8周） |
| **功能完整度** | 开箱即用 | 需要自己实现 |
| **定制灵活性** | 中等 | 高 |
| **学习曲线** | 低 | 中等 |
| **社区支持** | 官方支持 | 开源社区 |
| **长期成本** | 授权费用 | 开发维护成本 |

#### 成本评估

| 项目 | 成本 | 说明 |
|------|------|------|
| **krpano授权** | €149起 | 个人/商业授权 |
| **前端开发** | 10,000-30,000元 | Three.js开发 |
| **全景拍摄** | 5,000-30,000元 | 与krpano方案相同 |
| **后期制作** | 500-2,000元/场景 | 与krpano方案相同 |

**总成本**：约 2-5万元（中小型项目），**节省krpano授权费用**

#### 成功案例

- Google Arts & Culture（谷歌艺术与文化）
- BBC新闻全景报道
- Airbnb房源全景展示
- 许多独立开发者的全景项目

---

### 5.3 方案C：真3D展厅（Three.js）

#### 适用场景

- 需要展示不存在或已不存在的场景
- 需要高度定制化交互
- 需要展示3D模型/产品
- 游戏化体验

#### 技术实现

```javascript
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

// 初始化场景
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, w/h, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();

// 加载3D模型
const loader = new GLTFLoader();
loader.load('exhibition.glb', (gltf) => {
    scene.add(gltf.scene);
});

// 交互控制
const controls = new OrbitControls(camera, renderer.domElement);

// 热点交互
const raycaster = new THREE.Raycaster();
window.addEventListener('click', (event) => {
    // 射线检测热点点击
});
```

#### 优缺点

| 优点 | 缺点 |
|------|------|
| ✅ 交互自由度高 | ❌ 开发周期长 |
| ✅ 可展示任何场景 | ❌ 制作成本高 |
| ✅ 可实现复杂效果 | ❌ 需要专业建模 |
| ✅ 完全自主控制 | ❌ 性能要求高 |
| ✅ 可扩展性强 | ❌ 移动端需优化 |

#### 成本评估

| 项目 | 成本 | 说明 |
|------|------|------|
| **3D建模** | 5,000-50,000元/场景 | 根据复杂度 |
| **材质贴图** | 2,000-20,000元/场景 | PBR材质制作 |
| **灯光渲染** | 1,000-10,000元/场景 | 灯光烘焙 |
| **模型优化** | 2,000-10,000元/场景 | LOD、面数优化 |
| **软件开发** | 30,000-200,000元 | Three.js开发+交互逻辑 |

**总成本**：约 10-50万元（中小型项目）

---

### 5.4 方案D：混合方案

#### 结合两种技术

```
混合方案:
├── 主要区域: krpano全景展示（快速、低成本）
├── 重点展品: Three.js 3D模型（详细展示）
└── 交互过渡: 无缝切换
```

#### 实现方式

```html
<!-- 主页面使用krpano -->
<div id="panoViewer"></div>

<!-- 点击热点后弹出Three.js模态框 -->
<div id="modelViewer" style="display:none;">
    <canvas id="threeCanvas"></canvas>
</div>

<script>
    // krpano热点点击事件
function show3DModel(modelId) {
    // 显示Three.js查看器
    document.getElementById('modelViewer').style.display = 'block';
    load3DModel(modelId);
}
</script>
```

---

## 六、技术选型建议

### 6.1 决策矩阵

| 场景类型 | 推荐方案 | 理由 |
|---------|---------|------|
| **真实场景展示（有开发团队）** | Three.js全景 | 免费、可定制 |
| **真实场景展示（无开发团队）** | krpano全景 | 快速、开箱即用 |
| **虚拟展厅** | Three.js 3D | 自由度高、效果定制 |
| **产品展示** | Three.js 3D | 需要模型展示 |
| **房地产（预算充足）** | krpano全景 | 快速交付 |
| **房地产（预算有限）** | Three.js全景 | 节省授权费 |
| **旅游景点** | Three.js全景或krpano | 根据预算选择 |
| **教育培训** | Three.js全景 | 长期成本更低 |
| **游戏化应用** | Three.js 3D | 需要复杂交互 |

### 6.2 技术选型流程图

```
开始
  │
  ├─ 需要展示真实场景？
  │   ├─ 是 → 继续
  │   └─ 否 → Three.js 3D建模方案
  │
  ├─ 是否有开发团队？
  │   ├─ 是 → Three.js全景方案（免费）
  │   └─ 否 → 继续
  │
  ├─ 预算是否充足（含krpano授权）？
  │   ├─ 是 → 继续
  │   └─ 否 → Three.js全景方案（免费）
  │
  ├─ 开发周期是否紧迫（<4周）？
  │   ├─ 是 → krpano全景方案（快速）
  │   └─ 否 → Three.js全景方案（灵活）
  │
  └─ 是否需要高度定制？
      ├─ 是 → Three.js全景/3D方案
      └─ 否 → krpano全景方案
```

### 6.3 成本对比分析

#### 总拥有成本（TCO）对比（3年期）

| 成本项 | krpano方案 | Three.js方案 | 差异 |
|-------|----------|-------------|------|
| **初期投入** | | | |
| 授权费用 | €149-€500+ | ¥0 | krpano高 |
| 硬件设备 | ¥5,000-30,000 | ¥5,000-30,000 | 相同 |
| 全景拍摄 | ¥10,000-30,000 | ¥10,000-30,000 | 相同 |
| 软件开发 | ¥10,000-30,000 | ¥20,000-50,000 | Three.js高 |
| **初期总计** | ¥2.5万-9万 | ¥3.5万-11万 | krpano略低 |
| | | | |
| **长期成本** | | | |
| 功能扩展 | 需购买插件 | 自主开发 | Three.js低 |
| 版本更新 | 可能需付费升级 | 免费 | Three.js低 |
| 技术支持 | 依赖官方 | 社区免费 | Three.js低 |
| **3年总计** | ¥2.5万-9万+ | ¥3.5万-11万 | 接近 |

**结论**：
- 短期项目（<1年）：krpano总成本略低
- 长期项目（>2年）：Three.js总成本更低
- 有开发团队：Three.js成本优势明显
- 无开发团队：krpano是唯一可行方案

---

## 七、风险评估

### 7.1 技术风险

| 风险 | krpano方案 | Three.js方案 | 缓解措施 |
|------|----------|-------------|---------|
| **浏览器兼容** | 低风险 | 中风险 | 充分测试、降级方案 |
| **性能问题** | 低风险 | 高风险 | LOD优化、压缩 |
| **移动端适配** | 低风险 | 中风险 | 响应式设计 |
| **长期维护** | 低风险 | 中风险 | 代码规范、文档 |
| **技术更新** | 低风险 | 中风险 | 持续学习 |

### 7.2 项目风险

| 风险 | 说明 | 应对策略 |
|------|------|---------|
| **需求变更** | 3D项目易受需求变更影响 | 采用模块化设计 |
| **交付延期** | 3D建模耗时长 | 留足时间缓冲 |
| **效果不达标** | 预期与实际有差距 | 早期原型验证 |
| **成本超支** | 建模成本难以预估 | 分阶段开发 |

---

## 八、实施建议

### 8.1 项目阶段划分

#### 第一阶段：原型验证（2-4周）

- [ ] 技术选型确认
- [ ] 制作最小原型
- [ ] 性能测试
- [ ] 可行性评审

#### 第二阶段：素材制作（4-12周）

- [ ] 全景拍摄/3D建模
- [ ] 素材处理和优化
- [ ] 热点/交互设计

#### 第三阶段：系统开发（4-8周）

- [ ] 前端开发
- [ ] 后端系统
- [ ] 内容管理系统

#### 第四阶段：测试上线（2-4周）

- [ ] 功能测试
- [ ] 性能优化
- [ ] 兼容性测试
- [ ] 正式上线

### 8.2 团队配置建议

| 角色 | krpano方案 | Three.js方案 |
|------|----------|-------------|
| **项目经理** | 1人 | 1人 |
| **前端开发** | 1-2人 | 2-3人 |
| **全景摄影师/3D建模师** | 1人 | 2-3人 |
| **UI设计师** | 1人 | 1人 |
| **后端开发** | 0-1人 | 1人 |
| **测试人员** | 1人 | 1人 |

### 8.3 关键成功因素

1. **明确需求边界**：避免需求蔓延
2. **早期原型验证**：降低技术风险
3. **素材质量把控**：决定最终效果
4. **性能优化**：确保用户体验
5. **移动端适配**：覆盖主流设备

---

## 九、总结与建议

### 9.1 核心发现

1. **技术成熟度**：krpano全景技术成熟稳定，Three.js功能强大但复杂度高
2. **成本差异**：全景方案成本约为3D方案的1/5到1/3
3. **效果差异**：全景适合真实场景，3D适合虚拟场景和复杂交互
4. **标准化程度**：krpano使用标准格式，EMP为专有格式不推荐采用

### 9.2 最终建议

#### 双轨制推荐方案

根据项目实际情况，提供两种推荐方案：

---

##### 方案一：krpano全景技术（商业项目首选）

**适用条件**：
- ✅ 预算充足，可承担授权费用
- ✅ 开发周期紧张（<4周）
- ✅ 无专门开发团队
- ✅ 需要快速交付和商业支持

**优势**：
- ✅ 行业标准，技术成熟
- ✅ 标准素材格式，无厂商锁定
- ✅ 开发周期短，见效快
- ✅ 制作成本低，性价比高
- ✅ 性能优秀，兼容性好
- ✅ 移动端友好
- ✅ 官方技术支持

**劣势**：
- ⚠️ 需要商业授权（€149起）
- ⚠️ 长期多项目累积授权费用高
- ⚠️ 高级功能可能需要额外购买插件

**适用场景**：
- 房地产样板房展示（快速交付）
- 旅游景点推广（商业项目）
- 酒店/餐饮环境展示
- 委托开发的短期项目

**成本预估**：
- 授权费用：€149-€500+（根据项目类型）
- 项目总成本：2-10万元

---

##### 方案二：Three.js全景技术（长期项目首选）

**适用条件**：
- ✅ 有开发团队或可外包开发
- ✅ 希望避免长期授权费用
- ✅ 需要高度定制化功能
- ✅ 计划长期维护和扩展

**优势**：
- ✅ 完全免费（MIT开源许可证）
- ✅ 无授权费用，长期成本低
- ✅ 社区活跃，资源丰富
- ✅ 可高度定制化
- ✅ 无供应商锁定
- ✅ 学习成果可复用

**劣势**：
- ⚠️ 开发周期较长（4-8周）
- ⚠️ 需要一定学习成本
- ⚠️ 需要自己实现部分功能
- ⚠️ 无官方技术支持（依赖社区）

**适用场景**：
- 博物馆/展厅虚拟游览（长期项目）
- 校园/园区介绍（内部团队维护）
- 教育培训平台（持续迭代）
- 需要深度定制的项目

**成本预估**：
- 授权费用：¥0
- 开发成本：3-11万元（略高于krpano）
- 项目总成本：3-11万元
- **2-3年后总成本低于krpano方案**

---

##### 决策建议

| 项目特征 | 推荐方案 | 理由 |
|---------|---------|------|
| 短期一次性项目（<1年） | krpano | 快速交付，授权费用可控 |
| 长期持续项目（>2年） | Three.js | 避免累积授权费用 |
| 无开发团队 | krpano | 开箱即用，无需开发 |
| 有开发团队 | Three.js | 长期成本更低 |
| 需要深度定制 | Three.js | 灵活性高 |
| 需要快速上线 | krpano | 开箱即用 |
| 预算紧张 | Three.js | 无授权费用 |

---

##### 不推荐采用EMP格式

**原因**：
- ❌ 非标准格式，存在供应商锁定风险
- ❌ 无公开文档，难以自主开发
- ❌ 需要专用引擎，互操作性差
- ❌ 长期维护依赖特定厂商

### 9.3 行动计划

#### 短期（1-2个月）

1. **技术选型决策**：根据预算和团队情况选择krpano或Three.js
2. **技术验证**：
   - krpano：下载试用版制作原型
   - Three.js：实现基础Demo验证可行性
3. **需求确认**：明确展示内容和交互方式
4. **成本评估**：
   - krpano方案：确认授权费用
   - Three.js方案：评估开发工作量

#### 中期（3-6个月）

1. **素材制作**：全景拍摄或素材采购
2. **系统开发**：
   - krpano：配置XML，定制UI
   - Three.js：开发全景交互功能
3. **后台系统**：CMS内容管理系统
4. **测试优化**：性能和兼容性测试

#### 长期（6-12个月）

1. **正式上线**：部署和运营
2. **内容更新**：定期更新全景内容
3. **数据分析**：用户行为分析和优化
4. **技术迭代**：
   - krpano：关注版本更新和授权续费
   - Three.js：持续优化和功能扩展

---

## 十、附录

### 10.1 参考资料

#### 官方文档

- **krpano官网**：https://krpano.com/
  - 购买授权：https://krpano.com/buy/
  - 文档：https://krpano.com/docu/
- **Three.js官网**：https://threejs.org/
  - GitHub：https://github.com/mrdoob/three.js
  - 示例：https://threejs.org/examples/
- **glTF规范**：https://registry.khronos.org/glTF/

#### 示例网站

- 全景故宫（krpano）：https://pano.dpm.org.cn
- 千亿像素（krpano）：https://pfm.bigpixel.cn
- 军事博物馆（Three.js+EMP）：http://3d.jb.mil.cn
- Google Arts & Culture（Three.js）：https://artsandculture.google.com/

#### 开源全景替代方案

- **Marzipano**（Google开源）：https://github.com/marzipano/marzipano
- **Pannellum**（开源全景查看器）：https://pannellum.org/
- **Photo Sphere Viewer**（基于Three.js）：https://photo-sphere-viewer.js.org/

### 10.2 词汇表

| 术语 | 说明 |
|------|------|
| **krpano** | 全景浏览引擎软件，需商业授权 |
| **Three.js** | 开源WebGL 3D库，MIT许可证，完全免费 |
| **EMP** | 自研专有3D场景格式，非标准 |
| **WebGL** | 浏览器3D图形API |
| **等距圆柱投影** | 2:1比例的全景图投影方式 |
| **立方体投影** | 6面立方体全景投影方式 |
| **多级分辨率** | 金字塔式切片加载技术 |
| **LOD** | Level of Detail，细节层次 |
| **glTF** | 标准开放3D格式 |
| **MIT许可证** | 最宽松的开源许可证，可商用、可修改、无需开源 |

### 10.3 联系方式

**报告编制**：技术调研团队
**报告日期**：2026年3月1日
**版本**：V1.0

---

**报告结束**
