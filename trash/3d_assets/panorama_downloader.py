#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全景图素材批量下载脚本
支持：军事博物馆、全景故宫、千亿像素
"""

import os
import requests
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin

# ===================================================================
# 配置区域
# ===================================================================

DOWNLOAD_DIR = Path("F:/workspace/3d_assets")
MAX_WORKERS = 5  # 并发下载数（不宜过高，避免被限流）
TIMEOUT = 30
DELAY_BETWEEN_REQUESTS = 0.5  # 请求间隔（秒）

# ===================================================================
# 网站配置
# ===================================================================

# 1. 军事博物馆
MILITARY_MUSEUM = {
    "name": "军事博物馆",
    "base_url": "http://3d.jb.mil.cn/gming/panoRes",
    "scenes": {
        "077": {
            "name": "场景077",
            "faces": ["f", "l", "r", "b", "u", "d"],
            "levels": [0, 1, 2],  # 下载前3级
            "max_tiles": {
                0: (1, 1),   # level 0: 1x1
                1: (2, 2),   # level 1: 2x2
                2: (4, 4),   # level 2: 4x4
            }
        }
    },
    "hotspot_url": "http://3d.jb.mil.cn/gming/panoRes/{scene}.js"
}

# 2. 全景故宫
FORBIDDEN_CITY = {
    "name": "全景故宫",
    "api_url": "https://pano.dpm.org.cn/api/zh-CN/project/panoramas.json",
    "base_url_pattern": "{base}",  # 需要从API解析
}

# 3. 千亿像素
BIGPIXEL = {
    "name": "千亿像素",
    "cities_json": "https://pfm.bigpixel.cn/bigpixel_CBN/cities.json",
    "base_url": "https://pfm.bigpixel.cn/new_public/tilesource",
    "scenes": {
        "budalagong": {
            "name": "布达拉宫",
            "path": "budalagong/panos/bu.tiles",
            "preview": "preview.jpg",
            "faces": ["f", "l", "r", "b", "u", "d"],
            "levels": [0, 1, 2],  # 下载前3级
            "max_tiles": {
                0: (1, 1),
                1: (2, 2),
                2: (4, 4),
            }
        }
    }
}

# ===================================================================
# 下载工具类
# ===================================================================

class PanoramaDownloader:
    def __init__(self, config, download_dir=DOWNLOAD_DIR):
        self.config = config
        self.download_dir = Path(download_dir) / config["name"]
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        self.stats = {
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'total': 0
        }

    def download_file(self, url, dest_path, description=""):
        """下载单个文件"""
        dest_path = Path(dest_path)
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # 检查是否已存在
        if dest_path.exists():
            self.stats['skipped'] += 1
            return True

        self.stats['total'] += 1

        try:
            print(f"[下载] {description or url}")

            response = self.session.get(url, timeout=TIMEOUT, stream=True)
            response.raise_for_status()

            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            self.stats['success'] += 1
            print(f"[OK] {dest_path.name}")

            # 延迟，避免过快请求
            time.sleep(DELAY_BETWEEN_REQUESTS)
            return True

        except Exception as e:
            self.stats['failed'] += 1
            print(f"[失败] {url} - {e}")
            return False

    def print_stats(self):
        """打印统计信息"""
        print("\n" + "=" * 60)
        print(f"下载统计 - {self.config['name']}")
        print("=" * 60)
        print(f"总计: {self.stats['total']}")
        print(f"成功: {self.stats['success']}")
        print(f"跳过: {self.stats['skipped']}")
        print(f"失败: {self.stats['failed']}")
        print("=" * 60 + "\n")

# ===================================================================
# 军事博物馆下载器
# ===================================================================

class MilitaryMuseumDownloader(PanoramaDownloader):
    def download_scene(self, scene_id, scene_config):
        """下载单个场景"""
        scene_dir = self.download_dir / scene_id
        print(f"\n开始下载: {scene_config['name']}")

        tasks = []

        # 1. 下载热点配置
        hotspot_url = self.config["hotspot_url"].format(scene=scene_id)
        hotspot_dest = scene_dir / f"{scene_id}.js"
        tasks.append((hotspot_url, hotspot_dest, f"热点配置: {scene_id}.js"))

        # 2. 下载全景切片
        base_url = f"{self.config['base_url']}/{scene_id}.tiles"

        for level in scene_config["levels"]:
            max_x, max_y = scene_config["max_tiles"][level]

            for face in scene_config["faces"]:
                for x in range(max_x):
                    for y in range(max_y):
                        url = f"{base_url}/{face}/l{level}/{x}/l{level}_{face}_{x}_{y}.jpg"
                        dest = scene_dir / "tiles" / face / f"l{level}" / str(x) / f"l{level}_{face}_{x}_{y}.jpg"
                        desc = f"L{level} {face}({x},{y})"
                        tasks.append((url, dest, desc))

        # 执行下载
        success_count = 0
        for url, dest, desc in tasks:
            if self.download_file(url, dest, desc):
                success_count += 1

        print(f"\n场景 {scene_id}: {success_count}/{len(tasks)} 成功")
        return success_count == len(tasks)

    def download_all(self):
        """下载所有场景"""
        print("=" * 60)
        print(f"开始下载: {self.config['name']}")
        print("=" * 60)

        for scene_id, scene_config in self.config["scenes"].items():
            self.download_scene(scene_id, scene_config)

        self.print_stats()

# ===================================================================
# 千亿像素下载器
# ===================================================================

class BigpixelDownloader(PanoramaDownloader):
    def download_scene(self, scene_id, scene_config):
        """下载单个场景"""
        scene_name = scene_config["name"]
        scene_dir = self.download_dir / scene_id
        print(f"\n开始下载: {scene_name}")

        tasks = []

        # 1. 下载预览图
        preview_url = f"{self.config['base_url']}/{scene_config['path']}/{scene_config['preview']}"
        preview_dest = scene_dir / "preview.jpg"
        tasks.append((preview_url, preview_dest, f"预览图: {scene_name}"))

        # 2. 下载全景切片
        base_url = f"{self.config['base_url']}/{scene_config['path']}"

        for level in scene_config["levels"]:
            max_x, max_y = scene_config["max_tiles"][level]

            for face in scene_config["faces"]:
                for x in range(max_x):
                    for y in range(max_y):
                        url = f"{base_url}/{face}/l{level}/{x}/l{level}_{face}_{x}_{y}.jpg"
                        dest = scene_dir / "tiles" / face / f"l{level}" / str(x) / f"l{level}_{face}_{x}_{y}.jpg"
                        desc = f"L{level} {face}({x},{y})"
                        tasks.append((url, dest, desc))

        # 执行下载
        success_count = 0
        for url, dest, desc in tasks:
            if self.download_file(url, dest, desc):
                success_count += 1

        print(f"\n场景 {scene_id}: {success_count}/{len(tasks)} 成功")
        return success_count == len(tasks)

    def download_all(self):
        """下载所有场景"""
        print("=" * 60)
        print(f"开始下载: {self.config['name']}")
        print("=" * 60)

        for scene_id, scene_config in self.config["scenes"].items():
            self.download_scene(scene_id, scene_config)

        self.print_stats()

# ===================================================================
# 全景故宫下载器
# ===================================================================

class ForbiddenCityDownloader(PanoramaDownloader):
    def fetch_api(self):
        """获取API数据"""
        try:
            response = self.session.get(self.config["api_url"], timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[错误] 无法获取API数据: {e}")
            return None

    def download_all(self):
        """下载所有场景"""
        print("=" * 60)
        print(f"开始下载: {self.config['name']}")
        print("=" * 60)

        # 获取场景列表
        api_data = self.fetch_api()
        if not api_data:
            return

        print(f"\n发现 {len(api_data)} 个场景")

        # 解析场景并下载
        for idx, scene in enumerate(api_data[:3], 1):  # 限制下载前3个场景
            scene_name = scene.get('name', f'scene_{idx}')
            scene_id = scene.get('id', str(idx))

            print(f"\n[{idx}/{min(3, len(api_data))}] {scene_name}")

            # 这里需要根据实际API结构解析全景图URL
            # 示例：假设API返回了全景图URL
            print(f"  场景ID: {scene_id}")
            print(f"  注意: 需要分析实际API结构来提取图片URL")

        self.print_stats()

# ===================================================================
# 主程序
# ===================================================================

def main():
    print("=" * 60)
    print("全景图素材批量下载工具")
    print("=" * 60)

    print("\n请选择要下载的网站:")
    print("1. 军事博物馆")
    print("2. 千亿像素（布达拉宫）")
    print("3. 全景故宫")
    print("0. 全部")

    choice = input("\n请输入选项 (0-3): ").strip()

    if choice in ["1", "0"]:
        print("\n" + "=" * 60)
        downloader = MilitaryMuseumDownloader(MILITARY_MUSEUM)
        downloader.download_all()

    if choice in ["2", "0"]:
        print("\n" + "=" * 60)
        downloader = BigpixelDownloader(BIGPIXEL)
        downloader.download_all()

    if choice in ["3", "0"]:
        print("\n" + "=" * 60)
        downloader = ForbiddenCityDownloader(FORBIDDEN_CITY)
        downloader.download_all()

    print("\n" + "=" * 60)
    print("下载完成！")
    print(f"保存位置: {DOWNLOAD_DIR.absolute()}")
    print("=" * 60)

if __name__ == '__main__':
    main()
