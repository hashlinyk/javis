# Akshare 数据源使用指南

免费开源的财经数据接口库。

## 安装

```bash
pip install akshare
```

## 常用功能

### 获取实时行情

```python
import akshare as ak

# 获取所有A股实时行情
df = ak.stock_zh_a_spot_em()

# 常用字段
# - 代码: 股票代码
# - 名称: 股票名称
# - 最新价: 当前价格
# - 涨跌幅: 百分比
# - 成交量: 手
# - 成交额: 元
```

### 获取历史数据

```python
# 日K线数据
df = ak.stock_zh_a_hist(
    symbol="000001",      # 股票代码
    period="日k",         # 周期: 日k, 周k, 月k
    adjust="qfq"          # 复权: qfq(前), hfq(后), ""(不复权)
)

# 字段说明
# - 日期: 交易日期
# - 开盘, 收盘, 最高, 最低: OHLC
# - 成交量: 手
# - 成交额: 元
# - 振幅: 百分比
# - 涨跌幅, 涨跌额
# - 换手率: 百分比
```

### 获取指数行情

```python
# 获取所有指数实时行情
df = ak.stock_zh_index_spot_em()

# 常见指数代码
# 000001: 上证指数
# 399001: 深证成指
# 399006: 创业板指
```

### 获取财经新闻

```python
# 市场新闻
df = ak.stock_news_em(symbol="市场新闻")

# 个股新闻
df = ak.stock_news_em(symbol="000001")
```

## 数据处理

### 字段重命名

```python
rename_map = {
    '代码': 'symbol',
    '名称': 'name',
    '最新价': 'price',
    '涨跌幅': 'change_percent',
    '涨跌额': 'change_amount',
    '成交量': 'volume',
    '成交额': 'amount',
}

df.rename(columns=rename_map, inplace=True)
```

### 数据缓存

```python
from datetime import datetime, timedelta

class CachedDataSource:
    def __init__(self, cache_minutes=5):
        self._cache = None
        self._cache_time = None
        self._cache_minutes = cache_minutes

    def get_data(self):
        # 检查缓存是否有效
        if self._cache and self._cache_time:
            if datetime.now() - self._cache_time < timedelta(minutes=self._cache_minutes):
                return self._cache

        # 获取新数据
        data = ak.stock_zh_a_spot_em()
        self._cache = data
        self._cache_time = datetime.now()
        return data
```

## 常见问题

### 网络代理问题

```python
import os

# 跳过代理
os.environ['NO_PROXY'] = '*'
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
```

### 中文编码问题

```python
# 确保使用正确的编码
# -*- coding: utf-8 -*-

# 文件读写时指定编码
with open('data.csv', 'r', encoding='utf-8') as f:
    data = f.read()
```

## 相关项目

- stock-trader: A股交易决策辅助系统
  - 完整的 Akshare 封装实现
  - 位置: `javis_projects/active/stock-trader/src/core/data_sources`
