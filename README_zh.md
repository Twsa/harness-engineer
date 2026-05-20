# Harness Engineering

> **从 [nuwa-skill](https://github.com/alchaincyf/nuwa-skill) 蒸馏而来**

这是构建可靠 AI Agent 的技能框架，源自 OpenAI、Anthropic、Microsoft、Meta、Google 等头部公司的 100+ 项目研究。

## 核心维度

| 维度 | 描述 |
|------|------|
| **Agent Loop** | 计划 → 行动 → 观察 → 调整 → 循环 |
| **Context Engineering** | 将上下文视为有限资源，注意边际收益递减 |
| **Verification** | 生成器和评价器必须分离 |
| **Memory** | 用结构化持久化替代人工记忆 |
| **Multi-Agent** | 编排拓扑比模型选择更重要 |
| **Production Patterns** | Harness 是模型与现实之间的"操作系统" |

## 快速开始

```bash
python fetch_sources.py
```

将来源材料从 Anthropic、OpenAI 等抓取到 `references/` 目录。

## 核心心智模型

- **Harness = AI 的操作系统**：负责 prompt 构建、工具调度、上下文管理、终止判断
- **Context Rot**：上下文窗口越满，注意力越稀释 — 静态内容放前面，可变内容放后面
- **GAN 式评估**：使用独立评价器和可量化的评分标准，而非自我评价

## 资源

- `SKILL.md` — 完整技能文档
- `fetch_sources.py` — 批量来源抓取工具（来源为 `references/` 目录）
- `references/` — 已下载的研究资料