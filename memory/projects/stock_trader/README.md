# A股交易决策辅助系统 - 项目记录

**项目地址**: https://github.com/hashlinyk/stock-trader
**本地路径**: `F:/javis_projects/active/stock-trader`
**创建时间**: 2026-02-23

## 快速导航

- [项目概述](#项目概述)
- [核心功能](#核心功能)
- [技术架构](#技术架构)
- [使用方法](#使用方法)
- [问题记录](#问题记录)
- [开发日志](#开发日志)

## 项目概述

自动化股票分析系统，提供新闻采集、技术分析和邮件通知功能。

## 核心功能

### 1. 数据采集模块
- Akshare数据源封装
- 实时行情、历史数据获取
- 5分钟数据缓存机制

### 2. 技术分析模块
- MACD、KDJ、RSI、布林带、ATR指标
- 交易信号生成器
- 趋势判断（多头/空头/震荡）

### 3. 邮件通知系统
- 四种HTML邮件模板
- 163邮箱集成（yagmail + Jinja2）
- 定时发送功能

### 4. Web可视化界面
- Flask RESTful API（9个接口）
- 响应式暗色主题界面
- ECharts K线图
- 30秒自动刷新

### 5. 任务调度器
- 新闻摘要：每日 08:00, 12:00, 18:00
- 交易信号检查：交易时段每30分钟
- 价格预警：交易时段每5分钟
- 每日报告：15:30

## 技术架构

```
stock-trader/
├── .stock-trader/              # 配置目录
├── src/
│   ├── config/                 # 配置管理
│   ├── core/
│   │   ├── data_sources/       # 数据采集
│   │   ├── analysis/           # 技术分析
│   │   ├── notifier/           # 邮件通知
│   │   └── storage/            # 数据存储
│   ├── scheduler/              # 任务调度
│   ├── cli/                    # 命令行工具
│   ├── web/                    # Web界面
│   └── utils/                  # 工具函数
├── templates/email/            # 邮件模板
└── scripts/                    # 运行脚本
```

## 使用方法

### 启动Web界面
```bash
python -m src.main web
# 访问 http://localhost:5000
```

### CLI工具
```bash
python -m src.cli quote 000001
python -m src.cli news
python -m src.cli analyze 600519
```

### 守护进程
```bash
python -m src.main daemon
```

## 用户配置

- **邮箱**: lin_yuekai@163.com
- **SMTP**: smtp.163.com:465
- **监控股票**: 000001, 000002, 600000, 600519, 000858
- **监控指数**: 000001(上证), 399001(深证成指)

## 问题记录

详见 [问题记录](./issues.md)

## 开发日志

- [2026-02-23] 初始开发完成
- [2026-02-26] Web界面开发完成

## 相关知识

- [Flask RESTful API 开发](../../domain/programming/flask_rest_api.md)
- [Python 金融数据分析](../../domain/programming/python_finance.md)
- [自动化通知系统模式](../../patterns/solution_patterns/automated_notification_system.md)
