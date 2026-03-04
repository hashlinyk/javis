# 3D场景网站技术探索报告

## 一、探索目标

探索以下三个3D场景网站，分析技术栈并尝试下载素材：
1. **军事博物馆**：http://3d.jb.mil.cn/gming/index.html#
2. **全景故宫**：https://pano.dpm.org.cn/#/
3. **千亿像素看拉萨**：https://pfm.bigpixel.cn/bigpixel_CBN/gigapixel_cities_v2.html?category=china

---

## 二、技术分析

### 1️⃣ 军事博物馆（革命战争陈列数字展厅）

#### 技术栈

| 技术 | 说明 |
|------|------|
| **核心技术** | **Pixi.js** ✅ |
| 辅助库 | jQuery 1.11.3, AlloyFinger (手势控制) |
| 引擎 | empRuntime.min.js (自研引擎) |
| 渲染 | Canvas 2D + WebGL |
| 资源格式 | 自定义EMP格式 |

#### 关键发现

```javascript
// 核心脚本加载顺序
[
  "jquery-1.11.3.js",
  "empRuntime.min.js",        // 自研运行时
  "PIXI.js",                  // Pixi.js渲染引擎
  "AlloyFinger.js",           // 手势识别
  "empMain.js",               // 主逻辑
  "empCanvas.js",             // Canvas封装
  "empImage.js",              // 图片处理
  "canvasCtrls.js"            // 控制器
]
```

#### 技术特点

- ✅ **Pixi.js**：高性能2D WebGL渲染引擎
- ✅ **自研引擎**：EMP格式，可能是加密的资源包
- ✅ **Canvas + WebGL**：硬件加速渲染
- ✅ **手势控制**：支持移动端触摸交互

#### 资源结构

```
http://3d.jb.mil.cn/
├── empcommon/           # 公共资源
│   ├── empRuntime.min.js
│   └── jquery-1.11.3.js
├── gming/
│   ├── 2d/
│   │   ├── libs/PIXI.js
│   │   ├── js/canvas/
│   │   └── config/
│   └── css/
└── 资源文件（可能为加密的EMP格式）
```

---

### 2️⃣ 全景故宫（pano.dpm.org.cn）

#### 技术栈

| 技术 | 说明 |
|------|------|
| **核心技术** | **krpano.js** ✅ |
| 视频解码 | jsmpeg.min.js |
| UI框架 | Vue.js (chunk-vendors, app) |
| 轮播 | swiper.min.js |
| 渲染 | Canvas (852x932) |

#### 关键发现

```javascript
// 核心脚本
[
  "swiper.min.js",              // UI轮播
  "krpano.js",                  // ⭐ krpano全景引擎
  "jsmpeg.min.js",              // 视频解码
  "chunk-vendors.d0502170.js",  // Vue.js
  "app.216ecc9c.js"             // Vue应用
]
```

#### 技术特点

- ✅ **krpano**：专业的全景图引擎
- ✅ **Vue.js**：现代化前端框架
- ✅ **Canvas渲染**：单Canvas (852x932)
- ✅ **H5视频**：支持视频嵌入
- ✅ **响应式**：适配多端

#### krpano引擎简介

**krpano** 是一个强大的全景图查看引擎：
- 支持360°全景图和全景视频
- XML配置驱动
- 支持热点、导航、自动旋转
- 跨平台（Web、移动端）

---

### 3️⃣ 千亿像素看拉萨

#### 探索中...

页面加载较慢，需要进一步分析。

初步判断：
- 可能使用**Deep Zoom**或**金字塔图片**技术
- 支持超大分辨率图片的流式加载
- 可能使用WebGL或Canvas瓦片渲染

---

## 三、技术对比总结

| 网站 | 核心技术 | 渲染方式 | 应用场景 |
|------|---------|---------|---------|
| **军事博物馆** | Pixi.js | WebGL | 虚拟展厅、互动展示 |
| **全景故宫** | krpano | Canvas | 全景漫游、文化遗址 |
| **千亿像素** | 待确认 | 待确认 | 超高清图片浏览 |

---

## 四、素材下载尝试

### 军事博物馆

**挑战**：
- 使用**自研EMP格式**，可能加密
- 资源通过AJAX动态加载
- 需要逆向分析empRuntime.js

**可能方案**：
1. 浏览器开发者工具 → Network → 查找资源请求
2. 分析EMP格式解密逻辑
3. 提取Canvas截图或使用录屏

### 全景故宫

**机会**：
- krpano使用标准XML配置
- 全景图可能是标准图片格式（jpg/png）

**可能方案**：
1. 查找krpano XML配置文件
2. 定位全景图资源URL
3. 直接下载高清切片

### 千亿像素

**机会**：
- 瓦片式加载，可能有公开API
- 图片URL可能有规律

**可能方案**：
1. 分析瓦片URL模式
2. 批量下载瓦片
3. 拼接成完整图片

---

## 五、下一步行动

1. ✅ 已完成初步技术分析
2. ⏳ 待深入分析资源加载机制
3. ⏳ 尝试提取/下载3D素材
4. ⏳ 编写素材提取脚本

---

**更新时间**：2026-03-01
**状态**：进行中
