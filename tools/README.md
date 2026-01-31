# 工具集

这是我的工具箱，存放常用的脚本、工具和实用程序。

## 目录结构

```
tools/
├── README.md              # 本文件 - 工具集说明
├── arch_rules.md          # 架构规则 - 陈旧知识更新规则
├── automation/            # 自动化脚本
│   ├── README.md
│   ├── memory_backup.py   # 记忆备份工具
│   └── submodule_manager.py # 子模块管理工具
├── utilities/             # 实用工具
│   ├── README.md
│   └── load_config.py     # 配置加载器
└── integration/           # 集成工具
```

## 工具分类

### automation/

自动化任务脚本，提高工作效率

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `memory_backup.py` | 备份记忆系统 | 定期备份 memory/ 目录 |
| `submodule_manager.py` | 子模块管理 | 简化 git submodule 操作 |

### utilities/

通用实用工具，解决常见问题

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `load_config.py` | 配置加载器 | 跨平台读取配置文件 |

### arch_rules.md

架构规则文档，定义陈旧知识的更新触发条件和检查清单。

### integration/

与其他系统或服务的集成工具（待补充）

## 使用原则

1. 每个工具独立文档说明
2. 包含使用示例
3. 考虑跨平台兼容性
4. 错误处理完善
5. 提供 CLI 和 API 两种接口（如适用）

## 快速开始

```bash
# 查看配置
python tools/utilities/load_config.py --verify

# 添加项目
python tools/automation/submodule_manager.py add <url> <name>

# 备份记忆
python tools/automation/memory_backup.py
```

---
*创建时间: 2026-01-31*
