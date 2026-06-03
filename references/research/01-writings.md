# Research: Writings & Systematic Analysis

## Harness Engineering Framework

Sources analyzed from the critical references directory.

---

## Core Publications

### 1. Martin Fowler - "Harness engineering for coding agent users"
**Published**: April 2026
**Key论点**:
- Agent = Model + Harness (harness is everything outside the model itself)
- Feedforward and feedback controls must work together
- Regulation categories: maintainability, architecture fitness, behavior
- Steering loop: human iterates on harness based on agent behavior
- Harness templates for common service topologies

**反复出现的核心论点** (≥3次出现 = 真信念):
1. "Increase probability of good outcomes" - appears in intro and conclusion
2. "Self-correction before reaching human eyes" - repeats across sections
3. "Context engineering is a specific form of harness engineering" - appears in sidebar and main text
4. "Quality left" principle - catching issues early is cheaper

**自创术语**:
- Ambient affordances (with Ned Letcher)
- Harnessability
- Feedforward/sensor terminology from cybernetic tradition

### 2. Anthropic - "Effective harnesses for long-running agents"
**Published**: November 2025
**Key论点**:
- Two-part solution: initializer agent + coding agent
- Feature list with pass/fail status for each feature
- Progress file (claude-progress.txt) for cross-session state
- Context resets solve "context anxiety" problem
- Clean state at end of session = code ready to merge

**关键洞察**:
- Agents tend to try to do too much at once (one-shot failure mode)
- Later agents prematurely declare job done
- Git history + progress file = fast context recovery for new session

### 3. Anthropic - "Harness design for long-running application development"
**Published**: March 2026
**Key论点**:
- Generator-evaluator pattern (GAN-inspired)
- Three-agent architecture: planner, generator, evaluator
- Context resets largely unnecessary with Opus 4.5 (context anxiety removed)
- Grading criteria make subjective quality gradable
- Sprint contracts negotiated between generator and evaluator

**自创方法**:
- Four grading criteria: design quality, originality, craft, functionality
- Strategic decision after each evaluation: refine vs pivot
- "Sprint contract" for bridging spec to implementation

### 4. Anthropic - "Effective context engineering for AI agents"
**Published**: September 2025
**Key论点**:
- Context engineering vs prompt engineering distinction
- LLMs have "attention budget" - finite resource with diminishing marginal returns
- Position in sequence affects model focus (attention is all you need)
- Progressive disclosure over pre-loading all context
- Just-in-time retrieval vs pre-inference retrieval

### 5. Anthropic Research - "Trustworthy agents in practice"
**Published**: April 2026
**Key论点**:
- Four components: model, harness, tools, environment
- Human control tension: autonomy vs oversight
- Plan Mode for strategy-level oversight vs step-by-step
- Prompt injection defense at every layer

### 6. OpenAI - "Building effective agents"
**Published**: December 2024
**Key论点**:
- Simple composable patterns beat complex frameworks
- Workflows: predefined code paths
- Agents: LLMs dynamically direct own processes
- Start with simplest solution, increase complexity only when needed

---

## 推荐书单/来源

从这些文章推导的智识谱系:
- Cybernetics (Norbert Wiener) - feedforward/feedback terminology origin
- Fitness Functions (Thoughtworks) - architecture fitness concept
- GANs (Goodfellow et al) - generator-evaluator pattern inspiration
- Ashby's Law of Requisite Variety - harness templates argument

---

## 矛盾点

1. **Context resets**: Earlier Anthropic work emphasizes context resets as essential for Sonnet 4.5. Later work (Mar 2026) says Opus 4.5 largely removed context anxiety, making resets unnecessary. This is a genuine evolution in thinking as models improved.

2. **Harness complexity**: Martin Fowler describes layered harnesses ("wrapping harnesses on harnesses") but also acknowledges the metaphor stretches. There's tension between "simple harness" and "comprehensive control layer".