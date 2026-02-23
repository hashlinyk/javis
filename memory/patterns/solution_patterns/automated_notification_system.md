# 自动化通知系统模式

定时数据采集、分析和邮件通知的通用系统架构模式。

## 适用场景

- 财经数据监控和通知
- 系统监控和告警
- 定期报告生成
- 自动化数据采集

## 架构设计

```
notification-system/
├── config/                    # 配置模块
│   ├── base.py               # 配置管理器
│   └── config.json           # 配置文件
├── core/                      # 核心业务
│   ├── data_sources/         # 数据采集
│   │   ├── base.py           # 抽象基类
│   │   └── impl.py           # 具体实现
│   ├── analyzer/             # 分析引擎
│   │   ├── calculator.py     # 指标计算
│   │   └── signals.py        # 信号生成
│   └── notifier/             # 通知模块
│       ├── email.py          # 邮件发送
│       └── templates/        # 通知模板
├── scheduler/                 # 任务调度
│   └── runner.py             # 调度器
├── cli/                       # 命令行工具
│   └── commands.py
└── utils/                     # 工具函数
    └── logger.py
```

## 核心组件

### 1. 配置管理

```python
class ConfigManager:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self._load_local_config()  # 加载敏感配置

    def get(self, key: str, default=None):
        """支持点号路径的配置获取"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
```

**配置文件结构**:
- `config.json`: 主配置（可提交）
- `config.local.json`: 本地配置（敏感信息，不提交）

### 2. 数据采集

```python
from abc import ABC, abstractmethod

class DataSource(ABC):
    @abstractmethod
    def fetch_data(self) -> dict:
        """获取数据"""
        pass

class CachedDataSource(DataSource):
    def __init__(self, cache_minutes: int = 5):
        self._cache = None
        self._cache_time = None
        self._cache_minutes = cache_minutes

    def fetch_data(self) -> dict:
        if self._is_cache_valid():
            return self._cache
        data = self._fetch_fresh_data()
        self._update_cache(data)
        return data
```

### 3. 分析引擎

```python
class Analyzer:
    def calculate(self, data: dict) -> dict:
        """计算指标"""
        pass

class SignalGenerator:
    def generate(self, data: dict) -> list:
        """生成信号"""
        signals = []
        # 信号生成逻辑
        return signals
```

### 4. 通知系统

```python
from jinja2 import Template

class Notifier:
    def __init__(self, config):
        self.template_env = Environment(...)
        self.sender = self._init_sender()

    def send(self, template_name: str, context: dict):
        template = self.template_env.get_template(template_name)
        content = template.render(**context)
        self.sender.send(
            subject=context.get('subject'),
            content=content
        )
```

### 5. 任务调度

```python
import schedule

class TaskScheduler:
    def setup(self):
        schedule.every().day.at("08:00").do(self.morning_job)
        schedule.every(5).minutes.do(self.frequent_job)

    def run(self):
        while self.running:
            schedule.run_pending()
            time.sleep(60)

    def is_active_time(self) -> bool:
        """判断是否为活跃时间（仅在该时段执行高频任务）"""
        # 实现时间判断逻辑
        pass
```

## 设计要点

### 时间敏感任务

对于需要定时执行的任务，区分:

1. **定时任务**: 每天固定时间执行（如新闻摘要）
2. **高频任务**: 交易时段高频执行（如价格检查）

```python
# 高频任务需要判断时间
def job_check_price(self):
    if not self.is_trading_time():
        return
    # 执行检查逻辑
```

### 避免通知轰炸

实现去重机制，避免重复发送相同通知:

```python
class TaskScheduler:
    def __init__(self):
        self.last_alert = {}

    def check_alert(self, key: str, condition: bool):
        if condition:
            last = self.last_alert.get(key)
            if last is None or time_since(last) > threshold:
                self.send_alert(key)
                self.last_alert[key] = now()
```

### 模块化设计

每个功能模块独立:

- 数据源可以轻松替换
- 分析算法可独立升级
- 通知方式可扩展（邮件/短信/微信）

## 错误处理

```python
def job_with_error_handling(self):
    try:
        # 任务逻辑
        pass
    except NetworkError as e:
        logger.warning(f"网络错误，跳过本次: {e}")
    except Exception as e:
        logger.error(f"任务执行失败: {e}", exc_info=True)
        # 可选：发送错误通知
```

## 测试策略

```python
# CLI 命令支持测试
python -m cli test-email      # 测试邮件
python -m cli test-data       # 测试数据源
python -m cli test-signal     # 测试信号生成
```

## 扩展性

### 添加新的数据源

1. 继承 `DataSource` 基类
2. 实现 `fetch_data()` 方法
3. 在配置中指定数据源类型

### 添加新的通知方式

1. 实现 `NotificationSender` 接口
2. 在 `Notifier` 中注册
3. 创建对应的消息模板

## 相关项目

- stock-trader: A股交易决策辅助系统
  - 完整实现此模式的示例
  - 位置: `javis_projects/active/stock-trader`
