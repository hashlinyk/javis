#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D场景素材批量下载脚本
"""

import os
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# 下载配置
DOWNLOAD_DIR = Path("F:/workspace/3d_assets")
MAX_WORKERS = 10
TIMEOUT = 30

# 千亿像素 - 布达拉宫配置
BIGPIXEL_CONFIG = {
    'name': '布达拉宫',
    'preview_url': 'https://pfm.bigpixel.cn/new_public/tilesource/budalagong/panos/bu.tiles/preview.jpg',
    'base_url': 'https://pfm.bigpixel.cn/new_public/tilesource/budalagong/panos/bu.tiles',
    'faces': ['f', 'l', 'r', 'b', 'u', 'd'],  # 前左后右上下
    'levels': [0, 1, 2],  # 下载前3个级别（更高级别文件太大）
    'max_tiles': {
        0: (1, 1),   # level 0: 1x1
        1: (2, 2),   # level 1: 2x2
        2: (4, 4),   # level 2: 4x4
    }
}

def download_file(url, dest_path, description=""):
    """下载单个文件"""
    try:
        dest_path = Path(dest_path)
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if dest_path.exists():
            print(f"[OK] Already exists: {description or dest_path.name}")
            return True

        print(f"[DOWNLOAD] {description or url}")
        response = requests.get(url, timeout=TIMEOUT, stream=True)
        response.raise_for_status()

        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[OK] Downloaded: {description or dest_path.name}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed: {url} - {e}")
        return False

def download_bigpixel_preview():
    """下载布达拉宫预览图"""
    config = BIGPIXEL_CONFIG
    dest_dir = DOWNLOAD_DIR / 'bigpixel_lasa'

    url = config['preview_url']
    dest = dest_dir / 'preview.jpg'

    return download_file(url, dest, f"布达拉宫预览图")

def download_bigpixel_tiles():
    """下载布达拉宫全景切片"""
    config = BIGPIXEL_CONFIG
    dest_dir = DOWNLOAD_DIR / 'bigpixel_lasa' / 'tiles'

    tasks = []

    for level in config['levels']:
        max_x, max_y = config['max_tiles'][level]

        for face in config['faces']:
            for x in range(max_x):
                for y in range(max_y):
                    # 构建URL: {base_url}/{face}/l{level}/{x}/l{level}_{face}_{x}_{y}.jpg
                    url = f"{config['base_url']}/{face}/l{level}/{x}/l{level}_{face}_{x}_{y}.jpg"

                    dest = dest_dir / face / f"l{level}" / str(x) / f"l{level}_{face}_{x}_{y}.jpg"

                    desc = f"布达拉宫 L{level} {face}({x},{y})"
                    tasks.append((url, dest, desc))

    # 并发下载
    success_count = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(download_file, url, dest, desc): (url, dest, desc)
                   for url, dest, desc in tasks}

        for future in as_completed(futures):
            if future.result():
                success_count += 1

    print(f"\nBudalagong tiles: {success_count}/{len(tasks)} successful")
    return success_count == len(tasks)

def download_all():
    """下载所有素材"""
    print("=" * 60)
    print("3D Assets Batch Download")
    print("=" * 60)

    results = {}

    # 1. 布达拉宫 - 预览图
    print("\n[1/2] Downloading Budalagong preview...")
    results['bigpixel_preview'] = download_bigpixel_preview()

    # 2. 布达拉宫 - 切片
    print("\n[2/2] Downloading Budalagong tiles...")
    results['bigpixel_tiles'] = download_bigpixel_tiles()

    print("\n" + "=" * 60)
    print("Download Complete!")
    print("=" * 60)

    for name, success in results.items():
        status = "[OK]" if success else "[FAIL]"
        print(f"{name}: {status}")

    print(f"\nAssets saved to: {DOWNLOAD_DIR.absolute()}")

if __name__ == '__main__':
    download_all()
