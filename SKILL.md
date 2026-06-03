# Harness Engineering Framework Skill

> Agent = Model + Harness. Harness engineering is the discipline of designing the control layer around AI agents to increase the probability of good outcomes and enable self-correction.

---

## Core Philosophy

Harness engineering recognizes that AI agents are powerful but non-deterministic—they don't know your context, they think in tokens, and they need structured guidance to operate reliably. A well-designed harness serves two goals: **increasing the probability that the agent gets it right in the first place**, and **providing feedback loops that self-correct issues before they reach human eyes**.

The key insight from Martin Fowler and Anthropic's research: harness engineering is a form of **context engineering**—it's about curating what information the agent has access to and what behaviors it can exhibit.

---

## Mental Models

### 1. Feedforward vs Feedback Controls

**Feedforward controls** anticipate the agent's behavior and aim to steer it before it acts. Examples: coding conventions in AGENTS.md, Skills with bootstrap scripts, code mods, architectural rules, `.cursorrules` project rules, MCP tool annotations.

**Feedback controls** observe after the agent acts and enable self-correction. Examples: linting, testing, code review agents, static analysis, Playwright-based evaluators.

**Why it matters**: Separately, you get either an agent that repeats the same mistakes (feedback-only) or one that encodes rules but never finds out if they worked (feedforward-only). Both are needed in concert.

---

### 2. Multi-Agent Architecture Patterns

When single agent complexity grows, four patterns handle coordination:

| Pattern | Best For | Key Tradeoff |
|---------|---------|--------------|
| **Subagents** | Multiple distinct domains, parallel execution | Centralized control adds latency |
| **Skills** | Single agent with many specializations, progressive disclosure | Context accumulates over time |
| **Handoffs** | Sequential workflows with state transitions | More stateful, requires careful management |
| **Router** | Distinct verticals, parallel queries, synthesis | Stateless = no conversation history |

**Selection heuristic**: Start with single agent. Scale to multi-agent when context management or distributed development constraints emerge. Anthropic's research shows multi-agent with separate context windows enabled 90.2% better performance on complex research tasks.

**A2A Protocol**: Google's Agent2Agent Protocol enables agents to discover each other's capabilities, negotiate interactions, and collaborate through secure message exchange. **MCP (Model Context Protocol)** provides standardized external data/tool connectivity. Together they form the interoperability foundation for multi-agent ecosystems.

---

### 3. Computational vs Inferential Execution

**Computational controls** are deterministic and fast—tests, linters, type checkers, structural analysis. They run in milliseconds to seconds with reliable results.

**Inferential controls** use semantic analysis and AI code review. They're slower and more expensive but allow rich guidance and semantic judgment.

**The trade-off**: Computational controls are cheap enough to run on every change. Inferential controls are expensive and non-deterministic but increase trust when used appropriately.

---

### 4. The Steering Loop

The human's job is to **steer** the agent by iterating on the harness. When an issue happens multiple times, improve the feedforward and feedback controls to make it less probable in the future.

**Key insight**: Agents can help build their own harnesses—writing structural tests, generating draft rules from observed patterns, scaffolding custom linters, creating how-to guides from codebase archaeology.

---

### 5. Regulation Categories

Three distinct dimensions of what a harness regulates:

**Maintainability harness**: Regulates internal code quality—duplicate code, cyclomatic complexity, missing test coverage, architectural drift, style violations. Easiest to implement because pre-existing tooling is abundant.

**Architecture fitness harness**: Defines and checks architectural characteristics—performance requirements, observability standards, module boundaries. Uses fitness functions.

**Behavior harness**: Guides and senses whether the application functionally behaves as needed. The hardest problem—depends on AI-generated test suites which aren't yet reliable enough.

---

### 6. Context as Finite Resource

LLMs have an "attention budget" that depletes as context grows. Every new token introduced increases the need to carefully curate tokens.

**Strategies**:
- **Progressive disclosure**: Let agents discover context through exploration rather than stuffing everything upfront
- **Just-in-time retrieval**: Maintain lightweight identifiers and load data at runtime
- **Hybrid approach**: Pre-inject stable context (CLAUDE.md) while using tools for dynamic exploration

**The Golden Rule**: Find the smallest possible set of high-signal tokens that maximize the likelihood of desired outcome.

**Memory layer patterns**: Mem0 and similar systems provide multi-level memory (user, session, agent state) with single-pass ADD-only extraction. Agent-generated facts become first-class memories. Entity linking and multi-signal retrieval (semantic + BM25 + temporal) enable efficient recall without stuffing context windows.

---

### 7. Generator-Evaluator Pattern

Agents tend to be overly generous when evaluating their own work. Separating the agent doing the work from the agent judging it addresses this.

**Architecture** (from Anthropic's GAN-inspired design):
- **Generator**: Builds features one at a time, works in sprints
- **Evaluator**: Grades outputs against explicit criteria using tools like Playwright to interact with live systems
- **Planner**: Expands simple prompts into detailed product specs

**Why it works**: Tuning a standalone evaluator to be skeptical is far more tractable than making a generator critical of its own work.

**Sprint contracts**: Generator proposes what to build + how to verify; evaluator reviews before sprint begins. Bridges user stories to implementation without over-specifying.

---

### 8. Long-Running Agent Patterns

When agents must work across multiple context windows (hours or days), the challenge is bridging discrete sessions where each new session begins with no memory of what came before.

**Key patterns**:
- **Initializer agent**: Sets up the environment on first run with feature lists, progress files, git commits
- **Coding agent**: Makes incremental progress, leaves clean state for next session
- **Feature list**: Comprehensive file of requirements, each marked pass/fail
- **Progress file**: Log of what agents have done, enabling next agent to understand state
- **Context resets**: Clear the context window and start fresh with structured handoff artifacts

**The insight**: Effective engineers leave artifacts that let the next shift (or agent) pick up seamlessly.

**Note**: With Opus 4.5, context anxiety is largely eliminated, enabling continuous session working. Context resets remain valuable for explicit state management but are no longer required for anxiety prevention.

---

### 9. Harnessability

Not every codebase is equally amenable to harnessing. A strongly typed language has type-checking built-in. Clearly definable module boundaries afford architectural constraint rules. Frameworks abstract away details agents don't need to worry about.

**Ambient affordances**: Properties of the environment that make it legible, navigable, and tractable to agents.

**Project rules** (`.cursorrules`): Cursor AI's `.mdc` files in `.cursor/rules/` provide project-specific feedforward guidance—architecture, coding standards, framework usage, security requirements. These are explicit feedforward controls living alongside the codebase.

**Greenfield vs legacy**: Greenfield teams can bake harnessability in from day one. Legacy teams face the harder problem—the harness is most needed where it's hardest to build.

---

### 10. Trust Architecture

**Four components of an agent**:
1. **The model**: The intelligence
2. **The harness**: Instructions and guardrails
3. **Tools**: Services and applications the model can use
4. **The environment**: Where the agent runs and what it can access

**The security truth**: A well-trained model can still be exploited through a poorly configured harness, an overly permissive tool, or an exposed environment. Safeguards must account for all four layers.

**MCP Tool Annotations as risk vocabulary**: Four hints define tool behavior:
- `readOnlyHint`: Does the tool modify its environment?
- `destructiveHint`: If it modifies, is the change destructive (vs additive)?
- `idempotentHint`: Can you safely call it again with same arguments?
- `openWorldHint`: Does tool interact with external entities?

**The Lethal Trifecta** (Simon Willison): Three capabilities that combined create data exfiltration risk:
1. Access to private data
2. Exposure to untrusted content
3. Ability to externally communicate

Session risk is a property of the **session composition**, not any single tool. Runtime policy must track tool combinations, not just individual annotations.

---

### 11. Security & Sandbox Architecture

Agentic tools perform arbitrary code execution by design, introducing significant attack surfaces. Security must be enforced at the OS level, not just application level.

**Mandatory controls** (NVIDIA AI Red Team):
- **Network egress filtering**: Block arbitrary network access to prevent exfiltration and remote shells
- **File write restrictions**: Block writes outside active workspace (e.g., `~/.zshrc` = RCE risk)
- **Config file protection**: Block writes to hooks, skills, MCP configs—these often run outside sandbox

**Tiered implementation approach**:
1. Enterprise denylists for critical paths (cannot be overridden)
2. Read-write within workspace without approval
3. Specific allowlisted operations with approval
4. Default-deny for everything else

**Key insight**: Application-level controls can be bypassed via indirection (calling restricted tools through approved ones). OS-level controls (Seatbelt, microVM, Kata containers) work beneath the application layer.

**Indirection attack example**: `.cursorrules`, `CLAUDE.md`, `copilot-instructions.md` can contain prompt injections that modify agent behavior or gain code execution through hooks.

**Annotation trust model**: All annotations are hints, not contracts. Clients **must** treat annotations from untrusted servers as untrusted. Even `title` can be misleading. The spec explicitly acknowledges this limitation.

---

### 12. Self-Verification & Build Loops

Today's models are exceptional at self-improvement but don't naturally enter build-verify loops.

**The common failure pattern**: Agent writes solution → re-reads code → confirms looks ok → stops. Missing: actual verification against spec.

**Build-Self-Verify pattern** (LangChain):
1. **Plan & Discover**: Read task, scan codebase, build verification plan
2. **Build**: Implement with tests for happy paths AND edge cases
3. **Verify**: Run tests, compare against task spec (not own code)
4. **Fix**: Analyze errors, revisit spec, fix issues

**Deterministic context injection helps**: `PreCompletionChecklistMiddleware` intercepts before exit, reminds agent to run verification pass—similar to Ralph Wiggum Loop forcing continued execution.

**Time budgeting**: Agents are bad at time estimation. Inject time budget warnings to shift agent toward verification when time is low.

---

### 13. FinOps & Unit Economics

In agentic SaaS, cost is a reliability metric. Without loop limits and cost guardrails, cloud bills become the real product demo.

**CAPO (Cost-per-Accepted-Outcome)**: The fully loaded cost to deliver one accepted outcome for a specific workflow. Acceptance requires a concrete quality gate: automated validation, user approval, or downstream success signal.

**Agentic COGS stack**:
1. Model inference (usually largest contributor)
2. Tools and side effects (paid APIs, retries, write safeguards)
3. Orchestration runtime (workers, queues, sandboxed execution)
4. Memory and retrieval (embeddings, vector storage, context building)
5. Governance and observability (tracing, evaluation, safety filters)
6. Humans in the loop (review, escalations, support)

**Five budget guardrails**:
- **Loop/step limit**: Cap planning, reflection, verification cycles
- **Tool-call cap**: Total paid actions per run with sub-caps for expensive tools
- **Token budget**: Per-run ceiling, summarize history instead of re-sending
- **Wall-clock timeout**: Push long work to explicit background jobs
- **Tenant budgets and concurrency**: Limit blast radius with per-tenant caps

**Unit economics maturity**:
| Level | What you sell | FinOps focus |
|-------|--------------|--------------|
| Seat-bundled | Agents included with license | Gross margin volatility |
| Credits-based | X credits/month to spend | Credit price vs cost |
| Workflow metering | Per workflow type | CAPO per workflow |
| Outcome-linked | Pay when accepted | Acceptance integrity |
| Value-based | Guarantee business result | Deliverable at target margin |

---

### 14. Evaluation Frameworks

**pass@k evaluation**: Run task k times, count successes. Provides statistical confidence but expensive. Use when ground-truth is verifiable.

**Swiss Cheese Model**: Multiple evaluation layers, each with holes. Defense in depth—errors slip through one layer but get caught by others.

**Grader types** (Anthropic):
1. **Reference-free**: Purely structural (does it compile? pass tests?)
2. **Reference-based**: Compare against known-good outputs
3. **LLM-as-judge**: Semantic evaluation via another model

**Trajectory evaluation**: Focus on the full sequence of decisions and actions, not just final output. Two agents might reach same conclusion via very different paths—understanding those paths matters.

**SWE-agent benchmark pattern**: Agent-computer interfaces that enable LLMs to use tools for real repository tasks. SWE-bench tests ability to fix issues in real GitHub repos. State-of-the-art performance requires precise tool definition and state management.

---

### 15. Debugging & Failure Localization

**AgentRx framework**: Systematic 9-category failure taxonomy:
1. Reasoning errors
2. Tool use errors
3. State management errors
4. Context window overflow
5. Prompt injection
6. Tool definition gaps
7. Environment interaction failures
8. Iteration bugs
9. Specification mismatches

**Critical insight**: Isolating which category caused failure is the first step to fixing it. Generic "it failed" diagnoses lead to wasted effort on wrong fixes.

---

## Decision Heuristics

| Situation | Heuristic |
|-----------|------------|
| Agent keeps repeating same mistake | Add a computational feedback sensor (linter, test) |
| Agent produces generic/template outputs | Weight "originality" in evaluator criteria; add constraint rules |
| Agent declares task done prematurely | Require explicit evidence in feature list; add third-party evaluator |
| Context window filling up | Switch to incremental approach; use context reset |
| New codebase, no harness | Start with maintainability harness (easiest to implement) |
| Complex task, long horizon | Use generator-evaluator pattern with planner agent |
| Agent can't evaluate its own work | Separate evaluator agent with explicit grading criteria |
| Legacy codebase | Prioritize ambient affordances first—make the environment legible |
| Multiple distinct domains needed | Use subagents pattern with centralized orchestration |
| Single agent, many specializations | Use skills pattern with progressive disclosure |
| Sequential workflow with state | Use handoffs pattern |
| Distinct verticals, parallel queries | Use router pattern |
| Cost overruns in production | Implement CAPO tracking + loop/step limits |
| Multi-agent coordination needed | Use A2A protocol for capability discovery |
| Security-sensitive tool access | Implement MCP annotations + runtime policy on tool combinations |

---

## Expression DNA

- **Vocabulary**: feedforward, feedback, harness, sensor, guide, regulation, context engineering, ambient affordances, self-correction, CAPO, lethal trifecta, sprint contract
- **Tone**: Engineering-focused, precise, systems-thinking language
- **Structure**: Categorizes patterns, contrasts trade-offs, emphasizes iteration over one-shot solutions
- **Metaphors**: Cybernetic governors, steering loops, attention budgets, GAN-inspired architectures, Swiss cheese defense
- **Certainty**: Typically presents trade-offs rather than absolute rules; "it depends" is common

---

## Values &反模式

**Core values**:
1. Reduce human review toil while increasing system quality
2. Catch issues as early as possible (quality left)
3. Enable self-correction before issues reach human eyes
4. Treat context as finite resource to be curated, not stuffed

**反模式**:
- Stuffing all context upfront instead of curating high-signal tokens
- Feedback-only controls without feedforward
- Assuming AI-generated tests are sufficient without human validation
- Building harnesses for codebases that lack ambient affordances
- Over-engineering the harness before the problem is well-understood
- Shipping agents without cost guardrails (FinOps blindness)
- Ignoring tool annotation trust levels

---

## Honest Boundaries

- Cannot guarantee agents won't exploit poorly configured harnesses
- Cannot fully eliminate the need for human oversight, especially for novel situations
- Cannot make legacy codebases harnessable without first improving their ambient affordances
- Cannot predict agent behavior with certainty—only increase probability of good outcomes
- Behavioral harnesses (functional correctness) remain the hardest unsolved problem
- MCP annotations are hints, not enforcement—cannot be trusted absolutely
- FinOps metrics (CAPO) require mature observability infrastructure to track accurately
- Information about agent behavior is continuously evolving—this skill represents the state of the art as of May 2026

---

## Sources

Primary sources informing this framework:

1. **Martin Fowler** - "Harness engineering for coding agent users" (April 2026)
   - Feedforward/feedback framework
   - Regulation categories (maintainability, architecture fitness, behavior)
   - Steering loop concept
   - Harness templates for common service topologies

2. **Anthropic Engineering** - "Effective harnesses for long-running agents" (Nov 2025)
   - Initializer/coding agent pattern
   - Feature lists and progress files
   - Context resets for multi-session coherence

3. **Anthropic Engineering** - "Harness design for long-running application development" (Mar 2026)
   - Generator-evaluator architecture (GAN-inspired)
   - Three-agent system (planner/generator/evaluator)
   - Grading criteria design
   - Sprint contracts between generator and evaluator

4. **Anthropic Engineering** - "Effective context engineering for AI agents" (Sep 2025)
   - Context as finite resource
   - Attention budget concept
   - Progressive disclosure strategies
   - Hybrid context retrieval model

5. **Anthropic Research** - "Trustworthy agents in practice" (Apr 2026)
   - Four components of agents (model, harness, tools, environment)
   - Human control principles
   - Security layers and prompt injection defense

6. **OpenAI** - "Building effective agents" (Dec 2024)
   - Workflow vs agent distinction
   - Simple composable patterns
   - Framework evaluation guidance

7. **LangChain** - "The Anatomy of an Agent Harness" (Mar 2026)
   - "If you're not the model, you're the harness"
   - Harness primitives: filesystem, bash, tools, orchestration
   - Durable storage and context management

8. **LangChain** - "Improving Deep Agents with Harness Engineering" (Feb 2026)
   - Self-verification and build loops
   - PreCompletionChecklistMiddleware
   - Trace analysis as iterative improvement
   - 13.7 point improvement on Terminal Bench 2.0 via harness-only changes

9. **LangChain** - "Choosing the Right Multi-Agent Architecture" (Jan 2026)
   - Four patterns: subagents, skills, handoffs, router
   - Context management and distributed development constraints
   - Selection heuristics for each pattern

10. **NVIDIA** - "Practical Security Guidance for Sandboxing Agentic Workflows" (Jan 2026)
    - Mandatory network egress filtering
    - File write restrictions outside workspace
    - Config file protection (hooks, skills, MCP configs)
    - OS-level vs application-level controls
    - Tiered implementation approach

11. **Google Cloud** - "A developer's guide to production-ready AI agents" (Feb 2026)
    - MCP and A2A protocols for interoperability
    - Agent evaluation focuses on trajectories, not just outputs
    - Staged rollouts: sandbox → canary → production
    - Session management and persistent memory

12. **Red Hat** - "Harness engineering for structured workflows" (Apr 2026)
    - Structured workflows vs unstructured
    - AI-assisted development patterns

13. **MCP Blog** - "Tool Annotations as Risk Vocabulary" (Mar 2026)
    - Four annotation hints (readOnly, destructive, idempotent, openWorld)
    - Lethal trifecta for data exfiltration
    - Trust model (all annotations are hints)
    - Tool combination risk assessment

14. **InfoWorld** - "FinOps for agents: Loop limits, tool-call caps and the new unit economics of agentic SaaS" (Mar 2026)
    - CAPO (Cost-per-Accepted-Outcome) metric
    - Agentic COGS stack
    - Five budget guardrails
    - Unit economics maturity levels

15. **SWE-agent** - "Agent-Computer Interfaces Enable Automated Software Engineering" (2024)
    - Agent-computer interface design
    - SWE-bench benchmarking methodology
    - State management for tool-use agents

16. **Mem0** - "Building Production-Ready AI Agents with Scalable Long-Term Memory" (Apr 2026)
    - Multi-level memory (user, session, agent)
    - Single-pass ADD-only extraction
    - Agent-generated facts as first-class memories
    - Multi-signal retrieval (semantic + BM25 + temporal)

17. **Awesome Cursor Rules** - Project-specific AI behavior guidance
    - `.mdc` file format for project rules
    - Feedforward control patterns
    - Framework-specific coding standards

---

> 本Skill由 [女娲 · Skill造人术](https://github.com/alchaincyf/nuwa-skill) 生成
> 创建者：[花叔](https://x.com/AlchainHust)