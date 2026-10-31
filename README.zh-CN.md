**语言：** [English](README.md) | 简体中文

# agent-doc-skills

**别再让你的 coding agent 每个会话都从零开始重新认识你的仓库。**

一组轻量的 Agent Skills（`doc-init`、`doc-update`、`doc-compact`），支持 **Claude Code**、**Codex CLI**、**Cursor** 和 **OpenCode**。它负责构建并维护可导航、省 token 的项目知识库。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![skills.sh](https://skills.sh/b/x0c/agent-doc-skills)](https://skills.sh/x0c/agent-doc-skills)

---

## 为什么用 `agent-doc-skills`？

在日渐增长的代码库上使用 AI 编程助手时，通常会遇到两件事：
1. **冷启动失忆：** 每个新会话都从零开始。agent 要烧掉大量时间和 token 跑 `grep`、读几十个文件，只为搞懂你的架构。
2. **指令膨胀：** 你把所有东西都塞进 `CLAUDE.md` 或 `AGENTS.md`。很快它就涨到 5 万+ token，污染上下文窗口，导致模型忽略关键规则。

**`agent-doc-skills` 用渐进式披露同时解决这两个问题：**
不再把每个文档都塞进每次会话，而是把根目录的 `AGENTS.md` / `CLAUDE.md` 做成一张**精简的路由表**，指向各领域的文档（`docs/`）。agent 只读当前任务真正需要的那一篇。

```text
你的项目
├── AGENTS.md / CLAUDE.md       <-- 小入口与路由表（每次都加载）
└── docs/
    ├── architecture.md         <-- 改系统设计时按需加载
    ├── api-contracts.md        <-- 动接口时按需加载
    └── testing-standards.md    <-- 写测试时按需加载
```

---

## 安装

需要 **Node.js**（装 `skills` CLI 用）和 **Python 3**（跑自带的本地盘点 / 链接检查辅助脚本用）。

```bash
npx skills add x0c/agent-doc-skills -g
```

装完后新开一个 agent 会话，让宿主加载 `doc-init`、`doc-update` 和 `doc-compact`。

> **提示：** 要在多个编程助手之间管理 skills？用 **[agentsync](https://github.com/x0c/agentsync)** 把 `~/.config/agentsync/skills/` 自动同步到 Claude Code、Cursor、Codex 等 15+ 个工具。

---

## 快速上手与工作流

直接在 coding agent 会话里用人话调用这些 skill：

| Skill | 什么时候用 | 在 agent 里输入的示例 |
| :--- | :--- | :--- |
| **`doc-init`** | **第 1 天 / 新仓库：** 从现有代码、README 和配置引导建立可导航的项目文档，或升级全局文档治理契约。 | `使用 doc-init，根据这个项目现有的权威资料建立文档体系。` |
| **`doc-update`** | **日常开发：** 完成功能或修完 bug 后，把可复用的发现和架构决策沉淀到对应的文档里。 | `使用 doc-update，把这次任务的可复用发现记录到对应的文档里。` |
| **`doc-compact`** | **清理 / 审计：** 无损压缩臃肿文档（保留硬规则、数字和例外），并修复坏掉的 Markdown 链接。 | `使用 doc-compact，审计并压缩这个项目的文档。` |

### 只读审计模式

想先看看 `doc-compact` 能发现什么、再决定动不动文件？要一次只读审计：

```text
使用 doc-compact 审计这个项目的文档，不要修改文件。
```

---

## 原理与安全保证

和泛泛的“总结一下这个仓库”提示词不同，`agent-doc-skills` 把结构化的 agent 执行流程和确定性的 Python 辅助脚本结合起来：

- **基于证据，不编造规格：** 自带辅助脚本先扫描仓库结构、Git 历史、代码信号和 Markdown 链接。缺证据就明确报告缺口，不会现编文档。
- **无损压缩（`doc-compact`）：** 保留确切的作用域、例外、数值阈值、证据和机器解析标记，只去掉废话。
- **安全的全局预设注入：** `doc-init` 探测真实存在的全局指令文件，保留你已有的自定义指令和相邻托管块。
- **不擅自拉起后台子代理：** skill 默认直接在你的主会话里执行，遵守宿主的权限和模型策略。

---

## 🧩 AI 编程工具链里的相关工具

如果你每天在多个 AI 编程助手之间切换，看看这套本地优先工具链的其余部分：

| 仓库 | 说明 |
| :--- | :--- |
| **[corral](https://github.com/corral-dev/corral)** | 在终端会话管理器里并排跑 Claude Code、Codex、OpenCode、Cursor 和 Pi，再从 iPhone 或 Mac 上继续。 |
| **[subswap](https://github.com/x0c/subswap)** | 查剩余额度，一键切换 Claude Code、Codex、Cursor、Kimi Code 和 OpenCode 的账号，不用反复登录。 |
| **[agentsync](https://github.com/x0c/agentsync)** | 以一份本地源统一同步 `AGENTS.md`、`CLAUDE.md`、skills 和 MCP 配置到各编程助手。 |
| **[sesskit](https://github.com/x0c/sesskit)** | 从磁盘解析、导出本地 Claude Code、Codex CLI 和 Cursor 会话记录文件。 |

## 许可证

[MIT](LICENSE)
