# Research: Conversations & Interviews

## Harness Engineering Framework

This is a framework skill (not a personal distillation), so this file captures key dialogues and discussions from the source materials.

---

## Key Dialogues/Exchanges

### Martin Fowler's Exchange with Ned Letcher
**Topic**: Ambient Affordances
- Fowler uses Ned's term to describe properties that make codebases harnessable
- "Structural properties of the environment itself that make it legible, navigable, and tractable to agents"

### Anthropic Labs Team Exchanges
**Topic**: Generator-Evaluator Development
- Prithvi Rajasekaran describes iterative process of developing grading criteria
- Criteria wording shaped output character in unexpected ways ("museum quality" push)
- Generator would make strategic decisions: refine current direction or pivot

### Industry Convergence Moment
**Topic**: Multi-Session Coherence
- Community converged on similar insights as Anthropic's initializer/coding pattern
- "Ralph Wiggum" method using hooks/scripts for continuous iteration
- Shows independent discovery of similar patterns

---

## 即兴类比

1. **Context as Attention Budget**: Like human working memory, LLMs have limited capacity that depletes with each new token

2. **Harness as Cybernetic Governor**: Like a thermostat regulating temperature, a harness regulates code quality toward desired state

3. **Agents as Engineers in Shifts**: Each new session starts with no memory, like engineers working shifts without handoff notes

4. **GAN-Inspired Design**: Generator creates, evaluator judges, iterative refinement drives quality up

---

## 立场变化

**Evolution in Anthropic's thinking on context resets**:
- Nov 2025: Context resets essential due to context anxiety in Sonnet 4.5
- Mar 2026: Opus 4.5 largely removed context anxiety, enabling continuous session working

This represents genuine learning as frontier models improved.

---

## 拒绝回答的问题

Sources don't directly address:
- How to handle agent behavior when codebase has zero ambient affordances
- Optimal number of criteria in an evaluator before diminishing returns
- When to abandon a harness approach vs improving the codebase itself