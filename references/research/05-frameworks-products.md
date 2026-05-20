# 框架、产品与Reference Implementations

> 来源：awesome-harness-engineering Reference Implementations + best-of-Agent-Harnesses 完整分类

## 核心心智模型

### 模型1: Harness vs Framework vs Product的三层模型
**一句话**: 理解harness生态需要区分三层：框架（orchestration抽象）、harness配置（行为规则包）、产品（终端用户交付物）。

**证据**:
- best-of的三层分类：
  - **Frameworks**: n8n (189k), LangChain, AutoGen (58.1k), CrewAI (51.7k) — orchestration抽象
  - **Coding harness configs & SDKs**: superpowers (197k), everything-claude-code (187k), GStack (99.1k) — 行为规则包
  - **Coding agent products**: opencode (162k), Gemini CLI (104k), Codex (83.6k), OpenHands (74k) — 终端用户交付物
- awesome的Reference Implementations: Tutorials、Generators & Meta-Harnesses、Demo Harnesses

**应用**: 
- 学习阶段：从harness configs入手（superpowers, everything-claude-code）理解行为规则
- 开发阶段：用框架搭架子（LangGraph, AutoGen）
- 交付阶段：用产品或自己build产品

**局限**: 三层边界模糊；某些项目跨越多层（OpenHands既是产品又可配置）。

---

### 模型2: 框架的极简主义陷阱
**一句话**: 框架越重，harness越轻——好框架应该让自己消失，让harness规则成为主角。

**证据**:
- best-of: smolagents (~1k LOC core) vs LangChain (complex) — lean vs heavy
- best-of: AgentSilex "~300 lines of readable agent code" 作为最小可学习实现
- awesome: LangChain's "deepagents" = "LangGraph + planning tool + virtual filesystem + shell sandbox + subagent spawning"
- best-of评价: "slightly complex" vs "complex (product suite)" — 越复杂越难定制

**应用**: 优先选能让你改规则而非改框架代码的方案；避免over-engineered框架。

**局限**: 极简框架牺牲了生态集成；真实项目需要的功能最终还是要自己搭。

---

### 模型3: 产品化harness的工程成熟度
**一句话**: 成熟产品的harness配置（rules/skills）是经过大规模用户验证的行为模式，是高质量的起点而非终点。

**证据**:
- best-of: superpowers (197k stars) = "performance-oriented harness pack for Claude Code, Codex, OpenCode, Cursor"
- best-of: everything-claude-code (187k) = "28 specialized subagents, 119 reusable skills, 60 slash commands, 34 rules"
- best-of: awesome-cursorrules (39.6k stars) = "curated .cursorrules and skills that leverage Cursor's index-then-load model"
- best-of: GStack (99.1k) = "23 slash-command modes (CEO/eng/design review, QA, ship, browse, retro...)"

**应用**: 从成熟产品rules入手，按需剪裁，而非从零设计。

**局限**: 别人的workflow不一定适合你；盲目采用导致积累的技术债。

---

### 模型4: 开源协议是harness选择的隐性约束
**一句话**: Harness工具的许可证影响你能否闭源、是否需要回馈——license是选型的重要维度。

**证据**:
- best-of评分: ✅ (MIT/Apache/BSD/GPL) vs ⚠️ (Fair-code/Source-available) vs ❓ (No license)
- OpenHands: multi-license (⚠️)
- n8n: Fair-code (⚠️)
- mastra: Elastic-2.0 (⚠️)
- 大多数工具：MIT/Apache ✅

**应用**: 商业项目优先选MIT/Apache许可证；⚠️项目需要详细评估限制。

**局限**: 许可证复杂度高；同一个项目可能多license。

## Reference Implementations的分类价值

awesome-harness-engineering将Reference Implementations分为：
- **Tutorials & Educational**: 学习用，从零搭harness
- **Generators & Meta-Harnesses**: 自动生成harness配置的元工具
- **Demo Harnesses**: 可运行的参考实现
- **Adjacent Collections**: 相关但不直接属于harness的集合

## 框架对比速查

| 框架 | Stars | 复杂度 | 许可证 | 核心特点 |
|------|-------|--------|--------|---------|
| n8n | 189k | 复杂 | Fair-code | 工作流引擎 |
| AutoGen | 58.1k | 复杂 | CC-BY | Group chat, code exec |
| CrewAI | 51.7k | 复杂 | MIT | Role-based agents |
| LangGraph | - | 中等 | MIT | Graph-based state |
| OpenAI agents-python | 26.4k | 较简 | MIT | Handoffs, guardrails |
| smolagents | 27.4k | 较简 | Apache | Code-as-action |
| Semantic Kernel | 27.9k | 复杂 | MIT | Enterprise, multi-lang |
| Google ADK | 19.7k | 复杂 | Apache | Gemini-optimized |
| Mastra | 24k | 较简 | Elastic-2.0 | TypeScript-first |
| Letta | 22.8k | 较简 | MIT | Memory-first |

## 信息来源
- awesome-harness-engineering: Reference Implementations章节
- best-of-Agent-Harnesses: Frameworks、Coding harness configs & SDKs、Coding agent products、Libraries & SDKs章节
