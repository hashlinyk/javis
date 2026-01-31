# JARVIS - 工作区架构说明

## 概述

这是我的"大脑"架构 - 一个设计用于支持持续记忆积累和智能成长的文件系统结构。

## 核心设计理念

1. **持久化记忆**: 所有重要信息都存储在文件中，跨会话保持
2. **结构化知识**: 使用层次化的分类系统组织信息
3. **增量式成长**: 每次会话都向知识库添加新内容
4. **可追溯性**: 记录决策历史和经验教训
5. **跨平台支持**: 使用配置系统管理环境差异，不依赖硬编码路径

## 目录结构

```
workspace/                          # JARVIS 核心工作区（本仓库）
├── .claude/                       # Claude Code 配置
│   └── settings.local.json
├── .git/                          # 工作区版本控制
├── .javis/                        # JARVIS 配置
│   ├── config.json                # 主配置文件
│   └── README.md
├── memory/                        # 核心记忆模块
│   ├── README.md
│   ├── knowledge_base/            # 知识库索引系统
│   │   ├── README.md
│   │   ├── index.md              # 知识库主索引
│   │   └── tags.md               # 标签系统
│   ├── user_preferences.md
│   ├── session_history.md
│   ├── domain/                   # 领域知识
│   ├── patterns/                 # 解决方案模式
│   ├── best_practices/           # 最佳实践
│   └── experiences/              # 实战经验
├── skills/                        # Agent Skills 管理
│   └── README.md
├── tools/                         # 工具集
│   ├── README.md
│   ├── arch_rules.md             # 架构规则
│   ├── automation/               # 自动化脚本
│   ├── utilities/                # 实用工具
│   └── integration/              # 集成工具
├── CLAUDE.md                      # 会话启动提示
└── JARVIS.md                      # 本文件

F:\javis_projects/                 # 独立的项目管理目录（使用 git submodule）
├── .git/                          # 主仓库版本控制
├── .gitignore
├── .gitattributes
├── .gitmodules                    # 子模块配置
├── README.md
├── references/                    # 参考文档
│   └── AgentSkills介绍.md
├── active/                        # 活跃项目（作为 git submodule）
│   └── project-name/             # 每个项目是独立的 git 子模块
├── archive/                       # 归档项目（作为 git submodule）
│   └── project-name/             # 完成的项目
└── templates/                     # 项目模板（可选，作为独立仓库）
```

## 配置系统

JARVIS 使用 `.javis/config.json` 配置文件管理环境设置，支持跨平台使用。

### 配置文件位置

- 主配置: `.javis/config.json`
- 配置说明: `.javis/README.md`
- 配置工具: `tools/utilities/load_config.py`

### 环境变量

配置文件支持以下路径变量：
- `${CWD}` - 当前工作目录
- `${HOME}` - 用户主目录
- `${DEFAULT}` - 默认项目路径 (`${CWD}/../javis_projects`)

### 跨环境适配

在不同环境中使用时，只需修改配置文件中的路径即可，无需修改代码或文档。

## 工作流程

### 会话启动
1. 加载 CLAUDE.md 了解当前规则
2. 读取 JARVIS.md 理解架构
3. 查看 memory/knowledge_base/index.md 快速了解知识库
4. 检查 memory/session_history.md 查看最近的会话摘要
5. 检查 memory/user_preferences.md 了解当前用户偏好

### 知识积累
1. 遇到新知识 → 记录到 memory/domain/
2. 发现新模式 → 记录到 memory/patterns/
3. 学习最佳实践 → 记录到 memory/best_practices/
4. 重要经验教训 → 记录到 memory/experiences/

#### 项目管理

项目使用 **git submodule** 管理，每个项目都有独立的 git 仓库。

#### 创建新项目

**方法 1：从远程仓库添加**
```bash
cd javis_projects/active
git submodule add https://github.com/username/repo.git my-project
```

**方法 2：本地项目作为子模块**
```bash
# 首先在本地初始化项目
cd F:/somewhere/else
mkdir my-new-project
cd my-new-project
git init
# 添加文件并提交...

# 然后添加为子模块
cd F:/workspace/javis_projects/active
git submodule add F:/somewhere/else/my-new-project my-new-project
```

#### 子模块常用命令

```bash
# 更新子模块到最新提交
git submodule update --remote

# 初始化并克隆所有子模块
git submodule update --init --recursive

# 查看子模块状态
git submodule status

# 移除子模块
git submodule deinit my-project
git rm my-project
```

#### 归档项目

项目完成后，移动子模块到 `archive/`：

```bash
# 从 active 移除
git submodule deinit active/my-project
git rm active/my-project

# 添加到 archive
cd archive
git submodule add <url-or-path> my-project
```

## 成长指标

- 知识库条目数量
- 完成项目数量
- 解决问题模式库
- 用户偏好准确度

## 持续进化

这个架构会根据使用情况不断优化，目标是让每次会话都比上一次更"聪明"。
