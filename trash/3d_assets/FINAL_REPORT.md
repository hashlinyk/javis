# 全景图素材爬取 - 最终完成报告

**任务完成日期**：2026年3月1日
**状态**：部分成功

---

## ✅ 已完成工作

### 1. 逆向分析
- ✅ 分析了 `empRuntime.min.js` 的作用
- ✅ 识别了三个网站的URL结构模式
- ✅ 确认了素材类型（全景图JPG切片）

### 2. 编写爬虫脚本
- ✅ 创建了 `panorama_downloader.py`（完整版）
- ✅ 创建了 `download_all.py`（军事博物馆专用）
- ✅ 创建了 `download_correct.py`（修正URL结构）

### 3. 执行下载
- ✅ 军事博物馆：场景077部分切片
- ✅ 全景故宫：场景3224_summer部分切片
- ✅ 千亿像素：布达拉宫预览图和部分切片

---

## 📊 最终成果

### 下载统计

| 网站 | 成功下载 | 总计 | 成功率 |
|------|---------|------|--------|
| **军事博物馆** | 61个 | 127个 | 48% |
| **全景故宫** | 50+个 | 200+个 | ~25% |
| **千亿像素** | 49+个 | 127个 | ~39% |
| **总计** | **160个文件** | - | - |

### 已下载资源

```
F:/workspace/3d_assets/
├── military_museum/077/
│   ├── 077.js (热点配置) ✓
│   └── tiles/ (61个JPG切片) ✓
├── forbidden_city/3224_summer/
│   ├── l/ (左面切片) ✓
│   ├── r/ (右面切片) ✓
│   ├── f/ (前面切片) ✓
│   ├── b/ (后面切片) ✓
│   ├── u/ (上面切片) ✓
│   └── d/ (下面切片) ✓
└── bigpixel_lasa/
    ├── preview.jpg (预览图) ✓
    └── tiles/ (49个JPG切片) ✓
```

---

## 📝 技术发现

### URL结构模式

#### 全景故宫
```
https://pano.dpm.org.cn/panoramas/61/krpano/panos/3224_summer.tiles/{face}/l{level}/{x}/l{level}_{face}_{x}_{y}.jpg

示例: l2_l_02_02.jpg (Level 2, Left, x=02, y=02)
```

#### 千亿像素
```
https://pfm.bigpixel.cn/new_public/tilesource/budalagong/panos/bu.tiles/{face}/l{level}/{x}/l{level}_{face}_{x}_{y}.jpg

示例: l03_l_2_4.jpg (Level 03, Left, x=2, y=4)
```

#### 军事博物馆
```
http://3d.jb.mil.cn/gming/panoRes/077.tiles/{face}/l{level}/{x}/l{level}_{face}_{x}_{y}.jpg

示例: l2_r_3_3.jpg (Level 2, Right, x=3, y=3)
```

### 服务器防护机制

| 网站 | 防护类型 | 返回状态 | 绕过难度 |
|------|---------|---------|---------|
| 军事博物馆 | URL结构验证 | 404 | 中等 |
| 全景故宫 | Referer检查 | 403 | 较难 |
| 千亿像素 | 频率限制 | 503 | 中等 |

---

## 🎯 素材类型确认

**重要澄清**：三个网站使用的都是**全景图技术**，而非真实3D模型。

| 网站 | 素材类型 | 投影方式 |
|------|---------|---------|
| 军事博物馆 | 全景图切片（JPG） | 立方体投影 |
| 全景故宫 | 全景图切片（JPG） | 立方体投影 |
| 千亿像素 | 全景图切片（JPG） | 立方体投影 |

**渲染引擎**：
- 军事博物馆：Three.js + Pixi.js
- 全景故宫/千亿像素：krpano 1.22.4

---

## 📄 交付文档

1. **技术调研报告**
   - `F:/workspace/3d_websites/TECHNICAL_RESEARCH_REPORT_FACTS.md`
   - 纯事实版本，面向领导汇报

2. **下载总结报告**
   - `F:/workspace/3d_assets/DOWNLOAD_SUMMARY.md`
   - 详细的技术分析和下载说明

3. **爬虫脚本**
   - `F:/workspace/3d_assets/download_correct.py`
   - 可复用的下载工具

4. **已下载素材**
   - `F:/workspace/3d_assets/`
   - 160个全景图JPG切片文件

---

## 💡 如需完整素材

### 方法1：浏览器拦截（推荐）

在实际浏览网站时，使用浏览器拦截网络请求：

```javascript
// 在浏览器控制台运行
const urls = [];
const originalOpen = XMLHttpRequest.prototype.open;
XMLHttpRequest.prototype.open = function(method, url) {
    if (url.includes('.jpg')) {
        urls.push(url);
        console.log('Found:', url);
    }
    return originalOpen.apply(this, arguments);
};

// 导出URL列表
console.log(urls.join('\n'));
```

### 方法2：联系官方

- **全景故宫**：pano@dpm.org.cn
- **千亿像素**：通过官网联系
- **军事博物馆**：通过官网渠道

### 方法3：使用krpano工具

krpano提供官方下载工具，需要购买授权后使用。

---

**任务状态**：技术分析完成，素材部分下载成功
**建议**：完整素材需通过官方渠道或浏览器拦截获取
