# 配置驱动设计模式

## 概述

配置驱动设计是一种通过配置文件而非硬编码来控制应用行为的架构模式。这种模式提高了代码的灵活性、可移植性和可维护性。

## 解决的问题

### 硬编码路径问题

```python
# 糟糕的示例 - 硬编码路径
PROJECTS_PATH = "F:\\javis_projects"
WORKSPACE_PATH = "F:\\workspace"

# 问题：
# 1. 无法在不同环境中使用
# 2. 修改需要重新编译/部署
# 3. 难以维护多环境配置
```

### 环境适配问题

不同操作系统使用不同的路径分隔符和约定：
- Windows: `C:\Users\user\project`
- Linux: `/home/user/project`
- Mac: `/Users/user/project`

## 模式结构

```
配置驱动设计
├── 配置文件 (.json/.yaml/.toml)
├── 配置加载器 (Config Loader)
├── 路径解析器 (Path Resolver)
└── 应用逻辑 (Application Logic)
```

## 核心组件

### 1. 配置文件

使用结构化格式存储配置：

```json
{
  "version": "1.0",
  "paths": {
    "workspace": "${CWD}",
    "projects": "${DEFAULT}",
    "cache": "${HOME}/.cache/javis"
  },
  "features": {
    "auto_backup": true,
    "sync_enabled": false
  }
}
```

### 2. 配置加载器

```python
class ConfigLoader:
    def load(self, path: str) -> dict:
        """加载并解析配置文件"""
        pass

    def get(self, key: str, default=None) -> Any:
        """获取配置项"""
        pass
```

### 3. 路径解析器

```python
class PathResolver:
    def resolve(self, value: str) -> str:
        """解析路径变量"""
        value = value.replace("${CWD}", os.getcwd())
        value = value.replace("${HOME}", os.path.expanduser("~"))
        value = value.replace("${DEFAULT}", self.get_default(value))
        return value
```

## 实现示例

### 完整实现

```python
import json
import os
from pathlib import Path
from typing import Any, Dict

class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = self._load_and_resolve()

    def _load_and_resolve(self) -> Dict[str, Any]:
        """加载并解析配置"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        return self._resolve_paths(raw)

    def _resolve_paths(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """递归解析路径变量"""
        cwd = Path.cwd()
        home = Path.home()

        def resolve(value: Any) -> Any:
            if isinstance(value, str):
                value = value.replace('${CWD}', str(cwd))
                value = value.replace('${HOME}', str(home))
                return value
            elif isinstance(value, dict):
                return {k: resolve(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [resolve(item) for item in value]
            return value

        return resolve(config)

    def get(self, key: str, default=None) -> Any:
        """获取配置项（支持点号分隔的路径）"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
```

### 使用示例

```python
# 初始化
config = ConfigManager('.javis/config.json')

# 获取配置
projects_path = config.get('paths.projects')  # "F:/javis_projects"
auto_backup = config.get('features.auto_backup')  # True

# 使用路径
with open(projects_path / 'active' / 'my-project', 'r') as f:
    content = f.read()
```

## 变体

### 环境变量优先级

支持环境变量覆盖配置文件：

```python
class ConfigManager:
    def get(self, key: str, default=None) -> Any:
        # 1. 检查环境变量（转换为大写，用下划线连接）
        env_key = key.upper().replace('.', '_')
        env_value = os.environ.get(f'JARVIS_{env_key}')
        if env_value is not None:
            return self._parse_value(env_value)

        # 2. 从配置文件获取
        return self._get_from_config(key, default)
```

### 配置文件查找策略

```python
def find_config_path() -> Path:
    """查找配置文件"""
    candidates = [
        os.environ.get('JARVIS_CONFIG'),           # 环境变量
        '.javis/config.json',                       # 当前目录
        os.path.expanduser('~/.javis/config.json'), # 用户目录
        '/etc/javis/config.json',                  # 系统目录
    ]
    for path in candidates:
        if path and Path(path).exists():
            return Path(path)
    raise FileNotFoundError("找不到配置文件")
```

## 最佳实践

### 1. 配置验证

```python
from pydantic import BaseModel, validator

class JavisConfig(BaseModel):
    version: str
    workspace_path: Path
    projects_path: Path

    @validator('workspace_path', 'projects_path')
    def path_exists(cls, v):
        if not v.exists():
            raise ValueError(f"路径不存在: {v}")
        return v

config = JavisConfig.parse_obj(raw_config)
```

### 2. 默认值处理

```python
DEFAULT_CONFIG = {
    "version": "1.0",
    "workspace_path": str(Path.cwd()),
    "projects_path": str(Path.cwd().parent / "javis_projects"),
}

def load_with_defaults(path: str) -> dict:
    defaults = DEFAULT_CONFIG.copy()
    if Path(path).exists():
        with open(path, 'r') as f:
            user_config = json.load(f)
        defaults.update(user_config)
    return defaults
```

### 3. 配置迁移

```python
class ConfigMigrator:
    def migrate(self, old_config: dict, from_version: str) -> dict:
        """迁移旧配置到新版本"""
        if from_version == "0.9":
            # 重命名字段
            old_config["projects_path"] = old_config.pop("project_dir")
        elif from_version == "1.0":
            # 新增字段
            if "features" not in old_config:
                old_config["features"] = {"auto_backup": True}
        return old_config
```

## 适用场景

| 场景 | 适用性 |
|------|--------|
| 多环境部署 | ✅ 非常适合 |
| 路径管理 | ✅ 非常适合 |
| 特性开关 | ✅ 非常适合 |
| 性能调优 | ✅ 适合 |
| 常量配置 | ⚠️ 可用，但可能过度 |

## 优缺点

### 优点

- ✅ **灵活性**: 无需重新编译即可修改行为
- ✅ **可移植性**: 支持多环境适配
- ✅ **可维护性**: 配置与代码分离
- ✅ **透明性**: 配置清晰可见

### 缺点

- ❌ **复杂度**: 增加了系统复杂度
- ❌ **错误处理**: 需要处理配置错误
- ❌ **文档负担**: 需要维护配置文档

## JARVIS 中的应用

JARVIS 使用配置驱动设计解决跨平台问题：

1. **配置文件**: `.javis/config.json`
2. **加载器**: `tools/utilities/load_config.py`
3. **变量支持**: `${CWD}`, `${HOME}`, `${DEFAULT}`
4. **环境适配**: Windows/Linux/Mac 路径自动解析

## 相关标签

#design-pattern #configuration #cross-platform #flexibility

---
*创建时间: 2026-01-31*
