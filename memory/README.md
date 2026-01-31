# 记忆模块

这个目录是我的长期记忆存储，包含我所有的知识、经验和上下文信息。

## 一级披露 - 核心规则（必须优先遵守）

### 配置驱动设计
**禁止硬编码路径** - 所有路径必须通过配置系统解析
- 参考: `memory/patterns/config_driven_design.md`
- 配置文件: `.javis/config.json`
- 工具: `tools/utilities/load_config.py`

### 陈旧信息更新规则
**架构变更必须同步更新所有相关文档**
- 参考: `tools/arch_rules.md`
- 检查范围: 所有 .md 文件、配置文件、脚本中的硬编码路径

### 项目启动工作流程
**新项目必须按标准流程创建**
1. 创建 GitHub 仓库
2. 添加为 git submodule
3. 初始化项目结构
4. 提交并推送
5. 更新父仓库
6. 记录到记忆系统
- 参考: `memory/patterns/solution_patterns/project_setup_workflow.md`

---

## 目录结构

```
memory/
├── README.md              # 本文件 - 记忆模块说明
├── knowledge_base/        # 知识库索引系统
│   ├── README.md
│   ├── index.md          # 知识库主索引
│   └── tags.md           # 标签系统
├── user_preferences.md    # 用户偏好设置
├── session_history.md     # 会话历史摘要
├── domain/                # 领域专业知识
│   ├── programming/       # 编程相关知识
│   ├── system/           # 系统架构知识
│   └── security/         # 安全相关知识
├── patterns/             # 设计模式和解决方案
├── best_practices/       # 最佳实践
└── experiences/          # 实战经验和教训
```

## 使用原则

1. **持续性**: 每次会话都会自动加载这些记忆
2. **增量式**: 知识通过会话持续积累
3. **可追溯**: 重要决策和经验都被记录
4. **可检索**: 使用清晰的索引和标签系统

## 更新规则

- 学习新知识时更新对应的领域文件
- 了解用户偏好后更新 user_preferences.md
- 重要会话结束后更新 session_history.md
- **架构变更后必须按 tools/arch_rules.md 检查并更新所有陈旧引用**
