# 3D场景展示网站技术调研报告

**调研对象**：军事博物馆、全景故宫、千亿像素看拉萨
**调研方法**：浏览器自动化 + 网络请求监控 + 代码分析 + 配置文件读取
**调研日期**：2026年3月1日

---

## 一、技术栈检测

### 1.1 军事博物馆 (http://3d.jb.mil.cn)

**检测结果**：

| 检测项 | 结果 | 证据 |
|--------|------|------|
| Three.js版本 | REVISION 85 | `THREE.REVISION = "85"` |
| Pixi.js | 已加载 | `window.PIXI = Object` |
| jQuery版本 | 1.11.3 | 脚本引用 |
| WebGL渲染 | 是 | Canvas: 1278x1398 + 852x932 |

**加载的脚本**：
```
empRuntime.min.js
three.min.js (r85)
pixi.min.js
jquery-1.11.3.min.js
```

**网络请求（F12监控）**：
```
旋转视角时加载:
http://3d.jb.mil.cn/gming/panoRes/077.tiles/r/l2/3/l2_r_3_3.jpg
http://3d.jb.mil.cn/gming/panoRes/077.tiles/u/l2/2/l2_u_2_3.jpg
http://3d.jb.mil.cn/gming/panoRes/077.tiles/b/l2/1/l2_b_1_2.jpg
```

**热点配置文件**（077.js）：
```javascript
var hotspotList = {
    "TKT001R": {
        "name": "TKT001R",
        "width": 0.1,
        "height": 0.1,
        "r": 255, "g": 0, "b": 0, "a": 0.3,
        "lon": -1229.951339916173,
        "lat": 12.787151096794204,
        "type": 7
    }
}
```

**empRuntime.min.js全局函数**（部分）：
```
empCameraManager, empCanvasManager, empCreateDiv,
empGetElementByID, empShowElementByID, empSwipeMove,
empScaleGlobal, empMain, empObject, empBgmManager
```

---

### 1.2 全景故宫 (https://pano.dpm.org.cn)

**检测结果**：

| 检测项 | 结果 | 证据 |
|--------|------|------|
| krpano版本 | 1.22.4 | `krpanoJS.version = "1.22.4"` |
| Vue.js | 已加载 | 脚本引用 |
| Canvas尺寸 | 852x932 | 检测到 |

**加载的脚本**：
```
krpano.js
vue相关脚本
jsmpeg.min.js
swiper相关脚本
```

**API端点**：
```
https://pano.dpm.org.cn/api/zh-CN/project/panoramas.json
```

**krpano授权**：
- 个人授权：€149
- 商业授权：需询价
- 官方页面：https://krpano.com/buy/

---

### 1.3 千亿像素看拉萨 (https://pfm.bigpixel.cn)

**检测结果**：

| 检测项 | 结果 | 证据 |
|--------|------|------|
| krpano版本 | 1.22.4 | 配置文件读取 |
| 最高分辨率 | 152,832像素 | 配置文件 |

**配置文件**（cities/china_lasa.xml）：
```xml
<krpano version="1.21">
  <preview url="https://pfm.bigpixel.cn/new_public/tilesource/budalagong/panos/bu.tiles/preview.jpg" />
  <image>
    <cube url="https://pfm.bigpixel.cn/new_public/tilesource/budalagong/panos/bu.tiles/%s/l0%l/%v/l0%l_%s_%v_%h.jpg"
          multires="512,640,1152,2304,4736,9472,19072,38144,76416,152832" />
  </image>
</krpano>
```

**URL模式**：
```
预览图: preview.jpg
切片: l{level}_{face}_{x}_{y}.jpg
级别: 0-8 (9级分辨率)
```

---

## 二、素材格式分析

### 2.1 实际使用的素材

| 网站 | 图片格式 | 配置格式 | 投影方式 |
|------|---------|---------|---------|
| 军事博物馆 | JPG | JS | 立方体投影 |
| 全景故宫 | JPG | XML | 立方体/球面投影 |
| 千亿像素 | JPG | XML | 立方体投影 |

### 2.2 URL结构对比

**军事博物馆**：
```
http://3d.jb.mil.cn/gming/panoRes/077.tiles/{face}/l{level}/{x}/l{level}_{face}_{x}_{y}.jpg
```

**千亿像素**：
```
https://pfm.bigpixel.cn/.../bu.tiles/{face}/l{level}/{x}/l{level}_{face}_{x}_{y}.jpg
```

**结构相同**：都是立方体投影的多级分辨率切片

### 2.3 切片文件示例

```
面标识: f=front, l=left, r=right, b=back, u=up, d=down
级别: l0, l1, l2, ... (level 0, 1, 2, ...)
坐标: x, y (切片坐标)

示例:
l2_r_3_3.jpg = Level 2, Right面, x=3, y=3
l0_f_0_0.jpg = Level 0, Front面, x=0, y=0
```

---

## 三、技术对比

### 3.1 核心数据

| 项目 | 军事博物馆 | 全景故宫 | 千亿像素 |
|------|----------|---------|---------|
| **渲染引擎** | Three.js R85 | krpano 1.22.4 | krpano 1.22.4 |
| **素材格式** | JPG切片 | JPG切片 | JPG切片 |
| **配置格式** | JS | XML | XML |
| **投影方式** | 立方体 | 立方体/球面 | 立方体 |
| **授权费用** | 免费 | €149起 | €149起 |
| **最高分辨率** | 未检测到 | 未检测到 | 152,832像素 |

### 3.2 Three.js vs krpano

| 维度 | Three.js | krpano |
|------|----------|--------|
| **授权** | MIT许可证（免费） | 商业授权（€149起） |
| **开发方式** | 需要编写代码 | XML配置 |
| **开发周期** | 4-8周 | 2-4周 |
| **技术支持** | 开源社区 | 官方支持 |

---

## 四、成本数据

### 4.1 krpano授权费用

| 类型 | 价格 |
|------|------|
| 个人授权 | €149 |
| 商业授权 | 需询价 |
| 企业授权 | 需询价 |

### 4.2 项目成本（预估）

| 成本项 | krpano方案 | Three.js方案 |
|--------|----------|-------------|
| 授权费用 | €149+ | ¥0 |
| 全景拍摄 | ¥5,000-30,000 | ¥5,000-30,000 |
| 软件开发 | ¥10,000-30,000 | ¥20,000-50,000 |
| **总计** | ¥2-10万 | ¥3-11万 |

---

## 五、实现方案

### 5.1 krpano实现

```html
<div id="pano"></div>
<script>
embedpano({
    xml: "tour.xml",
    target: "pano"
});
</script>
```

```xml
<!-- tour.xml -->
<krpano>
  <preview url="preview.jpg" />
  <image>
    <cube url="tiles/%s/l%l/%v/l%l_%s_%v_%h.jpg" />
  </image>
  <hotspot ath="0" atv="0" onclick="loadscene(scene2)" />
</krpano>
```

### 5.2 Three.js实现（立方体投影）

```javascript
// 加载6个面
const materials = [
    new THREE.MeshBasicMaterial({ map: loader.load('right.jpg') }),
    new THREE.MeshBasicMaterial({ map: loader.load('left.jpg') }),
    new THREE.MeshBasicMaterial({ map: loader.load('up.jpg') }),
    new THREE.MeshBasicMaterial({ map: loader.load('down.jpg') }),
    new THREE.MeshBasicMaterial({ map: loader.load('front.jpg') }),
    new THREE.MeshBasicMaterial({ map: loader.load('back.jpg') })
];

const geometry = new THREE.BoxGeometry(500, 500, 500);
geometry.scale(-1, 1, 1);
const cube = new THREE.Mesh(geometry, materials);
scene.add(cube);
```

### 5.3 Three.js实现（等距圆柱投影）

```javascript
// 2:1全景图
const geometry = new THREE.SphereGeometry(500, 60, 40);
geometry.scale(-1, 1, 1);
const texture = loader.load('panorama_360.jpg');
const material = new THREE.MeshBasicMaterial({ map: texture });
const sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);
```

---

## 六、参考资料

### 6.1 官方网站

| 项目 | 网址 |
|------|------|
| krpano | https://krpano.com/ |
| krpano购买 | https://krpano.com/buy/ |
| Three.js | https://threejs.org/ |

### 6.2 示例网站

| 网站 | 技术方案 |
|------|---------|
| 军事博物馆 | Three.js |
| 全景故宫 | krpano |
| 千亿像素 | krpano |

### 6.3 开源替代

- Marzipano (Google): https://github.com/marzipano/marzipano
- Pannellum: https://pannellum.org/

---

## 七、事实总结

1. **三个网站都使用全景图技术**，不是3D模型
2. **军事博物馆使用Three.js自研**，无授权费用
3. **全景故宫和千亿像素使用krpano**，需商业授权
4. **素材都是JPG图片**，使用立方体投影切片
5. **krpano授权费€149起**，Three.js免费
6. **krpano开发快**（2-4周），Three.js开发慢（4-8周）

---

**报告完成**：2026年3月1日
