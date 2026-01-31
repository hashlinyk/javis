# 工作区设置最佳实践

## 概述

本文档总结了工作区架构设计和维护的最佳实践，适用于需要长期维护的知识驱动型工作区。

## 架构设计原则

### 1. 清晰的分层

```
核心层
├── 配置系统        # 环境相关
├── 记忆系统        # 知识积累
├── 工具系统        # 自动化
└── 技能系统        # 能力扩展

应用层
├── 项目管理        # git submodule
├── 会话上下文      # session_history
└── 用户偏好        # user_preferences
```

### 2. 跨平台优先

**规则**: 避免硬编码路径，使用配置文件管理环境差异。

**错误示例**:
```python
PROJECTS_PATH = "F:\\javis_projects"  # 仅 Windows 有效
```

**正确示例**:
```python
config = ConfigManager()
projects_path = config.get('javis_projects_path')  # 跨平台
```

### 3. 可追溯性

所有重要决策和变更都应该被记录：

| 变更类型 | 记录位置 |
|----------|----------|
| 架构调整 | `memory/session_history.md` |
| 知识新增 | `memory/knowledge_base/index.md` |
| 用户偏好 | `memory/user_preferences.md` |
| 配置变更 | `.javis/config.json` + git commit |

## 记忆系统维护

### 知识分类原则

1. **domain/**: 领域知识（技术文档、概念）
2. **patterns/**: 可复用的解决方案模式
3. **best_practices/**: 最佳实践
4. **experiences/**: 实战经验和教训

### 知识添加流程

```
1. 识别知识类型
   ↓
2. 选择正确目录
   ↓
3. 编写内容（包含标签）
   ↓
4. 更新索引 (knowledge_base/index.md)
   ↓
5. 更新标签 (knowledge_base/tags.md)
   ↓
6. 提交到 git
```

### 内容编写规范

```markdown
# 标题

## 概述
简要说明主题

## 核心内容
详细描述

## 使用示例
```bash
# 命令示例
```

## 相关标签
#tag1 #tag2

---
*创建时间: YYYY-MM-DD*
```

## 配置管理

### 配置文件结构

```json
{
  "version": "版本号",
  "环境变量": "${VAR_NAME}",
  "配置项": "值"
}
```

### 配置更新流程

1. 修改 `.javis/config.json`
2. 运行验证脚本（如果有）
3. 更新相关文档
4. 提交到 git

### 环境适配清单

迁移到新环境时检查：

- [ ] 复制配置文件到新位置
- [ ] 更新路径变量
- [ ] 验证配置加载器
- [ ] 检查工具脚本路径
- [ ] 测试符号链接（如果使用）

## 项目管理

### Git Submodule 最佳实践

#### 添加项目

```bash
# 使用辅助脚本（推荐）
python tools/automation/submodule_manager.py add <url> <name>

# 或使用原生命令
cd javis_projects/active
git submodule add <url> <name>
```

#### 更新项目

```bash
# 更新所有子模块到父仓库记录的 commit
git submodule update --init --recursive

# 更新到远程最新
git submodule update --remote
```

#### 归档项目

```bash
# 使用辅助脚本
python tools/automation/submodule_manager.py archive <name>
```

### 子模块命名规范

| 类型 | 命名 | 示例 |
|------|------|------|
| 个人项目 | `kebab-case` | `my-tool` |
| 组织项目 | `org-project` | `anthropic-jarvis` |
| 实验项目 | `exp-*` | `exp-new-feature` |

## 工具开发

### 脚本组织结构

```
tools/
├── automation/        # 自动化脚本
│   ├── script.py
│   └── README.md      # 脚本使用说明
└── utilities/         # 实用工具
    ├── helper.py
    └── README.md
```

### 脚本编写规范

```python
#!/usr/bin/env python3
"""
脚本描述

详细说明脚本的功能、参数、使用方法。
"""

import argparse
from pathlib import Path

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='脚本描述')
    parser.add_argument('arg', help='参数说明')
    args = parser.parse_args()

    # 实现逻辑
    print(f"参数: {args.arg}")

if __name__ == '__main__':
    main()
```

### 文档要求

每个工具目录都应包含 README.md，说明：
- 工具列表
- 使用方法
- 依赖要求
- 示例代码

## 版本控制

### Git 提交规范

```
类型(范围): 描述

[可选详细说明]

[可选引用]
```

类型：
- `feat`: 新功能
- `fix`: 修复
- `docs`: 文档
- `refactor`: 重构
- `chore`: 构建/工具

示例：
```
feat(config): 添加配置系统支持跨平台

- 创建 .javis/config.json 配置文件
- 实现 load_config.py 配置加载器
- 更新 CLAUDE.md 支持配置初始化

Closes #1
```

### 分支策略

- `master`: 主分支，稳定版本
- `feature/*`: 功能分支
- `fix/*`: 修复分支

### .gitignore 规则

```
# 配置中的敏感信息（如果存在）
.javis/config.local.json

# IDE
.vscode/
.idea/

# 备份文件
*.bak
*~

# 临时文件
.tmp/
.cache/
```

## 安全考虑

### 敏感信息处理

1. **不要提交**:
   - API 密钥
   - 密码
   - 个人身份信息

2. **使用环境变量**:
   ```json
   {
     "api_key": "${API_KEY}"
   }
   ```

3. **配置文件分离**:
   - `config.json`: 公共配置（提交到 git）
   - `config.local.json`: 本地配置（不提交）

### 脚本安全

1. 避免执行外部命令时注入攻击
2. 验证用户输入
3. 使用绝对路径避免路径遍历
4. 设置适当的文件权限

## 常见问题

### Q1: 如何迁移到新环境？

**A**: 1. 克隆工作区仓库 2. 创建 `.javis/config.json` 配置文件 3. 运行 `tools/utilities/load_config.py --verify` 验证配置

### Q2: 子模块更新后代码丢失？

**A**: 子模块使用 commit hash 引用，更新到远程最新会切换到新的 commit。如果要保留修改，需要在子模块中提交并更新父仓库引用。

### Q3: 配置文件找不到？

**A**: 检查：
1. `.javis/config.json` 是否存在
2. 路径是否正确
3. 环境变量 `JARVIS_CONFIG` 是否设置

## 相关标签

#best-practices #workspace #configuration #git #maintenance

---
*创建时间: 2026-01-31*
