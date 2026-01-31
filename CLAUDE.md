语言：中文

# 会话初始化规则

每次会话启动时，按以下顺序加载上下文：

1. **读取 JARVIS.md** - 理解工作区架构设计理念
2. **读取 memory/README.md** - 了解记忆系统结构
3. **检查 memory/session_history.md** - 查看最近的会话摘要
4. **检查 memory/user_preferences.md** - 了解当前用户偏好

# 核心工作原则

1. **记忆驱动**: 所有新知识都应记录到 memory/ 中对应的分类
2. **项目追踪**: 项目开发在 projects/active/ 中进行，完成后归档
3. **持续优化**: 发现架构不足时提出改进建议
4. **上下文连贯**: 重要决策和思考过程应被记录以便追溯

# 记忆更新触发条件

- 学习到新的技术知识 → 更新 memory/domain/
- 发现可复用的解决方案 → 更新 memory/patterns/
- 了解到用户偏好 → 更新 memory/user_preferences.md
- 完成重要项目 → 更新 projects/ 并记录到 memory/session_history.md
