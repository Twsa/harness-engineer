# 上下文工程、工具设计与MCP模式

> 来源：awesome-harness-engineering Context Delivery、Tool Design、Skills & MCP章节 + best-of-Agent-Harnesses Progressive disclosure harnesses

## 核心心智模型

### 模型1: Progressive Disclosure（渐进披露）
**一句话**: 先给地图，不给百科全书——索引优先，详细按需加载，控制token成本同时保证信息可用。

**证据**:
- awesome-harness-engineering: "map, not encyclopedia" principle
- best-of Progressive disclosure harnesses描述: "Formats, runtimes, and patterns that reveal context, tools, or instructions in layers—index first, details on demand"
- awesome cursorrules: 39.6k stars, leverage Cursor's index-then-load model
- agents.md (21.5k stars): "hierarchical scope and progressive disclosure so agents get a map of what exists, then load only what's relevant"
- Claude Code 5-stage progressive compaction: budget reduction → snip → microcompact → context collapse → auto-compact

**应用**: 每个项目用AGENTS.md做顶层索引，详细规则分散在skills目录，按需加载。

**局限**: 索引本身的维护需要成本；层次设计不当会导致agent找不到信息。

---

### 模型2: 工具即UX（Tool as UX）
**一句话**: 工具接口设计是agent的UX——命名、schema、错误处理决定agent能否正确使用工具。

**证据**:
- Anthropic Writing Effective Tools for Agents: "tool design is agent UX"
- Anthropic: naming, schemas, error surfaces as core tool design dimensions
- awesome-harness-engineering Tool Design章节: ReAct (Thought/Action/Observation loop structure)
- awesome: "Extended Thinking — Claude API Docs: thinking blocks **must be preserved** when passing tool results back"

**应用**: 写工具时假设agent是最终用户，用做用户产品的标准做工具schema。

**局限**: 模型对工具接口的理解能力有限，太复杂的schema反而适得其反。

---

### 模型3: MCP作为Harness的USB协议
**一句话**: MCP（Model Context Protocol）是harness组件互联的事实标准——像USB一样，定义接口而非实现。

**证据**:
- awesome: MCP出现在Skills & MCP、Production Infrastructure等多个章节
- best-of: github-mcp-server (30k stars), MCP Registry, MCP-Zero, MCP Python/TS SDK
- MCP Registry: "official, community-driven registry for MCP servers—the 'app store' MCP clients use to discover servers"
- awesome: Google ADK's MCP integration, Docker MCP Gateway, Composio (1000+ toolkits)

**应用**: MCP server优先；工具开发遵循MCP schema规范。

**局限**: MCP生态还在成熟中；不同框架对MCP的支持程度不一。

---

### 模型4: ReAct Loop作为基础原子
**一句话**: Thought/Action/Observation循环是几乎所有harness的共同基础，理解这个loop是设计harness的前提。

**证据**:
- awesome Agent Loop章节首条: "The foundational paper defining the Thought/Action/Observation loop structure that underlies virtually every agent harness"
- OpenAI Unrolling the Codex Agent Loop: "the canonical decomposition of what happens inside one agent loop iteration: observe, plan, act, verify"
- LangGraph Low Level Concepts: "models the agent loop explicitly as a directed graph with typed state, conditional edges, and checkpointing"
- A Scheduler-Theoretic Framework (70 open-source projects, 60% adopt Agent Loop pattern)

**应用**: 设计新harness时，先画出状态机和状态转换，再实现细节。

**局限**: 某些场景（纯推理、生成式）不需要完整的ReAct loop；过度工程化。

---

### 模型5: 工具检索代替工具堆砌
**一句话**: 不要把1000个工具全塞进context——用语义检索按需获取，token效率决定上下文质量。

**证据**:
- best-of: MCP-Zero (483 stars): "hierarchical semantic routing over 308 servers / 2,797 tools with ~98% token reduction"
- best-of: ToolGen (178 stars, ICLR 2025): "47k+ tools without context stuffing—retrieval and invocation in one generative step"
- best-of: ToolRAG (25 stars): "serves only the tools the user query demands, unlimited tool sets with zero context penalty"
- awesome: LangGraph BigTool: "retrieval and on-demand tool loading so agents scale beyond context without stuffing every schema upfront"

**应用**: 工具数量>50时，引入工具检索层而非手工管理工具列表。

**局限**: 检索质量依赖工具描述的语义清晰度；检索本身也有延迟。

## 关键模式

### Extended Thinking集成
Anthropic Extended Thinking关键约束（写入记忆）：
- `budget_tokens` controls reasoning depth per turn
- thinking blocks **must be preserved** when passing tool results back（忽略它们会破坏多步推理）
- thinking mode cannot change mid-turn

### Middleware Hook模式
LangChain AgentMiddleware（六钩子）:
- `before_agent`, `before_model`, `wrap_model_call`, `wrap_tool_call`, `after_model`, `after_agent`
- 跨切面关注点（PII重写、动态工具注入、模型切换、生产模式重试）的标准注入点

### 关键引用
> "Named, schemas, error surfaces, and the principle that tool design is agent UX." — Anthropic Writing Effective Tools for Agents

> "ReAct: Synergizing Reasoning and Acting in Language Models" — foundational paper for virtually every agent harness

## 信息来源
- awesome-harness-engineering: Agent Loop, Context Delivery & Compaction, Tool Design, Skills & MCP章节
- best-of-Agent-Harnesses: Progressive disclosure harnesses, Plugins/MCPs章节
- Anthropic Writing Effective Tools for Agents (https://www.anthropic.com/engineering/writing-effective-tools-for-agents)
- Anthropic Extended Thinking (https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
- LangGraph Low Level Concepts (https://langchain-ai.github.io/langgraph/concepts/low_level/)
- MCP-Zero, ToolGen, ToolRAG, LangGraph BigTool (来自best-of列表)
