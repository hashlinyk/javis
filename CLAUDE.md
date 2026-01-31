语言：中文

# 会话初始化规则

每次会话启动时，按以下顺序加载上下文：

1. **读取配置** - 解析 `.javis/config.json` 获取环境路径和设置
2. **读取 JARVIS.md** - 理解工作区架构设计理念
3. **读取 memory/README.md** - 了解记忆系统结构
4. **检查 memory/session_history.md** - 查看最近的会话摘要
5. **检查 memory/user_preferences.md** - 了解当前用户偏好

## 环境路径说明

- **workspace_path**: 核心工作区路径（本目录）
- **javis_projects_path**: 项目目录路径，由配置文件指定（默认为 `../javis_projects`）

**重要**: 不再依赖符号链接，所有路径通过配置文件动态解析，支持跨平台使用。

## 配置文件位置

- 主配置: `.javis/config.json`
- 配置说明: `.javis/README.md`
- 配置工具: `tools/utilities/load_config.py`

如需在不同环境中使用，只需修改配置文件中的路径即可。

# 核心工作原则

1. **记忆驱动**: 所有新知识都应记录到 memory/ 中对应的分类
2. **项目追踪**: 项目开发在 `javis_projects_path/active/` 中进行（使用 git submodule），完成后归档
3. **持续优化**: 发现架构不足时提出改进建议
4. **上下文连贯**: 重要决策和思考过程应被记录以便追溯
5. **技能开发**: 创建和管理的 Agent Skills 放在 skills/ 目录
6. **跨平台支持**: 所有路径通过配置系统解析，避免硬编码

# 记忆更新触发条件

- 学习到新的技术知识 → 更新 memory/domain/ 和 memory/knowledge_base/index.md
- 发现可复用的解决方案 → 更新 memory/patterns/
- 了解到用户偏好 → 更新 memory/user_preferences.md
- 完成重要项目 → 记录到 memory/session_history.md
- 创建新 Agent Skill → 添加到 skills/ 目录
