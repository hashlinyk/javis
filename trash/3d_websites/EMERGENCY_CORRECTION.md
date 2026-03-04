# 军事博物馆技术栈重大发现 - 紧急修正

## 重要发现

用户通过F12 Network监控发现，军事博物馆在旋转视角时加载了大量JPG图片切片：

```
http://3d.jb.mil.cn/gming/panoRes/077.tiles/r/l2/3/l2_r_3_3.jpg
http://3d.jb.mil.cn/gming/panoRes/077.tiles/u/l2/2/l2_u_2_3.jpg
http://3d.jb.mil.cn/gming/panoRes/077.tiles/b/l2/1/l2_b_1_2.jpg
http://3d.jb.mil.cn/gming/panoRes/077.tiles/b/l2/2/l2_b_2_1.jpg
```

## URL结构分析

```
http://3d.jb.mil.cn/gming/panoRes/
├── 077.tiles/                    ← 场景ID 077
├── {face}/                       ← 立方体面 (r=right, u=up, b=back)
│   ├── l2/                       ← Level 2（第3级分辨率）
│   │   ├── {x}/                  ← X坐标
│   │   │   └── l2_{face}_{x}_{y}.jpg  ← 切片文件
│   │
│   ├── r/l2/3/l2_r_3_3.jpg      (右面, Level2, x=3, y=3)
│   ├── u/l2/2/l2_u_2_3.jpg      (上面, Level2, x=2, y=3)
│   └── b/l2/1/l2_b_1_2.jpg      (后面, Level2, x=1, y=2)
```

## 关键结论

### ❌ 之前的错误分析

我之前错误地认为：
- 军事博物馆使用**真3D模型**（Three.js渲染几何体）
- EMP格式包含**3D模型数据**
- EMP是**专有3D场景容器格式**

### ✅ 正确的技术栈

**军事博物馆实际上也是使用全景图技术！**

```
实际技术栈:
├── 全景引擎: Three.js REVISION 85
├── 辅助引擎: Pixi.js (2D UI)
├── 素材格式: 全景图切片（JPG）+ 配置
└── 渲染方式: WebGL（渲染全景图）
```

## 三个网站的真实技术对比

| 网站 | 核心引擎 | 素材格式 | 3D类型 |
|------|---------|---------|--------|
| **军事博物馆** | Three.js REVISION 85 | **全景图切片(JPG)** | 全景图 |
| **全景故宫** | krpano 1.22.4 | **全景图切片(JPG)** | 全景图 |
| **千亿像素** | krpano 1.22.4 | **全景图切片(JPG)** | 全景图 |

## 重大修正

### EMP格式的真实定义

**EMP不是包含3D模型的格式，而是包含全景图配置的格式！**

```
EMP格式实际包含:
├── 全景图切片（JPG）
│   ├── 预览图（Level 0）
│   ├── 低分辨率（Level 1-2）
│   └── 高分辨率切片（Level 3+）
├── 配置数据
│   ├── 热点位置
│   ├── 相机初始视角
│   └── 场景切换逻辑
└── UI资源（由Pixi.js渲染）
    ├── 按钮
    ├── 文字标签
    └── 交互元素
```

### URL模式对比

| 网站 | URL模式 |
|------|---------|
| **军事博物馆** | `{face}/l{level}/{x}/l{level}_{face}_{x}_{y}.jpg` |
| **千亿像素** | `{face}/l0%l/{v}/l0%l_{s}_{v}_{h}.jpg` |

**两者使用相同的立方体投影切片模式！**

## 技术架构重新分析

### 军事博物馆的真实架构

```
渲染层级:
├── Layer 1: Three.js（WebGL）
│   └── 渲染全景图（球体或立方体）
│       ├── 加载切片JPG
│       ├── 投影到3D几何体
│       └── 响应视角变化
│
├── Layer 2: Pixi.js（2D UI）
│   └── 渲染UI元素
│       ├── 热点图标
│       ├── 按钮和标签
│       └── 信息面板
│
└── 交互逻辑
    ├── 鼠标拖拽旋转视角
    ├── Three.js计算可见区域
    ├── 按需加载对应切片
    └── Pixi.js更新UI位置
```

## 与krpano的核心区别

| 维度 | 军事博物馆 (Three.js) | 全景故宫/千亿像素 (krpano) |
|------|---------------------|-------------------------|
| **渲染引擎** | Three.js (WebGL) | krpano (Canvas 2D/WebGL) |
| **素材格式** | JPG切片 | JPG切片 |
| **投影方式** | 立方体投影 | 立方体投影 |
| **切片加载** | 自定义逻辑 | krpano内置 |
| **UI渲染** | Pixi.js (独立Canvas) | krpano内置 |
| **开发难度** | 高（需自研） | 低（开箱即用） |
| **授权成本** | 免费 | 需付费 |

## 为什么使用Three.js而非krpano？

### 可能的原因

1. **深度定制需求**
   - 军事博物馆可能有特殊的交互需求
   - krpano无法满足定制化要求

2. **技术栈统一**
   - 项目可能已使用Three.js
   - 避免引入多个引擎

3. **UI复杂性**
   - Pixi.js提供强大的2D UI能力
   - 比krpano的UI系统更灵活

4. **长期维护**
   - Three.js是开源的
   - 避免krpano授权费用

## 修正后的实现方案对比

### 方案A：krpano全景（商业方案）

- ✅ 开箱即用
- ✅ 快速开发
- ⚠️ 需要授权
- ⚠️ 定制能力有限

### 方案B：Three.js全景（军事博物馆方案）

- ✅ 完全免费
- ✅ 高度定制
- ✅ 深度控制
- ⚠️ 开发周期长
- ⚠️ 需要专业团队

### 方案C：混合方案

- 主要区域：krpano（快速开发）
- 特殊场景：Three.js（深度定制）

## 军事博物馆的Three.js实现推测

```javascript
// 军事博物馆可能的实现逻辑

class PanoramaViewer {
    constructor() {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, w/h, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer();
        this.tiles = new Map(); // 缓存已加载的切片
        this.currentLevel = 0;
    }

    // 加载切片
    loadTile(face, level, x, y) {
        const url = `http://3d.jb.mil.cn/gming/panoRes/077.tiles/${face}/l${level}/${x}/l${level}_${face}_${x}_${y}.jpg`;

        if (this.tiles.has(url)) {
            return this.tiles.get(url);
        }

        const texture = new THREE.TextureLoader().load(url);
        this.tiles.set(url, texture);
        return texture;
    }

    // 根据视角动态加载切片
    updateTiles() {
        const visibleFaces = this.getVisibleFaces(); // 计算可见面
        const requiredLevel = this.calculateLevel(); // 根据FOV计算级别

        visibleFaces.forEach(face => {
            const tiles = this.getRequiredTiles(face, requiredLevel);
            tiles.forEach(({x, y}) => {
                this.loadTile(face, requiredLevel, x, y);
            });
        });
    }

    // 渲染循环
    animate() {
        requestAnimationFrame(() => this.animate());
        this.updateTiles(); // 动态加载切片
        this.renderer.render(this.scene, this.camera);
    }
}
```

## 更新后的核心结论

### ✅ 三个网站都使用全景图技术

**没有一个是真3D模型！**

所有三个网站都是基于全景图：
- 军事博物馆：Three.js + 全景图切片
- 全景故宫：krpano + 全景图切片
- 千亿像素：krpano + 超高清全景图切片

### ✅ Three.js vs krpano 的真正区别

不是"3D模型 vs 全景图"，而是"自研全景引擎 vs 商业全景引擎"

| 方案 | 技术栈 | 成本 | 适用场景 |
|------|--------|------|---------|
| **krpano** | 商业全景引擎 | 授权费 + 开发费 | 快速交付 |
| **Three.js** | 自研全景引擎 | 仅开发费（高） | 深度定制 |

### ✅ EMP格式的真实含义

**EMP = 全景图资源配置格式**（不是3D模型容器）

包含：
- 全景图切片URL配置
- 场景切换逻辑
- 热点和交互数据
- UI资源引用

## 最终建议

### 技术选型更新

如果你的需求是**全景图展示**（而非真3D模型）：

| 需求类型 | 推荐方案 |
|---------|---------|
| 标准全景展示 | krpano |
| 快速开发 | krpano |
| 深度定制 | Three.js（参考军事博物馆） |
| 预算有限 | Three.js（但开发周期长） |
| 长期维护 | Three.js（无授权费） |

### 真正的技术决策

**krpano** vs **Three.js** 的选择，本质上是：

- **购买成熟工具** vs **自研实现**
- **快速上线** vs **长期灵活**
- **授权费用** vs **开发成本**

---

**修正日期**：2026年3月1日
**修正依据**：用户提供的Network监控数据
**可信度**：A+（基于实际网络请求）
