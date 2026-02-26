# 技术分析指标实现

使用 pandas-ta 计算常用技术指标。

## 安装

```bash
pip install pandas-ta
```

## 移动平均线 (MA)

```python
import pandas_ta as ta

# 简单移动平均
df['ma5'] = ta.sma(df['close'], length=5)
df['ma10'] = ta.sma(df['close'], length=10)
df['ma20'] = ta.sma(df['close'], length=20)
df['ma60'] = ta.sma(df['close'], length=60)
```

## MACD

```python
# MACD (12, 26, 9)
macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
df['macd'] = macd.iloc[:, 0]      # DIF
df['macd_signal'] = macd.iloc[:, 1]  # DEA
df['macd_hist'] = macd.iloc[:, 2]    # MACD柱

# 信号判断
# 金叉: hist从负变正
# 死叉: hist从正变负
```

## KDJ

```python
# KDJ (9, 3, 3)
stoch = ta.stoch(df['high'], df['low'], df['close'], k=9, d=3, smooth_k=3)
df['k'] = stoch.iloc[:, 0]
df['d'] = stoch.iloc[:, 1]

# J = 3K - 2D
df['j'] = 3 * df['k'] - 2 * df['d']

# 超买超卖
# K > 80: 超买
# K < 20: 超卖
```

## RSI

```python
# RSI (14)
df['rsi'] = ta.rsi(df['close'], length=14)

# 强弱判断
# RSI > 70: 强势
# RSI < 30: 弱势
```

## 布林带 (BOLL)

```python
# 布林带 (20, 2)
bbands = ta.bbands(df['close'], length=20, std=2)
df['bb_upper'] = bbands.iloc[:, 0]    # 上轨
df['bb_middle'] = bbands.iloc[:, 1]  # 中轨
df['bb_lower'] = bbands.iloc[:, 2]   # 下轨

# 突破判断
# 价格 > 上轨: 突破
# 价格 < 下轨: 跌破
```

## ATR

```python
# 平均真实波幅
df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
```

## 信号生成

### MACD 信号

```python
def check_macd_signal(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    hist = latest['macd_hist']
    prev_hist = prev['macd_hist']

    if prev_hist <= 0 and hist > 0:
        return 'buy'   # 金叉
    elif prev_hist >= 0 and hist < 0:
        return 'sell'  # 死叉
    return None
```

### KDJ 信号

```python
def check_kdj_signal(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    k = latest['k']
    d = latest['d']
    prev_k = prev['k']
    prev_d = prev['d']

    # 金叉
    if prev_k <= prev_d and k > d:
        if k < 30:
            return 'strong_buy'  # 低位金叉
        return 'buy'

    # 死叉
    elif prev_k >= prev_d and k < d:
        if k > 70:
            return 'strong_sell'  # 高位死叉
        return 'sell'

    # 超买超卖
    if k > 80:
        return 'overbought'
    elif k < 20:
        return 'oversold'

    return None
```

### 趋势判断

```python
def get_trend(df):
    latest = df.iloc[-1]

    # 多头排列
    if (latest['ma5'] > latest['ma10'] > latest['ma20'] > latest['ma60']):
        return 'bullish'

    # 空头排列
    elif (latest['ma5'] < latest['ma10'] < latest['ma20'] < latest['ma60']):
        return 'bearish'

    # 震荡
    else:
        return 'neutral'
```

## 相关文档

- [pandas-ta 官方文档](https://twopirllc.github.io/pandas-ta/)
- [股票技术指标说明](https://www.investopedia.com/technical-analysis-4427779)
