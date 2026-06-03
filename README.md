# Harness Engineering Framework Skill

> **Agent = Model + Harness（智能体 = 模型 + 驾驭层）**
>
> Harness Engineering（驾驭工程）是一门将 AI 智能体从「能跑」打磨到「能稳」的控制层设计学科——提高一次做对的概率，并让系统在偏离正轨时能自我修正。

---

## 这是什么

这是一个 Claude Skill，将 2026 年业界对「Harness Engineering」的共识沉淀成可调用的心智模型与决策启发式，覆盖 15 个核心主题：

- 前馈控制 vs 反馈控制
- 多智能体架构模式（Subagent / Skills / Handoffs / Router）
- 上下文是有限资源（注意力预算、渐进式披露）
- 生成器-评估器模式（GAN 启发）
- 长时任务模式（Initializer / Coding Agent / 特性清单）
- Trust 架构与 MCP 工具注解
- 安全沙箱（OS 级控制 / 致命三件套）
- 自验证与构建回路
- FinOps 与 CAPO 单元经济
- 评估框架（pass@k、Swiss Cheese）
- 调试与失败定位（AgentRx 9 类分类）

完整内容见 [`SKILL.md`](./SKILL.md)。

---

## 核心理念

AI 智能体强大但**非确定性**——它不了解你的上下文、以 token 思考、需要结构化引导才能稳定运行。一个好的驾驭层要同时做到两件事：

1. **提高一次性做对的概率**（前馈）
2. **出问题能自我修正，不让人类兜底**（反馈）

只用反馈 → 智能体重复犯同样的错；只用前馈 → 规则写了一堆，但永远不知道是否生效。两者必须配合。

---

## 15 个心智模型速览

| # | 模型 | 一句话 |
|---|------|--------|
| 1 | 前馈 vs 反馈 | 事前引导 vs 事后纠偏，二者缺一不可 |
| 2 | 多智能体架构 | 单体起步，按需扩展到 Subagent / Skills / Handoffs / Router |
| 3 | 计算型 vs 推理型控制 | 便宜确定的（lint/test）vs 贵但语义丰富的（AI review） |
| 4 | 转向回路 | 人类的职责是迭代驾驭层本身 |
| 5 | 监管类别 | 维护性 / 架构适配 / 行为——三者难度递增 |
| 6 | 上下文是有限资源 | 找最小集合的高信噪比 token，别一把塞 |
| 7 | 生成器-评估器 | 自我评估会偏宽容，分开两个智能体 |
| 8 | 长时智能体 | 跨上下文靠特性清单 + 进度文件 + 初始化智能体 |
| 9 | 可驾驭性 | 不是所有代码库都好驾驭，先改善「环境可供性」 |
| 10 | 信任架构 | 模型 / 驾驭层 / 工具 / 环境四层都需防护 |
| 11 | 安全沙箱 | 必须在 OS 层做强制控制，App 层会被绕 |
| 12 | 自验证回路 | 「看起来对了」≠「验证过了」——强制 build-verify 循环 |
| 13 | FinOps | 没有成本护栏，云账单就是真实的产品演示 |
| 14 | 评估框架 | 多层防御，每层都有孔，组合起来才有用 |
| 15 | 调试失败 | 用 9 类分类法定位问题，不要泛泛地「它挂了」 |

---

## 决策启发式

| 场景 | 启发式 |
|------|--------|
| 智能体反复犯同样的错 | 加一个计算型反馈传感器（lint / test） |
| 输出总像模板 | 在评估器里加权「原创性」；加约束规则 |
| 智能体过早宣布完成 | 强制要求证据清单 + 第三方评估器 |
| 上下文快满了 | 切到增量推进 + 上下文重置 |
| 新代码库，无驾驭层 | 从「维护性驾驭层」起步（最好实现） |
| 长时复杂任务 | 用生成器-评估器 + Planner 智能体 |
| 智能体无法自评 | 拆出独立的评估器，给明确评分标准 |
| 遗留代码库 | 优先改善「环境可供性」，让代码可被读懂 |
| 多个独立领域 | Subagent 模式 + 中心化编排 |
| 单智能体多专长 | Skills 模式 + 渐进式披露 |
| 顺序工作流有状态 | Handoffs 模式 |
| 不同垂直域，并行查询 | Router 模式 |
| 生产成本失控 | CAPO 追踪 + 循环/工具调用上限 |
| 多智能体协调 | A2A 协议做能力发现 |
| 工具访问涉敏感 | MCP 注解 + 运行时组合策略 |

---

## 表达 DNA

- **词汇**：feedforward / feedback / harness / sensor / guide / regulation / context engineering / ambient affordances / self-correction / CAPO / lethal trifecta / sprint contract
- **语气**：工程导向、精确、系统思维
- **结构**：分类对比、权衡对比、强调迭代而非一次性方案
- **隐喻**：赛博治理器、转向回路、注意力预算、GAN 架构、瑞士奶酪防御
- **确定性**：通常呈现权衡而非绝对规则，「it depends」是常态

---

## 反模式

- 把所有上下文一把塞，而不是精选高信噪比 token
- 只用反馈控制，没有前馈
- 默认 AI 生成的测试就够了，跳过人工验证
- 在缺乏「环境可供性」的代码库上硬上驾驭层
- 问题还没摸清就过度设计驾驭层
- 不带成本护栏就上线智能体（FinOps 失明）
- 忽略工具注解的信任级别

---

## 如何使用

这个 Skill 通过 `SKILL.md` 暴露给 Claude Code / Claude Agent SDK：

- **Claude Code**：在对话中通过 Skill 工具调用（`harness-engineer`）
- **SDK**：作为可注入的上下文，按需检索心智模型与决策启发式
- **人工阅读**：把 `SKILL.md` 当参考手册——遇到具体问题查对应章节

---

## 信息边界

诚实声明此 Skill 做不到的事：

- 无法保证智能体不会利用配置不当的驾驭层
- 无法消除人类监督的需要，尤其在陌生场景
- 无法让遗留代码库在没改善「环境可供性」前就可被驾驭
- 无法预测智能体行为——只能提高好结果的概率
- **行为驾驭层**（功能正确性）仍是未解决的难题
- MCP 注解是提示，不是强制——不能绝对信任
- FinOps 指标（CAPO）需要成熟的可观测性基础设施
- 智能体行为研究持续演进——此 Skill 反映 **2026 年 5 月** 的前沿

---

## 来源

主要来源（详见 `SKILL.md` 末尾）：

- Martin Fowler — Harness engineering for coding agent users
- Anthropic Engineering — Effective harnesses for long-running agents
- Anthropic Engineering — Harness design for long-running application development
- Anthropic Engineering — Effective context engineering for AI agents
- Anthropic Research — Trustworthy agents in practice
- OpenAI — Building effective agents
- LangChain — The Anatomy of an Agent Harness / Improving Deep Agents / Choosing Multi-Agent Architecture
- NVIDIA — Practical Security Guidance for Sandboxing Agentic Workflows
- Google Cloud — A developer's guide to production-ready AI agents
- Red Hat — Harness engineering for structured workflows
- MCP Blog — Tool Annotations as Risk Vocabulary
- InfoWorld — FinOps for agents
- SWE-agent — Agent-Computer Interfaces
- Mem0 — Production-Ready AI Agents with Scalable Long-Term Memory
- Awesome Cursor Rules

---

> 本 Skill 由 [女娲 · Skill 造人术](https://github.com/alchaincyf/nuwa-skill) 生成
> 创建者：[花叔](https://x.com/AlchainHust)
