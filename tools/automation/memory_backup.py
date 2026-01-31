#!/usr/bin/env python3
"""
记忆模块备份工具

定期备份 memory/ 目录到 javis_projects 的 archive 目录。
"""

import os
import shutil
import datetime
from pathlib import Path

def backup_memory():
    """备份记忆模块"""
    workspace = Path("F:/workspace")
    javis_projects = Path("F:/javis_projects")

    memory_dir = workspace / "memory"
    archive_dir = javis_projects / "archive" / "memory_backups"

    # 创建备份目录
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = archive_dir / f"memory_backup_{timestamp}"

    print(f"开始备份记忆模块...")
    print(f"源目录: {memory_dir}")
    print(f"目标目录: {backup_dir}")

    # 复制目录
    if backup_dir.exists():
        shutil.rmtree(backup_dir)

    shutil.copytree(memory_dir, backup_dir)

    print(f"备份完成: {backup_dir}")

    # 保留最近 10 个备份
    backups = sorted(archive_dir.glob("memory_backup_*"), reverse=True)
    for old_backup in backups[10:]:
        print(f"删除旧备份: {old_backup}")
        shutil.rmtree(old_backup)

if __name__ == "__main__":
    backup_memory()
