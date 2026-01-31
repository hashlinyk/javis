#!/usr/bin/env python3
"""
JARVIS Git Submodule 管理工具

简化 git submodule 的常用操作：添加、归档、更新、查看状态。
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class SubmoduleManager:
    """Git Submodule 管理器"""

    def __init__(self, projects_path: str = None):
        """
        初始化管理器

        Args:
            projects_path: javis_projects 目录路径，默认为 ../javis_projects
        """
        if projects_path is None:
            self.projects_path = Path(__file__).parent.parent.parent.parent / "javis_projects"
        else:
            self.projects_path = Path(projects_path)

        if not self.projects_path.exists():
            raise FileNotFoundError(f"项目目录不存在: {self.projects_path}")

        self.active_path = self.projects_path / "active"
        self.archive_path = self.projects_path / "archive"

    def _run_git(self, args: List[str], cwd: Path = None) -> subprocess.CompletedProcess:
        """执行 git 命令"""
        cmd = ["git"] + args
        result = subprocess.run(
            cmd,
            cwd=cwd or self.projects_path,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        return result

    def add(self, url_or_path: str, name: str, target: str = "active") -> bool:
        """
        添加子模块

        Args:
            url_or_path: 仓库 URL 或本地路径
            name: 子模块名称
            target: 目标目录 (active/archive)

        Returns:
            是否成功
        """
        target_path = self.active_path if target == "active" else self.archive_path

        print(f"添加子模块: {name}")
        print(f"  源: {url_or_path}")
        print(f"  目标: {target_path / name}")

        # 检查是否已存在
        if (target_path / name).exists():
            print(f"错误: 子模块 {name} 已存在")
            return False

        result = self._run_git(
            ["submodule", "add", url_or_path, str(target_path / name)],
            cwd=self.projects_path
        )

        if result.returncode != 0:
            print(f"错误: {result.stderr}")
            return False

        print(f"成功: 子模块 {name} 已添加")
        return True

    def remove(self, name: str, target: str = "active") -> bool:
        """
        移除子模块

        Args:
            name: 子模块名称
            target: 目标目录 (active/archive)

        Returns:
            是否成功
        """
        target_path = self.active_path if target == "active" else self.archive_path

        print(f"移除子模块: {name}")

        # 检查是否存在
        if not (target_path / name).exists():
            print(f"错误: 子模块 {name} 不存在")
            return False

        # 执行 deinit
        result = self._run_git(
            ["submodule", "deinit", "-f", str(target_path / name)],
            cwd=self.projects_path
        )

        if result.returncode != 0:
            print(f"错误 (deinit): {result.stderr}")
            return False

        # 执行 rm
        result = self._run_git(
            ["rm", "-f", str(target_path / name)],
            cwd=self.projects_path
        )

        if result.returncode != 0:
            print(f"错误 (rm): {result.stderr}")
            return False

        # 清理 .git/modules
        modules_path = self.projects_path / ".git" / "modules" / name
        if modules_path.exists():
            import shutil
            try:
                shutil.rmtree(modules_path)
            except Exception as e:
                print(f"警告: 无法清理 .git/modules/{name}: {e}")

        print(f"成功: 子模块 {name} 已移除")
        return True

    def archive(self, name: str) -> bool:
        """
        归档项目（从 active 移动到 archive）

        Args:
            name: 项目名称

        Returns:
            是否成功
        """
        print(f"归档项目: {name}")

        # 检查源路径
        if not (self.active_path / name).exists():
            print(f"错误: 项目 {name} 不在 active/ 中")
            return False

        # 获取子模块的 URL 或路径
        result = self._run_git(
            ["config", "--file", ".gitmodules", f"submodule.active/{name}.url"],
            cwd=self.projects_path
        )

        if result.returncode == 0:
            url_or_path = result.stdout.strip()
        else:
            url_or_path = None
            print("警告: 无法获取子模块 URL，尝试使用本地路径")

        # 移除 from active
        if not self.remove(name, "active"):
            return False

        # 添加到 archive
        if url_or_path:
            return self.add(url_or_path, name, "archive")
        else:
            print("错误: 需要子模块的 URL 才能重新添加到 archive")
            return False

    def update(self, name: str = None, remote: bool = False) -> bool:
        """
        更新子模块

        Args:
            name: 子模块名称，None 表示更新全部
            remote: 是否更新到远程最新

        Returns:
            是否成功
        """
        args = ["submodule", "update"]
        if remote:
            args.append("--remote")
        else:
            args.append("--init")
            args.append("--recursive")

        if name:
            args.append(str(self.active_path / name))
            print(f"更新子模块: {name}")
        else:
            print("更新所有子模块...")

        result = self._run_git(args, cwd=self.projects_path)

        if result.returncode != 0:
            print(f"错误: {result.stderr}")
            return False

        print(result.stdout or "更新完成")
        return True

    def status(self) -> None:
        """显示子模块状态"""
        result = self._run_git(["submodule", "status"], cwd=self.projects_path)

        if result.returncode != 0:
            print(f"错误: {result.stderr}")
            return

        print("子模块状态:")
        print(result.stdout)

    def list_active(self) -> List[str]:
        """列出活跃项目"""
        if not self.active_path.exists():
            return []

        return [d.name for d in self.active_path.iterdir() if d.is_dir() and not d.name.startswith('.')]

    def list_archive(self) -> List[str]:
        """列出归档项目"""
        if not self.archive_path.exists():
            return []

        return [d.name for d in self.archive_path.iterdir() if d.is_dir() and not d.name.startswith('.')]


def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(
        description='JARVIS Git Submodule 管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 添加新项目到 active
  python submodule_manager.py add https://github.com/user/repo.git my-project

  # 添加本地项目到 active
  python submodule_manager.py add /path/to/local/project my-project

  # 归档项目
  python submodule_manager.py archive my-project

  # 移除项目
  python submodule_manager.py remove my-project

  # 更新所有子模块
  python submodule_manager.py update

  # 更新到远程最新
  python submodule_manager.py update --remote

  # 更新特定子模块
  python submodule_manager.py update my-project

  # 查看状态
  python submodule_manager.py status

  # 列出项目
  python submodule_manager.py list --active
  python submodule_manager.py list --archive
        """
    )

    parser.add_argument('--projects', '-p', help='javis_projects 目录路径')

    subparsers = parser.add_subparsers(dest='command', help='命令')

    # add 命令
    add_parser = subparsers.add_parser('add', help='添加子模块')
    add_parser.add_argument('url_or_path', help='仓库 URL 或本地路径')
    add_parser.add_argument('name', help='子模块名称')
    add_parser.add_argument('--target', '-t', choices=['active', 'archive'], default='active',
                           help='目标目录 (默认: active)')

    # remove 命令
    remove_parser = subparsers.add_parser('remove', help='移除子模块')
    remove_parser.add_argument('name', help='子模块名称')
    remove_parser.add_argument('--target', '-t', choices=['active', 'archive'], default='active',
                               help='目标目录 (默认: active)')

    # archive 命令
    archive_parser = subparsers.add_parser('archive', help='归档项目 (active -> archive)')
    archive_parser.add_argument('name', help='项目名称')

    # update 命令
    update_parser = subparsers.add_parser('update', help='更新子模块')
    update_parser.add_argument('name', nargs='?', help='子模块名称（可选）')
    update_parser.add_argument('--remote', '-r', action='store_true', help='更新到远程最新')

    # status 命令
    subparsers.add_parser('status', help='显示子模块状态')

    # list 命令
    list_parser = subparsers.add_parser('list', help='列出项目')
    list_parser.add_argument('--active', '-a', action='store_true', help='列出活跃项目')
    list_parser.add_argument('--archive', '-r', action='store_true', help='列出归档项目')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        manager = SubmoduleManager(args.projects)

        if args.command == 'add':
            manager.add(args.url_or_path, args.name, args.target)
        elif args.command == 'remove':
            manager.remove(args.name, args.target)
        elif args.command == 'archive':
            manager.archive(args.name)
        elif args.command == 'update':
            manager.update(args.name, args.remote)
        elif args.command == 'status':
            manager.status()
        elif args.command == 'list':
            if args.active:
                projects = manager.list_active()
                print("活跃项目:")
                for p in projects:
                    print(f"  - {p}")
            if args.archive:
                projects = manager.list_archive()
                print("归档项目:")
                for p in projects:
                    print(f"  - {p}")
            if not args.active and not args.archive:
                projects = manager.list_active()
                print("活跃项目:")
                for p in projects:
                    print(f"  - {p}")

    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
