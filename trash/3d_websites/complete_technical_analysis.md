# 3D场景网站完整技术分析报告

## 探索完成 ✅

已完成对三个3D场景网站的技术探索和素材路径分析。

---

## 一、网站技术栈总结

### 1. 军事博物馆 (3d.jb.mil.cn)

| 技术组件 | 具体实现 |
|---------|---------|
| **核心引擎** | Pixi.js (WebGL 2D渲染引擎) |
| **自研引擎** | empRuntime.min.js (EMP格式) |
| **交互库** | AlloyFinger.js (手势识别) |
| **渲染方式** | Canvas + WebGL |
| **资源格式** | EMP (加密/压缩格式) |
| **jQuery** | 1.11.3 |

**技术特点**：
- ✅ 使用Pixi.js进行高性能WebGL渲染
- ✅ 自研EMP资源格式，可能加密
- ✅ 支持手势控制和交互
- ⚠️ 资源提取难度：高（需逆向EMP格式）

---

### 2. 全景故宫 (pano.dpm.org.cn)

| 技术组件 | 具体实现 |
|---------|---------|
| **核心引擎** | **krpano 1.22.4** (专业全景引擎) |
| **前端框架** | Vue.js |
| **视频解码** | jsmpeg.min.js |
| **UI组件** | Swiper |
| **渲染方式** | Canvas (852x932) |
| **资源格式** | 标准图片 + XML配置 |

**技术特点**：
- ✅ krpano是行业标准的全景图引擎
- ✅ 使用标准XML配置文件
- ✅ 资源可能为标准图片格式
- ✅ 资源提取难度：中

---

### 3. 千亿像素看拉萨 (pfm.bigpixel.cn)

| 技术组件 | 具体实现 |
|---------|---------|
| **核心引擎** | **krpano 1.22.4** (同全景故宫) |
| **配置文件** | cities.json + XML |
| **渲染方式** | Canvas瓦片渲染 |
| **图片格式** | 切片式全景图 |
| **资源组织** | 多城市配置 |

**技术特点**：
- ✅ 同样使用krpano引擎
- ✅ 发现配置文件路径！
- ✅ XML配置可能包含图片URL
- ✅ 资源提取难度：低-中

---

## 二、素材资源路径分析

### 千亿像素 - 已发现路径 ✅

通过`cities.json`配置文件，发现了完整的资源结构：

```json
{
  "name": "布达拉宫",
  "category": "china",
  "img": "./imgs/china-lasa.png",
  "id": "lasa",
  "xml": "cities/china_lasa.xml"  // ⭐ XML配置文件
}
```

**资源URL推测**：
- 配置文件：`https://pfm.bigpixel.cn/bigpixel_CBN/cities/china_lasa.xml`
- 图片预览：`https://pfm.bigpixel.cn/bigpixel_CBN/imgs/china-lasa.png`
- 全景切片：可能在XML中定义

---

## 三、krpano引擎资源提取方法

### 方法1：直接解析XML配置

```bash
# 1. 获取XML配置
curl https://pfm.bigpixel.cn/bigpixel_CBN/cities/china_lasa.xml

# 2. XML中通常包含：
#    - <scene> 元素定义场景
#    - <image> 元素定义全景图
#    - <cube> 或 <sphere> 定义图片类型
#    - <mobile> 内部预览图
```

### 方法2：浏览器开发者工具

```javascript
// 在浏览器控制台执行
// 查找krpano对象
if (window.krpano) {
  // 获取场景列表
  console.log(krpano.get('scenes'));

  // 获取当前场景
  console.log(krpano.get('xml.scene'));

  // 获取图片URL
  const baseUrl = krpano.get('scene[%XMLSCENE%].url');
  console.log(baseUrl);
}
```

### 方法3：网络请求抓包

1. 打开开发者工具 → Network
2. 切换场景/缩放
3. 查找图片请求（通常是.jpg, .png）
4. 分析URL规律
5. 批量下载

---

## 四、krpano全景图典型XML结构

```xml
<krpano>
  <scene name="scene1" title="场景1">
    <!-- 全景图配置 -->
    <image>
      <cube url="tiles/face_%s.jpg" />  <!-- 六面体 -->
      <!-- 或 -->
      <sphere url="tiles/pano_%v_%h.jpg" />  <!-- 球体 -->
    </image>

    <!-- 预览图 -->
    <preview url="preview.jpg" />

    <!-- 缩略图 -->
    <thumb url="thumb.jpg" />
  </scene>
</krpano>
```

---

## 五、素材下载建议

### 最容易提取：千亿像素看拉萨 ✅

**步骤**：
1. 访问 `https://pfm.bigpixel.cn/bigpixel_CBN/cities/china_lasa.xml`
2. 解析XML，找到图片URL
3. 下载高清切片
4. 使用krpano工具或其他全景查看器查看

**预期资源**：
- 预览图：`https://pfm.bigpixel.cn/bigpixel_CBN/imgs/china-lasa.png`
- 全景切片：可能在XML中定义为tiles/xxx.jpg
- 配置文件：china_lasa.xml

### 中等难度：全景故宫

**挑战**：
- 使用Vue.js单页应用
- 可能有API鉴权
- 资源可能分片加载

**方法**：
1. Network面板筛选图片请求
2. 查找krpano相关请求
3. 定位XML配置
4. 提取图片URL

### 高难度：军事博物馆

**挑战**：
- 使用自研EMP格式（可能加密）
- empRuntime.min.js混淆
- 资源动态解密

**方法**：
1. 逆向分析empRuntime.js
2. 找到解密函数
3. 提取加密密钥/算法
4. 编写解密脚本

---

## 六、技术实现建议

### 如果要实现类似3D场景网站

#### 方案1：krpano（推荐全景）

**优点**：
- 行业标准，成熟稳定
- 配置灵活（XML驱动）
- 跨平台支持好
- 文档丰富

**缺点**：
- 商业授权费用
- 定制开发需要学习XML

**适用场景**：房地产全景、旅游景点、虚拟展厅

#### 方案2：Three.js（推荐3D模型）

**优点**：
- 开源免费
- 功能强大
- 社区活跃
- 可定制性高

**缺点**：
- 学习曲线陡
- 性能优化需要经验

**适用场景**：3D产品展示、游戏、交互式可视化

#### 方案3：Pixi.js（推荐2D/伪3D）

**优点**：
- 性能优秀（WebGL加速）
- API简单易用
- 文件体积小

**缺点**：
- 主要用于2D
- 3D功能有限

**适用场景**：虚拟展厅、互动展示、H5营销页面

---

## 七、下一步行动

1. ✅ 技术栈分析完成
2. ⏳ 解析拉萨XML配置文件
3. ⏳ 提取全景图切片URL
4. ⏳ 尝试下载素材
5. ⏳ 编写自动化下载脚本

---

**报告完成时间**：2026-03-01
**状态**：技术分析完成，素材提取进行中
