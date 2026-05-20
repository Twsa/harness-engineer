# Multi-Agent & Orchestration

> Multi-Agent 系统的核心问题：如何让多个专业化的 agent 高效协作，同时保持可控制性、可观测性和容错能力。

---

## 1. 核心框架

### AutoGen (Microsoft)

**状态**: 维护模式 → 已被 Microsoft Agent Framework (MAF) 取代

AutoGen 是微软研究院开创的多 Agent 框架，提出了双层 API 设计：

- **Core API**: 消息传递、事件驱动 Agent、本地/分布式运行时
- **AgentChat API**: 面向快速原型，支持双 Agent 对话和群聊
- **Extensions API**: LLM 客户端实现（OpenAI、AzureOpenAI）、代码执行等能力

```python
# AgentTool: 将 Agent 作为 Tool 调用，实现多 Agent 编排
math_agent_tool = AgentTool(math_agent, return_value_as_last_message=True)
chemistry_agent_tool = AgentTool(chemistry_agent, return_value_as_last_message=True)

agent = AssistantAgent(
    "assistant",
    tools=[math_agent_tool, chemistry_agent_tool],
    max_tool_iterations=10,
)
```

**典型案例**: Magentic-One — 多 Agent 团队，处理 Web 浏览、代码执行、文件操作等任务。

---

### CrewAI

**定位**: 独立框架（不依赖 LangChain），兼顾高-level 简单性和低-level 精确控制。

两种核心范式：

| 范式 | 特点 | 适用场景 |
|------|------|----------|
| **Crews** | 自治决策、动态任务委托、角色协作 | 复杂、探索性任务 |
| **Flows** | 事件驱动、精确控制、状态管理、条件分支 | 生产级精确工作流 |

```python
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,
        tasks=self.tasks,
        process=Process.sequential,  # 或 Process.hierarchical
        verbose=True,
    )
```

关键机制：YAML 配置化 Agent/Task 定义，支持 `crewai create crew` 脚手架。

---

### OpenHands

**定位**: AI-driven 开发助手（类 Devin/Jules），覆盖 SDK/CLI/GUI/Cloud 多形态。

- **SWE-bench**: 77.6% 准确率（开源前列）
- 核心组件：Agent SDK、CLI、Local GUI、REST API
- 支持 Slack/Jira/Linear 集成、RBAC、协作功能

---

### SWE-agent

**定位**: 专用 Agent，用于 GitHub Issue 修复 + 安全漏洞发现。

- 学术项目（Princeton/Stanford）
- 核心设计理念：leave maximal agency to the LM（最大化语言模型自主权）
- 配置完全由单一 `yaml` 文件驱动，适合研究复现

---

## 2. 多 Agent 编排模式（LangChain 分类）

LangChain 总结了四种经典多 Agent 模式，各有优劣：

### 2.1 Subagents（子 Agent）

- 每个子 Agent **独立运行**，通过工具调用交互
- **无状态** → 强上下文隔离，Token 效率高
- 支持**并行执行**
- 适合：大上下文域、多领域并行查询

```
场景：对比 Python/JavaScript/Rust → 三个语言 Agent 并行工作
Token: ~9K（vs Skills 的 ~15K）
```

### 2.2 Skills（技能）

- 主 Agent 动态调用技能，所有技能**共享单一上下文窗口**
- 有状态 → 重复请求节省 40-50% 调用
- 适合：单域重复请求，但大上下文会累积 Token

### 2.3 Handoffs（交接）

- Agent 之间**显式交接**，传递完整上下文
- 有状态，支持流式交接
- 必须**顺序执行**，多域场景效率低（7+ 调用，~14K+ tokens）

### 2.4 Router（路由器）

- 意图识别后**分发到专用 Agent**，结果汇总
- 支持并行执行
- 无状态（每次独立）
- 适合：多领域、并行查询场景

### 性能对比总结

| 模式 | 单次请求 | 重复请求 | 并行执行 | 大上下文域 |
|------|---------|---------|---------|-----------|
| Subagents | — | — | ✅ | ✅ |
| Skills | ✅ | ✅ | — | — |
| Handoffs | ✅ | ✅ | — | — |
| Router | ✅ | — | ✅ | ✅ |

---

## 3. 多 Agent 失败模式与工程化原则（GitHub Blog）

GitHub 团队在 Copilot + 内部自动化中发现：多 Agent 系统更像**分布式系统**而非对话界面。

### 三大失败根因

#### 失败1：自然语言的歧义性
Agent 之间交换的数据格式不一致 → Schema 校验失败。

**解法：Typed Schemas（类型化模式）**
```typescript
type UserProfile = {
  id: number;
  email: string;
  plan: "free" | "pro" | "enterprise";
};
```
Schema 违规视为契约失败，快速失败（fail-fast），避免错误状态传播。

#### 失败2：模糊意图导致不确定行为
"分析这个问题并帮助团队采取行动" → 不同 Agent 可能：关闭、指派、升级、不处理。

**解法：Action Schemas（动作模式）**
```typescript
const ActionSchema = z.discriminatedUnion("type", [
  { type: "request-more-info", missing: string[] },
  { type: "assign", assignee: string },
  { type: "close-as-duplicate", duplicateOf: number },
  { type: "no-action" }
]);
```
Agent 必须返回**有限、明确的动作集**，任何其他输出都是验证失败。

#### 失败3：松散接口导致运行时错误
Schema 和 Action Schema 定义了契约，但没有强制执行层。

**解法：MCP（Model Context Protocol）**
- 定义显式 input/output schema
- **调用前验证**，防止坏状态进入生产系统
- Schema 定义结构，MCP 负责执行

### 核心工程原则
1. **Schema 即契约**：跨 Agent 接口必须类型化
2. **Action 需枚举**：输出空间必须有限、可验证
3. **MCP 即执行层**：验证前置于运行

---

## 4. 学术前沿

### AdaptOrch: 拓扑感知编排（2026）

**核心论点**：当主流 LLM 基准性能趋于收敛时，**编排拓扑**（而非模型选择）成为系统性能的主导因素。

**四大拓扑**：
- **Parallel（并行）**：独立子任务并行处理
- **Sequential（顺序）**：依赖链式执行
- **Hierarchical（层级）**：管理器 Agent 协调子 Agent
- **Hybrid（混合）**：组合以上模式

**三大贡献**：
1. **Performance Convergence Scaling Law**：证明何时拓扑选择 > 模型选择
2. **Topology Routing Algorithm**：O(|V|+|E|) 时间复杂度，将任务 DAG 映射到最优拓扑
3. **Adaptive Synthesis Protocol**：带终止保证的一致性评分

**实验结果**：在 SWE-bench、GPQA、RAG 任务上，拓扑感知编排比静态拓扑基线提升 **12-23%**，且使用相同底层模型。

---

### Plan-and-Act: 规划-执行分离（2025）

**核心思想**：将**高层规划**（Planner）和**低层执行**（Executor）解耦，使用不同模型。

```
用户目标 → Planner 生成结构化计划 → Executor 转化为环境动作
```

**关键技术**：
- 合成数据生成：为真实轨迹标注可行计划 + 增强泛化样本
- WebArena-Lite: **57.58%**（SOTA）
- WebVoyager: **81.36%**（Text-only SOTA）

**与 ReAct 的区别**：ReAct 在单模型内混合规划与执行；Plan-and-Act 使用专用 Planner 模型生成显式高层计划，再由 Executor 细粒度执行。

---

## 5. 编排设计的核心张力

| 张力维度 | 一端 | 另一端 |
|---------|------|-------|
| 自主性 vs 控制 | Crews（高自治） | Flows（精确控制） |
| 上下文效率 | Subagents（隔离，无冗余） | Skills/Handoffs（累积，有状态） |
| 复杂性 | Router（简单分发） | Hierarchical（管理器协调） |
| 失败恢复 | Stateless（独立重试） | Stateful（上下文携带，容错好） |
| 执行顺序 | Parallel（高效） | Sequential（必需时保证正确性） |

---

## 6. 实践建议

1. **从单 Agent 开始**：多 Agent 引入额外复杂度，只有在上下文溢出或团队边界清晰时才引入
2. **选择拓扑看任务特征**：多域并行查询 → Subagents/Router；单域深度 → Skills/Handoffs
3. **Schema-first**：任何 Agent 间数据交换先定义 Schema，用 MCP 强制验证
4. **Action 枚举化**：Agent 输出空间必须有限，防止歧义扩散
5. **编排拓扑是可优化维度**：AdaptOrch 表明同等模型下拓扑选择可带来 12-23% 提升，应作为一等公民设计

---

## 关键概念映射

| 概念 | 代表框架/论文 |
|------|-------------|
| 双层 API（Core + AgentChat） | AutoGen |
| Crews + Flows 双范式 | CrewAI |
| 工具化 Agent（AgentTool） | AutoGen |
| 子 Agent 并行 + 上下文隔离 | LangChain Subagents |
| 状态化技能调用 | LangChain Skills |
| 显式交接传递上下文 | LangChain Handoffs |
| 意图路由分发 | LangChain Router |
| Typed Schema 契约 | GitHub Blog |
| Action Schema 枚举 | GitHub Blog |
| MCP 执行验证层 | GitHub Blog |
| 拓扑选择 > 模型选择 | AdaptOrch |
| 规划-执行解耦 | Plan-and-Act |
| 工具增强 Agent | SWE-agent |
