# Python 金融数据分析

使用 Python 进行 A股数据采集、技术分析和自动化交易的实践经验。

## 数据源

### Akshare

免费开源的财经数据接口库。

**安装**:
```bash
pip install akshare
```

**常用功能**:

```python
import akshare as ak

# 获取实时行情（所有A股）
df = ak.stock_zh_a_spot_em()

# 获取历史数据
df = ak.stock_zh_a_hist(symbol="000001", period="日k", adjust="qfq")

# 获取财经新闻
df = ak.stock_news_em(symbol="市场新闻")

# 获取指数行情
df = ak.stock_zh_index_spot_em()
```

**注意事项**:
- 数据字段名为中文，需要重命名
- 周期参数: "日k", "周k", "月k"
- 复权参数: "qfq"(前复权), "hfq"(后复权), ""(不复权)

## 技术分析

### pandas-ta

纯 Python 实现的技术分析库。

**安装**:
```bash
pip install pandas-ta
```

**常用指标**:

```python
import pandas_ta as ta

# 移动平均线
df['ma5'] = ta.sma(df['close'], length=5)

# MACD
macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
df['macd'] = macd.iloc[:, 0]
df['macd_signal'] = macd.iloc[:, 1]
df['macd_hist'] = macd.iloc[:, 2]

# RSI
df['rsi'] = ta.rsi(df['close'], length=14)

# KDJ
stoch = ta.stoch(df['high'], df['low'], df['close'], k=14, d=3)
df['k'] = stoch.iloc[:, 0]
df['d'] = stoch.iloc[:, 1]
df['j'] = 3 * stoch.iloc[:, 0] - 2 * stoch.iloc[:, 1]

# 布林带
bbands = ta.bbands(df['close'], length=20, std=2)
df['bb_upper'] = bbands.iloc[:, 0]
df['bb_middle'] = bbands.iloc[:, 1]
df['bb_lower'] = bbands.iloc[:, 2]

# ATR
df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
```

### 信号生成逻辑

**MACD 金叉/死叉**:
```python
if prev_hist <= 0 and hist > 0:
    signal = 'buy'  # 金叉
elif prev_hist >= 0 and hist < 0:
    signal = 'sell'  # 死叉
```

**KDJ 超买/超卖**:
```python
if k > 80:
    signal = 'overbought'  # 超买
elif k < 20:
    signal = 'oversold'    # 超卖
```

**RSI 强弱**:
```python
if rsi > 70:
    signal = 'sell'   # 强
elif rsi < 30:
    signal = 'buy'    # 弱
```

## 邮件通知

### yagmail

简化 Gmail/SMTP 发送的库。

**安装**:
```bash
pip install yagmail
```

**使用**:
```python
import yagmail

# 初始化
yag = yagmail.SMTP(
    user='your_email@163.com',
    password='auth_code',  # 163邮箱使用授权码
    host='smtp.163.com',
    port=465
)

# 发送邮件
yag.send(
    to='recipient@example.com',
    subject='邮件主题',
    contents=['<html>内容</html>', 'attachment.pdf']  # 支持HTML和附件
)
```

**163邮箱配置**:
- SMTP服务器: smtp.163.com
- 端口: 465 (SSL)
- 认证: 需要使用16位授权码，不是邮箱密码

### Jinja2 邮件模板

**安装**:
```bash
pip install jinja2
```

**使用**:
```python
from jinja2 import Environment, FileSystemLoader

# 初始化模板环境
env = Environment(
    loader=FileSystemLoader('templates/email'),
    autoescape=True
)

# 渲染模板
template = env.get_template('news_digest.html')
html = template.render(news_list=news, date='2026-02-23')
```

## 任务调度

### schedule

轻量级定时任务库。

**安装**:
```bash
pip install schedule
```

**使用**:
```python
import schedule
import time

def job():
    print("执行任务")

# 定时任务
schedule.every().day.at("08:00").do(job)
schedule.every(5).minutes.do(job)
schedule.every().monday.do(job)

# 运行调度器
while True:
    schedule.run_pending()
    time.sleep(60)
```

### 交易时间判断

```python
from datetime import datetime, time as dt_time

def is_trading_time():
    now = datetime.now()

    # 周末不交易
    if now.weekday() >= 5:
        return False

    current_time = now.time()

    # 上午: 9:30-11:30
    morning_start = dt_time(9, 30)
    morning_end = dt_time(11, 30)

    # 下午: 13:00-15:00
    afternoon_start = dt_time(13, 0)
    afternoon_end = dt_time(15, 0)

    return (morning_start <= current_time <= morning_end) or \
           (afternoon_start <= current_time <= afternoon_end)
```

## Windows 后台运行

### 任务计划程序（推荐）

使用 PowerShell 安装：

```powershell
$action = New-ScheduledTaskAction -Execute "python" -Argument "-m src.main daemon" -WorkingDirectory "F:\project"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "MyApp" -Action $action -Trigger $trigger -Principal $principal
```

### Windows 服务

使用 pywin32：

```bash
pip install pywin32
```

```python
import win32serviceutil
import win32service

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MyService"
    _svc_display_name_ = "我的服务"

    def SvcDoRun(self):
        # 服务运行逻辑
        pass

    def SvcStop(self):
        # 停止服务
        pass
```

### 后台窗口（VBS）

```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "python -m src.main daemon", 0
Set WshShell = Nothing
```

## 股票代码规范

- **上海交易所**: 6xxxxx（如 600000 浦发银行）
- **深圳交易所**: 0xxxxx（如 000001 平安银行）
- **指数代码**: 000001（上证）、399001（深证成指）

## 数据处理技巧

### 成交量/额格式化

```python
def format_volume(volume: int) -> str:
    if volume >= 100000000:
        return f"{volume/100000000:.2f}亿手"
    elif volume >= 10000:
        return f"{volume/10000:.2f}万手"
    return f"{volume}手"

def format_amount(amount: float) -> str:
    if amount >= 100000000:
        return f"{amount/100000000:.2f}亿元"
    elif amount >= 10000:
        return f"{amount/10000:.2f}万元"
    return f"{amount:.2f}元"
```

### 涨跌幅颜色判断

```python
def get_color_class(change_percent: float) -> str:
    if change_percent > 0:
        return 'up'      # 红色（A股上涨为红）
    elif change_percent < 0:
        return 'down'    # 绿色（A股下跌为绿）
    return 'flat'
```

## 相关项目

- stock-trader: A股交易决策辅助系统
  - 包含完整的Web可视化界面
  - 位置: `javis_projects/active/stock-trader`
  - 仓库: https://github.com/hashlinyk/stock-trader

