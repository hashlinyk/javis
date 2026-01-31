# 实用工具

这个目录存放 JARVS 的实用工具脚本。

## 工具列表

### load_config.py

JARVIS 配置加载器，用于跨平台读取 `.javis/config.json` 配置文件。

#### 使用方法

```bash
# 显示当前配置
python tools/utilities/load_config.py

# 获取特定配置项
python tools/utilities/load_config.py --get javis_projects_path

# 验证路径配置
python tools/utilities/load_config.py --verify

# 美化输出完整配置
python tools/utilities/load_config.py --pretty

# 指定配置文件路径
python tools/utilities/load_config.py --config /path/to/config.json
```

#### Python API

```python
from tools.utilities.load_config import JavisConfig

# 加载配置
config = JavisConfig()

# 获取配置项
projects_path = config.get('javis_projects_path')
language = config.get('language')

# 获取路径对象
workspace = config.get_workspace_path()
projects = config.get_javis_projects_path()

# 验证路径
status = config.verify_paths()
# {'workspace': True, 'javis_projects': True, 'config': True}
```

---

*创建时间: 2026-01-31*
