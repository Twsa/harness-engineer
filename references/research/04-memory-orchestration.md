# 记忆、状态与编排

> 来源：awesome-harness-engineering Memory & State、Task Runners & Orchestration章节 + best-of-Agent-Harnesses Multi-agent and orchestration章节

## 核心心智模型

### 模型1: 三层记忆架构
**一句话**: Agent需要三层记忆——工作记忆（当前session）、 эпизодический（跨session经验）、语义记忆（结构化知识）。

**证据**:
- awesome Memory章节: episodic/semantic memory from ICLR 2026 MemAgents Workshop
- Mem0 (56.1k stars): "user/org/session memory, retrieves on demand"
- awesome: MemAgents Workshop (ICLR 2026) covering episodic/semantic memory, knowledge graphs, retrieval pipelines
- claude-mem (76.6k stars): "captures everything an agent does during a session, AI-compresses it, and injects relevant context into future sessions"

**应用**: 架构设计时明确三层边界；不同类型信息走不同存储。

**局限**: 记忆压缩有信息损失；记忆越久，维护成本越高。

---

### 模型2: Session Bridging（会话桥接）
**一句话**: 长生命周期任务需要在会话之间传递状态——当前上下文、工作目录、进度快照。

**证据**:
- Anthropic Harness Design for Long-Running Apps: "Session bridging, feature lists, incremental progress, testing"
- awesome: "hibernation-and-wake checkpointing for resuming interrupted tasks without losing context"
- Meta Ranking Engineer Agent: "hibernate-and-wake checkpointing for resuming interrupted 6-hour tasks"
- Agentic AI trends: "multi-agent distributed systems with load balancing and auto-scaling"

**应用**: 长时间任务自动checkpoint；中断后从checkpoint恢复而非从头开始。

**局限**: Checkpoint存储成本；状态序列化可能丢失隐式上下文。

---

### 模型3: 编排拓扑决定行为（Orchestration Topology）
**一句话**: 多Agent系统的行为由拓扑决定——manager模式、 decentralized handoffs、hierarchical、group chat——选错拓扑是最常见的架构错误。

**证据**:
- OpenAI: "single-agent vs. multi-agent orchestration (manager vs. decentralized handoffs)"
- best-of: AutoGen (58.1k), CrewAI (51.7k), OpenAI agents-python (26.4k) — 不同拓扑对应不同框架
- CrewAI: role-based agents (roles, goals, backstories) in Crews
- OpenAI agents-python: "handoffs, guardrails, and multi-LLM routing; minimal surface so you own the loop"
- ADK: multi-agent topology, tool registration model, eval pipeline

**应用**: 简单任务用单Agent；需要分工用manager模式；独立并行用worker pool；需要协商用group chat。

**局限**: 拓扑选择受团队技能影响；复杂拓扑难以调试。

---

### 模型4: Human-in-the-Loop作为Harness原子
**一句话**: HITL不是可选项，是harness设计的核心维度——决定何时介入、介入多深、保持何种控制。

**证据**:
- awesome Human-in-the-Loop章节: 不同层次的human involvement
- best-of: Cline的"per-step human approval"
- Anthropic: "human control, value alignment, secure interactions, transparency, and privacy" (Trustworthy agents)
- awesome: "human-in-the-loop governance" for Azure SRE Agent (35,000+ production incidents)
- Anthropic: "trustworthiness as operationalized through five principles"

**应用**: 关键决策点（删除、部署、支付）必须引入HITL；日常操作可完全自主。

**局限**: 过度HITL失去agent效率优势；不同文化对HITL接受度不同。

## 关键引用
> "The agent harness is the de facto operating system of machine agency" — best-of-Agent-Harnesses

## 信息来源
- awesome-harness-engineering: Memory & State, Task Runners & Orchestration, Human-in-the-Loop章节
- best-of-Agent-Harnesses: Multi-agent and orchestration章节
- Mem0 (https://github.com/mem0ai/mem0)
- claude-mem (https://github.com/thedotmack/claude-mem)
- Anthropic Trustworthy agents (https://www.anthropic.com/research/trustworthy-agents)
