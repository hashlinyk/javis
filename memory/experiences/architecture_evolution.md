# 架构演进记录

## 概述

本文档记录 JARVIS 架构设计过程中的重要经验教训和决策记录，帮助理解架构演变的原因。

## 版本 0.1 - 初始设计（2026-01-31）

### 设计决策

**目标**: 建立支持长期记忆和持续成长的工作区架构。

**方案**:
- 使用 git submodule 管理 javis_projects
- 创建记忆系统框架（memory/）
- 建立 skills/ 目录

**结果**:
- ✅ 基础架构建立
- ✅ 记忆系统框架可用

### 遇到的问题

**问题 1**: 符号链接跨平台失效

```bash
# Windows 下创建的符号链接
workspace/javis_projects -> /f/javis_projects

# 在其他环境中无法正常工作
```

**原因**:
- 符号链接在不同环境（Git Bash、WSL、Windows、Linux）行为不一致
- 硬编码路径 `/f/javis_projects` 只在特定环境有效

**教训**:
- 符号链接不是跨平台的可靠方案
- 需要使用更灵活的路径管理方式

## 版本 0.5 - 配置系统引入（2026-01-31）

### 设计决策

**目标**: 解决跨平台路径问题，支持环境迁移。

**方案**:
- 创建 `.javis/` 配置目录
- 实现 `config.json` 配置文件
- 开发 `load_config.py` 配置加载器
- 支持路径变量 `${CWD}`, `${HOME}`, `${DEFAULT}`

**配置示例**:
```json
{
  "workspace_path": "${CWD}",
  "javis_projects_path": "${DEFAULT}",
  "language": "zh-CN"
}
```

### 结果

**成功**:
- ✅ 跨平台支持实现
- ✅ 路径不再硬编码
- ✅ 环境迁移变得简单

**待改进**:
- 配置文件需要手动创建
- 缺少配置验证机制

### 经验

**经验 1**: 配置驱动设计优于符号链接

| 方案 | 灵活性 | 跨平台 | 维护性 |
|------|--------|--------|--------|
| 符号链接 | ❌ | ❌ | ❌ |
| 配置文件 | ✅ | ✅ | ✅ |

**经验 2**: 相对路径比绝对路径更可移植

```json
// 好 - 相对路径
{
  "javis_projects_path": "../javis_projects"
}

// 可接受 - 带变量
{
  "javis_projects_path": "${DEFAULT}"
}

// 差 - 绝对路径
{
  "javis_projects_path": "F:\\javis_projects"
}
```

## 版本 0.8 - 工具化辅助（2026-01-31）

### 设计决策

**目标**: 简化 git submodule 的复杂操作。

**问题**:
```bash
# 移除子模块需要 4 步
git submodule deinit -f my-project
git rm -f my-project
rm -rf .git/modules/my-project
rm -rf my-project
```

**方案**: 创建 `submodule_manager.py` 辅助脚本

```python
# 一条命令完成
manager = SubmoduleManager()
manager.remove("my-project")
```

### 结果

**成功**:
- ✅ 操作简化，降低错误率
- ✅ 自动清理 .git/modules
- ✅ 统一的接口风格

**经验**:

**经验 3**: 复杂操作应该封装

| 操作类型 | 是否需要封装 | 理由 |
|----------|-------------|------|
| 单次命令 | ❌ | 简单，直接使用 |
| 多步骤流程 | ✅ | 容易出错，应封装 |
| 跨文件操作 | ✅ | 涉及多个文件，应封装 |
| 重复性操作 | ✅ | 提高效率 |

**经验 4**: 脚本应提供 CLI 和 API 两种接口

```python
# CLI 使用
python submodule_manager.py add <url> <name>

# API 使用
from submodule_manager import SubmoduleManager
manager = SubmoduleManager()
manager.add(url, name)
```

## 版本 1.0 - 架构稳定（2026-01-31）

### 最终架构

```
workspace/
├── .javis/config.json          # 配置系统
├── memory/                     # 记忆系统
│   ├── knowledge_base/
│   ├── domain/
│   ├── patterns/
│   ├── best_practices/
│   └── experiences/
├── tools/                      # 工具系统
│   ├── automation/
│   └── utilities/
└── skills/                     # 技能系统

javis_projects/                # 项目目录
├── active/                     # 活跃项目
└── archive/                    # 归档项目
```

### 关键改进

1. **移除符号链接依赖**: 使用配置文件管理路径
2. **陈旧知识更新规则**: `tools/arch_rules.md` 定义更新触发条件
3. **子模块管理工具**: 简化常用操作

### 架构决策总结

| 决策 | 方案 | 原因 |
|------|------|------|
| 路径管理 | 配置文件 | 跨平台支持 |
| 项目管理 | git submodule | 独立版本控制 |
| 工具组织 | 分类目录 | 清晰的职责划分 |
| 配置格式 | JSON | 简单、广泛支持 |

## 重要教训

### 教训 1: 早期就要考虑跨平台

不要假设只在一种环境中使用。即使是个人项目，未来也可能需要在其他环境中运行。

**反模式**:
```python
# Windows 专用
PROJECTS_PATH = "F:\\javis_projects"
```

**正模式**:
```python
# 跨平台
config = ConfigManager()
projects_path = config.get('javis_projects_path')
```

### 教训 2: 记录决策原因

决策原因比决策本身更重要。当未来需要回顾或修改时，了解"为什么这样设计"比"这是什么设计"更有价值。

```markdown
## 设计决策

**选择方案 A 而非方案 B 的原因**:
1. 原因 1: ...
2. 原因 2: ...

**未来可能的替代方案**:
- 如果出现条件 X，可以考虑方案 C
```

### 教训 3: 工具化重复操作

任何需要执行超过一次的操作都应该考虑工具化。即使只是几行命令，封装成工具也有助于：

- 减少错误
- 统一接口
- 便于维护
- 提高效率

### 教训 4: 保持文档同步

架构变更时，必须同步更新所有相关文档：

1. 检查 .md 文件中的路径引用
2. 更新 README 中的架构描述
3. 记录变更到 session_history.md
4. 添加陈旧引用检测（如果可能）

## 待观察问题

### 问题 1: 配置文件创建

当前配置文件需要手动创建，能否自动检测和生成？

**可能的方案**:
- 运行向导式初始化脚本
- 检测默认配置，自动生成

### 问题 2: 知识检索效率

随着知识库增长，如何快速找到相关知识？

**可能的方案**:
- 添加全文索引
- 实现标签云视图
- 关键词搜索优化

### 问题 3: 子模块协作

多人协作时，如何处理子模块的冲突和同步？

**可能的方案**:
- 定义子模块更新流程文档
- 添加冲突检测脚本
- 实现自动同步工具

## 相关标签

#architecture #experience #lessons-learned #evolution

---
*创建时间: 2026-01-31*
