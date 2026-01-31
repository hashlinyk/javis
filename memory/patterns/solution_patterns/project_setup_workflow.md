# 项目启动工作流程

## 概述

这是在 JARVIS 工作区中启动新项目的标准工作流程，确保项目管理的一致性和可追溯性。

## 标准流程

```
1. 创建 GitHub 仓库
   ↓
2. 添加为 git submodule 到 active/
   ↓
3. 初始化项目结构
   ↓
4. 提交并推送
   ↓
5. 更新父仓库引用
   ↓
6. 记录到记忆系统
```

## 详细步骤

### 1. 创建 GitHub 仓库

使用 `gh` CLI 创建仓库：

```bash
cd F:/javis_projects/active

# 创建公开仓库
gh repo create <repo-name> --public --description "<描述>" --confirm

# 创建私有仓库
gh repo create <repo-name> --private --description "<描述>" --confirm
```

**参数说明**:
- `<repo-name>`: 仓库名称（使用 kebab-case，如 `marriage-simulator`）
- `--public` / `--private`: 设置仓库可见性
- `--description`: 仓库描述
- `--confirm`: 跳过确认提示

### 2. 添加为 git submodule

```bash
cd F:/javis_projects/active
git submodule add https://github.com/<username>/<repo-name>.git <repo-name>
```

**注意**: 空仓库初始化时可能遇到 "branch yet to be born" 错误，这是正常的。

### 3. 初始化项目结构

```bash
cd F:/javis_projects/active/<repo-name>

# 初始化 git（如果子模块初始化失败）
git init
git checkout -b main
git remote add origin https://github.com/<username>/<repo-name>.git

# 创建项目文件（根据项目类型）
mkdir -p src docs tests
# 添加 README、.gitignore 等文件
```

### 4. 提交并推送

```bash
# 添加所有文件
git add -A

# 首次提交（遵循提交规范）
git commit -m "feat: 初始化项目

- 创建项目基础结构
- 添加 README 和配置文件

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# 推送到远程
git push -u origin main
```

### 5. 更新父仓库引用

```bash
cd F:/javis_projects/active

# 确保子模块被正确注册
git add -A
git commit -m "feat: 添加 <repo-name> 子模块

- 项目位于: https://github.com/<username>/<repo-name>.git

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# 推送到父仓库远程
git push
```

### 6. 记录到记忆系统

根据项目类型，更新相应的记忆文件：

- **新技能**: 更新 `skills/` 目录和 `memory/knowledge_base/index.md`
- **新工具**: 更新 `tools/` 目录和 `memory/best_practices/workspace_setup.md`
- **新项目**: 更新 `memory/session_history.md`

## 命名规范

### 仓库名称

| 类型 | 格式 | 示例 |
|------|------|------|
| 工具 | `kebab-case` | `my-tool` |
| 游戏 | `kebab-case` | `marriage-simulator` |
| 库 | `kebab-case` | `awesome-library` |

### 提交信息格式

```
<type>(<scope>): <subject>

[可选的详细说明]

[可选的引用]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## 常见问题

### Q: 空仓库添加为子模块时报错？

A: 空仓库需要先初始化并提交内容才能正确作为子模块。按照第3步操作即可。

### Q: 如何修改仓库可见性？

```bash
# 设为私有
gh repo edit <username>/<repo-name> --visibility private --accept-visibility-change-consequences

# 设为公开
gh repo edit <username>/<repo-name> --visibility public --accept-visibility-change-consequences
```

### Q: 子模块引用不正确？

```bash
# 移除错误引用
git rm --cached <repo-name>

# 重新添加
git submodule add https://github.com/<username>/<repo-name>.git <repo-name>
```

## 相关文档

- [Git Submodule 使用](/memory/domain/programming/git_submodule.md)
- [工作区设置最佳实践](/memory/best_practices/workspace_setup.md)
- [子模块管理工具](/tools/automation/submodule_manager.py)

## 相关标签

#workflow #project-management #git #github #submodule

---
*创建时间: 2026-01-31*
*更新时间: 2026-01-31*
