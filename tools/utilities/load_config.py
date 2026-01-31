#!/usr/bin/env python3
"""
JARVIS 配置加载器

用于跨平台读取 .javis/config.json 配置文件，支持环境变量和路径解析。
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any


class JavisConfig:
    """JARVIS 配置管理器"""

    def __init__(self, config_path: str = None):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径，默认为 .javis/config.json
        """
        if config_path is None:
            # 查找配置文件：环境变量 -> 当前目录 -> 脚本目录
            config_path = os.environ.get('JARVIS_CONFIG')
            if config_path is None:
                script_dir = Path(__file__).parent.parent.parent
                config_path = script_dir / '.javis' / 'config.json'

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载并解析配置文件"""
        if not self.config_path.exists():
            return self._get_default_config()

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                raw_config = json.load(f)
            return self._resolve_paths(raw_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"警告: 配置文件读取失败 ({e})，使用默认配置", file=sys.stderr)
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "version": "1.0",
            "workspace_path": str(Path.cwd()),
            "javis_projects_path": str(Path.cwd().parent / "javis_projects"),
            "language": "zh-CN",
            "session_mode": "javis-assistant",
            "auto_backup": {
                "enabled": True,
                "schedule": "daily",
                "max_backups": 7
            }
        }

    def _resolve_paths(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """解析配置中的路径变量"""
        cwd = Path.cwd()
        config_dir = self.config_path.parent.parent  # workspace 根目录

        def resolve_value(value: Any) -> Any:
            """递归解析值"""
            if isinstance(value, str):
                # 替换路径变量
                value = value.replace('${CWD}', str(cwd))
                value = value.replace('${DEFAULT}', str(cwd.parent / "javis_projects"))
                value = value.replace('${HOME}', str(Path.home()))
                return value
            elif isinstance(value, dict):
                return {k: resolve_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [resolve_value(item) for item in value]
            return value

        return resolve_value(config)

    def get(self, key: str, default=None):
        """获取配置项"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def get_javis_projects_path(self) -> Path:
        """获取 javis_projects 路径"""
        return Path(self.get('javis_projects_path'))

    def get_workspace_path(self) -> Path:
        """获取工作区路径"""
        return Path(self.get('workspace_path'))

    def verify_paths(self) -> Dict[str, bool]:
        """验证配置的路径是否存在"""
        return {
            "workspace": self.get_workspace_path().exists(),
            "javis_projects": self.get_javis_projects_path().exists(),
            "config": self.config_path.exists()
        }

    def to_json(self) -> str:
        """导出为 JSON 字符串"""
        return json.dumps(self.config, indent=2, ensure_ascii=False)


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description='JARVIS 配置管理工具')
    parser.add_argument('--config', '-c', help='配置文件路径')
    parser.add_argument('--get', '-g', help='获取配置项（支持点号分隔的路径）')
    parser.add_argument('--verify', '-v', action='store_true', help='验证配置路径')
    parser.add_argument('--pretty', '-p', action='store_true', help='美化输出配置')

    args = parser.parse_args()

    config = JavisConfig(args.config)

    if args.get:
        value = config.get(args.get)
        if isinstance(value, (dict, list)):
            print(json.dumps(value, indent=2, ensure_ascii=False))
        else:
            print(value)
    elif args.verify:
        results = config.verify_paths()
        print("路径验证结果:")
        for name, exists in results.items():
            status = "[OK]" if exists else "[X]"
            path = config.get(name + '_path' if name != 'config' else 'config_path')
            print(f"  {status} {name}: {path}")
    elif args.pretty:
        print(config.to_json())
    else:
        print(f"配置文件: {config.config_path}")
        print(f"版本: {config.get('version')}")
        print(f"语言: {config.get('language')}")
        print(f"会话模式: {config.get('session_mode')}")
        print(f"\n工作区路径: {config.get_workspace_path()}")
        print(f"项目路径: {config.get_javis_projects_path()}")


if __name__ == '__main__':
    main()
