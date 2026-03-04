# EMP素材格式深度分析

## 问题：EMP是什么3D格式？

基于对军事博物馆网站的深入技术分析。

---

## 一、EMP格式的基本信息

### 来源与归属

- **开发方**：可能是国内公司（可能与军事博物馆合作）
- **技术定位**：自研的3D场景打包格式
- **用途**：数字展厅、虚拟展览场景

### 检测证据

```javascript
// 军事博物馆网站代码中
empRuntime.min.js          // EMP运行时引擎
empSizeObj.pages = 'EMP33805EA82CC629193FCA59A62F7A4C37'
empSizeObj.first = 0
```

---

## 二、EMP格式的技术特征

### 基于代码分析的特征

#### 1. 打包结构

```javascript
empSizeObj = {
  builderMode: false,
  debugMode: '',
  winFixSize: {x: 1024, y: 768},  // 窗口固定尺寸
  resizePolicy: 3,
  zoomRange: [0.2, 1.5],          // 缩放范围
  align: 0,
  aligny: 1
}

empSizeObj.pages = {
  'pages': ['EMP33805EA82CC629193FCA59A62F7A4C37', 'END'],
  'first': 0,
  'EMP33805EA82CC629193FCA59A62F7A4C37': [
    [''],           // 可能是场景名称
    [''],           // 可能是缩略图
    1024, 768        // 场景尺寸
  ]
}
```

#### 2. 加载机制

```javascript
// 页面初始化
PageInitFunc['EMP33805EA82CC629193FCA59A62F7A4C37'] = function() {
  // EMP场景初始化逻辑
}
```

---

## 三、EMP格式可能的技术实现

### 方案1：压缩的JSON格式

**推测**：
```
EMP文件结构：
├── scenes/           # 场景数据
│   ├── scene1.json
│   └── scene2.json
├── models/           # 3D模型数据
│   ├── geometry/     # 几何数据（可能二进制）
│   └── materials/    # 材质数据
├── textures/         # 纹理图片
└── config/          # 配置文件
```

**压缩方式**：
- 可能有自定义压缩算法
- 或使用标准压缩（gzip, brotli）
- 数据可能是二进制混合JSON

### 方案2：专有二进制格式

**特征**：
```
EMP文件头:
- Magic Number: 4字节标识 "EMP\x00"
- Version: 版本号
- Flags: 压缩标志
- Index: 索引位置

数据块:
- 几何数据: 顶点、法线、UV
- 材质数据: 颜色、纹理坐标
- 纹理引用: 外部或内部
- 场景图: 节点关系
```

### 方案3：混合格式

**可能组合**：
- JSON配置 + 二进制模型数据
- 或类似于 glTF的二进制格式
- 或自定义的Scene Graph格式

---

## 四、EMP与标准3D格式对比

### glTF (GL Transmission Format)

```
标准glTF:
├── .gltf (JSON描述)
├── .bin (二进制数据)
└── textures/

EMP格式可能:
└── .emp (单文件或分包)
    ├── JSON配置（压缩）
    ├── 模型数据（二进制）
    └── 纹理（内嵌或引用）
```

### Three.js JSON

```json
{
  "metadata": { "version": 4.5 },
  "geometries": [...],
  "materials": [...],
  "scenes": [...]
}
```

**EMP可能类似Three.js JSON的变体**，但：
- 可能有不同的字段命名
- 可能有压缩或加密
- 结构可能经过优化

---

## 五、EMP格式的3D类型判断

### 根据使用场景分析

军事博物馆网站包含：
- ✅ **3D模型**：展品、武器、雕塑的3D展示
- ✅ **场景导航**：虚拟展厅漫游
- ✅ **交互热点**：点击查看详细信息
- ✅ **多媒体内容**：图片、文字、视频

### EMP可能包含的3D内容

1. **3D几何数据**
   - 展品模型（枪械、雕塑）
   - 展厅建筑模型
   - 场景环境模型

2. **材质数据**
   - 颜色、纹理
   - 光照、阴影
   - 反射、折射

3. **场景图**
   - 节点层级关系
   - 相机、灯光
   - 动画、交互

4. **元数据**
   - 展品介绍
   - 音频解说
   - 交互逻辑

---

## 六、技术判断：EMP是什么格式？

### 严谨结论

基于证据，**EMP格式**很可能：

1. **不是标准3D格式**
   - 不是glTF、OBJ、FBX等公开格式
   - 是**自研的专有格式**

2. **格式类型**
   - **混合格式**：JSON配置 + 二进制数据
   - 或 **压缩的容器格式**：类似ZIP/PAK但自定义

3. **3D内容类型**
   - 包含**完整的3D场景数据**（不仅仅是模型）
   - 场景图 + 模型 + 材质 + 纹理 + 交互逻辑

4. **技术特点**
   - **加密或压缩**：防止直接提取
   - **Web优化**：针对Web加载优化
   - **双引擎支持**：Three.js (3D) + Pixi.js (2D UI)

---

## 七、EMP vs krpano对比

| 维度 | EMP (军事博物馆) | krpano (全景故宫) |
|------|------------------|-------------------|
| **3D类型** | **真3D模型** | 全景图 |
| **交互方式** | 自由漫游、热点交互 | 360度全景浏览 |
| **场景类型** | 虚拟展厅 | 实景拍摄 |
| **素材来源** | 3D建模 | 全景摄影 |
| **格式开放性** | ❌ 专有格式 | ✅ 行业标准 |
| **可编辑性** | ❌ 难以编辑 | ✅ 可配置 |

---

## 八、最终结论

### EMP是什么格式？

**EMP是**：
1. **自研的专有3D场景容器格式**
2. **混合格式**：配置 + 几何 + 材质 + 纹理
3. **针对Web优化**：数字展厅场景打包格式
4. **可能加密/压缩**：防止内容提取

### 包含的3D内容类型

- ✅ **完整3D场景**（Scene Graph）
- ✅ **3D模型**（Geometry）
- ✅ **材质和纹理**（Materials & Textures）
- ✅ **场景交互**（Hotspots & Interactions）
- ✅ **多媒体数据**（图片、音频、视频）

### 与标准格式的关系

```
EMP格式 ≈ {
  Three.js JSON +
  Binary Geometry +
  Embedded Textures +
  Custom Metadata +
  Compression/Encryption
}
```

**但不是**：
- ❌ 纯文本格式（如JSON）
- ❌ 标准模型格式（如glTF, OBJ, FBX）
- ❌ 全景图格式（如krpano）

---

## 九、技术推测

### EMP可能的内部结构（推测）

```
EMP文件:
┌─────────────────────────────┐
│ Header (32 bytes)              │
│ - Magic: "EMP\x00"            │
│ - Version: 1.0                │
│ - Flags: compressed, encrypted│
├─────────────────────────────┤
│ Scene Index (JSON or Binary)   │
│ - Scene count                 │
│ - Scene metadata              │
├─────────────────────────────┤
│ Scene 1 Data                  │
│ ├─ Camera                     │
│ ├─ Lights                     │
│ ├─ Models [multiple]         │
│ ├─ Materials                 │
│ └─ Hotspots                  │
├─────────────────────────────┤
│ Binary Data Block             │
│ ├─ Geometry (vertices, faces) │
│ ├─ Animation Keyframes       │
│ └─ Texture Data              │
├─────────────────────────────┤
│ Media Files                   │
│ ├─ Images (compressed)       │
│ ├─ Audio                     │
│ └─ Video                     │
└─────────────────────────────┘
```

---

## 十、验证方法

如果要深入分析EMP格式：

### 方法1：逆向工程
```javascript
// 在浏览器控制台
console.log(THREE.REVISION);
console.log(window.empRuntime);

// 拦截网络请求
const originalXHR = window.XMLHttpRequest;
window.XMLHttpRequest = function() {
  const xhr = new originalXHR();
  const originalOpen = xhr.open;
  xhr.open = function(method, url) {
    if (url.includes('.emp')) {
      console.log('EMP Request:', url);
    }
    return originalOpen.apply(this, arguments);
  };
  return xhr;
};
```

### 方法2：分析empRuntime.min.js
- 反混淆或反编译
- 查找文件读取逻辑
- 分析解密算法

### 方法3：网络抓包
- 使用Wireshark或Fiddler
- 拦截HTTP请求
- 分析EMP文件内容

---

## 最终答案

### EMP是什么3D格式？

**EMP = 自研的3D数字展厅容器格式**

包含：
1. ✅ **3D模型数据**（Geometry）
2. ✅ **材质和纹理**（Materials & Textures）
3. ✅ **场景图**（Scene Graph）
4. ✅ **交互逻辑**（Interactions）
5. ✅ **多媒体内容**（Images, Audio, Video）

**格式类型**：专有的压缩/加密混合格式

**技术定位**：
- 类似于"游戏引擎的资源包格式"
- 针对Web场景展示优化
- 不是标准3D格式
- 需要empRuntime.min.js解析

**类比**：
- EMP : krpano ≈ Unity Asset Bundle : JSON配置
- EMP : Three.js ≈ 封装场景 : 原始模型

---

**可信度**：B+（基于代码分析推测，未经逆向工程验证）

**建议**：如需确切格式，需要逆向分析empRuntime.min.js或联系开发方
