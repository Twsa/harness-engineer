# Verification & Reliability 蒸馏笔记

> 来源：03_msft_meta、04_blogs（githubblog/cursor/nvidia/infoworld）、02_arxiv（fault/evaluation/benchmark相关）
> 主题聚焦：evals、self-healing、reliability、verification

---

## 1. 核心问题定义

### AI Agent Reliability 的科学基础
**论文：arXiv 2602.16666 - Towards a Science of AI Agent Reliability**

AI agent在执行重要任务时，准确率提升的表象与实际失败率之间存在显著差距。当前评估的根本局限：将agent行为压缩为单一成功指标，掩盖了关键操作缺陷。

**四个可靠性维度，12个具体指标：**

| 维度 | 指标 |
|------|------|
| **Consistency（一致性）** | 跨运行的行为一致性、相同输入的输出稳定性 |
| **Robustness（鲁棒性）** | 抗扰动能力、对输入变化的敏感性 |
| **Predictability（可预测性）** | 失败模式可预测、错误边界有界 |
| **Safety（安全性）** | 危险操作隔离、数据泄露防护 |

**关键发现：** 在14个模型、2个基准测试上的评估表明，近期能力提升仅带来可靠性方面的小幅改进。

---

## 2. Sandbox 设计与实现

### Cursor Agent Sandboxing
**来源：Cursor Blog - Agent Sandboxing**

**目标：** 消除中断的同时提升安全性，为agent提供足够权限保持有效性，同时拒绝产生风险的操作权限。

**跨平台实现：**

#### macOS - Seatbelt
- 评估了App Sandbox、容器、VM、Seatbelt四种方案
- App Sandbox需签名每个agent可能执行的二进制，引入复杂性
- Seatbelt（`sandbox-exec`）提供细粒度策略语言，约束整个子进程树
- 动态生成策略：基于workspace级别、管理员级别设置和`.cursorignore`

```scheme
(deny file-write* (regex "^.*/\\.vscode($|/.*)"))
(deny file-write* (require-all
    (regex "^.*/\\.cursor($|/.*)")
    (require-not (regex "^.*/\\.cursor/(rules|commands|worktrees|skills|agents)($|/.*)"))))
```

#### Linux - Landlock + seccomp
- Landlock：文件系统限制，使忽略的文件对沙盒进程完全不可访问
- seccomp：阻止不安全的系统调用
- 策略：用户workspace映射到overlay文件系统，用Landlocked副本覆盖忽略的文件

#### Windows - WSL2
- 构建原生Windows沙盒较难，现有沙盒原语主要面向浏览器
- 当前在WSL2内运行Linux沙盒
- 与Microsoft合作确保必要原语可用

**Teaching Agents to Use Sandbox：**
1. 更新Shell工具描述，说明沙盒约束（文件系统/git/网络访问）
2. 使用Cursor Bench内部基准评估影响
3. 识别常见失败模式：agent重复重试相同终端命令而不更改权限
4. 改进Shell工具结果渲染：明确显示失败原因，建议权限升级
5. 离线评估性能显著提升
6. 生产环境逐步推出，持续收集反馈

**效果：** 沙盒agent比非沙盒agent停止频率降低40%

---

## 3. 安全控制框架

### NVIDIA AI Red Team - Mandatory Controls
**来源：NVIDIA Developer Blog - Practical Security Guidance**

**Must-Have（三项强制控制）：**

#### 1. Network Egress Controls
- 阻止网络访问任意站点，防止数据外泄或建立远程shell
- 允许已批准的连接，拒绝未经授权的连接
- 限制DNS解析到指定信任解析器，防止DNS-based外泄
- 默认-ask + 企业级denylist（用户无法覆盖）

#### 2. Block File Writes Outside Workspace
- 阻止向workspace外写入文件，防止持久化、sandbox逃逸、RCE技术
- 保护文件类型：`~/.zshrc`（RCE+sandbox逃逸）、`~/.gitconfig`、`~/.curlrc`（重定向敏感数据）、`~/.local/bin`（放置后门二进制）

#### 3. Block Writes to Agent Configuration Files
- 保护`.cursorrules`、`CLAUDE.md`、`copilot-instructions.md`等agent配置文件
- 保护hooks、MCP服务器配置（stdio transport定义的shell命令）
- Claude Skills中的脚本/代码/辅助函数
- 直接手动修改是唯一可接受的修改机制

**Recommended Controls：**
- 阻止workspace外的文件读取
- 整个IDE和所有生成函数都在沙盒中运行（使用独立用户）
- 使用虚拟化隔离沙盒内核（microVM、Kata容器、完整VM）
- 每个特定操作实例都需要用户批准（不允许"允许一次/运行多次"）
- 秘密注入方法防止secrets被agent共享
- 沙盒生命周期管理，防止代码/IP/secrets积累

**Tiered Implementation：**
1. 企业级denylist：关键文件访问无法被用户覆盖
2. workspace内读写（配置文除外）无需批准
3. 特定白名单操作（如读取`~/.ssh/gitlab-key`）可批准
4. 其他操作默认拒绝，逐案用户批准

---

## 4. Agentic RAG 可靠性

### A-RAG: Agentic Retrieval-Augmented Generation
**来源：arXiv 2602.03442**

**问题：** 现有RAG系统依赖两种范式：
1. 单次检索算法 + 拼接 passages 到模型输入
2. 预定义工作流 + step-by-step执行

两者都不允许模型参与检索决策。

**解决方案：** A-RAG框架，向模型暴露分层检索接口

**三个检索工具：**
- Keyword Search（关键词搜索）
- Semantic Search（语义搜索）
- Chunk Read（块读取）

**关键能力：**
- 模型自适应搜索和检索不同粒度的信息
- 在多个开放域QA基准测试中持续优于现有方法
- 使用更少检索token达到同等或更好性能
- 随模型规模和测试时计算可扩展

---

## 5. ReAct: Reasoning + Acting
**来源：arXiv 2210.03629**

**核心思想：** 在交错方式中同时生成推理轨迹和任务特定动作

**推理轨迹的作用：**
- 诱导、跟踪、更新动作计划
- 处理异常

**动作的作用：**
- 接入外部资源（知识库、环境）
- 收集额外信息

**在问答（HotpotQA）和事实验证（Fever）上：**
- 克服CoT推理中的幻觉和错误传播问题
- 通过简单Wikipedia API交互生成人类可读的任务解决轨迹

**在交互式决策基准（ALFWorld和WebShop）：**
- 比模仿学习和强化学习方法分别提升34%和10%的绝对成功率
- 仅需1-2个in-context examples

---

## 6. FinOps for Agents - 经济可靠性
**来源：InfoWorld - FinOps for agents**

**核心观点：** 在agentic SaaS中，**成本即可靠性指标**

**问题：** 少量会话命中边界情况时，agent会"更努力"——重规划、重新查询、重新总结、重试工具调用。用户看到响应稍慢，财务看到可变支出阶跃变化。

**解决方案：Loop Limits & Tool Call Caps**

**实践方法：**
- 产品、工程、财务同室复盘agent traces
- 协议在用户体验中定义护栏
- 定义loop限制防止无限重试
- 工具调用上限保护边际

---

## 7. 关键模式总结

### Reliability Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Reliability Framework              │
├─────────────────────────────────────────────────────────────┤
│  Consistency          │  Robustness        │  Safety      │
│  ─────────────        │  ──────────         │  ──────      │
│  • Deterministic exec │  • Input perturbed  │  • Sandbox   │
│  • Same I→Same O      │  • Error bounds     │  • Egress    │
│                       │                     │  • Config    │
├─────────────────────────────────────────────────────────────┤
│                    Predictability                           │
│                    ───────────────                           │
│                    • Failure modes predictable               │
│                    • Error severity bounded                  │
└─────────────────────────────────────────────────────────────┘
```

### Tiered Control Implementation
```
Enterprise Denylist (cannot override)
         │
         ▼
   Workspace R/W (no approval needed)
         │
         ▼
   Whitelisted Operations (case-by-case)
         │
         ▼
   Default Deny → User Approval
```

---

## 8. 核心参考文献

| 来源 | 类型 | 关键贡献 |
|------|------|----------|
| Cursor Blog | Blog | 沙盒实现、agent训练、40%中断减少 |
| NVIDIA Dev Blog | Blog | 安全控制框架、mandatory/recommended分层 |
| InfoWorld | Blog | FinOps、成本即可靠性 |
| arXiv 2602.16666 | Paper | 12个可靠性指标、4维度框架 |
| arXiv 2602.03442 | Paper | Agentic RAG、分层检索接口 |
| arXiv 2210.03629 | Paper | ReAct范式、推理+动作协同 |
