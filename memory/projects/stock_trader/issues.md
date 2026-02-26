# A股交易系统 - 问题记录

## 已知问题

### 1. 网络代理连接错误 🔴

**错误**: `ProxyError('Unable to connect to proxy', RemoteDisconnected)`

**影响**: 实时行情、指数数据无法获取

**原因**: 系统配置了代理但代理服务器未响应

**解决方案**:
```python
# 方法1: 配置 akshare 跳过代理
import os
os.environ['NO_PROXY'] = '*'
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

# 方法2: 修改 akshare 源码
# 在 requests 调用时添加 proxies={'http': None, 'https': None}
```

**状态**: 待修复

---

### 2. 中文编码问题 🟡

**错误**: 获取历史数据时 `"日k"` 显示为 `'��k'`

**影响**: K线图无法加载，交易信号无法生成

**位置**: `src/core/data_sources/akshare_source.py`

**原因**: 字符串编码处理问题

**解决方案**:
```python
# 确保文件使用 UTF-8 编码
# -*- coding: utf-8 -*-

# 或显式指定编码
period_map = {
    "daily": "日k",
    "weekly": "周k",
    "monthly": "月k"
}
```

**状态**: 待修复

---

### 3. 缺少 favicon.ico 🟢

**错误**: 浏览器控制台 404 错误

**影响**: 仅控制台报错，不影响功能

**解决方案**:
1. 创建 `src/web/static/favicon.ico`
2. 在 HTML 中添加: `<link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">`

**状态**: 可选修复

---

## 问题排查经验

### 依赖问题

**现象**: `ModuleNotFoundError: No module named 'xxx'`

**解决**:
```bash
pip install -r requirements.txt
```

### 导入路径问题

**现象**: 模块存在但导入失败

**原因**: 通过 `python -m src.main` 启动时，需使用完整模块路径

**解决**:
```python
# 错误
from config.base import StockTraderConfig

# 正确
from src.config.base import StockTraderConfig
```

### 网络问题调试

```python
import akshare as ak

# 测试连接
try:
    df = ak.stock_zh_a_spot_em()
    print(f"成功获取 {len(df)} 条数据")
except Exception as e:
    print(f"失败: {e}")
```

## 相关文档

- [Python 问题排查指南](../../domain/programming/troubleshooting_guide.md)
- [Flask 常见问题](../../domain/programming/flask_rest_api.md#常见问题)
