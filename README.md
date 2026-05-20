# Harness Engineering

> **Distilled from [nuwa-skill](https://github.com/alchaincyf/nuwa-skill)**

This is a skill framework for building reliable AI agents, sourced from research across 100+ projects at OpenAI, Anthropic, Microsoft, Meta, and Google.

[中文版](README_zh.md)

## Core Dimensions

| Dimension | Description |
|-----------|-------------|
| **Agent Loop** | Plan → Act → Observe → Adjust → Repeat |
| **Context Engineering** | Treat context as a finite resource with diminishing returns |
| **Verification** | Generators and evaluators must be separated |
| **Memory** | Map over manual — use structured persistence |
| **Multi-Agent** | Orchestration topology matters more than model choice |
| **Production Patterns** | Harness is the "OS" between model and reality |

## Quick Start

```bash
python fetch_sources.py
```

This fetches source materials from Anthropic, OpenAI, and other references into `references/`.

## Key Mental Models

- **Harness = OS for AI**: Handles prompt construction, tool dispatch, context management, termination judgment
- **Context Rot**: Attention degrades as context window fills — place static content early, variable content late
- **GAN-Style Evaluation**: Use independent evaluators with quantifiable grading criteria, not self-evaluation

## Resources

- `SKILL.md` — Full skill documentation
- `fetch_sources.py` — Bulk source material fetcher (sources from `references/`)
- `references/` — Downloaded research materials