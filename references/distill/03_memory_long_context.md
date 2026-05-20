# Memory & Long-Running Context：持久化记忆、Compaction 与 Context 管理

> 来源：01_critical（Anthropic + OpenAI）、04_blogs（LangChain ×2 + Claude Code）、02_arxiv（9篇相关论文）
> 主题：持久化 memory、compaction、context 管理、长期任务

---

## 核心挑战：Context 的有限性与任务持久性的矛盾

长生命周期 Agent 面临一个根本矛盾：**任务持续时间 > Context Window 容量**。

LLM 的 Context Window 是有限的，但复杂任务（软件工程、数据分析、SRE 事故处理）可能跨越数小时甚至数天。Agent Loop 的默认模式——将所有历史塞入 Context——必然在某个时刻崩溃。

所有参考来源都指向同一个结论：**Harness 必须主动管理 Context，不能依赖"无限上下文"的假设**。

---

## 一、Context 压缩（Compaction）策略

### 1.1 压缩的三种模式

| 模式 | 触发方式 | 代表来源 |
|------|---------|---------|
| **Harness 控制压缩** | Harness 检测到 Context 接近上限，强制触发压缩 | Anthropic、Claude Code |
| **Agent 自主压缩** | Agent 自身判断何时压缩、用何种粒度 | LangChain Autonomous Context Compression |
| **自适应渐进压缩** | 随着对话进行，逐步降低旧观察的粒度 | OPENDEV「Adaptive Context Compaction」|

**Claude Code 的 Compaction 模型**尤为清晰：
- **Truncation（截断）**：直接丢弃最早的消息对，保留系统提示和最近历史
- **Synthesis（综合）**：将一段消息对压缩为一句摘要，保留语义要点
- **Working Memory（工作记忆）**：显式区分"当前任务相关"与"历史积累"

### 1.2 Context Rot（上下文腐化）

LangChain 博客明确提出 **Context Rot** 概念：随着 Context 窗口被填入越来越多的历史文本，模型对早期关键信息的"感知"会下降，即使这些信息仍在窗口内。

压缩是对抗 Context Rot 的核心手段，但压缩本身也有风险：**摘要可能丢失关键细节，特别是当模型需要"回顾"被压缩的决策理由时**。

### 1.3 LangChain Deep Agents SDK 的 Autonomous Compression

LangChain 在 Deep Agents SDK 中实现了**Agent 自主触发压缩**的工具：

```
压缩触发条件：
- 工具执行次数过多（工具调用累积）
- Context 利用率接近阈值
- Agent 主动判断"当前上下文已包含足够历史"

压缩操作：
- 将早期消息对替换为压缩后的摘要
- 摘要保留：任务目标、已完成步骤、当前障碍、关键约束
```

**设计哲学**：让 Agent 自己决定何时压缩，因为 Agent 最清楚哪些信息对当前子任务仍然关键。Harness 提供压缩工具，但不替代 Agent 做判断。

---

## 二、持久化记忆（Persistent Memory）

### 2.1 多层记忆架构

基于 Mem0、claude-mem 等开源实践，成熟 Agent 系统采用**三层记忆架构**：

| 层级 | 内容 | 持久性 | 检索方式 |
|------|------|--------|---------|
| **Working Memory** | 当前 Session 的完整上下文 | Session 结束即销毁 | 直接塞入 Context |
| **Episodic Memory** | 跨 Session 的经验记录（总结、成果） | 持久化存储 | 按需检索（RAG） |
| **Semantic Memory** | 结构化知识、规则、偏好 | 持久化存储 | 向量检索/查询 |

### 2.2 Session Bridging（会话桥接）

Anthropic 的 Harness 设计指南将 **Session Bridging** 列为长运行任务的核心工程手段：

```
Bridge 需要传递的信息：
1. 当前进度快照（已完成步骤、当前位置）
2. 工作目录状态（文件修改、中间结果）
3. 上下文摘要（历史决策要点、约束条件）
4. Feature Flags（任务特定配置）
```

**Hibernate & Wake 模式**（Meta Ranking Engineer Agent 实践）：
- 任务中断时：执行 checkpoint，保存完整状态
- 任务恢复时：从 checkpoint 加载，跳过已验证的步骤
- 防止中断导致"重复劳动"和"状态不一致"

### 2.3 OPENDEV 的 Automated Memory System

OPENDEV（终端编程 Agent）提出了一套具体的跨 Session 记忆系统：

- **项目特定知识积累**：每次 Session 结束后，将项目相关的工具使用模式、路径约定、偏好配置写入持久化存储
- **Event-driven System Reminders**：Agent 不仅被动检索记忆，还会在特定操作（如 git push）触发相关提醒
- **对抗 Instruction Fade-out**：防止"初始指令"在长对话后期被稀释

---

## 三、Context 管理的架构模式

### 3.1 Agent Loop 的结构性问题 → Structured Graph Harness

arXiv 论文 **SGH (Structured Graph Harness, 2604.11378)** 从调度理论角度分析了 Agent Loop 的三个结构性弱点：

1. **隐式依赖**：步骤间的依赖关系藏在 Context 里，调试困难
2. **无界恢复循环**：错误恢复没有上限，可能无限循环
3. **可变执行历史**：Context 本身在每次迭代后变化，导致不可重复

SGH 提出的解法：将控制流从隐式 Context 提升为**显式静态 DAG**：

```
SGH 三项承诺：
1. 执行计划在版本内不可变（plan version）
2. 规划、执行、恢复分离为三层
3. 恢复遵循严格的升级协议（escalation protocol）

交换：牺牲部分表达力 → 获得：可控性、可验证性、可实现性
```

### 3.2 Task-Decoupled Planning（TDP）

arXiv 论文 **TDP (2601.07577)** 针对"纠缠上下文"问题提出任务解耦：

```
核心思路：用 DAG 分解任务，限制每个子任务的 Context 范围

- Supervisor 将任务分解为 DAG 结构的子目标
- Planner 和 Executor 各自只有"当前子任务"的上下文
- 错误被限制在子任务内，不会传播到其他分支
- 减少 Token 消耗最高达 82%（TravelPlanner, ScienceWorld, HotpotQA）

这实际上是一种"Context 隔离"策略：通过架构约束而不是压缩来管理 Context
```

### 3.3 双Agent架构：规划与执行分离

OPENDEV 和 Plan-and-Act (2503.09572) 都采用了**Planner + Executor 分离**：

- **Planner**：维护高层计划上下文，不需要理解底层执行细节
- **Executor**：维护当前步骤的详细上下文，不需要全局计划
- **优势**：两个 Agent 的 Context 各自独立增长，互不污染

---

## 四、Context 与 Runtime 的对齐问题

### 4.1 Interpreter Persistence（解释器持久性）

arXiv 论文 **Agents Learn Their Runtime (2603.01209)** 揭示了一个微妙但关键的问题：

```
发现：训练时的轨迹（traces）与部署时的 Runtime 必须匹配

2x2 实验设计：
- 训练时持久 / 部署时持久 → 正常
- 训练时持久 / 部署时无状态 → 80%  episodes 触发 missing-variable 错误
- 训练时无状态 / 部署时持久 → 3.5x Token 浪费（重复推导已保持状态）
- 训练时无状态 / 部署时无状态 → 正常

结论：解释器持久性应被视为 Agent 训练轨迹的一阶语义
```

这对 Harness 设计有直接指导：**Harness 的状态管理策略必须在训练和部署中保持一致**。

---

## 五、Context 管理的工程实践总结

### 5.1 压缩策略的选择

| 场景 | 推荐策略 | 理由 |
|------|---------|------|
| 短任务（< 50 步） | 不压缩 | 压缩开销大于收益 |
| 中等任务（50-200 步） | Harness 控制压缩 | 稳定可预测 |
| 长任务/多 Session | Agent 自主压缩 + Session Bridge | Agent 最清楚关键信息 |
| 超长任务（天级） | TDP/DAG 解耦 + 分层记忆 | Context 隔离是唯一可行方案 |

### 5.2 长期任务的 Checkpoint 设计

基于 Anthropic 指南和 Meta Ranking Agent 的实践：

```
Checkpoint 应包含：
- 当前 Context 的压缩摘要
- 文件系统状态差异（而非全量快照）
- 工具调用的历史（用于重放和验证）
- 任务特定的状态机位置

Checkpoint 频率：
- 每完成一个有意义子目标时触发
- 不在工具调用级别做 checkpoint（开销太大）
```

### 5.3 可观测性是 Context 管理的前提

LangChain 的 Harness Engineering 实践（Terminal Bench 从 Top 30 → Top 5）表明：

> 没有 Tracing，就无法知道 Context 为什么失效。

必须追踪：
- Context 利用率随时间的变化曲线
- 压缩操作的触发条件和效果
- 每个压缩周期内 Agent 的任务完成率

---

## 六、关键引用

| 来源 | 核心贡献 |
|------|---------|
| Anthropic - Engineering Effective Harnesses | Session bridging, checkpointing, feature flags, trust characteristics |
| LangChain - Autonomous Context Compression | Agent 自主压缩工具, Context rot 对抗 |
| LangChain - Harness Engineering | Tracing → 迭代改进, 自验证驱动 |
| Claude Code - Compaction Explained | Truncation / Synthesis / Working Memory 三模式 |
| OPENDEV (2603.05344) | Adaptive context compaction, dual-agent, event-driven memory |
| SGH (2604.11378) | Agent Loop → DAG, 不可变计划, 三层分离 |
| TDP (2601.07577) | Task-decoupled planning, scoped contexts, 82% token 减少 |
| Interpreter Persistence (2603.01209) | Train-runtime 对齐, 状态持久性作为训练语义 |
| Mem0 / claude-mem | 三层记忆架构, 跨 Session 记忆 |

---

## 七、未解决问题 & 开放挑战

1. **压缩信息损失**：当前压缩都是单向有损的，如何验证摘要没有丢失关键约束？
2. **Checkpoint 粒度**：过粗丢失进度，过细开销过大，最优粒度未知
3. **多 Agent 记忆共享**：当多个 Agent 并行工作时，记忆一致性问题
4. **Context 压缩的可验证性**：如何测试压缩操作没有改变 Agent 的正确行为？
5. **长期记忆的衰减**：随着记忆积累，检索质量如何保持？
