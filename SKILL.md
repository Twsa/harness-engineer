---
name: harness-engineer
description: |
  Harness Engineering（AI Agent Harness 工程学）的思维框架与实践方法。
  基于 OpenAI、Anthropic、Microsoft、Meta、Google 等头部公司的 100+ 项目研究，
  蒸馏出 6 维度核心知识：Agent Loop、Context Engineering、Verification、Memory、
  Multi-Agent、Production Patterns。
  适用场景：构建 Agent 系统、设计工具边界、制定评测方案、部署生产级 Agent。
---
# Harness Engineering Skill

## 核心心智模型

### M1. Harness 是介于模型和现实之间的"操作系统"

Agent = Model + Harness + Tools + Environment (Anthropic Trustworthy Agents)

Harness 负责：prompt 构建、tool dispatch、context 管理、termination 判断。
模型负责：推理和生成。
Tools 负责：操作边界（没有工具，模型能读不能写）。
Environment 负责：代码运行的物理/网络空间。

### M2. Context 是有限资源，有边际收益递减

LLM 的上下文窗口是有限的，Context Rot（上下文腐化）随窗口填入增长而加剧。
注意力焦点被稀释，模型对早期关键信息感知下降。

**实践含义**：
- 不要给 Agent 1000 页手册，给它一张地图
- 静态内容放 prompt 前面，可变内容放后面（cache-friendly ordering）
- 用 markdown 文件（Prompt.md / Plan.md / Implement.md / Documentation.md）做持久化项目记忆

### M3. Agent Loop = Plan → Act → Observe → Adjust → Repeat

不是"一次调用完成任务"，而是"循环直到终止信号"。

关键工程决策：
- 何时触发 compaction（压缩）
- 如何在 session 间传递状态（Feature List / Git History / Checkpoint）
- 终止信号是什么（assistant message ≠ 真正完成）

### M4. 生成器和评价器必须分离

Self-evaluation 存在过度自信问题：Agent 倾向于赞美自己平庸的产出。
GAN 思想引入 Harness：Planner（制定计划）+ Generator（执行）+ Evaluator（独立评估）。
Evaluator 用可量化的 grading criteria 将主观判断转化为可评分项。

### M5. Multi-Agent 编排拓扑 > 模型选择

AdaptOrch（2026）证明：在主流 LLM 基准性能收敛时，编排拓扑选择比模型选择更能提升性能（12-23% 提升）。

四大拓扑：Parallel / Sequential / Hierarchical / Hybrid。
选择依据：任务特征决定拓扑，不存在万能解。

### M6. 生产级 Agent 的三难困境：安全 × 效率 × 能力

每个安全约束都有代价。Sandbox 减少 40% 中断，但需要显式教 Agent 理解约束。
Default-deny + 每次单独审批 vs 允许一次/运行多次：后者不是 adequate control。

---

## 核心启发式

### HE1. 从简单模式开始，逐步增加复杂度

Prompt Chaining / Retrieval / In-context Examples 优先，只有必要时才引入 Agent。
引入 Agent 后，从单 Agent 开始，只有在上下文溢出或团队边界清晰时才引入多 Agent。

### HE2. 给 Agent 地图，不给手册

巨大指令文件浪费上下文。"当所有东西都是重点时，就没有任何重点。"
用结构化文档（docs/ 目录）作为知识系统记录，用 AGENTS.md 做目录索引而非百科全书。
Progressive disclosure：Agent 从小而稳定的入口开始，被教会下一步去哪里找。

### HE3. 每个 Milestone 有明确的 Done When

没有终止判断标准，Agent 会无限循环或过早终止。
Done When = 验收标准 + 验证命令 + 停止-修复规则。
验证失败时必须修复，再继续（Stop-and-fix rule）。

### HE4. 工具设计原则：Scope 清晰 + 自包含 + 可组合

好工具特征：
- 做一件明确的事，不过大也不过小
- 能独立运行，不依赖其他工具的中间状态
- 多个工具能组合，Agent 能动态选择
- description 和参数 schema 清晰

### HE5. Session 间交接产物必须可恢复

长任务失败的根本：Agent 假设"所有状态都在 Context 里"。
必须显式留下：
- Feature List（claude-progress.txt）：完成的功能清单
- Git History：结构化交接产物
- Markdown 状态文件：当前进度快照
- Checkpoint（按子目标频率）：Context 压缩摘要 + 文件系统 diff

### HE6. 压缩不是银弹，设计好过压缩

三种压缩模式：Truncation（直接丢弃）/ Synthesis（压缩为摘要）/ Working Memory（工作记忆隔离）。
Agent 自主压缩 > Harness 强制压缩（Agent 最清楚哪些信息对当前子任务仍关键）。
TDP/DAG 解耦是超长任务的唯一可行方案：Context 隔离通过架构约束而非压缩实现。

### HE7. Schema 即契约，Action 需枚举

多 Agent 失败根因：自然语言的歧义性。
- Typed Schema：跨 Agent 接口必须类型化，违规即契约失败（fail-fast）
- Action Schema：Agent 输出空间必须有限，防止歧义扩散
- MCP：Schema 定义 + 执行验证，是多 Agent 可靠协作的保障

### HE8. Sandbox 是训练问题，不只是配置问题

教 Agent 理解 sandbox 约束：更新 Shell 工具描述，说明文件系统/git/网络访问权限。
改进工具结果渲染：明确显示失败原因和权限升级建议。
效果：Sandboxed agents 比无 sandbox 减少 40% 中断。

### HE9. 评测 = 单元测试思维，不是基准跑分

Agent 评测结构：Task（测试单元）/ Trial（一次尝试）/ Grader（评分逻辑）/ Eval Harness（运行基础设施）。
多维 Grading：deterministic_tests + llm_rubric + static_analysis + state_check + tool_calls。
Eval 必须可重复、可集成 CI，不能靠人工评分。

### HE10. 生产部署 = 渐进 + 可观测 + 可中断

- 灰度 + 反馈：离线评估是局部图景，生产反馈不可或缺
- Checkpoint/Hydration：支持中断恢复（Hibernate-and-Wake 模式）
- Sandbox 生命周期管理：防止代码/IP/secrets 积累（Ephemeral Sandboxes）
- Observability 先于优化：没有 Tracing，就无法知道 Context 为什么失效

---

## Agent Loop 与 Context Engineering

### Agent Loop 结构（OpenAI Codex）

```
User Input → Build Prompt → Inference (text→tokens→sample→text)
→ Model Output: Final Response OR Tool Call
→ Execute Tool → Append Output → Re-query
→ Repeat until Assistant Message (termination)
```

多轮对话时 prompt 呈二次方增长。解决方案：
- Prompt Caching：精确前缀匹配，命中时采样变线性
- Compaction：超过阈值用 /responses/compact 替换为摘要
- Zero Data Retention（ZDR）：为支持 ZDR 客户保持无状态

### 三 Agent 架构（Anthropic Harness Design）

```
Planner Agent   → 制定计划，分解里程碑
Generator Agent → 执行实现
Evaluator Agent → 独立评估（分离 self-evaluation 问题）
```

### 长程 Agent 的双组件结构（Anthropic Effective Harnesses）

- Initializer Agent：首个 session 专用，建立环境基础（init.sh、claude-progress.txt、初始 git commit）
- Coding Agent：每轮做增量推进，留下清晰的下游交接产物

两个主要失败模式：
1. One-shotting：试图一次性完成全部工作，上下文中途耗尽
2. Premature declaration：后续 session 看到已有进展就宣布完成

### Context Engineering 核心原则（Anthropic）

Context Engineering ≠ Prompt Engineering：
- Prompt Engineering：针对单次任务编写最优指令
- Context Engineering：为每次推理策展和维护最优 token 集合（系统指令、工具、MCP、外部数据、消息历史）

### Durable Project Memory（OpenAI 25 小时 run 经验）

用 Markdown 文件写入 Agent 可重复访问的 spec/plan/status：
- **Prompt.md**：Spec + Deliverables。冻结目标，含 Goals/non-goals、Hard constraints、"Done when"
- **Plan.md**：Milestones + Validations。将开放式工作转化为检查点，含停止修复规则
- **Implement.md**：执行操作指南。Plan.md 为真理源，每 milestone 后验证
- **Documentation.md**：状态/决策共享记忆和审计日志

---

## Tool Design

### 工具作为 Agent 的能力边界

Model（智能来源）←→ Harness（指令+guardrails）←→ Tools（能力边界）←→ Environment（运行环境）

工具定义了 Agent 能做什么。没有工具，Claude 能读收据但不能提交。

### MCP 工具注解系统

```typescript
interface ToolAnnotations {
  readOnlyHint?: boolean;      // 默认: false
  destructiveHint?: boolean;   // 默认: true
  idempotentHint?: boolean;    // 默认: false
  openWorldHint?: boolean;      // 默认: true
}
```

无注解时假定最坏情况（非只读、破坏性、非幂等、开放世界）。

### Interpreter Persistence 对齐问题

训练轨迹与部署 Runtime 必须匹配（ArXiv 2603.01209）：
- 训练持久 / 部署持久 → 正常
- 训练持久 / 部署无状态 → 80% episodes 触发 missing-variable 错误
- 训练无状态 / 部署持久 → 3.5x Token 浪费

结论：**解释器持久性应被视为 Agent 训练轨迹的一阶语义**。

---

## Multi-Agent 编排

### 四大编排模式（LangChain）

| 模式 | 特点 | 适用场景 |
|------|------|---------|
| **Subagents** | 并行隔离，无状态，Token 效率高 | 多领域并行查询 |
| **Skills** | 共享上下文，有状态，重复请求节省 40-50% | 单域重复请求 |
| **Handoffs** | 显式交接，传递完整上下文，顺序执行 | 需要状态传递的复杂任务 |
| **Router** | 意图识别后分发，独立执行 | 多领域并行、并行执行 |

### 框架对比

- **AutoGen**（Microsoft）：Core/AgentChat/Extensions 三层 API，AgentTool 将 Agent 作为工具调用
- **CrewAI**：Crews（高自治）+ Flows（精确控制），YAML 配置化，独立于 LangChain
- **OpenHands**：SDK/CLI/GUI/Cloud 多形态，77.6% SWE-bench 开源 SOTA
- **SWE-agent**：maximal agency 设计，yaml 配置驱动，适合研究

### Plan-and-Act 与 ReAct 的区别

- **ReAct**：单模型内混合规划与执行
- **Plan-and-Act**：专用 Planner 模型生成显式高层计划，Executor 细粒度执行（WebArena-Lite 57.58% SOTA）

---

## Verification 与 Reliability

### 可靠性四维度框架（12 个指标）

| 维度 | 指标 |
|------|------|
| Consistency | 跨运行行为一致性、相同输入输出稳定性 |
| Robustness | 抗扰动能力、输入变化敏感性 |
| Predictability | 失败模式可预测、错误边界有界 |
| Safety | 危险操作隔离、数据泄露防护 |

### Sandbox 跨平台实现

| 平台 | 技术 | 关键点 |
|------|------|-------|
| macOS | Seatbelt（sandbox-exec） | subprocess tree 级别约束，动态生成策略 |
| Linux | Landlock + seccomp | 文件系统限制，阻止不安全 syscal |
| Windows | WSL2 | 原生 Windows sandbox 难支持通用工具 |

**NVIDIA 推荐隔离强度**：VM/Kata > gVisor > Bubblewrap/Docker（共享内核风险最高）

### NVIDIA Mandatory 安全控制

1. **Network Egress Controls**：阻止任意站点访问，默认 ask + 企业级 denylist
2. **Block File Writes Outside Workspace**：阻止 workspace 外写入，防止持久化和 RCE
3. **Block Writes to Agent Configuration Files**：保护 .cursorrules、AGENTS.md 等

### FinOps 视角：成本 = 可靠性

边界情况时 Agent 会"更努力"——重规划、重查询、重总结、重试。
控制机制：Loop Limits（防止无限重试）+ Tool Call Caps（限制单次会话工具调用数）。

---

## Memory 与 Long-Running Context

### 三层记忆架构

| 层级 | 内容 | 持久性 | 检索 |
|------|------|--------|------|
| Working Memory | 当前 Session 完整上下文 | Session 结束即销毁 | 直接塞入 Context |
| Episodic Memory | 跨 Session 经验记录 | 持久化 | 按需检索（RAG） |
| Semantic Memory | 结构化知识、规则、偏好 | 持久化 | 向量检索/查询 |

### Session Bridging 与 Checkpoint

**Bridge 需传递的信息**：当前进度快照 + 工作目录状态 + 上下文摘要 + Feature Flags

**Hibernate-and-Wake 模式**（Meta REA）：
- 任务中断时：执行 checkpoint，保存完整状态
- 任务恢复时：从 checkpoint 加载，跳过已验证步骤
- 防止中断导致"重复劳动"和"状态不一致"

### SGH：将 Agent Loop 转化为静态 DAG

结构性问题：隐式依赖 + 无界恢复循环 + 可变执行历史。
解决方案：计划版本内不可变 + 规划/执行/恢复三层分离 + 严格升级协议。
交换：牺牲部分表达力 → 获得：可控性、可验证性、可实现性。

---

## Production Patterns

### GuardRail 三元结果模型（OpenAI）

| 结果 | 行为 | 适用 |
|------|------|------|
| `stop` | 完全阻断 | 严重政策违规 |
| `suspend` | 暂停等待人工 | 中等风险 |
| `flag` | 标记但不阻断 | 监控/趋势分析 |

### Authorization 双模型（LangChain）

| 模式 | 身份 | 适用 |
|------|------|------|
| Assistants | 委托用户身份（On-behalf-of） | 需要访问用户个人数据 |
| Claws | 固定服务凭证 | 跨用户操作、系统级任务 |

### 生产部署检查清单

**Sandbox**：
- OS-level 隔离而非纯 App-level
- Default-deny + 需明确审批的例外
- Allow-once/run-many 不足以防护
- 配置文件写入需特别保护

**Authorization**：
- 用户委托 vs 服务凭证需明确区分
- Token scope 最小权限原则
- 写操作需显式申请和审批

**Observability**：
- 完整执行链路追踪（不只是最终结果）
- 工具调用入参/返回值记录
- 异常/失败模式可分析
- 支持分布式 trace（多 Agent 场景）

**生产发布**：
- Checkpoint 支持中断恢复
- 渐进式发布策略
- Sandbox 生命周期管理
- 人工审批点合理放置

---

## 评测与 Evals

### Agent 评测结构

| 概念 | 定义 |
|------|------|
| Task | 有定义输入和成功标准的单个测试 |
| Trial | 每次 Task 的尝试（因输出可变，需多次运行） |
| Grader | 评分某方面表现的逻辑（一个 Task 可有多个 Grader） |
| Eval Harness | 运行评测的基础设施 |
| Eval Suite | 为测量特定能力设计的 Task 集合 |

### 多维 Grading 策略

```yaml
grader:
  - type: deterministic_tests   # 确定性测试
  - type: llm_rubric             # LLM 评审（主观质量）
  - type: static_analysis        # 静态分析（ruff, mypy, bandit）
  - type: state_check            # 状态检查（安全日志、DB状态）
  - type: tool_calls             # 必需的工具调用序列
```

### 关键评测发现

- **OccuBench**：没有单一模型在所有行业领域占主导；隐式故障（截断数据、缺失字段）比显式错误（超时、500）更难检测
- **GPT-5.2**：从最小到最大推理投入提升 27.5 points
- **Cursor Bench**：sandboxed agents 比非 sandboxed 减少 40% 中断

---

## 关键原文引用

> "Humans steer. Agents execute." — OpenAI Harness Engineering

> "Give Codex a map, not a 1,000-page instruction manual." — OpenAI Harness Engineering

> "When everything is 'important,' nothing is." — OpenAI Harness Engineering

> "Agent is a system where the AI model dynamically directs its own process and tool usage to accomplish a task." — Anthropic Building Effective Agents

> "Context Engineering: curating and maintaining the optimal set of tokens for each LLM inference." — Anthropic Effective Context Engineering

> "Generator and Evaluator separation solves the self-evaluation problem." — Anthropic Harness Design

> "Without Tracing, you cannot know why Context failed." — LangChain Harness Engineering

> "Cost is a reliability metric in Agentic SaaS." — InfoWorld FinOps for Agents

---

## 来源索引

### 核心文献

| 文章 | 核心贡献 |
|------|---------|
| OpenAI - Harness Engineering | 零代码全 Agent 构建、"Map not Manual"、25 小时 run |
| OpenAI - Codex Agent Loop | Quadratic Problem、Compaction、ZDR 设计 |
| OpenAI - Long Horizon Tasks | Durable Project Memory（4件套）、时间视野 |
| Anthropic - Building Effective Agents | Agent 定义、Workflow vs. Agent |
| Anthropic - Effective Context Engineering | Context Engineering vs. Prompt Engineering、Context Rot |
| Anthropic - Harness Design | 三 Agent 架构、Self-Evaluation 分离 |
| Anthropic - Effective Harnesses | Initializer+Coding 双组件、Session Bridging |
| Anthropic - Trustworthy Agents | Agent 四组件模型（Model/Harness/Tools/Environment） |

### 框架文献

| 框架/论文 | 核心贡献 |
|----------|---------|
| ReAct (arXiv 2210.03629) | 推理+动作协同，ALFWorld +34% |
| LATS (arXiv 2310.04406) | 统一推理/动作/规划，HumanEval 92.7% SOTA |
| TDP (arXiv 2601.07577) | Task-Decoupled Planning，82% token 减少 |
| SGH (arXiv 2604.11378) | Agent Loop → DAG，三层分离 |
| OccuBench (arXiv 2604.10866) | 多行业 Agent 评测，隐式故障最难 |
| AdaptOrch (arXiv 2602.01465) | 拓扑选择 > 模型选择，12-23% 提升 |
| Interpreter Persistence (arXiv 2603.01209) | 训练/运行时对齐，80% 错误率风险 |

### 工具生态

| 工具 | 用途 |
|------|------|
| MCP (Model Context Protocol) | Anthropic 主推的工具交互标准 |
| smolagents (Hugging Face) | 轻量代码 Agent (~1000 行)，MCP 支持 |
| Daytona | OCI 兼容沙箱，<90ms 启动 |
| Mem0 | Agent 记忆层，v3 LoCoMo 91.6 |
| Claude-mem | Claude Code 专用 SQLite 持久记忆 |
| DeepEval | LLM 评测框架，assert-based 测试思维 |
| LiteLLM | 100+ 模型统一网关 |
| Cursor Rules | 项目规则引擎（.mdc 格式） |

---

## 使用场景

| 场景 | 启动建议 |
|------|---------|
| 设计新的 Agent Harness | 先画四组件图（Model/Harness/Tools/Env），确认职责边界 |
| 上下文溢出 | 先考虑压缩策略，再考虑 DAG/TDP 解耦 |
| 多 Agent 协作失败 | 检查 Schema 是否类型化，Action 是否枚举 |
| Agent 过度自信 | 引入独立 Evaluator，分离生成和评价 |
| 评测设计 | 从 deterministic_tests 开始，逐步增加 llm_rubric |
| 生产部署 | Checkpoint + 渐进灰度 + 完整 Observability |
| 安全沙箱 | Default-deny，Allow-once/run-many 不足 |
| 成本失控 | 引入 Loop Limits + Tool Call Caps，FinOps 思维 |
