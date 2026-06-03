# Research: Decisions & Architecture

## Harness Engineering Framework

---

## Key Architectural Decisions

### Decision 1: Generator-Evaluator Separation
**Context**: Agents evaluate own work too generously
**Decision**: Separate the agent doing work from agent judging it
**Evidence**: GAN-inspired architecture showed dramatic improvement
**Result**: Evaluator can be tuned to be skeptical; generator has concrete feedback

### Decision 2: Three-Agent Architecture
**Context**: Earlier two-agent (initializer + coding) approach hit ceilings
**Decision**: Add planner agent to automate spec creation
**Key insight**: Planner stays at product-level, doesn't specify technical details upfront
**Result**: More ambitious scope without spec errors cascading to implementation

### Decision 3: Context Reset Pattern
**Context**: Sonnet 4.5 exhibited "context anxiety" - wrapped up prematurely near context limits
**Decision**: Explicit context resets with structured handoff artifacts
**Evolution**: Opus 4.5 largely eliminated context anxiety, enabling continuous sessions
**Lesson**: Model capabilities change harness requirements

### Decision 4: Sprint Contracts
**Context**: Product spec intentionally high-level; gap to testable implementation
**Decision**: Generator and evaluator negotiate "done" before each sprint
**Mechanism**: Generator proposes what to build + how to verify; evaluator reviews
**Result**: Bridges user stories to implementation without over-specifying

### Decision 5: Feature List with Pass/Fail
**Context**: Agents one-shot apps or declare premature completion
**Decision**: Comprehensive feature list with explicit pass/fail status
**Implementation**: JSON format (more stable than Markdown for model editing)
**Rule**: "Unacceptable to remove or edit tests"

---

## Critical Insights

1. **Quality left principle**: Catching issues earlier (in commit/pre-commit) is cheaper than later (in pipeline/production)

2. **Attention budget is finite**: Every token added depletes capacity; curate high-signal tokens

3. **Ambient affordances enable harnessability**: Legacy codebases need environment improvements first

4. **Harness templates reduce variety**: Ashby's Law - committing to topology narrows the space, making comprehensive harness achievable

---

## Unresolved Architectural Questions

- Optimal number of evaluator grading criteria before diminishing returns
- When to abandon harness approach vs improving codebase structure
- How to handle agent behavior with zero ambient affordances