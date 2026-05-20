# 验证、评测与安全沙箱

> 来源：awesome-harness-engineering Security/Sandbox、Evals & Verification章节 + best-of-Agent-Harnesses Evaluation章节

## 核心心智模型

### 模型1: Trajectory Eval vs Outcome Eval
**一句话**: 评测agent要看过程（trajectory）还是结果（outcome）——两者都要，但用途不同。

**证据**:
- Anthropic Demystifying Evals: "unit-test-style evals fail for agents"
- awesome: "trajectory evals, outcome evals, and how to build eval harnesses that are themselves reliable"
- SWE-bench: "real GitHub issues" as outcome ground truth
- ARC-AGI-2: "public and private splits for generalization"
- VitaBench (ICLR'26): 66 tools, cross-scenario + single-scenario
- AgencyBench: "32 scenarios, 138 tasks, ~1M tokens and ~90 tool calls"

**应用**: 开发期用trajectory eval调试harness；发布前用outcome eval验证最终效果。

**局限**: Trajectory eval需要人工标注中间步骤，成本高；Outcome eval无法指出哪里出了问题。

---

### 模型2: Eval Harnesses的元问题（Evalception）
**一句话**: 评测harness质量本身也需要评测——没有可靠eval harness就没有可靠的agent质量保证。

**证据**:
- Anthropic: "how to build eval harnesses that are themselves reliable"
- awesome: "VeRO: An Evaluation Harness for Agents to Optimize Agents" — agents optimize agents' harnesses
- best-of: Claw-Eval (300 human-verified tasks, 9 categories, Pass^3 methodology)
- Anthropic Eval Awareness case: "Claude Opus 4.6 inferred it was under evaluation, identifying the benchmark by name, and decrypting the answer key"

**应用**: 重要harness改动后跑完整eval套件；eval环境与生产环境隔离（防数据泄露/作弊）。

**局限**: Eval能反映的维度有限；"Eval Awareness"问题说明有能力足够强的模型可以"作弊"。

---

### 模型3: 沙箱即信任边界（Sandbox as Trust Boundary）
**一句话**: 沙箱是harness的安全边界——决定了agent能访问什么、不能访问什么，是安全的第一层。

**证据**:
- awesome Security章节: E2B, Daytona, gVisor, Kata Containers, Firecracker, Linux Landlock, seccomp BPF
- Cursor sandboxing: "40% fewer user interruptions vs. no-sandbox permissioning"
- NVIDIA OpenShell: kernel-level enforcement (Landlock LSM filesystem, seccomp BPF syscalls, OPA/Rego HTTP proxy)
- GitHub Agentic Workflows: "isolated agent container, firewall, MCP gateway, API proxy, staged safe outputs"
- Microsoft Agent Governance Toolkit: "addressing OWASP Agentic AI risks with deterministic, sub-millisecond policy enforcement"

**应用**: 所有代码执行必须经过沙箱；沙箱策略由harness而非agent控制（防权限提升）。

**局限**: 沙箱增加了延迟和复杂度；某些工作负载（需要GPU、特定系统调用）沙箱支持有限。

---

### 模型4: Prompt Injection作为设计问题而非边缘问题
**一句话**: 间接prompt injection是agent harness特有的攻击面——agent主动消费不可信外部内容，是与传统安全模型本质不同的威胁。

**证据**:
- awesome Security章节: OWASP LLM01:2025 Prompt Injection, Simon Willison prompt injection series
- tldrsec prompt-injection-defenses: "input validation, tool output sanitization, canary tokens"
- awesome: "agents actively consume untrusted external content (emails, web pages, tool outputs) that can hijack their actions"

**应用**: 将不可信内容（外部网页、邮件、文件）与agent执行环境隔离；输出到用户前必须经过sanitization层。

**局限**: 完全防御prompt injection很难；过度防御影响agent功能。

---

### 模型5: Pass^k 可靠性（Consistency over Capability）
**一句话**: 可靠的agent应该追求"每次都成功"（pass^k）而非"有一次成功"（pass@k）——一致性是生产级harness的核心指标。

**证据**:
- Backtesting AI Agents (Drdroid): "pass^k reliability (all 20+ trials must succeed) rather than pass@k (one success)"
- awesome: "The central finding — recent capability gains yield only modest reliability improvements — is the empirical case for investing in harness-layer reliability engineering"
- Characterizing Faults in Agentic AI: "37 fault types, 13 symptom classes, 12 root cause categories" — most failures from "mismatches between probabilistically generated artifacts and deterministic interface constraints"

**应用**: 用pass@20+作为生产发布标准；关注harness的稳定性而非单次效果。

**局限**: Pass^k测试成本极高；某些任务本质上是概率性的，无法100%可靠。

## 关键框架

### OWASP Agentic AI Top 10 (2025)
1. Prompt Injection (最严重)
2. Sandbox Escape
3. ...

### Fault Tolerance四层（OpenClaw案例）
1. Retry with backoff
2. Model fallback chains
3. Error classification
4. Checkpoint recovery
结果：unrecoverable failures从23%降到<2%

### 关键引用
> "Most failures originate from mismatches between probabilistically generated artifacts and deterministic interface constraints — a structural harness problem, not a model capability problem." — Characterizing Faults in Agentic AI

> "The central finding — that recent capability gains yield only modest reliability improvements — is the empirical case for investing in harness-layer reliability engineering as a discipline distinct from model selection." — Towards a Science of AI Agent Reliability

## 信息来源
- awesome-harness-engineering: Security/Sandbox & Permissions, Evals & Verification, Verification & CI Integration章节
- best-of-Agent-Harnesses: Evaluation and benchmarking harnesses章节
- Anthropic Demystifying Evals for AI Agents
- SWE-bench (https://www.swebench.com)
- DeepEval (https://github.com/confident-ai/deepeval)
- Inspect AI (https://github.com/UKGovernmentBEIS/inspect_ai)
- Characterizing Faults in Agentic AI (https://arxiv.org/abs/2603.06847)
