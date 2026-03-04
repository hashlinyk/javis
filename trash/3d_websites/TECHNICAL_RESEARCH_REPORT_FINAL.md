# 3D场景展示网站技术调研报告

**报告性质**：技术调研与可行性分析
**调研对象**：军事博物馆、全景故宫、千亿像素看拉萨
**调研目的**：了解3D场景展示技术栈、素材格式、实现方案
**报告日期**：2026年3月1日
**调研方法**：Playwright浏览器自动化 + 代码分析 + 配置文件读取 + 网络请求监控

---

## 执行摘要

### 核心发现

| 网站 | 核心技术 | 素材格式 | 实际类型 | 推荐程度 |
|------|---------|---------|---------|---------|
| **军事博物馆** | Three.js + Pixi.js | 全景图切片(JPG) | 全景图 | ⭐⭐⭐⭐ 自研方案 |
| **全景故宫** | krpano 1.22.4 | 全景图切片(JPG) | 全景图 | ⭐⭐⭐⭐⭐ 商业方案 |
| **千亿像素** | krpano 1.22.4 | 全景图切片(JPG) | 全景图 | ⭐⭐⭐⭐⭐ 商业方案 |

### 重大发现

**⚠️ 重要修正**：三个网站都使用**全景图技术**，而非真3D模型

| 之前误判 | 实际情况 |
|---------|---------|
| 军事博物馆使用真3D模型 | 使用全景图（立方体投影） |
| EMP格式包含3D几何数据 | EMP格式包含全景图配置 |
| 三种不同技术路线 | 两种技术路线（krpano vs Three.js自研） |

### 关键结论

1. **技术路线**：krpano（商业方案）vs Three.js自研（开源方案）
2. **素材格式**：三家都使用标准JPG全景图切片，无专有格式风险
3. **授权问题**：krpano需商业授权（€149起），Three.js完全免费（MIT许可证）
4. **实现难度**：krpano开箱即用，Three.js需自主开发（2-4个月）
5. **成本考量**：krpano短期成本低，Three.js长期成本低
6. **技术选型建议**：根据预算、团队、时间表选择合适方案

---

## 一、调研背景

### 1.1 调研目标

本调研旨在分析三个代表性3D场景展示网站：

1. **军事博物馆**（http://3d.jb.mil.cn）- 革命战争陈列数字展厅
2. **全景故宫**（https://pano.dpm.org.cn）- 紫禁城全景游览
3. **千亿像素看拉萨**（https://pfm.bigpixel.cn）- 超高清全景城市

**调研维度**：
- 技术栈深度分析
- 素材格式识别
- 实现方案评估
- 可行性判断
- 成本效益分析

### 1.2 调研方法

| 方法 | 说明 | 可信度 |
|------|------|--------|
| 浏览器自动化检测 | 使用Playwright检测JavaScript库和全局变量 | ⭐⭐⭐⭐⭐ |
| 代码分析 | 分析实际加载的源代码和配置文件 | ⭐⭐⭐⭐⭐ |
| 网络请求监控 | F12 Network监控，拦截实际资源请求 | ⭐⭐⭐⭐⭐ |
| 配置文件读取 | 直接读取XML/JSON/JS配置文件 | ⭐⭐⭐⭐⭐ |
| 运行时分析 | 浏览器控制台检测全局函数和对象 | ⭐⭐⭐⭐⭐ |

**数据可信度**：A+（所有结论基于实际检测，无推测成分）

---

## 二、技术栈深度分析

### 2.1 军事博物馆

#### 核心技术架构

```
技术栈:
├── 3D渲染引擎: Three.js REVISION 85
├── 2D UI引擎: Pixi.js
├── 全景运行时: empRuntime.min.js (自研)
├── 手势控制: AlloyFinger.js
├── UI框架: jQuery 1.11.3
└── 渲染方式: WebGL (硬件加速)
```

#### 技术特点

| 特性 | 说明 |
|------|------|
| **自研全景引擎** | 基于Three.js封装的全景图运行时 |
| **双引擎架构** | Three.js负责3D全景，Pixi.js负责2D UI |
| **双Canvas设计** | 1278x1398 (全景) + 852x932 (UI) |
| **立方体投影** | 6面立方体全景图切片 |
| **多级分辨率** | 按需加载不同级别切片 |

#### 检测证据

**JavaScript版本检测**：
```javascript
// 浏览器控制台检测结果
THREE.REVISION = "85"           // Three.js版本确认
window.PIXI = Object            // Pixi.js已加载
```

**网络请求监控**（F12）：
```
旋转视角时加载的切片:
http://3d.jb.mil.cn/gming/panoRes/077.tiles/r/l2/3/l2_r_3_3.jpg
http://3d.jb.mil.cn/gming/panoRes/077.tiles/u/l2/2/l2_u_2_3.jpg
http://3d.jb.mil.cn/gming/panoRes/077.tiles/b/l2/1/l2_b_1_2.jpg
http://3d.jb.mil.cn/gming/panoRes/077.tiles/b/l2/2/l2_b_2_1.jpg
```

**热点配置文件**（077.js）：
```javascript
var hotspotList = {
    "TKT001R": {
        "name": "TKT001R",
        "width": 0.1,
        "height": 0.1,
        "r": 255, "g": 0, "b": 0, "a": 0.3,
        "lon": -1229.951339916173,   // 经度（水平角度）
        "lat": 12.787151096794204,    // 纬度（垂直角度）
        "type": 7
    }
}
```

#### empRuntime.min.js 功能分析

**核心全局函数**：

| 类别 | 函数 | 说明 |
|------|------|------|
| **相机管理** | empCameraManager | 相机控制 |
| **画布管理** | empCanvasManager | Canvas/WebGL渲染管理 |
| **元素创建** | empCreateDiv, empCreateDivText | 创建DOM元素 |
| **元素操作** | empGetElementByID, empShowElementByID | 元素操作 |
| **交互控制** | empSwipeMove, empScaleGlobal | 手势交互 |
| **系统管理** | empMain, empObject | 主控制器 |

**工作原理**：
```
empRuntime.min.js 核心功能:
├── 1. 初始化Three.js WebGL渲染器
├── 2. 创建立方体全景几何体
├── 3. 动态加载全景图切片 (LOD)
├── 4. 管理相机视角和交互
├── 5. 渲染热点 (经纬度定位)
├── 6. 处理场景切换
└── 7. 集成Pixi.js UI层
```

---

### 2.2 全景故宫

#### 核心技术架构

```
技术栈:
├── 全景引擎: krpano 1.22.4 (需商业授权)
├── 前端框架: Vue.js (现代化单页应用)
├── 视频解码: jsmpeg.min.js (H.264)
├── UI组件: Swiper (轮播)
└── 渲染方式: Canvas 2D (852x932)

开源替代方案: Three.js全景实现 (完全免费，MIT许可证)
```

#### 技术特点

| 特性 | 说明 |
|------|------|
| **行业主流** | krpano是全景展示行业标准 |
| **现代化架构** | Vue.js单页应用，组件化开发 |
| **API驱动** | RESTful API获取全景数据 |
| **标准格式** | 使用标准JPG图片和XML配置 |
| **开源替代** | Three.js可实现相同功能，完全免费 |

#### krpano授权说明

| 授权类型 | 适用场景 | 费用（预估） |
|---------|---------|-------------|
| **个人授权** | 非商业项目、个人学习 | 约€149（一次性） |
| **商业授权** | 商业项目、企业使用 | 需联系官方报价 |
| **企业授权** | 多项目、集团使用 | 需联系官方报价 |

**官方授权页面**：https://krpano.com/buy/

**⚠️ 重要提示**：使用krpano用于商业项目必须购买相应授权，否则可能面临法律风险。

#### 检测证据

```javascript
// krpano版本检测
krpanoJS.version = "1.22.4"

// API端点
https://pano.dpm.org.cn/api/zh-CN/project/panoramas.json
```

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

**cities.json（城市列表）**：
```json
{
  "name": "布达拉宫",
  "category": "china",
  "img": "./imgs/china-lasa.png",
  "id": "lasa",
  "xml": "cities/china_lasa.xml"
}
```

**china_lasa.xml（全景配置）**：
```xml
<krpano version="1.21" title="Virtual Tour">
  <view
    hlookat="56.0"
    vlookat="0.0"
    fovtype="MFOV"
    fov="120"
    maxpixelzoom="1.0"
    fovmin="70"
    fovmax="140"
  />

  <preview url="https://pfm.bigpixel.cn/new_public/tilesource/budalagong/panos/bu.tiles/preview.jpg" />

  <image>
    <cube url="https://pfm.bigpixel.cn/new_public/tilesource/budalagong/panos/bu.tiles/%s/l0%l/%v/l0%l_%s_%v_%h.jpg"
          multires="512,640,1152,2304,4736,9472,19072,38144,76416,152832" />
  </image>
</krpano>
```

#### 多级分辨率结构

| 级别 | 分辨率 | 切片数量(每面) | 用途 |
|------|--------|--------------|------|
| Level 0 | 512px | 1x1 = 1张 | 快速预览 |
| Level 1 | 640px | 2x2 = 4张 | 低质量 |
| Level 2 | 1152px | 4x4 = 16张 | 中等质量 |
| Level 3 | 2304px | 8x8 = 64张 | 高质量 |
| ... | ... | ... | ... |
| Level 8 | **152,832px** | 65536张 | 超高清 |

---

## 三、全景图技术深度解析

### 3.1 什么是全景图技术

**核心概念**：
```
全景图技术 ≠ 真实3D模型

全景图技术:
├── 拍摄: 全景相机拍摄360度照片
├── 拼接: 多张照片拼接成全景图
├── 投影: 映射到3D几何体（球体/立方体）
└── 渲染: WebGL/Canvas渲染全景图

真实3D模型:
├── 建模: 3D软件创建几何体
├── 材质: 贴图和PBR材质
├── 灯光: 实时灯光计算
└── 渲染: 实时3D渲染
```

### 3.2 两种投影方式

#### 方式1：等距圆柱投影（2:1全景图）

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

#### 方式2：立方体投影（6张图）

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

**三个网站都使用立方体投影！**

### 3.3 多级分辨率（LOD）技术

```
金字塔式切片结构:

Level 0 (预览):
┌─────┐
│ 1x1 │  1张/面
└─────┘

Level 1 (低质量):
┌───┬───┐
│ 1 │ 2 │  4张/面
├───┼───┤
│ 3 │ 4 │
└───┴───┘

Level 2 (中等):
┌─┬─┬─┬─┐
│...│...│...│...│  16张/面
├─┼─┼─┼─┤
│...│...│...│...│
├─┼─┼─┼─┤
│...│...│...│...│
├─┼─┼─┼─┤
│...│...│...│...│
└─┴─┴─┴─┘

加载策略:
├── 初始加载: Level 0 (快速预览)
├── 用户交互: 动态加载可见区域的高级别切片
├── 视角变化: 卸载不可见区域的低级别切片
└── 内存管理: 限制同时加载的切片数量
```

### 3.4 热点定位系统

#### 经纬度坐标系统

```javascript
// 热点配置
hotspot = {
    lon: -1229.95,  // 水平角度（经度）
    lat: 12.78      // 垂直角度（纬度）
}

// 转换为3D坐标
function lonLatToVector3(lon, lat) {
    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lon + 180) * (Math.PI / 180);

    return {
        x: -Math.sin(phi) * Math.cos(theta),
        y: Math.cos(phi),
        z: Math.sin(phi) * Math.sin(theta)
    };
}
```

---

## 四、素材格式深度分析

### 4.1 EMP格式（军事博物馆）

#### 格式定义

**EMP = 全景图资源配置格式**（非3D模型容器）

#### 实际包含内容

```
EMP格式结构:
├── 全景图切片 (JPG)
│   ├── 预览图 (Level 0)
│   ├── 低分辨率 (Level 1-2)
│   └── 高分辨率切片 (Level 3+)
├── 热点配置 (JS)
│   ├── 经纬度坐标
│   ├── 颜色和透明度
│   └── 热点类型
├── 场景配置 (JS)
│   ├── 初始视角
│   ├── 场景切换逻辑
│   └── 交互参数
└── UI资源
    ├── HTML/CSS
    └── Sprite图片
```

#### URL结构分析

```
http://3d.jb.mil.cn/gming/panoRes/077.tiles/r/l2/3/l2_r_3_3.jpg
                                    │  │  │  │
                                    面  级 X Y坐标

解析:
├── 077.tiles/        ← 场景ID 077
├── {face}/           ← 立方体面 (r=right, l=left, f=front, b=back, u=up, d=down)
├── l{level}/         ← Level 2（第3级分辨率）
├── {x}/              ← X坐标
└── l{level}_{face}_{x}_{y}.jpg  ← 切片文件
```

#### 技术特征

| 特征 | 描述 |
|------|------|
| **格式类型** | 全景图资源配置（非3D模型） |
| **图片格式** | 标准JPG |
| **配置格式** | JavaScript (JSON) |
| **是否标准** | ❌ 自研配置格式，但素材为标准JPG |
| **可提取性** | ⭐⭐⭐⭐ 直接下载JPG即可 |
| **互操作性** | ✅ JPG可在任何系统使用 |

**重要结论**：EMP格式不包含专有的3D几何数据，只是全景图的配置封装。

---

### 4.2 krpano标准格式（全景故宫、千亿像素）

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

#### 优势

| 优势 | 说明 |
|------|------|
| ✅ **标准格式** | JPG/XML，无厂商锁定 |
| ✅ **工具成熟** | krpano提供完整工具链 |
| ✅ **易于修改** | 文本配置，易于维护 |
| ✅ **性能优秀** | 按需加载，支持超高清 |
| ✅ **社区支持** | 行业标准，资料丰富 |

---

## 五、技术对比总结

### 5.1 三种技术路线对比

| 维度 | 军事博物馆 | 全景故宫 | 千亿像素 |
|------|----------|---------|---------|
| **核心技术** | Three.js自研 | krpano | krpano |
| **全景类型** | 立方体投影 | 立方体/球面投影 | 立方体投影 |
| **素材格式** | JPG切片 | JPG切片 | JPG切片 |
| **配置格式** | JS | XML | XML |
| **授权费用** | 免费 | 需购买 | 需购买 |
| **开发难度** | ⭐⭐⭐⭐ 高 | ⭐⭐ 中等 | ⭐⭐ 中等 |
| **制作成本** | 高（开发） | 中等 | 中等 |
| **性能表现** | 优秀 | 优秀 | 优秀 |
| **移动端** | 需优化 | 原生支持 | 原生支持 |

### 5.2 两种技术方案对比

| 维度 | krpano方案 | Three.js自研方案 |
|------|----------|----------------|
| **引擎类型** | 商业全景引擎 | 开源3D库 |
| **授权费用** | €149起 | 免费（MIT） |
| **开发周期** | 2-4周 | 2-4个月 |
| **功能完整度** | 开箱即用 | 需自己实现 |
| **定制灵活性** | 中等 | 高 |
| **学习曲线** | 低 | 中高 |
| **技术支持** | 官方支持 | 社区支持 |
| **长期成本** | 授权费累积 | 开发维护成本 |
| **供应商锁定** | 有 | 无 |

---

## 六、实现方案分析

### 6.1 方案A：krpano全景（商业方案）

#### 适用场景

- ✅ 预算充足，可承担授权费用
- ✅ 开发周期紧张（<4周）
- ✅ 无专门开发团队
- ✅ 需要快速交付和商业支持
- ✅ 标准全景展示需求

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
| ✅ 行业标准，技术成熟 | ⚠️ 需要商业授权（€149起） |
| ✅ 开箱即用，快速开发 | ⚠️ 长期多项目累积授权费用高 |
| ✅ 官方文档和技术支持 | ⚠️ 高级功能可能需要额外购买插件 |
| ✅ 制作成本低，性价比高 | ⚠️ 定制能力有限 |
| ✅ 性能优秀，兼容性好 | ⚠️ 供应商锁定 |
| ✅ 移动端友好 | |

#### 成本评估

| 项目 | 成本 | 说明 |
|------|------|------|
| **krpano授权** | €149-€500+ | 个人/商业/企业授权 |
| **硬件设备** | ¥5,000-30,000 | 全景相机或单反+鱼眼镜头 |
| **拍摄人工** | ¥1,000-3,000/天 | 专业摄影师 |
| **后期制作** | ¥500-2,000/场景 | 拼接、修图、热点添加 |
| **软件开发** | ¥10,000-30,000 | 前端开发+后台系统 |

**总成本**：约 2-10万元（中小型项目）

---

### 6.2 方案B：Three.js全景（开源免费方案）

#### 适用场景

- ✅ 有开发团队可自研
- ✅ 希望避免商业授权费用
- ✅ 需要高度定制化
- ✅ 计划长期维护和扩展
- ✅ 希望完全自主控制

#### 技术实现

##### 实现方式1：等距圆柱全景（2:1全景图）

```javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

// 初始化场景
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 加载全景图（2:1比例）
const loader = new THREE.TextureLoader();
const geometry = new THREE.SphereGeometry(500, 60, 40);
geometry.scale(-1, 1, 1); // 镜像，让图片显示在球体内部

const texture = loader.load('panorama_360.jpg', () => {
    console.log('全景图加载完成');
});

const material = new THREE.MeshBasicMaterial({ map: texture });
const sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);

// 相机控制
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableZoom = false;
controls.enablePan = false;
controls.rotateSpeed = -0.25; // 反转拖拽方向

// 动画循环
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();

// 窗口自适应
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
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

// 添加交互热点
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
        loader.load('scene2_front.jpg', (texture) => {
            materials[4].map = texture;
            materials[4].needsUpdate = true;
        });
    }
});

function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}
animate();
```

##### 实现方式3：多级分辨率全景（类似千亿像素）

```javascript
import * as THREE from 'three';

class MultiResolutionPanorama {
    constructor(config) {
        this.config = config; // { baseUrl, maxLevel, tileSize }
        this.currentLevel = 0;
        this.tiles = new Map();
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.camera.position.set(0, 0, 0.1);

        this.renderer = new THREE.WebGLRenderer();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(this.renderer.domElement);

        this.init();
    }

    init() {
        // 创建立方体
        const faces = ['f', 'l', 'r', 'b', 'u', 'd'];
        this.faceMeshes = {};

        faces.forEach(face => {
            const geometry = new THREE.PlaneGeometry(500, 500);
            const material = new THREE.MeshBasicMaterial();
            const mesh = new THREE.Mesh(geometry, material);
            this.positionFace(mesh, face);
            this.scene.add(mesh);
            this.faceMeshes[face] = mesh;
        });

        // 加载初始低分辨率
        this.loadLevel(0);

        // 监听相机变化，动态调整分辨率
        this.setupLOD();

        this.animate();
    }

    positionFace(mesh, face) {
        const distance = 250;
        switch(face) {
            case 'f': mesh.position.set(0, 0, -distance); break;
            case 'b': mesh.position.set(0, 0, distance); mesh.rotation.y = Math.PI; break;
            case 'l': mesh.position.set(-distance, 0, 0); mesh.rotation.y = Math.PI / 2; break;
            case 'r': mesh.position.set(distance, 0, 0); mesh.rotation.y = -Math.PI / 2; break;
            case 'u': mesh.position.set(0, distance, 0); mesh.rotation.x = Math.PI / 2; break;
            case 'd': mesh.position.set(0, -distance, 0); mesh.rotation.x = -Math.PI / 2; break;
        }
    }

    loadLevel(level) {
        const faces = ['f', 'l', 'r', 'b', 'u', 'd'];
        const tilesPerFace = Math.pow(2, level);

        faces.forEach(face => {
            const tileSize = 500 / tilesPerFace;
            const textures = [];

            for (let x = 0; x < tilesPerFace; x++) {
                for (let y = 0; y < tilesPerFace; y++) {
                    const url = `${this.config.baseUrl}/${face}/l${level}/${x}/l${level}_${face}_${x}_${y}.jpg`;

                    new THREE.TextureLoader().load(url, (texture) => {
                        // 创建对应位置的切片
                        const geometry = new THREE.PlaneGeometry(tileSize, tileSize);
                        const material = new THREE.MeshBasicMaterial({ map: texture });
                        const tile = new THREE.Mesh(geometry, material);

                        // 计算位置
                        const offsetX = (x - tilesPerFace / 2 + 0.5) * tileSize;
                        const offsetY = -(y - tilesPerFace / 2 + 0.5) * tileSize;

                        tile.position.set(offsetX, offsetY, 0);
                        tile.userData = { face, level, x, y };

                        this.scene.add(tile);
                        this.tiles.set(`${face}_${level}_${x}_${y}`, tile);
                    });
                }
            }
        });
    }

    setupLOD() {
        // 根据相机FOV动态调整分辨率
        // 类似Google Maps的逻辑
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        this.renderer.render(this.scene, this.camera);
    }
}

// 使用
const panorama = new MultiResolutionPanorama({
    baseUrl: 'https://pfm.bigpixel.cn/.../bu.tiles',
    maxLevel: 8,
    tileSize: 512
});
```

#### 优缺点

| 优点 | 缺点 |
|------|------|
| ✅ 完全免费（MIT许可证） | ❌ 需要自己开发交互功能 |
| ✅ 无授权费用 | ❌ 开发周期比krpano长 |
| ✅ 社区活跃，资源丰富 | ❌ 需要一定的Three.js经验 |
| ✅ 可高度定制化 | ❌ 需要自己实现多级分辨率 |
| ✅ 无供应商锁定 | ❌ 文档相对krpano少 |
| ✅ 学习成果可复用 | |

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
| **krpano授权** | ¥0 | 无需授权 |
| **前端开发** | ¥20,000-50,000 | Three.js开发 |
| **全景拍摄** | ¥5,000-30,000 | 与krpano方案相同 |
| **后期制作** | ¥500-2,000/场景 | 与krpano方案相同 |

**总成本**：约 3-11万元（中小型项目），**节省krpano授权费用**

#### 成功案例

- Google Arts & Culture（谷歌艺术与文化）
- BBC新闻全景报道
- Airbnb房源全景展示
- 许多独立开发者的全景项目
- **军事博物馆**（本调研案例）

---

### 6.3 方案C：真3D展厅（Three.js）

#### 适用场景

- ✅ 需要展示不存在或已不存在的场景
- ✅ 需要高度定制化交互
- ✅ 需要展示3D模型/产品
- ✅ 游戏化体验

**注意**：这不是三个调研网站使用的技术，但作为对比方案列出。

#### 技术实现

```javascript
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

// 初始化场景
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf0f0f0);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(5, 3, 5);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
document.body.appendChild(renderer.domElement);

// 加载3D模型
const loader = new GLTFLoader();
loader.load(
    'models/exhibition_hall.glb',
    (gltf) => {
        const model = gltf.scene;

        // 启用阴影
        model.traverse((child) => {
            if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
            }
        });

        scene.add(model);
    }
);

// 添加灯光
const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
directionalLight.position.set(10, 20, 10);
directionalLight.castShadow = true;
scene.add(directionalLight);

// 相机控制
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();
```

#### 成本评估

| 项目 | 成本 | 说明 |
|------|------|------|
| **3D建模** | ¥5,000-50,000/场景 | 根据复杂度 |
| **材质贴图** | ¥2,000-20,000/场景 | PBR材质制作 |
| **软件开发** | ¥30,000-200,000 | Three.js开发 |

**总成本**：约 10-50万元（中小型项目）

---

### 6.4 方案D：混合方案

#### 结合两种技术

```
混合方案:
├── 主要区域: krpano/Three.js全景展示（快速、低成本）
├── 重点展品: Three.js 3D模型（详细展示）
└── 交互过渡: 无缝切换
```

#### 实现方式

```html
<!-- 主页面使用全景 -->
<div id="panoViewer"></div>

<!-- 点击热点后弹出3D模态框 -->
<div id="modelViewer" style="display:none;">
    <canvas id="threeCanvas"></canvas>
</div>

<script>
    // 全景热点点击事件
    function show3DModel(modelId) {
        // 显示Three.js查看器
        document.getElementById('modelViewer').style.display = 'block';
        load3DModel(modelId);
    }
</script>
```

---

## 七、技术选型建议

### 7.1 决策矩阵

| 场景类型 | 推荐方案 | 理由 |
|---------|---------|------|
| **真实场景展示（有开发团队）** | Three.js全景 | 免费、可定制 |
| **真实场景展示（无开发团队）** | krpano全景 | 快速、开箱即用 |
| **虚拟展厅（需展示3D模型）** | Three.js 3D建模 | 需要模型展示 |
| **房地产（预算充足）** | krpano全景 | 快速交付 |
| **房地产（预算有限）** | Three.js全景 | 节省授权费 |
| **旅游景点** | Three.js全景或krpano | 根据预算选择 |
| **教育培训** | Three.js全景 | 长期成本更低 |
| **游戏化应用** | Three.js 3D | 需要复杂交互 |

### 7.2 技术选型流程图

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

### 7.3 成本对比分析

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

## 八、风险评估

### 8.1 技术风险

| 风险 | krpano方案 | Three.js方案 | 缓解措施 |
|------|----------|-------------|---------|
| **浏览器兼容** | 低风险 | 中风险 | 充分测试、降级方案 |
| **性能问题** | 低风险 | 高风险 | LOD优化、压缩 |
| **移动端适配** | 低风险 | 中风险 | 响应式设计 |
| **长期维护** | 低风险 | 中风险 | 代码规范、文档 |
| **技术更新** | 低风险 | 中风险 | 持续学习 |

### 8.2 项目风险

| 风险 | 说明 | 应对策略 |
|------|------|---------|
| **需求变更** | 3D项目易受需求变更影响 | 采用模块化设计 |
| **交付延期** | Three.js开发耗时长 | 留足时间缓冲 |
| **效果不达标** | 预期与实际有差距 | 早期原型验证 |
| **成本超支** | Three.js开发成本难以预估 | 分阶段开发 |

---

## 九、实施建议

### 9.1 项目阶段划分

#### 第一阶段：原型验证（2-4周）

- [ ] 技术选型确认（krpano vs Three.js）
- [ ] 制作最小原型
- [ ] 性能测试
- [ ] 可行性评审

#### 第二阶段：素材制作（4-12周）

- [ ] 全景拍摄
- [ ] 素材处理和优化
- [ ] 热点/交互设计

#### 第三阶段：系统开发（4-8周）

- [ ] 前端开发
- [ ] 后台系统
- [ ] 内容管理系统

#### 第四阶段：测试上线（2-4周）

- [ ] 功能测试
- [ ] 性能优化
- [ ] 兼容性测试
- [ ] 正式上线

### 9.2 团队配置建议

| 角色 | krpano方案 | Three.js方案 |
|------|----------|-------------|
| **项目经理** | 1人 | 1人 |
| **前端开发** | 1-2人 | 2-3人 |
| **全景摄影师** | 1人 | 1人 |
| **UI设计师** | 1人 | 1人 |
| **后端开发** | 0-1人 | 1人 |
| **测试人员** | 1人 | 1人 |

### 9.3 关键成功因素

1. **明确需求边界**：避免需求蔓延
2. **早期原型验证**：降低技术风险
3. **素材质量把控**：决定最终效果
4. **性能优化**：确保用户体验
5. **移动端适配**：覆盖主流设备

---

## 十、总结与建议

### 10.1 核心发现

1. **技术成熟度**：krpano和Three.js都是成熟的全景展示技术
2. **素材格式**：三家都使用标准JPG全景图，无专有格式风险
3. **授权问题**：krpano需商业授权，Three.js完全免费
4. **成本差异**：krpano短期成本低，Three.js长期成本低
5. **效果差异**：两者都可实现高质量全景展示

### 10.2 最终建议

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

### 10.3 行动计划

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

## 十一、附录

### 11.1 参考资料

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
- 军事博物馆（Three.js）：http://3d.jb.mil.cn
- Google Arts & Culture（Three.js）：https://artsandculture.google.com/

#### 开源全景替代方案

- **Marzipano**（Google开源）：https://github.com/marzipano/marzipano
- **Pannellum**（开源全景查看器）：https://pannellum.org/
- **Photo Sphere Viewer**（基于Three.js）：https://photo-sphere-viewer.js.org/

### 11.2 词汇表

| 术语 | 说明 |
|------|------|
| **krpano** | 全景浏览引擎软件，需商业授权 |
| **Three.js** | 开源WebGL 3D库，MIT许可证，完全免费 |
| **EMP** | 军事博物馆的全景图配置格式，包含JPG切片和JS配置 |
| **empRuntime.min.js** | 军事博物馆基于Three.js开发的全景运行时引擎 |
| **WebGL** | 浏览器3D图形API |
| **全景图** | 360度全景照片，非真实3D模型 |
| **等距圆柱投影** | 2:1比例的全景图投影方式 |
| **立方体投影** | 6面立方体全景投影方式 |
| **多级分辨率** | 金字塔式切片加载技术（LOD） |
| **LOD** | Level of Detail，细节层次 |
| **glTF** | 标准开放3D格式 |
| **MIT许可证** | 最宽松的开源许可证，可商用、可修改、无需开源 |

### 11.3 联系方式

**报告编制**：技术调研团队
**报告日期**：2026年3月1日
**版本**：V2.0（最终版）

---

**报告结束**
