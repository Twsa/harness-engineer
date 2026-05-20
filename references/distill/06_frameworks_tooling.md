# Frameworks & Tooling 蒸馏

> AI Agent 开发的核心框架、工具和最佳实践

---

## 1. LLM 评测框架

### DeepEval (Confident AI)

**定位**: 开源 LLM 评测框架，用于生成式 AI 的单元/集成测试

**核心特性**:
- **G-Eval 算法**: 使用 LLM 评估生成内容，支持 4 指标: 摘要相关性、问答准确性、幻觉检测、指令遵循
- **默认指标**: Task Completion (任务完成度)、Hallucination (幻觉率)、Answer Relevancy (答案相关性)、Contextual Precision/Rrecall
- **框架集成**: LangChain、LlamaIndex、CrewAI、AutoGen、Google ADK、Strands
- **评测模式**: RAGAS 基准模式、默认评测模式
- **设计理念**: 开发者应像测软件一样测 LLM 输出 — 红队测试、回归测试、冒烟测试

**技术实现**:
```
支持文件格式: JSON、CSV
评测方式: assert-based测试 + OAI包子类化
集成方式: Pytest插件、CI/CD集成
```

---

### LiteLLM (BerriAI)

**定位**: 统一 LLM API 网关，支持 100+ 模型提供商的 OpenAI 兼容格式

**核心能力**:
- **统一接口**: 所有provider使用OpenAI格式，零代码切换provider
- **支持Provider**: OpenAI、Anthropic、Google、Azure、Hugging Face、AWS Bedrock/Velocity、Ollama等100+
- **部署方式**: Proxy Server (LLM Gateway)、Python SDK
- **可靠性**: 最多5次重试、超时控制、幂等性保证
- **用量追踪**: spend tracking、断路器模式、流式输出支持

**代码示例**:
```python
from litellm import completion
response = completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hi"}]
)
```

**企业特性**:
- 价格对比、预算控制
- 多provider负载均衡
- 速率限制
- 结构化输出 (response_format)

---

## 2. Agent 代码执行沙箱

### Daytona

**定位**: OCI/Docker兼容的沙箱运行时，用于AI代码执行

**核心指标**:
- **Spin-up时间**: <90ms
- **兼容性**: OCI标准 (Docker镜像直接运行)
- **支持语言**: Python、TypeScript、JavaScript

**技术架构**:
- SDK + REST API + CLI
- 支持自定义runner镜像
- 适合: 代码Agent、沙箱化工具执行、自动化测试

**适用场景**: AI编码Agent的代码执行层，需要安全隔离的代码运行环境

---

### smolagents (Hugging Face)

**定位**: 轻量级代码Agent库，核心约1000行代码

**核心设计**:
- **模型无关**: 通过LiteLLM集成任何LLM Provider
- **代码优先**: Agent直接生成并执行代码，而非调用工具
- **MCP支持**: 内置Model Context Protocol工具集成

**执行后端**:
| 后端 | 说明 |
|------|------|
| E2B | 云端沙箱 |
| Modal | Serverless计算 |
| Docker | 本地容器 |
| Pyodide | 浏览器WASM |
| Blaxel | 自托管沙箱 |

**核心组件**:
```python
from smolagents import CodeAgent, LiteLLMModel
agent = CodeAgent(model=LiteLLMModel(model_id="gpt-4"))
```

---

## 3. 记忆系统

### Mem0 (Mem0ai)

**定位**: 为AI Agent设计的记忆层，跨会话持久化用户信息

**v3算法 (2026年4月)**:
| 指标 | v2 | v3 |
|------|-----|-----|
| LoCoMo | 71.4 | 91.6 |
| LongMemEval | 67.8 | 94.8 |

**技术实现**:
- **单次提取**: ADD-only记忆提取模式，降低延迟
- **实体链接**: 自动关联相关记忆实体
- **检索模式**: 即时、语义、图谱三种模式

**API接口**:
```python
# 存储记忆
mem0.add(user_id, "用户喜欢日本料理")
# 检索
memories = mem0.search(user_id, "晚餐推荐")
```

---

### Claude-mem (thedotmack)

**定位**: Claude Code专用持久记忆系统，v6.5.0

**技术栈**:
- **存储**: SQLite本地存储
- **解析**: AST抽象语法树解析
- **Node.js**: >=18.0.0

**核心功能**:
- 自动压缩记忆内容
- 项目上下文理解
- 跨项目记忆复用

**与Mem0区别**: Claude-mem偏本地CLI工具，Mem0偏云端/API服务

---

## 4. 项目规则引擎

### Cursor Rules (awesome-cursorrules)

**定位**: Cursor IDE的项目规则集合，使用`.mdc`格式

**规则分类**:
- **前端**: React、Vue、Svelte、Angular、Next.js、Nuxt
- **后端**: Node.js、Python、Django、FastAPI、Rails
- **移动**: React Native、Flutter、Swift、Kotlin
- **数据库**: PostgreSQL、MongoDB、Redis、Prisma
- **DevOps**: Docker、Kubernetes、CI/CD
- **语言**: TypeScript、Python、Rust、Go
- **其他**: CSS状态管理、测试、安全、文档

**格式示例**:
```markdown
---
description: React组件规则
tags: [react, frontend]
---

- 使用函数组件 + Hooks
- Props使用TypeScript接口
- 组件文件以大写开头
```

---

## 5. Agent推理框架

### ReAct (arXiv:2210.03629)

**论文**: Yao et al., 2022 - "Synergizing Reasoning and Acting in Language Models"

**核心思想**: 交错生成推理轨迹(thought)和动作(action)

**方法**:
- 推理链帮助模型诱导、跟踪、更新动作计划
- 动作使模型能接口外部源(知识库、环境)
- 处理异常情况

**实验结果**:
| 任务 | 提升 |
|------|------|
| HotpotQA (问答) | 克服幻觉和错误传播 |
| Fever (事实验证) | 外部知识API交互 |
| ALFWorld (交互决策) | +34%成功率 |
| WebShop (网购导航) | +10%成功率 |

---

### LATS (arXiv:2310.04406)

**论文**: Zhou et al., 2023 - "Language Agent Tree Search Unifies Reasoning Acting and Planning"

**全称**: Language Agent Tree Search

**核心创新**:
- 首个统一推理、动作、规划的通用框架
- 将Monte Carlo Tree Search (MCTS)引入LLM Agent
- LM-powered value functions + self-reflections
- 环境外部反馈机制

**性能**:
| 基准 | 模型 | 结果 |
|------|------|------|
| HumanEval | GPT-4 | **92.7%** pass@1 (SOTA) |
| WebShop | GPT-3.5 | 75.9平均分 (媲美梯度微调) |

---

## 6. MCP (Model Context Protocol)

### 协议设计

**定位**: Anthropic推出的Agent工具交互标准协议

**工具注解系统**:
```typescript
interface ToolAnnotations {
  title?: string;
  readOnlyHint?: boolean;     // 默认: false
  destructiveHint?: boolean;  // 默认: true
  idempotentHint?: boolean;   // 默认: false
  openWorldHint?: boolean;    // 默认: true
}
```

**四大注解含义**:
- `readOnlyHint`: 工具是否修改环境
- `destructiveHint`: 变化是否是破坏性的(而非添加性)
- `idempotentHint`: 相同参数重复调用是否安全
- `openWorldHint`: 工具是否与外部实体交互

**默认策略**: 无注解时假定最坏情况(非只读、破坏性、非幂等、开放世界)

### 2026路线图

**四大方向**:
1. **传输层扩展**: 支持更多连接方式，可扩展性
2. **Agent间通信**: 原生多Agent协作协议
3. **治理成熟**: SEP (Specification Enhancement Proposals) 流程完善
4. **企业就绪**: 认证、审计、合规

**SEP流程**: 社区驱动的协议增强提案机制

---

## 7. Agentic SaaS FinOps

### 单位经济学新范式

**核心观点**: 在Agentic SaaS中，**成本即可靠性指标**

**成本失控场景**:
- Agent遇到边界情况时倾向于"更努力"
- 重规划、重查询、重总结、重试
- 用户感知变慢，账单却激增

**控制机制**:

| 机制 | 作用 |
|------|------|
| Loop Limits | 防止无限重试 |
| Tool Call Caps | 限制单次会话工具调用数 |
| Model Routing | 简单任务用小模型 |

**实践建议**:
- 产品、工程、财务三方协同
- 回放Agent执行轨迹，协议成本护栏
- 护栏即用户体验定义

---

## 8. Vercel Agent友好页面

### Content Negotiation策略

**问题**: AI Agent需要读取网页内容，但传统HTML面向人类用户

**解决方案**:
```typescript
// Next.js rewrites配置
async rewrites() {
  return [
    {
      matcher: ['/blog/:path*'],
      destination: '/api/markdown/:path*'
    }
  ]
}
```

**两种渲染模式**:
1. **浏览器请求**: 返回HTML + JS (人类可读)
2. **Agent请求** (Accept: text/markdown): 返回纯Markdown

**实现方式**:
- Route Handler动态内容协商
- 服务端将富文本转为Markdown
- 响应头区分Content-Type

---

## 9. 工具链全景图

```
┌─────────────────────────────────────────────────────────┐
│                    AI Agent 架构                         │
├─────────────────────────────────────────────────────────┤
│  用户界面层  │  Web / CLI / API                         │
├─────────────┼───────────────────────────────────────────┤
│  Agent核心  │  ReAct / LATS / CoT / ToT                │
├─────────────┼───────────────────────────────────────────┤
│  框架层     │  smolagents / LangChain / AutoGen        │
├─────────────┼───────────────────────────────────────────┤
│  工具协议   │  MCP (Model Context Protocol)             │
├─────────────┼───────────────────────────────────────────┤
│  执行环境   │  Daytona (沙箱) / Docker / E2B / Modal    │
├─────────────┼───────────────────────────────────────────┤
│  LLM路由    │  LiteLLM (100+ Provider统一网关)          │
├─────────────┼───────────────────────────────────────────┤
│  评测体系   │  DeepEval / G-Eval / RAGAS               │
├─────────────┼───────────────────────────────────────────┤
│  记忆系统   │  Mem0 / Claude-mem                       │
└─────────────┴───────────────────────────────────────────┘
```

---

## 10. 关键工具选型指南

| 场景 | 推荐工具 | 原因 |
|------|----------|------|
| LLM统一调用 | LiteLLM | 100+ provider，OpenAI格式 |
| Agent代码执行 | smolagents + Daytona | 轻量、MCP支持、<90ms启动 |
| 记忆系统 | Mem0 | 专门为Agent设计，v3性能优异 |
| 项目规范 | Cursor Rules | 团队代码风格统一 |
| LLM输出评测 | DeepEval | 单元测试思维，可集成CI |
| 工具标准化 | MCP | Anthropic主推，行业趋势 |
| Agent推理 | LATS | 统一推理+动作+规划 |

---

## 来源索引

### GitHub README
- `05_github/PatrickJS_awesome-cursorrules_README.md` - Cursor Rules规则集
- `05_github/confident-ai_deepeval_README.md` - DeepEval评测框架
- `05_github/BerriAI_litellm_README.md` - LiteLLM统一网关
- `05_github/huggingface_smolagents_README.md` - smolagents代码Agent
- `05_github/thedotmack_claude-mem_README.md` - Claude-mem记忆
- `05_github/mem0ai_mem0_README.md` - Mem0记忆层
- `05_github/daytonaio_daytona_README.md` - Daytona沙箱

### Blog
- `04_blogs/mcp_blog_modelcontextprotocol_io_posts_2026_03_16_tool_annotations.txt` - MCP工具注解
- `04_blogs/mcp_blog_modelcontextprotocol_io_posts_2026_mcp_roadmap.txt` - MCP路线图
- `04_blogs/infoworld_...finops_for_agents...txt` - FinOps for Agents
- `04_blogs/vercel_vercel_com_blog_making_agent_friendly_pages...txt` - Agent友好页面

### arXiv
- `02_arxiv/arxiv_arxiv_org_abs_2210_03629.txt` - ReAct论文
- `02_arxiv/arxiv_arxiv_org_abs_2310_04406.txt` - LATS论文
