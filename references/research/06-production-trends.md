# 生产基础设施、运维与2026趋势

> 来源：awesome-harness-engineering Production Infrastructure、Observability、Debugging章节 + best-of-Agent-Harnesses Related Resources

## 核心心智模型

### 模型1: Agent as Production Service（生产级Agent运维）
**一句话**: Agent从实验走向生产需要CI/CD、监控、on-call——是工程问题而非算法问题。

**证据**:
- awesome: AI Agent Cost Optimization Guide 2026: "loop/step limits, tool-call caps, per-run token budgets, wall-clock timeouts"
- awesome: "FinOps for Agents: Cost-per-Accepted-Outcome (CAPO) as the right unit economic metric"
- best-of: "State of Agent Engineering 2026" (LangChain 1300+ professionals survey): 57.3% have agents in production, 89% have observability, only 52% run evals
- Microsoft Azure SRE Agent: "35,000+ production incidents autonomously", time-to-mitigation 40.5h → 3min
- Meta Ranking Engineer Agent: "up to 17x speedup over PyTorch baselines with 100% correctness across 250 problems"

**应用**: 上生产前必须有：监控看板、cost tracking、eval套件、rollback机制。

**局限**: 监控成本可能超过agent成本；生产debug比训练时复杂得多。

---

### 模型2: CAPO（Cost-per-Accepted-Outcome）作为单位经济指标
**一句话**: Agent的真正成本不是token消耗，而是"被用户接受的产出"——所有优化都应指向CAPO下降。

**证据**:
- awesome: "FinOps for Agents: Loop Limits, Tool-Call Caps, and the New Unit Economics of Agentic SaaS"
- awesome: "Cost-per-Accepted-Outcome (CAPO) as the right unit economic metric — shifting cost measurement from tokens consumed to business value delivered"
- awesome: "Anthropic prompt caching (90% discount on cached tokens)"
- awesome: "model routing and caching (40-60% savings)"

**应用**: 
- 追踪每个harness配置的CAPO而非单次token消耗
- 对比无agent baseline vs 有agent的business outcome

**局限**: CAPO难以归因；很多收益是间接的。

---

### 模型3: Observability是Harness的感官系统
**一句话**: 没有trace的harness是黑盒——每一步决策、工具调用、上下文变化都需要被记录和追溯。

**证据**:
- awesome Observability & Tracing章节: LangSmith, AgentOps, AgentVista
- best-of: "State of Agent Engineering 2026": 89% have implemented observability while only 52% run evals
- awesome: "Quantifying Infrastructure Noise in Agentic Coding Evals" — container resource config alone produces 6+ percentage point swings
- LangChain middleware: after_tool_call hook for logging every tool invocation

**应用**: 从第一天就集成trace；trace数据是调优harness的唯一依据。

**局限**: Trace数据量大，存储成本高；过度trace影响性能。

---

### 模型4: Self-Healing Harness（自愈式Harness）
**一句话**: 生产harness应该能检测回归、自动归因、自动dispatch修复agent——把ops变成自动化的反馈环。

**证据**:
- awesome: "How My Agents Self-Heal in Production" (LangChain, April 3, 2026)
- awesome: "detect regressions, attribute whether the last deploy caused them, then dispatch a coding agent to open a fix PR automatically"
- awesome: Live-SWE-agent "self-evolving scaffold — the harness itself adapts based on failure signals"
- awesome: "Agents Learn Their Runtime: Interpreter Persistence as Training-Time Semantics" — runtime persistence is learned, must be honored at deployment

**应用**: 监控→检测→归因→修复PR形成闭环；每次失败都是harness改进的输入。

**局限**: 自愈可能掩盖根本问题；过度自动化修复导致失控。

---

### 模型5: Plan.md / Implement.md作为Harness Artifacts
**一句话**: 可信的harness将计划文档作为一等公民——Plan.md（Milestones+验证门）、Implement.md（决策日志）是harness与agent共享的记忆。

**证据**:
- OpenAI: "Plan.md, Implement.md, Documentation.md as reusable harness artifacts"
- OpenAI Run Long-Horizon Tasks with Codex: "introduces Plan.md, Implement.md, Documentation.md as reusable harness artifacts"
- awesome: "Long-horizon task planning: introduces Plan.md, Implement.md, Documentation.md"
- get-shit-done (62.9k): "goal-backward planning and wave-based execution over fresh context windows; avoids context rot by design"
- SWE-agent: "edit state, command execution, and issue-focused loop"

**应用**: 复杂任务创建Plan.md；每个milestone设验证门；Implement.md记录决策历史。

**局限**: 文档维护需要成本；过度文档化导致agent过度规划。

## 2026年行业趋势

来自 "State of Agent Engineering 2026" (LangChain, 1300+ professionals):
- 57.3% have agents in production (up from 51%)
- Quality is top barrier at 32%
- 89% have observability
- Only 52% run evals
- Model策略: 49% use multiple providers

来自 Anthropic 2026 Agentic Coding Trends Report:
- "harness setup alone can swing benchmarks by 5+ percentage points"
- Shift from single-agent to orchestrated multi-agent teams
- "agentic engineering platform" category emerging

## 关键引用
> "The discipline of designing the scaffolding — context delivery, tool interfaces, planning artifacts, verification loops, memory systems, and sandboxes" — OpenAI Harness Engineering

> "Harness quality—not just model quality—determines whether agents actually ship" — best-of-Agent-Harnesses

## 信息来源
- awesome-harness-engineering: Production Infrastructure & Operations, Observability & Tracing, Debugging & Developer Experience, Planning & Task Decomposition章节
- best-of-Agent-Harnesses: Related Resources
- State of Agent Engineering 2026 (LangChain)
- 2026 Agentic Coding Trends Report (Anthropic)
- FinOps for Agents (InfoWorld)
- How My Agents Self-Heal in Production (LangChain, April 2026)
