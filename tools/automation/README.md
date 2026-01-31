# 自动化脚本

这个目录包含提高工作效率的自动化工具。

## 可用脚本

### memory_backup.py

记忆模块备份工具，定期备份 `memory/` 目录到 `F:\workspace\memory_backups`。

```bash
python tools/automation/memory_backup.py
```

**功能**:
- 备份完整的 memory/ 目录
- 使用时间戳命名备份
- 自动保留最近 10 个备份

### submodule_manager.py

Git Submodule 管理工具，简化子模块的常用操作。

```bash
# 添加新项目
python tools/automation/submodule_manager.py add https://github.com/user/repo.git my-project

# 归档项目
python tools/automation/submodule_manager.py archive my-project

# 移除项目
python tools/automation/submodule_manager.py remove my-project

# 更新所有子模块
python tools/automation/submodule_manager.py update

# 查看状态
python tools/automation/submodule_manager.py status

# 列出项目
python tools/automation/submodule_manager.py list --active
python tools/automation/submodule_manager.py list --archive
```

**功能**:
- 添加子模块（支持远程 URL 和本地路径）
- 归档项目（从 active 移动到 archive）
- 移除子模块（自动清理 .git/modules）
- 更新子模块（初始化或更新到远程最新）
- 查看子模块状态
- 列出活跃/归档项目

**优势**:
- 自动执行完整的 deinit + rm 流程
- 自动清理 .git/modules 目录
- 简化常用操作，减少命令复杂度
- 跨平台支持（使用 pathlib）

## 添加新脚本

1. 创建脚本文件
2. 添加详细的文档字符串
3. 在本文件中更新说明

## 使用说明

确保 Python 3 已安装并配置到 PATH 环境变量中。
