#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全景图素材下载脚本 - 基于实际URL结构
"""

import requests
import time
from pathlib import Path

DOWNLOAD_DIR = Path("F:/workspace/3d_assets")
TIMEOUT = 30
DELAY = 1.0

def download_file(url, dest_path):
    """下载文件"""
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    if dest_path.exists():
        return True

    try:
        response = requests.get(url, timeout=TIMEOUT, stream=True)
        response.raise_for_status()

        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[OK] {dest_path.name}")
        time.sleep(DELAY)
        return True

    except Exception as e:
        print(f"[FAIL] {url} - {e}")
        return False

def download_forbidden_city():
    """
    下载全景故宫素材
    URL示例: https://pano.dpm.org.cn/panoramas/61/krpano/panos/3224_summer.tiles/l/l2/02/l2_l_02_02.jpg
    """
    print("\n" + "=" * 60)
    print("全景故宫下载")
    print("=" * 60)

    base_url = "https://pano.dpm.org.cn/panoramas/61/krpano/panos/3224_summer.tiles"
    save_dir = DOWNLOAD_DIR / "forbidden_city" / "3224_summer"

    faces = ["l", "r", "f", "b", "u", "d"]
    levels = [0, 1, 2]
    max_tiles = {0: (1, 1), 1: (2, 2), 2: (4, 4)}

    success = 0
    total = 0

    for level in levels:
        max_x, max_y = max_tiles[level]
        for face in faces:
            for x in range(max_x):
                for y in range(max_y):
                    # 格式: l2_l_02_02.jpg (level 2, left, x=02, y=02)
                    level_str = f"l{level}"
                    x_str = f"{x:02d}"
                    y_str = f"{y:02d}"
                    filename = f"{level_str}_{face}_{x_str}_{y_str}.jpg"

                    url = f"{base_url}/{face}/{level_str}/{x_str}/{filename}"
                    dest = save_dir / face / level_str / filename

                    total += 1
                    if download_file(url, dest):
                        success += 1

    print(f"\n全景故宫: {success}/{total} 成功")

def download_bigpixel():
    """
    下载千亿像素素材
    URL示例: https://pfm.bigpixel.cn/new_public/tilesource/budalagong/panos/bu.tiles/l/l03/2/l03_l_2_4.jpg
    """
    print("\n" + "=" * 60)
    print("千亿像素下载")
    print("=" * 60)

    base_url = "https://pfm.bigpixel.cn/new_public/tilesource/budalagong/panos/bu.tiles"
    save_dir = DOWNLOAD_DIR / "bigpixel_lasa"

    faces = ["l", "r", "f", "b", "u", "d"]
    levels = [0, 1, 2, 3]
    max_tiles = {0: (1, 1), 1: (2, 2), 2: (4, 4), 3: (8, 8)}

    success = 0
    total = 0

    # 下载预览图
    preview_url = f"{base_url}/preview.jpg"
    if download_file(preview_url, save_dir / "preview.jpg"):
        success += 1
    total += 1

    for level in levels:
        max_x, max_y = max_tiles[level]
        for face in faces:
            for x in range(max_x):
                for y in range(max_y):
                    # 格式: l03_l_2_4.jpg (level 3, left, x=2, y=4)
                    level_str = f"l0{level}" if level < 10 else f"l{level}"
                    filename = f"{level_str}_{face}_{x}_{y}.jpg"

                    url = f"{base_url}/{face}/{level_str}/{x}/{filename}"
                    dest = save_dir / "tiles" / face / level_str / filename

                    total += 1
                    if download_file(url, dest):
                        success += 1

    print(f"\n千亿像素: {success}/{total} 成功")

if __name__ == '__main__':
    print("=" * 60)
    print("全景图素材下载工具")
    print("=" * 60)

    # 下载全景故宫
    download_forbidden_city()

    # 下载千亿像素
    download_bigpixel()

    print("\n" + "=" * 60)
    print("下载完成！")
    print(f"保存位置: {DOWNLOAD_DIR.absolute()}")
    print("=" * 60)
