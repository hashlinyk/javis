# Agent Skills

## 概述

Agent Skills 是一种简单、开放的格式，用于为智能代理提供新的能力和专业知识。它允许开发者将专门知识封装成可重复使用的指令包，使代理能够根据任务需要动态加载相关能力。

Agent Skills 本质上是包含 `SKILL.md` 文件的文件夹，该文件包含元数据（至少包括名称和描述）以及指导代理如何执行特定任务的指令。Skills 还可以捆绑脚本、模板和参考资料。

## 解决的核心问题

- **缺乏上下文**：代理越来越强大，但往往缺乏可靠完成实际工作所需的上下文
- **知识封装**：需要将过程性知识和特定于公司、团队、用户的上下文打包成可按需加载的格式
- **能力扩展**：代理需要能够基于正在处理的任务扩展其能力

## Skills 的结构

一个 skill 是一个包含 `SKILL.md` 文件的文件夹：

```
my-skill/
├── SKILL.md          # 必需：指令 + 元数据
├── scripts/          # 可选：可执行代码
├── references/       # 可选：文档
└── assets/           # 可选：模板、资源
```

## 工作机制：渐进式披露

1. **发现阶段**：在启动时，代理只加载每个可用 skill 的名称和描述
2. **激活阶段**：当任务与 skill 的描述匹配时，代理将完整的 `SKILL.md` 指令读入上下文
3. **执行阶段**：代理遵循指令，根据需要选择性加载引用文件或执行捆绑代码

## SKILL.md 文件格式

### 前置元数据（必需）

```yaml
---
name: skill-name
description: 对此 skill 功能和使用时机的描述
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
compatibility: 需要 git、docker、jq 和互联网访问
allowed-tools: Bash(git:*) Bash(jq:*) Read
---
```

### 字段规范

| 字段 | 必需 | 约束条件 |
|------|------|----------|
| `name` | 是 | 最多64个字符。仅限小写字母、数字和连字符。不能以连字符开头或结尾 |
| `description` | 是 | 最多1024个字符。非空。描述 skill 的功能和使用时机 |
| `license` | 否 | 许可证名称 |
| `compatibility` | 否 | 最多500个字符。指示环境要求 |
| `metadata` | 否 | 用于额外元数据的任意键值映射 |
| `allowed-tools` | 否 | skill 可使用的预批准工具的空格分隔列表 |

### name 字段要求

- 必须是1-64个字符
- 只能包含Unicode小写字母数字字符和连字符（a-z和-）
- 不能以-开头或结尾
- 不能包含连续连字符（--）
- 必须与父目录名匹配

### description 字段要求

- 必须是1-1024个字符
- 应该描述 skill 的功能和使用时机
- 应该包含帮助代理识别相关任务的特定关键字

## 可选目录

### scripts/

包含代理可以运行的可执行代码。脚本应该：
- 自包含或明确记录依赖关系
- 包含有用的错误消息
- 优雅地处理边缘情况

支持的语言：Python、Bash、JavaScript 等

### references/

包含代理在需要时可以读取的附加文档：
- `REFERENCE.md` - 详细技术参考
- `FORMS.md` - 表单模板或结构化数据格式
- 特定于域的文件

### assets/

包含静态资源：
- 模板（文档模板、配置模板）
- 图像（图表、示例）
- 数据文件（查找表、模式）

## Agent Skills 的功能

- **领域专业知识**：将专门知识打包成可重复使用的指令
- **新能力**：为代理提供新能力（如创建演示文稿、构建MCP服务器）
- **可重复的工作流程**：将多步骤任务转换为一致且可审计的工作流程
- **互操作性**：在不同兼容skills的代理产品中重用相同的skill

## 集成方式

### 集成方法

**基于文件系统的代理**：在计算机环境（bash/unix）中运行，通过shell命令激活Skills

**基于工具的代理**：通过实现专用工具来触发skills并访问捆绑资产

### 集成要求

1. **发现**：在配置目录中发现skills
2. **加载元数据**：在启动时加载名称和描述
3. **匹配**：将用户任务与相关skills匹配
4. **激活**：通过加载完整指令激活skills
5. **执行**：根据需要执行脚本和访问资源

### 元数据加载（XML 格式）

```xml
<available_skills>
  <skill>
    <name>pdf-processing</name>
    <description>从PDF文件中提取文本和表格，填写表单，合并文档。</description>
    <location>/path/to/skills/pdf-processing/SKILL.md</location>
  </skill>
</available_skills>
```

### 上下文管理策略

1. **元数据**（约100个tokens）：启动时为所有skills加载
2. **指令**（建议<5000个tokens）：激活skill时加载完整的`SKILL.md`正文
3. **资源**（按需）：只有在需要时才加载文件

**重要**：保持主要的`SKILL.md`在500行以下。

## 安全考虑

- **沙盒化**：在隔离环境中运行脚本
- **白名单**：只执行来自受信任skills的脚本
- **确认**：在运行潜在危险操作之前询问用户
- **日志记录**：记录所有脚本执行以便审计

## 生态系统支持

- Gemini CLI
- Autohand Code CLI
- OpenCode
- Cursor
- Claude Code
- GitHub
- VS Code

Agent Skills格式最初由Anthropic开发，作为开放标准发布。

## 参考工具

[skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref)参考库提供Python实用程序和CLI：

```bash
# 验证skill目录
skills-ref validate <path>

# 为代理提示生成<available_skills> XML
skills-ref to-prompt <path>...
```

## 文件引用规范

在skill中引用其他文件时，使用相对于skill根目录的路径：

```markdown
详情请参见[参考指南](references/REFERENCE.md)。
运行提取脚本：scripts/extract.py
```

保持文件引用距离`SKILL.md`一级深度。避免深层嵌套的引用链。

## 项目信息

GitHub: https://github.com/agentskills/agentskills

---
*来源: AgentSkills介绍.md (2026-01-31)*
