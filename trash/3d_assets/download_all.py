#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全景图素材批量下载脚本 - 直接执行版
"""

import os
import requests
import time
from pathlib import Path

# 配置
DOWNLOAD_DIR = Path("F:/workspace/3d_assets")
TIMEOUT = 30
DELAY = 0.5

# 军事博物馆配置
MILITARY_BASE = "http://3d.jb.mil.cn/gming/panoRes/077.tiles"
FACES = ["f", "l", "r", "b", "u", "d"]
LEVELS = [0, 1, 2]
MAX_TILES = {0: (1, 1), 1: (2, 2), 2: (4, 4)}

def download_file(url, dest_path):
    """下载文件"""
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    if dest_path.exists():
        print(f"[跳过] {dest_path.name}")
        return True

    try:
        print(f"[下载] {dest_path.name}")
        response = requests.get(url, timeout=TIMEOUT, stream=True)
        response.raise_for_status()

        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        time.sleep(DELAY)
        return True

    except Exception as e:
        print(f"[失败] {url} - {e}")
        return False

def download_military_museum():
    """下载军事博物馆素材"""
    save_dir = DOWNLOAD_DIR / "military_museum" / "077"
    print(f"\n保存目录: {save_dir}")

    success = 0
    total = 0

    # 下载热点配置
    hotspot_url = "http://3d.jb.mil.cn/gming/panoRes/077.js"
    if download_file(hotspot_url, save_dir / "077.js"):
        success += 1
    total += 1

    # 下载全景切片
    for level in LEVELS:
        max_x, max_y = MAX_TILES[level]
        for face in FACES:
            for x in range(max_x):
                for y in range(max_y):
                    url = f"{MILITARY_BASE}/{face}/l{level}/{x}/l{level}_{face}_{x}_{y}.jpg"
                    dest = save_dir / "tiles" / face / f"l{level}" / str(x) / f"l{level}_{face}_{x}_{y}.jpg"
                    total += 1
                    if download_file(url, dest):
                        success += 1

    print(f"\n军事博物馆: {success}/{total} 成功")

def download_bigpixel():
    """下载千亿像素素材"""
    base_url = "https://pfm.bigpixel.cn/new_public/tilesource/budalagong/panos/bu.tiles"
    save_dir = DOWNLOAD_DIR / "bigpixel_lasa"
    print(f"\n保存目录: {save_dir}")

    success = 0
    total = 0

    # 下载预览图
    preview_url = f"{base_url}/preview.jpg"
    if download_file(preview_url, save_dir / "preview.jpg"):
        success += 1
    total += 1

    # 下载切片
    for level in LEVELS:
        max_x, max_y = MAX_TILES[level]
        for face in FACES:
            for x in range(max_x):
                for y in range(max_y):
                    url = f"{base_url}/{face}/l{level}/{x}/l{level}_{face}_{x}_{y}.jpg"
                    dest = save_dir / "tiles" / face / f"l{level}" / str(x) / f"l{level}_{face}_{x}_{y}.jpg"
                    total += 1
                    if download_file(url, dest):
                        success += 1

    print(f"\n千亿像素: {success}/{total} 成功")

if __name__ == '__main__':
    print("=" * 60)
    print("全景图素材下载工具")
    print("=" * 60)

    # 下载军事博物馆
    download_military_museum()

    # 下载千亿像素
    download_bigpixel()

    print("\n" + "=" * 60)
    print(f"下载完成！保存位置: {DOWNLOAD_DIR.absolute()}")
    print("=" * 60)
