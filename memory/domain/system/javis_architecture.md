# JARVIS 架构

## 概述

JARVIS 是一个为智能代理设计的记忆驱动工作区架构，支持持续知识积累和跨平台使用。

## 核心设计理念

### 1. 记忆驱动

所有重要信息和上下文都存储在文件中，跨会话保持。通过结构化的记忆系统，每次会话都能利用历史积累的知识。

### 2. 跨平台支持

使用配置文件而非硬编码路径，支持在不同操作系统间快速切换。

### 3. 模块化设计

工作区划分为独立的功能模块，职责清晰，易于维护。

## 目录结构

```
workspace/                          # 核心工作区
├── .claude/                       # Claude Code 配置
├── .javis/                        # JARVIS 配置
│   ├── config.json                # 主配置文件
│   └── README.md                  # 配置说明
├── memory/                        # 记忆系统
│   ├── knowledge_base/            # 知识库索引
│   │   ├── index.md               # 主索引
│   │   └── tags.md                # 标签系统
│   ├── domain/                    # 领域知识
│   │   ├── programming/           # 编程知识
│   │   ├── system/                # 系统知识
│   │   └── security/              # 安全知识
│   ├── patterns/                  # 解决方案模式
│   ├── best_practices/            # 最佳实践
│   ├── experiences/               # 实战经验
│   ├── user_preferences.md        # 用户偏好
│   └── session_history.md         # 会话历史
├── skills/                        # Agent Skills
├── tools/                         # 工具集
│   ├── automation/                # 自动化脚本
│   │   ├── memory_backup.py
│   │   └── submodule_manager.py
│   └── utilities/                 # 实用工具
│       └── load_config.py
├── CLAUDE.md                      # 会话初始化规则
└── JARVIS.md                      # 架构说明

javis_projects/                    # 项目目录
├── .gitmodules                    # Submodule 配置
├── active/                        # 活跃项目（子模块）
└── archive/                       # 归档项目（子模块）
```

## 配置系统

### config.json 配置项

```json
{
  "version": "1.0",
  "workspace_path": "${CWD}",
  "javis_projects_path": "${DEFAULT}",
  "language": "zh-CN",
  "session_mode": "javis-assistant",
  "auto_backup": {
    "enabled": true,
    "schedule": "daily",
    "max_backups": 7
  }
}
```

### 路径变量

- `${CWD}`: 当前工作目录
- `${DEFAULT}`: 默认项目路径 (`${CWD}/../javis_projects`)
- `${HOME}`: 用户主目录

### 环境适配

**Windows**:
```json
{
  "javis_projects_path": "F:\\javis_projects"
}
```

**Linux/Mac**:
```json
{
  "javis_projects_path": "/home/user/javis_projects"
}
```

**相对路径（推荐）**:
```json
{
  "javis_projects_path": "../javis_projects"
}
```

## 会话初始化流程

1. **加载配置**: 读取 `.javis/config.json`，解析环境路径
2. **理解架构**: 读取 `JARVIS.md` 了解整体设计
3. **记忆上下文**: 读取 `memory/README.md` 了解记忆系统
4. **历史回顾**: 检查 `memory/session_history.md` 查看近期会话
5. **用户偏好**: 检查 `memory/user_preferences.md` 了解用户习惯

## 记忆更新规则

知识更新遵循以下触发条件：

| 触发条件 | 更新目标 |
|----------|----------|
| 学习新知识 | `memory/domain/` + `knowledge_base/index.md` |
| 发现新模式 | `memory/patterns/` |
| 用户偏好 | `memory/user_preferences.md` |
| 完成项目 | `memory/session_history.md` |
| 创建 Skill | `skills/` 目录 |

## 陈旧知识处理

架构变更时的处理规则记录在 `tools/arch_rules.md`，包括：

- 目录重命名/移动时的检查清单
- 文件删除时的引用清理
- 架构调整时的文档同步
- Git 配置变更的说明更新

## 工具系统

### 自动化脚本

| 脚本 | 功能 |
|------|------|
| `memory_backup.py` | 备份记忆系统 |
| `submodule_manager.py` | 简化 git submodule 操作 |

### 实用工具

| 工具 | 功能 |
|------|------|
| `load_config.py` | 跨平台配置加载器 |

## 项目管理策略

### Git Submodule 使用

- 每个项目作为独立的 git 子模块
- `active/` 目录存放活跃项目
- `archive/` 目录存放已完成项目
- 使用 `submodule_manager.py` 简化操作

### 项目生命周期

1. **创建**: 添加为子模块到 `active/`
2. **开发**: 独立提交、推送到远程
3. **完成**: 移动到 `archive/`

## 扩展性

架构设计支持以下扩展：

1. **新增记忆类别**: 在 `memory/` 下添加新目录
2. **新增工具**: 在 `tools/` 下添加新脚本
3. **新增技能**: 在 `skills/` 下创建新技能
4. **新增配置项**: 扩展 `config.json` 配置

## 相关标签

#architecture #workspace #cross-platform #memory-system #git-submodule

---
*创建时间: 2026-01-31*
