# 核心原则：Harness Engineering的本质

> 来源：awesome-harness-engineering Foundations章节 + best-of-Agent-Harnesses 核心定义

## 核心定义

### OpenAI的定义（Foundations第一条）
**Harness engineering** is the discipline of designing the scaffolding — context delivery, tool interfaces, planning artifacts, verification loops, memory systems, and sandboxes — that surrounds an AI agent and determines whether it succeeds or fails on real tasks.

This list focuses on the *harness*, not the model. Every component here exists because the model can't do it alone — and the best harnesses are designed knowing those components will become unnecessary as models improve.

### best-of-Agent-Harnesses的定义
An agent harness is the runtime that closes the loop between a stateless model and the outside world—managing perception, action, memory, and constraint enforcement—making it the de facto operating system of machine agency and, consequently, the layer where nearly all meaningful questions about AI autonomy, reliability, and control are actually resolved.

### Martin Fowler的三角模型
Three interlocking systems:
- **Context Engineering**: curating what the agent knows (what context is delivered)
- **Architectural Constraints**: deterministic linters and structural tests (what rules the agent must follow)
- **Entropy Management**: periodic agents that repair documentation drift (how the system self-heals)

### Anthropic的关键洞察
- "every harness component assumes the model can't do something; those assumptions expire"
- Harness setup alone can swing benchmarks by 5+ percentage points (2026 Agentic Coding Trends Report)

### best-of的核心论点：Harness为什么重要
Every prior wave of automation was constrained by brittleness: you scripted exact behavior, and when the world deviated, the system broke. Foundation models inverted that problem—they're flexible but directionless, stateless, and disconnected from anything real. The agent harness exists to bridge that gap.

Architecturally, it plays the role the kernel played in operating systems or the controller played in industrial robotics—mediating between raw capability and a messy environment—but with a critical difference: the "capability" it governs is general-purpose cognition.

## 核心心智模型提炼

### 模型1: 假设过期模型（Assumptions Expire）
**一句话**: 每个harness组件都基于"模型现在做不到某事"的假设，但这些假设会随模型进化而失效。

**证据**:
- Anthropic: "every harness component assumes the model can't do something; those assumptions expire"
- Anthropic Harness Design for Long-Running Apps: "harness design for sustained, multi-session development tasks"
- LangChain: "co-evolution warning — models trained with specific harnesses can become overfitted to those designs"

**应用**: 设计harness时，明确标注每个组件的"假设"，预判哪些会随模型进化消失。

**局限**: 难以预测模型进化速度；过度设计的"未来性"可能浪费资源。

---

### 模型2: 作为OS的Harness
**一句话**: Harness是AI agent的操作系统——调度资源、执行策略、保护边界、管理状态。

**证据**:
- best-of: "it plays the role the kernel played in operating systems or the controller played in industrial robotics"
- LangChain Anatomy of Agent Harness: five primitives (filesystem, code execution, sandbox, memory, context management)
- Martin Fowler: "harness engineers who design and maintain agent environments rather than inspecting individual outputs"

**应用**: 用OS设计的成熟原则（进程隔离、内存管理、系统调用接口）来设计harness。

**局限**: AI workload与传统计算有本质不同，直接借用OS隐喻可能产生误导。

---

### 模型3: 上下文即护城河（Context is Moat）
**一句话**: 在模型同质化时代，harness质量是差异化来源；尤其是上下文工程（什么信息、以什么结构、在什么时机送达）。

**证据**:
- Martin Fowler: context engineering as first of three interlocking systems
- awesome-harness-engineering: "progressive disclosure" as core pattern
- Context Engineering for Azure SRE Agent: "Intent Met" score rose from 45% to 75% on novel incidents
- best-of: "Harness quality—not just model quality—determines whether agents actually ship"

**应用**: 把上下文工程当作核心竞争优势持续投入，而非一次性配置。

**局限**: 上下文工程需要持续维护，与代码库和流程共同进化。

---

### 模型4: Feedforward + Feedback双环
**一句话**: Harness = 前馈引导（告诉agent怎么工作）+ 反馈修正（在输出到用户前拦截错误）。

**证据**:
- Birgitta Böckeler (Martin Fowler): "feedforward guides plus feedback sensors that self-correct before output reaches human eyes"
- Computational controls (linters, tests) vs inferential ones (LLM-as-judge)
- LangChain: "reasoning sandwich" concentrating maximum thinking at planning and verification phases

**应用**: 每个harness组件明确是前馈型还是反馈型，两者配对设计。

**局限**: 过度反馈修正导致agent失去自主性；前馈过度又失去适应性。

---

### 模型5: 框架- harness的区分
**一句话**: 框架提供抽象，harness提供约束；好harness知道自己要约束什么，而不是让模型自由发挥。

**证据**:
- awesome: "This list focuses on the harness, not the model"
- best-of Frameworks章节: n8n, LangChain, AutoGen, CrewAI — 这些是应用框架，不是harness
- awesome中的真正harness: SWE-agent, OpenHands, claude-mem — 专注于特定问题的约束和流程

**应用**: 选型时区分"我搭什么舞台"（框架）vs"我给演员什么规则"（harness）。

**局限**: 好的harness往往与特定框架绑定，迁移成本高。

## 关键引用

> "Better models make harnesses more important: more capabilities mean more failure modes, and production needs retry logic, fallbacks, and validation." — best-of-Agent-Harnesses

> "Harness quality—not just model quality—determines whether agents actually ship." — best-of-Agent-Harnesses

> "The term itself barely exists in formal literature yet, which should concern anyone who cares about AI governance, because the harness is where abstract alignment goals either get operationalized into concrete constraints or quietly don't." — best-of-Agent-Harnesses

## 信息来源
- awesome-harness-engineering Foundations章节（100+引用项目）
- best-of-Agent-Harnesses What is an agent harness / Why harnesses matter章节（101个排名项目）
- OpenAI Harness Engineering (https://openai.com/index/harness-engineering/)
- Martin Fowler Harness Engineering (https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
- Anthropic Building Effective Agents (https://www.anthropic.com/research/building-effective-agents)
- Anthropic Harness Design for Long-Running Apps (https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Azure SRE Agent Context Engineering (https://techcommunity.microsoft.com/blog/appsonazureblog/context-engineering-lessons-from-building-azure-sre-agent/4481200/)
