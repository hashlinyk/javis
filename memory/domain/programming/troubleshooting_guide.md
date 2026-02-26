# Python 开发问题排查

常见 Python 开发问题的排查和解决方法。

## 依赖管理问题

### 模块未找到

**错误**: `ModuleNotFoundError: No module named 'xxx'`

**排查步骤**:
1. 确认依赖已安装: `pip list | grep xxx`
2. 检查Python环境: `which python` 或 `where python`
3. 虚拟环境检查: `pip list` 在正确环境中

**解决方案**:
```bash
# 安装缺失的依赖
pip install <package_name>

# 或从 requirements.txt 安装
pip install -r requirements.txt

# 指定版本
pip install <package_name>==<version>
```

### 导入路径问题

**错误**: 模块已安装但导入失败

**原因**: 相对导入 vs 绝对导入

**解决方案**:
```python
# 错误：当通过 python -m src.main 启动时
from config.base import StockTraderConfig  # 会失败

# 正确：使用完整模块路径
from src.config.base import StockTraderConfig

# 或在 __main__ 中添加路径
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

## 网络问题

### 代理连接错误

**错误**: `ProxyError('Unable to connect to proxy', ...)`

**原因**: 系统配置了代理但代理服务器未响应

**解决方案**:
```python
# 方法1: 配置请求跳过代理
import requests
session = requests.Session()
session.trust_env = False  # 忽略系统代理设置
session.proxies = {'http': None, 'https': None}

# 方法2: 设置环境变量
import os
os.environ['NO_PROXY'] = '*'
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

# 方法3: 使用本地配置
proxies = {
    'http': None,
    'https': None,
}
requests.get(url, proxies=proxies)
```

### akshare 数据获取失败

**错误**: 实时行情返回空或超时

**排查**:
1. 检查网络连接
2. 验证代理设置
3. 尝试手动调用 akshare API

```python
import akshare as ak

# 测试连接
try:
    df = ak.stock_zh_a_spot_em()
    print(f"获取到 {len(df)} 条数据")
except Exception as e:
    print(f"错误: {e}")
```

## 编码问题

### 中文乱码

**错误**: `'日k'` 显示为 `'��k'`

**原因**: 文件编码或终端编码不一致

**解决方案**:
```python
# 文件开头指定编码
# -*- coding: utf-8 -*-

# 读取文件时指定编码
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 输出时指定编码
print(content.encode('utf-8').decode('utf-8'))

# 环境变量设置（Windows）
# set PYTHONIOENCODING=utf-8
```

### JSON 中文编码

```python
import json

# 确保中文正常显示
json_str = json.dumps(data, ensure_ascii=False, indent=2)

# 读取JSON
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

## Flask 问题

### 模板未找到

**错误**: `TemplateNotFound`

**检查**:
1. templates 目录在正确位置
2. 模板文件名拼写正确
3. Flask 应用初始化路径正确

```python
# 正确的结构
project/
├── app.py
└── templates/
    └── index.html

# app.py 中
app = Flask(__name__, template_folder='templates')
```

### CORS 错误

**错误**: 浏览器控制台 CORS policy 错误

**解决方案**:
```python
from flask_cors import CORS

# 全局启用
CORS(app)

# 或特定路由
@app.route('/api/data')
@cross_origin()
def get_data():
    return jsonify(data)
```

## 性能问题

### 循环导入

**错误**: `ImportError` 或 `AttributeError` (部分初始化)

**解决方案**:
```python
# 方法1: 延迟导入（在函数内导入）
def some_function():
    from module import something
    return something

# 方法2: 重新组织代码结构
# 避免循环依赖

# 方法3: 使用 __init__.py 控制导入顺序
```

### 内存泄漏

**排查**:
```python
import tracemalloc
tracemalloc.start()

# ... 运行代码 ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

## 日志调试

### 启用详细日志

```python
import logging

# 设置级别
logging.basicConfig(level=logging.DEBUG)

# 或针对特定模块
logging.getLogger('akshare').setLevel(logging.DEBUG)

# 记录日志
logger = logging.getLogger(__name__)
logger.debug('调试信息')
logger.info('普通信息')
logger.warning('警告')
logger.error('错误')
```

### 异常追踪

```python
import traceback

try:
    # 可能出错的代码
    pass
except Exception as e:
    logger.error(f"错误: {e}", exc_info=True)
    # 或
    traceback.print_exc()
```

## Windows 特定问题

### 路径分隔符

```python
from pathlib import Path

# 使用 Path 而非字符串拼接
path = Path('folder') / 'subfolder' / 'file.txt'

# 跨平台兼容
file_path = Path.cwd() / 'data' / 'file.txt'
```

### 进程管理

```bash
# 查找进程
netstat -ano | findstr :5000
tasklist | findstr python

# 终止进程
taskkill /F /PID <pid>
taskkill /F /IM python.exe

# 注意: Git Bash 需要使用双斜杠
taskkill //F //PID 12345
```

## 相关经验

- stock-trader 项目问题排查记录
  - 网络代理导致数据获取失败
  - 导入路径配置错误
  - 中文编码问题

参见: `memory/session_history.md` 中的 2026-02-26 记录
