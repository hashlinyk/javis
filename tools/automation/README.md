# 自动化脚本

这个目录包含提高工作效率的自动化工具。

## 可用脚本

### memory_backup.py

记忆模块备份工具，定期备份 `memory/` 目录到 `F:\javis_projects\archive\memory_backups`。

```bash
python tools/automation/memory_backup.py
```

**功能**:
- 备份完整的 memory/ 目录
- 使用时间戳命名备份
- 自动保留最近 10 个备份

## 添加新脚本

1. 创建脚本文件
2. 添加详细的文档字符串
3. 在本文件中更新说明

## 使用说明

确保 Python 3 已安装并配置到 PATH 环境变量中。
