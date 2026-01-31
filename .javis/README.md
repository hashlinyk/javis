# JARVIS 配置目录

这个目录存放 JARVS 的工作区配置文件。

## 文件说明

### config.json

主配置文件，包含以下配置项：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `workspace_path` | 工作区路径（相对于配置文件） | `${CWD}` (当前目录) |
| `javis_projects_path` | 项目目录路径 | `${DEFAULT}` (同级的 javis_projects) |
| `language` | 会话语言 | `zh-CN` |
| `session_mode` | 会话模式 | `javis-assistant` |
| `auto_backup` | 自动备份配置 | 见下方 |

### auto_backup 配置

| 配置项 | 说明 |
|--------|------|
| `enabled` | 是否启用自动备份 |
| `schedule` | 备份计划 (daily/weekly) |
| `max_backups` | 最大备份数量 |

## 路径变量

支持以下特殊变量：

- `${CWD}` - 当前工作目录
- `${DEFAULT}` - 默认值（javis_projects_path 默认为 `${CWD}/../javis_projects`）
- `${HOME}` - 用户主目录

## 环境适配

在不同环境中，配置文件会被自动解析：

### Windows
```json
{
  "javis_projects_path": "F:\\javis_projects"
}
```

### Linux/Mac
```json
{
  "javis_projects_path": "/home/user/javis_projects"
}
```

### 相对路径（推荐）
```json
{
  "javis_projects_path": "../javis_projects"
}
```

## 配置优先级

1. `.javis/config.json` (工作区配置)
2. 环境变量 `JARVIS_CONFIG`
3. 默认配置

---

*创建时间: 2026-01-31*
