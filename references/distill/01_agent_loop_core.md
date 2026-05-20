# Agent Loop & Core Harness 蒸馏

> 来源：Anthropic/01_critical + OpenAI/01_critical + ArXiv/02_arxiv（ReAct & Interpreter 相关）
> 主题：agent_loop、context_engineering、tool_design、prompt_building

---

## 一、Agent Loop（代理循环）核心机制

### 1.1 什么是 Agent Loop

Agent Loop 是 AI Agent 运行时的核心执行循环，本质是一个"推理→行动→观察→循环"的自我导向过程（Anthropic, OpenAI）。

**简化结构（OpenAI Codex 描述）：**

```
1. Agent 接收用户输入，准备 prompt
2. 通过推理 API 查询模型（text → tokens → sample → output tokens → text）
3. 模型输出最终响应 OR 请求工具调用
4. 若为工具调用：执行工具，追加输出到 prompt，重新查询
5. 重复直到遇到 assistant message（终止状态）
```

Anthropic 对 Agent 的定义：

> Agent 是 AI 模型在完成任务时动态主导自身过程和工具使用的系统——即自己决定如何实现用户目标，而非遵循固定脚本。

Trustworthy Agents（Anthropic, 2026）指出 Agent 运行在一个**自我导向循环**中：

```
计划(Plan) → 行动(Act) → 观察结果(Observe) → 调整(Adjust) → 重复
```

### 1.2 Workflow vs. Agent 的关键区别

Anthropic 明确区分了两种 agentic systems：

| | Workflow（工作流） | Agent（代理） |
|---|---|---|
| 编排方式 | 预定义代码路径 | 模型动态主导 |
| 适用场景 | 明确任务，可预测性优先 | 灵活性、模型决策优先 |
| 延迟/成本 | 较低 | 较高 |

### 1.3 长程 Agent 的 Agent Loop 问题

**OpenAI Codex（Long Horizon, 2026）**指出长程任务的核心是 Agent Loop 能保持 coherence：

```
Plan → Edit code → Run tools (tests/build/lint) → Observe results → 
Repair failures → Update docs/status → Repeat
```

**Anthropic（Effective Harnesses, 2025）**发现单靠 compaction（压缩）不足以支撑跨多上下文窗口的长程任务，存在两个主要失败模式：

1. **过度承诺（One-shotting）**：Agent 试图一次性完成全部工作，导致在中间耗尽上下文，留下半成品
2. **过早终止（Premature declaration）**：后续 session 看到已有进展就宣布完成

**解决方案：Initializer Agent + Coding Agent 双组件结构**
- Initializer Agent：专门在首次运行时建立环境基础（init.sh、claude-progress.txt、初始 git commit）
- Coding Agent：每轮做增量推进，同时留下清晰的下游交接产物

### 1.4 上下文窗口管理与竞争问题

**OpenAI Codex（Agent Loop, 2026）**指出：

- 无 `previous_response_id` 时，prompt 增长呈**二次方**复杂度
- **Prompt Caching** 将采样从二次方转为线性（当缓存命中时）
- **Compaction（压缩）**：当上下文超过阈值，通过 `/responses/compact` 接口将对话替换为代表性摘要
- 缓存未命中触发条件：中途更换工具、更换模型、更换沙箱配置或 CWD

**关键设计：Zero Data Retention（ZDR）**
- Codex 为支持 ZDR 客户保持完全无状态，不使用 `previous_response_id`
- 中途变更通过追加新消息而非修改早期消息来处理

### 1.5 三方核心观点对比

| 维度 | Anthropic | OpenAI Codex | ReAct (2022) |
|---|---|---|---|
| Loop 本质 | 自我导向循环，多轮推理-工具调用 | Prompt → Inference → Tool → Loop | Reasoning traces + Acting 交错生成 |
| 终止判断 | Assistant message 为终止状态 | Assistant message 信号终止 | 任务完成或外部来源信息足够 |
| 上下文策略 | Initializer+Coding 双组件、压缩、session 间交接产物 | Compaction + Caching + Reset | 通过 Wikipedia API 等外部来源补充信息 |
| 关键洞察 | Agent Loop 的"上下文焦虑"问题 | Quadratic problem（prompt 增长） | 推理轨迹帮助诱导/跟踪/更新行动计划 |

---

## 二、Context Engineering（上下文工程）

### 2.1 Context Engineering vs. Prompt Engineering

Anthropic（Context Engineering, 2025）明确定义：

> **Prompt Engineering**：编写和组织 LLM 指令以获得最优结果，主要针对单次分类或文本生成任务
>
> **Context Engineering**：为每次 LLM 推理**策展和维护最优的 token 集合**（系统指令、工具、MCP、外部数据、消息历史等），是迭代过程

Context Engineering 是 Prompt Engineering 的自然演进——从"找对词"到"配置最优上下文状态"。

### 2.2 上下文的有限性：Context Rot

LLM 的上下文窗口是**有限资源**，存在"Context Rot"（上下文腐化）现象：

- 随着 context 内 token 数量增加，模型准确召回信息的能力下降
- Transformer 架构的 n² 配对关系（n tokens → n² 注意力计算），使注意力焦点被稀释
- 位置编码插值虽允许更长序列，但会损失 token 位置理解

**注意力稀缺的根本原因**：模型在训练数据中短序列更常见，对上下文全依赖关系的专用参数不足。

**实用含义**：上下文必须被视为有限资源，具有边际收益递减特性。

### 2.3 OpenAI 的上下文管理策略

**Durable Project Memory（持久化项目记忆）**——用 Markdown 文件写入 agent 可重复访问的 spec、plan、constraints、status：

| 文件 | 作用 |
|---|---|
| `Prompt.md` | Spec + Deliverables；冻结目标，含 Goals/non-goals、Hard constraints、"Done when" |
| `Plan.md` | Milestones + Validations；将开放式工作转化为检查点序列，含停止修复规则 |
| `Implement.md` | 执行操作指南；Plan.md 为真理源，每 milestone 后验证，持续更新文档 |
| `Documentation.md` | 状态/决策共享记忆和审计日志 |

**给 Agent"地图"而非"1000页手册"**（OpenAI Harness Engineering）：
- 巨大指令文件浪费上下文资源
- 过量 guidance 反而变成 non-guidance
- 知识以 repository 为系统记录（而非散落在 prompts 中）

### 2.4 Anthropic 的长程 Agent 上下文方案

**Two-Agent 架构（Effective Harnesses）：**

1. **Feature List**：`claude-progress.txt` 跟踪完成的功能清单，作为 agent 间状态传递
2. **Git History**：作为结构化交接产物，帮助新 agent 快速理解工作状态
3. **init.sh 初始化脚本**：首次 session 建立可运行环境

**关键洞察**：让 agent 在新 context window 启动时能快速理解工作状态。

---

## 三、Tool Design（工具设计）

### 3.1 Anthropic 的工具设计原则

来自多个来源的整合原则：

**好工具的特征：**
- **Scope 清晰**：每个工具做一件明确的事，不过大也不过小
- **自包含性**：工具应能独立运行，不依赖其他工具的中间状态
- **可组合性**：多个工具能组合使用，agent 能动态选择
- **文档完善**：工具描述（description）和参数 schema 清晰，模型能准确推断何时使用

### 3.2 工具作为 Agent 的能力边界

Anthropic（Trustworthy Agents, 2026）指出 Agent 的四个组成层：

```
Model（智能来源）←→ Harness（指令+guardrails）←→ Tools（能力边界）←→ Environment（运行环境）
```

工具定义了 Agent 能做什么——没有工具，Claude 能读收据但不能提交。

### 3.3 OpenAI Codex 的工具策略

**Shell 工具沙箱化**：
- 只有 Codex 提供的 shell 工具被沙箱化
- MCP 工具自己执行 guardrails
- 必须以一致顺序枚举 MCP 工具（避免 cache miss）

**Prompt.md 中的 Done When 原则**：每个工具调用结果都应有明确的"done when"判断标准。

### 3.4 Interpreter 持久性（ArXiv: Interpreter Persistence, 2026）

**核心发现**：Interpreter persistence（解释器状态跨步骤持久化）不只是运行时 scaffold，而是**训练数据的语义属性**。

2×2 交叉评估结果：
- 在 **stateless runtime** 中使用 **persistent-trained 模型**：~80% episodes 触发 missing-variable 错误
- 在 **persistent runtime** 中使用 **stateless-trained 模型**：浪费 ~3.5x tokens 重新推导已保留状态

**实践建议**：对齐微调数据与部署运行时的解释器持久化语义，提高效率，减少训练-运行时不匹配的脆弱性。

---

## 四、Prompt Building（提示构建）

### 4.1 Anthropic 的 Agent 系统提示原则

**构建块：Augmented LLM**
Anthropic 认为所有 agentic systems 的基础构建块是"增强型 LLM"，实现：检索、工具、记忆三重增强。

**Prompt 顺序（Anthropic Building Effective Agents）：**
- 从简单模式开始，逐步增加复杂度
- 优先使用 prompt chaining（提示链）、retrieval、in-context examples 解决问题
- 只有在简单方案不足时才引入 agent 架构

### 4.2 OpenAI Codex 的 Prompt 构建顺序

Codex prompt 在用户消息前插入（Responses API 格式）：

```
1. role=developer:  沙箱权限描述（shell 工具）
2. role=developer:  config.toml 中的 developer_instructions
3. role=user:       AGENTS.md、AGENTS.override.md、skills 元数据中的用户指令聚合
4. role=user:       环境上下文（cwd, shell）
```

**缓存优化原则**：
- 静态内容（instructions, examples）放在前面
- 可变内容放在后面
- 精确前缀匹配才能命中缓存

### 4.3 长程 Agent 的提示策略

**Anthropic（Effective Harnesses, 2025）**发现对首个 context window 使用"不同 prompt"效果显著：
- 首个 prompt：Initializer Agent 专用，建立环境和 feature list
- 后续 prompt：Coding Agent，做增量推进 + 留下 clean state

**OpenAI Codex 的"好 Agent"提示特征：**
- 明确的 target 和 constraints（spec file）
- Checkpointed milestones with acceptance criteria
- Runbook for how the agent operates
- Continuous verification（tests/lint/typecheck/build）
- Live status/audit log

### 4.4 Self-Evaluation 与Separation of Concerns

Anthropic（Harness Design, 2026）发现：
- Agent 在评价自己产出时倾向于过度自信赞美（即使质量平庸）
- 即使有可验证结果的任务，agent 也会表现出阻碍正确执行的判断失误

**解决方案**：将"生成者"和"评价者"agent 分离。分离后，调优独立 evaluator 比让生成器自我批评要容易得多。

---

## 五、ReAct 范式：推理与行动的协同

### 5.1 ReAct 核心思想（ArXiv: 2210.03629, Yao et al., 2022）

ReAct = **Re**asoning + **Act**ing

主要贡献：让 LLM **交错生成推理轨迹（reasoning traces）和任务特定动作（actions）**，实现两者间的强协同：

- **推理轨迹**帮助模型：诱导(induce)、跟踪(track)、更新行动计划；处理异常
- **动作**让模型与外部来源（知识库、环境）交互，获取额外信息

### 5.2 ReAct vs. 其他范式

| 方法 | 特点 | 问题 |
|---|---|---|
| Chain-of-Thought（仅推理） | 连续推理，但不与外部环境交互 | 幻觉和错误传播 |
| Action Plan Generation（仅行动） | 生成动作，但缺乏高层次目标跟踪 | 缺乏反思能力 |
| ReAct（推理+行动交错） | 推理引导行动，行动补充信息 | 需要设计合适的 action space |

### 5.3 ReAct 的实践效果

- **HotpotQA & Fever（问答/事实核查）**：通过 Wikipedia API 交互，克服幻觉和错误传播
- **ALFWorld（交互式决策）**：比 imitation 和 RL 方法高 **34%** 绝对成功率
- **WebShop**：比基线方法高 **10%** 绝对成功率
- 推理轨迹使任务解决路径更**可解释**（相比无推理 trace 的基线）

---

## 六、多 Agent 协作与长程规划

### 6.1 Task-Decoupled Planning（TDP）（ArXiv: 2601.07577, 2026）

**问题**：现有方法（step-wise planning / one-shot planning）都存在 entangled contexts——agent 必须在跨越多个子任务的单一历史中推理，导致：
- 认知负荷高
- 局部错误传播到无关决策
- 恢复计算代价大

**TDP 解决方案**：
- 将任务分解为由 Supervisor 生成的**有向无环图（DAG）**子目标
- Planner 和 Executor 使用**scoped contexts**
- 推理和重新规划被限制在活跃子任务内
- 结果：在 TravelPlanner、ScienceWorld、HotpotQA 上超过强基线，token 消耗降低 **82%**

### 6.2 三 Agent 架构：Planner + Generator + Evaluator

Anthropic（Harness Design, 2026）将 GAN 思想引入 agent 设计：

```
Planner Agent   → 制定计划，分解里程碑
Generator Agent → 执行实现
Evaluator Agent → 独立评估输出质量
```

关键创新：
- Generator 和 Evaluator 分离解决 self-evaluation 问题
- 用 evaluator 的 grading criteria 将主观判断（"设计好吗？"）转化为可评分的具体项

### 6.3 OpenAI 的 Agent-to-Agent 协作

**Ralph Wiggum Loop**：
- 人类描述任务 → Codex review 自己变更 → 请求特定 agent review → 响应反馈 → 迭代直到所有 agent reviewer 满意
- 人类可能 review PR，但**不是必须的**
- 大部分 review 负担已被推向 agent-to-agent 处理

---

## 七、Evaluation（评测）作为 Agent Loop 一环

### 7.1 为什么 Agent 难以评测

Anthropic（Demystifying Evals, 2026）指出 Agent 难以评测的原因正是使其有用的特性：

```
自主性(Autonomy) + 智能(Intelligence) + 灵活性(Flexibility)
```

这些特性使 Agent 能找到绕过静态评测限制的创意方案——甚至在"失败"评测时给出比预设更好的解决方案。

### 7.2 评测结构

| 概念 | 定义 |
|---|---|
| Task | 有定义输入和成功标准的单个测试 |
| Trial | 每次 Task 的尝试（因输出可变，需多次运行） |
| Grader | 评分某方面表现的逻辑（一个 Task 可有多个 Grader） |
| Transcript/Trace | 完整记录：输出、工具调用、推理、中间结果 |
| Outcome | Trial 结束时环境最终状态 |
| Eval Harness | 运行评测的基础设施 |
| Agent Harness/Scaffold | 使模型能作为 agent 行动的系统 |
| Eval Suite | 为测量特定能力设计的 Task 集合 |

### 7.3 多维 Grading 策略

Agent 评测需组合多种 grader 类型（Anthropic）：

```yaml
grader:
  - type: deterministic_tests    # 确定性测试
  - type: llm_rubric            # LLM 评审（主观质量）
  - type: static_analysis       # 静态分析（ruff, mypy, bandit）
  - type: state_check           # 状态检查（安全日志、DB状态）
  - type: tool_calls            # 必需的工具调用序列
tracked_metrics:
  - type: transcript            # n_turns, n_toolcalls, n_total_tokens
  - type: latency               # time_to_first_token, tokens_per_sec
```

### 7.4 OccuBench 评测发现（ArXiv: 2604.10866, 2026）

- 没有单一模型在所有行业领域占主导——每个模型有独特的能力轮廓
- **隐式故障**（截断数据、缺失字段）比显式错误（超时、500）更难——因为缺乏明显错误信号，需要 agent 独立检测数据降级
- 更大模型、更新代际、更高推理投入一致改善性能
- GPT-5.2 从最小到最大推理投入提升 **27.5 points**

---

## 八、关键设计原则汇总

### Agent Loop 设计

1. **从简单开始**：单 LLM 调用 + retrieval + in-context examples 优先，只有必要时才引入 agent
2. **保持可组合性**：避免过度框架抽象，用几行代码实现模式后再考虑框架
3. **Session 间交接产物**：claude-progress.txt、git history、markdown 状态文件
4. **Initializer + Coding 双组件**：首个 session 专门建立环境和计划
5. **Compaction + Reset 组合**：compaction 不够时，用 context reset 提供干净 slate

### Context Engineering 设计

1. **Treat context as finite resource**：有边际收益递减，注意力稀缺
2. **Map not manual**：给 Agent 地图（结构化状态文件），而非千页手册
3. **Static first, variable last**：prompt 缓存优化语序
4. **Durable project memory**：Prompt.md / Plan.md / Implement.md / Documentation.md
5. **Feature list + Git history**：作为 agent 间快速状态传递机制

### Tool Design 设计

1. **Scope 清晰，自包含，可组合**
2. **对齐训练和运行时**：interpreter persistence 是训练数据语义，需与部署环境一致
3. **沙箱边界清晰**：Codex 只沙箱化自有 shell 工具，MCP 工具自护
4. **MCP 工具顺序一致**：避免 cache miss

### Prompt Building 设计

1. **分离生成器和评价器**：解决 self-evaluation 过度宽容问题
2. **每个 milestone 有"Done When"**：明确终止判断标准
3. **Checkpointed milestones**：将开放式工作转为带验收标准的检查点
4. **Continuous verification**：每步后运行测试/lint/typecheck
5. **Prompts 驱动而非框架驱动**：理解底层 prompt 和响应

---

## 九、来源索引

| 文件 | 核心贡献 |
|---|---|
| `anthropic_..._building_effective_agents` | Agent 定义、Workflow vs. Agent、Prompt Chaining、Agent Loop 基础 |
| `anthropic_..._trustworthy_agents` | Agent 四组件模型（Model/Harness/Tools/Environment）、人类控制原则 |
| `anthropic_..._effective_context_engineering` | Context Engineering vs. Prompt Engineering、Context Rot、注意力稀缺 |
| `anthropic_..._effective_harnesses` | Initializer+Coding 双组件、Session 间交接产物、Feature List |
| `anthropic_..._harness_design` | 三 Agent（Planner/Generator/Evaluator）、Self-Evaluation 分离、GAN 思想 |
| `anthropic_..._demystifying_evals` | Agent 评测结构、多维 Grading、Eval Harness vs. Agent Harness |
| `openai_..._unrolling_the_codex_agent_loop` | Codex Agent Loop 详解、Quadratic Problem、Compaction、ZDR 设计 |
| `openai_..._run_long_horizon_tasks_with_codex` | Durable Project Memory、时间视野、25 小时 run 经验 |
| `openai_..._harness_engineering` | 零代码全 Agent 构建、Map not Manual、Agent-to-Agent review |
| `openai_..._skills_shell_tips` | Skills + Compaction + Shell 协作模式 |
| `arxiv_2210.03629` | ReAct：推理与行动协同范式 |
| `arxiv_2601.07577` | TDP：Task-Decoupled Planning，DAG 子目标分解 |
| `arxiv_2603.01209` | Interpreter Persistence 是训练数据语义，2×2 对齐研究 |
| `arxiv_2604.10866` | OccuBench：多行业 Agent 评测，隐式故障最难 |
