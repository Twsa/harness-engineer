# Research: External Views

## Harness Engineering Framework

---

## Key External Perspectives

### Martin Fowler's Perspective
- Frameworks harness engineering within software engineering discipline
- Draws from agile/continuous delivery traditions
- Emphasizes maintainability harness as entry point
- Acknowledges harness engineering relates to context engineering

### Anthropic Engineering Perspective
- Focus on practical agentic coding problems
- Long-running agent challenge as primary motivation
- GAN-inspired generator-evaluator as key innovation
- Grading criteria making subjective quality "gradable"

### OpenAI Perspective
- Emphasizes simple patterns over complex frameworks
- Workflow vs agent distinction
- Start simple, add complexity only when needed

---

## 主要批评

1. **AI-generated tests not reliable enough**: Martin Fowler notes "puts a lot of faith into AI-generated tests, that's not good enough yet"

2. **Behaviour harness unsolved**: The elephant in the room - functional correctness remains hardest problem

3. **Context stuffers miss the point**: Pre-loading all context wastes the attention budget on low-signal tokens

4. **Over-harnessed codebases**: "Wrapping harnesses on harnesses doesn't make sense"

---

## 与同行对比

| Aspect | Martin Fowler | Anthropic | OpenAI |
|--------|--------------|-----------|--------|
| Focus | Trust & quality | Long-running agents | Simple patterns |
| Main contribution | Mental model framework | Generator-evaluator | Workflow/agent taxonomy |
| View of complexity | Needs layered approach | Solvable with architecture | Start simple |
| View of context | Must curate, not stuff | Attention budget concept | - |

---

## 共识点

- Agents need structured guidance beyond the model
- Feedforward + feedback controls both necessary
- Human oversight remains important
- Simple patterns beat complex frameworks

---

## 分歧点

- How to handle long-running sessions (context resets vs continuous)
- Role of AI-generated tests
- How much to pre-load vs retrieve just-in-time