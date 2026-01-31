# Skills 管理

这里存放我创建和管理的 Agent Skills。

## 什么是 Agent Skills？

Agent Skills 是一种开放的格式，用于为智能代理提供新能力和专业知识。更多详细信息请参考：

- **知识文档**: `../memory/domain/programming/agent_skills.md`
- **原始文档**: `F:\javis_projects\references\AgentSkills介绍.md`

## 目录结构

```
skills/
├── README.md              # 本文件
└── [skill-name]/         # 具体的 skills
    ├── SKILL.md          # 必需：指令 + 元数据
    ├── scripts/          # 可选：可执行代码
    ├── references/       # 可选：文档
    └── assets/           # 可选：模板、资源
```

## 创建新 Skill

遵循以下步骤：

1. 创建技能目录：`mkdir skills/my-skill`
2. 创建 SKILL.md 文件，包含必需的 YAML 元数据
3. 编写技能指令
4. （可选）添加脚本、参考资料或资源文件

## SKILL.md 格式

```yaml
---
name: skill-name
description: 对此 skill 功能和使用时机的描述
---

# 技能说明

详细的指令内容...
```

字段要求：
- `name`: 1-64个字符，仅限小写字母、数字和连字符，必须与目录名匹配
- `description`: 1-1024个字符，描述功能和使用时机

## 使用

当需要使用某个 skill 时，我会自动加载对应的 `SKILL.md` 文件。
