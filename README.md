# JARVIS Workspace

一个为智能代理设计的记忆驱动型工作区，支持持续知识积累和跨平台使用。

## 概述

JARVIS（Just A Really Very Intelligent System）是一个工作区架构，旨在支持长期记忆积累和智能成长。通过结构化的记忆系统、配置驱动的环境管理和工具化的辅助脚本，让每次会话都比上一次更"聪明"。

## 核心特性

- **记忆驱动**: 所有重要信息都存储在文件中，跨会话保持
- **跨平台支持**: 配置文件管理环境差异，支持 Windows/Linux/Mac
- **模块化设计**: 清晰的职责划分，易于维护和扩展
- **工具化辅助**: 简化常用操作，提高工作效率
- **Git Submodule**: 独立的项目版本控制

## 目录结构

```
workspace/
├── .javis/                    # JARVIS 配置
│   ├── config.json            # 主配置文件
│   └── README.md
├── memory/                    # 记忆系统
│   ├── knowledge_base/        # 知识库索引
│   ├── domain/               # 领域知识
│   ├── patterns/             # 解决方案模式
│   ├── best_practices/       # 最佳实践
│   ├── experiences/         # 实战经验
│   ├── user_preferences.md   # 用户偏好
│   └── session_history.md    # 会话历史
├── skills/                    # Agent Skills
├── tools/                     # 工具集
│   ├── automation/           # 自动化脚本
│   └── utilities/            # 实用工具
├── CLAUDE.md                 # 会话初始化规则
├── JARVIS.md                 # 架构说明
└── README.md                 # 本文件

javis_projects/               # 项目目录
├── active/                   # 活跃项目
└── archive/                  # 归档项目
```

## 快速开始

### 环境要求

- Python 3.7+
- Git
- Git Bash (Windows) 或终端 (Linux/Mac)

### 安装配置

1. **克隆仓库**:
```bash
git clone <repo-url> workspace
cd workspace
```

2. **创建配置文件**:
```bash
# .javis/config.json
{
  "version": "1.0",
  "workspace_path": "${CWD}",
  "javis_projects_path": "../javis_projects",
  "language": "zh-CN"
}
```

3. **验证配置**:
```bash
python tools/utilities/load_config.py --verify
```

4. **初始化子模块**:
```bash
cd javis_projects
git submodule update --init --recursive
```

### 验证安装

```bash
# 检查配置
python tools/utilities/load_config.py --verify

# 查看项目列表
python tools/automation/submodule_manager.py list --active

# 测试记忆系统
ls memory/domain/programming/
```

## 使用指南

### 项目管理

```bash
# 添加新项目
python tools/automation/submodule_manager.py add <url> <project-name>

# 归档项目
python tools/automation/submodule_manager.py archive <project-name>

# 更新项目
python tools/automation/submodule_manager.py update
```

### 配置管理

```bash
# 查看配置
python tools/utilities/load_config.py

# 获取配置项
python tools/utilities/load_config.py --get javis_projects_path

# 验证路径
python tools/utilities/load_config.py --verify
```

### 记忆系统

知识按以下分类组织：

| 分类 | 说明 | 目录 |
|------|------|------|
| 领域知识 | 技术文档、概念 | `memory/domain/` |
| 解决方案模式 | 可复用模式 | `memory/patterns/` |
| 最佳实践 | 编码、设计规范 | `memory/best_practices/` |
| 实战经验 | 经验教训 | `memory/experiences/` |

查看 [知识库索引](memory/knowledge_base/index.md) 了解完整内容。

## 文档

- **[JARVIS.md](JARVIS.md)** - 架构设计说明
- **[CLAUDE.md](CLAUDE.md)** - 会话初始化规则
- **[配置说明](.javis/README.md)** - 配置系统文档
- **[知识库](memory/knowledge_base/index.md)** - 记忆系统索引
- **[项目管理](javis_projects/README.md)** - Git Submodule 使用指南

## 工具列表

### 自动化脚本

| 工具 | 功能 |
|------|------|
| `memory_backup.py` | 备份记忆系统 |
| `submodule_manager.py` | 子模块管理 |

### 实用工具

| 工具 | 功能 |
|------|------|
| `load_config.py` | 配置加载器 |

详细文档见 [tools/README.md](tools/README.md)

## 架构设计

### 设计理念

1. **记忆驱动**: 所有知识持久化存储
2. **跨平台优先**: 配置驱动，无硬编码
3. **模块化**: 清晰的职责划分
4. **可追溯**: 记录决策和变更

### 关键组件

- **配置系统**: `.javis/config.json` + `load_config.py`
- **记忆系统**: `memory/` + 知识库索引
- **工具系统**: `tools/` 自动化和实用工具
- **技能系统**: `skills/` Agent Skills

了解架构细节见 [JARVIS.md](JARVIS.md) 和 [memory/experiences/architecture_evolution.md](memory/experiences/architecture_evolution.md)。

## 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

MIT License

---

*创建时间: 2026-01-31*
