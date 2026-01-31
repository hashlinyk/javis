# Git Submodule

## 概述

Git Submodule 是 Git 的一个功能，允许将一个 Git 仓库作为子目录包含到另一个 Git 仓库中。每个子模块保持自己的 Git 历史，可以独立提交和更新。

## 核心概念

### 子模块的特点

- **独立仓库**: 每个子模块是一个完整的 Git 仓库
- **版本锁定**: 父仓库记录子模块的特定 commit hash
- **独立更新**: 子模块可以独立提交和更新
- **递归克隆**: 克隆时可以选择递克隆所有子模块

### 父仓库与子模块的关系

```
父仓库
├── .gitmodules        # 子模块配置文件
├── submodule-a/        # 子模块目录（只包含引用）
└── .git/
    └── modules/        # 子模块的实际存储
```

## 常用命令

### 添加子模块

```bash
# 添加远程仓库作为子模块
git submodule add https://github.com/user/repo.git submodule-name

# 添加本地仓库作为子模块
git submodule add /path/to/local/repo submodule-name
```

### 初始化和克隆

```bash
# 克隆包含子模块的仓库（不拉取子模块内容）
git clone https://github.com/user/main-repo.git

# 初始化并拉取所有子模块
git submodule update --init --recursive

# 一条命令克隆并初始化子模块
git clone --recursive https://github.com/user/main-repo.git
```

### 更新子模块

```bash
# 更新到父仓库记录的 commit
git submodule update --init

# 更新到子模块的最新 commit
git submodule update --remote

# 拉取子模块的最新更改（进入子模块目录后）
cd submodule-name
git pull origin main
```

### 查看状态

```bash
# 查看子模块状态
git submodule status

# 输出格式:
#  - 空格: 与 .gitmodules 中记录的 commit 一致
#  - +: commit 有新的更新
#  - -: commit 初始化未完成
#  - U: 子模块有冲突
```

### 移除子模块

```bash
# 1. 取消注册子模块
git submodule deinit -f submodule-name

# 2. 从 git 索引中移除
git rm -f submodule-name

# 3. 清理 .git/modules 中的子模块数据
rm -rf .git/modules/submodule-name

# 4. 删除未追踪的子模块文件
rm -rf submodule-name
```

## .gitmodules 文件

`.gitmodules` 文件记录子模块的配置：

```ini
[submodule "active/my-project"]
	path = active/my-project
	url = https://github.com/user/my-project.git
```

### 配置说明

- `submodule "路径"`: 子模块的唯一标识
- `path`: 子模块在父仓库中的路径
- `url`: 子模块的仓库地址

## 常见问题

### 子模块处于游离状态

当进入子模块目录时，Git 可能显示处于游离状态（detached HEAD）。这是正常的，因为子模块跟踪特定的 commit。

**解决方案**:
```bash
# 如果需要修改子模块，先创建分支
git checkout -b my-feature

# 修改后提交
git add .
git commit -m "修改内容"

# 更新父仓库的子模块引用
cd ..
git add submodule-name
git commit -m "更新子模块"
```

### 子模块 URL 变更

当子模块的远程地址变更时，需要更新 `.gitmodules`：

```bash
# 1. 编辑 .gitmodules 文件，更新 url
# 2. 同步配置
git submodule sync

# 3. 更新子模块
git submodule update --init --recursive
```

## JARVIS 中的使用

JARVIS 使用 Git Submodule 管理项目，实现：

1. **独立版本控制**: 每个项目有自己的 Git 历史
2. **灵活归档**: 项目完成后可以从 active/ 移动到 archive/
3. **独立协作**: 每个项目可以独立推送到远程仓库

### 推荐操作

使用 `tools/automation/submodule_manager.py` 简化操作：

```bash
# 添加项目
python tools/automation/submodule_manager.py add <url> <name>

# 归档项目
python tools/automation/submodule_manager.py archive <name>

# 更新项目
python tools/automation/submodule_manager.py update
```

## 相关标签

#git #version-control #submodule #project-management

---
*创建时间: 2026-01-31*
