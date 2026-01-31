# JARVIS - 工作区架构说明

## 概述

这是我的"大脑"架构 - 一个设计用于支持持续记忆积累和智能成长的文件系统结构。

## 核心设计理念

1. **持久化记忆**: 所有重要信息都存储在文件中，跨会话保持
2. **结构化知识**: 使用层次化的分类系统组织信息
3. **增量式成长**: 每次会话都向知识库添加新内容
4. **可追溯性**: 记录决策历史和经验教训

## 目录结构

```
workspace/                      # JARVIS 核心工作区（本仓库）
├── .claude/                   # Claude Code 配置
│   └── settings.local.json
├── memory/                    # 核心记忆模块
│   ├── README.md
│   ├── knowledge_base.md
│   ├── user_preferences.md
│   ├── session_history.md
│   ├── domain/               # 领域知识
│   ├── patterns/             # 解决方案模式
│   ├── best_practices/       # 最佳实践
│   └── experiences/          # 实战经验
├── tools/                     # 工具集
├── CLAUDE.md                  # 会话启动提示
└── JARVIS.md                  # 本文件

F:\javis_projects/             # 独立的项目管理目录（独立 git 仓库）
├── .git/                      # 独立的版本控制
├── .gitignore                 # 项目通用忽略规则
├── .gitattributes             # Git 属性配置
├── README.md
├── active/                    # 活跃项目
│   └── project-name/         # 每个项目可独立 git init
├── archive/                   # 归档项目
└── templates/                 # 项目模板
```

## 工作流程

### 会话启动
1. 加载 CLAUDE.md 了解当前规则
2. 读取 JARVIS.md 理解架构
3. 查看 memory/ 中最新的知识更新
4. 检查 projects/ 中的活跃项目

### 知识积累
1. 遇到新知识 → 记录到 memory/domain/
2. 发现新模式 → 记录到 memory/patterns/
3. 学习最佳实践 → 记录到 memory/best_practices/
4. 重要经验教训 → 记录到 memory/experiences/

### 项目管理
1. 新项目创建在 `F:\javis_projects/active/` 中
2. 每个项目独立 git 仓库，不与工作区混在一起
3. 完成后移动到 `F:\javis_projects/archive/` 中

## 成长指标

- 知识库条目数量
- 完成项目数量
- 解决问题模式库
- 用户偏好准确度

## 持续进化

这个架构会根据使用情况不断优化，目标是让每次会话都比上一次更"聪明"。
