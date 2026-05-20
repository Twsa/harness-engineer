#!/usr/bin/env python3
"""Bulk fetch harness engineering source materials."""
import asyncio
import aiohttp
import os
import re
import time
from pathlib import Path
from urllib.parse import urlparse

BASE = Path("/home/vagrant/code/AI/harness-engineer/references")
BASE.mkdir(parents=True, exist_ok=True)

# Slugify URL to safe filename
def slug(url):
    p = urlparse(url)
    name = p.netloc + p.path
    name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    name = re.sub(r'_+', '_', name).strip('_')
    return name[:120]

# URL classifications
CRITICAL = [
    ("anthropic", "https://www.anthropic.com/research/building-effective-agents"),
    ("anthropic", "https://www.anthropic.com/engineering/harness-design-long-running-apps"),
    ("anthropic", "https://www.anthropic.com/engineering/writing-effective-tools-for-agents"),
    ("anthropic", "https://www.anthropic.com/engineering/beyond-permission-prompts"),
    ("anthropic", "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents"),
    ("anthropic", "https://www.anthropic.com/research/what-is-an-agent"),
    ("anthropic", "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents"),
    ("anthropic", "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"),
    ("anthropic", "https://www.anthropic.com/research/trustworthy-agents"),
    ("openai", "https://openai.com/index/harness-engineering"),
    ("openai", "https://openai.com/index/unrolling-the-codex-agent-loop"),
    ("openai", "https://developers.openai.com/blog/run-long-horizon-tasks-with-codex"),
    ("openai", "https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents"),
    ("openai", "https://openai.com/index/unlocking-the-codex-harness"),
    ("openai", "https://developers.openai.com/blog/skills-shell-tips"),
    ("openai", "https://openai.com/index/the-next-evolution-of-the-agents-sdk"),
    ("openai", "https://developers.openai.com/blog/eval-skills"),
    ("openai", "https://developers.openai.com/cookbook/examples/partners/agentic_governance_guide/agentic_governance_cookbook"),
    ("openai", "https://developers.openai.com/api/docs/guides/agents/sandboxes"),
    ("openai", "https://platform.openai.com/docs/guides/function-calling"),
    ("martinfowler", "https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html"),
    ("martinfowler", "https://martinfowler.com/articles/harness-engineering.html"),
]

HIGH_ARXIV = [
    ("arxiv", "https://arxiv.org/abs/2603.05344"),   # Terminal harness paper
    ("arxiv", "https://arxiv.org/abs/2603.25723"),   # Natural-Language Agent Harnesses
    ("arxiv", "https://arxiv.org/abs/2210.03629"),   # ReAct
    ("arxiv", "https://arxiv.org/abs/2603.01209"),   # Interpreter Persistence
    ("arxiv", "https://arxiv.org/abs/2601.13206"),   # Real-Time Deadlines
    ("arxiv", "https://arxiv.org/abs/2604.11378"),   # Scheduler-Theoretic Framework
    ("arxiv", "https://arxiv.org/abs/2604.14228"),   # Claude Code Design Space
    ("arxiv", "https://arxiv.org/abs/2310.04406"),   # LATS
    ("arxiv", "https://arxiv.org/abs/2602.01465"),   # Agyn multi-agent
    ("arxiv", "https://arxiv.org/abs/2503.09572"),   # Plan-and-Act
    ("arxiv", "https://arxiv.org/abs/2602.16873"),   # AdaptOrch
    ("arxiv", "https://arxiv.org/abs/2601.07577"),   # TDP
    ("arxiv", "https://arxiv.org/abs/2601.07190"),   # Active Context Compression
    ("arxiv", "https://arxiv.org/abs/2602.03442"),   # A-RAG
    ("arxiv", "https://arxiv.org/abs/2603.27355"),   # LLM Readiness Harness
    ("arxiv", "https://arxiv.org/abs/2602.16666"),   # Science of AI Agent Reliability
    ("arxiv", "https://arxiv.org/abs/2603.06847"),   # Characterizing Faults
    ("arxiv", "https://arxiv.org/abs/2602.22480"),   # VeRO
    ("arxiv", "https://arxiv.org/abs/2604.10866"),   # OccuBench
    ("arxiv", "https://arxiv.org/abs/2603.11088"),   # Attack and Defense Survey
]

HIGH_MSFT_META = [
    ("microsoft", "https://techcommunity.microsoft.com/blog/appsonazureblog/how-we-build-azure-sre-agent-with-agentic-workflows/4508753"),
    ("microsoft", "https://techcommunity.microsoft.com/blog/appsonazureblog/context-engineering-lessons-from-building-azure-sre-agent/4481200"),
    ("microsoft", "https://techcommunity.microsoft.com/blog/microsoft-security-blog/authorization-and-governance-for-ai-agents-runtime-authorization-beyond-identity/4509161"),
    ("microsoft", "https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0"),
    ("microsoft", "https://www.microsoft.com/en-us/research/blog/systematic-debugging-for-ai-agents-introducing-the-agentrx-framework"),
    ("meta", "https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation"),
    ("meta", "https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure/"),
]

MEDIUM_BLOG = [
    ("langchain", "https://blog.langchain.com/the-anatomy-of-an-agent-harness"),
    ("langchain", "https://blog.langchain.com/improving-deep-agents-with-harness-engineering"),
    ("langchain", "https://blog.langchain.com/how-middleware-lets-you-customize-your-agent-harness"),
    ("langchain", "https://blog.langchain.com/plan-and-execute-agents"),
    ("langchain", "https://blog.langchain.com/choosing-the-right-multi-agent-architecture"),
    ("langchain", "https://blog.langchain.com/autonomous-context-compression"),
    ("langchain", "https://blog.langchain.com/two-different-types-of-agent-authorization"),
    ("langchain", "https://blog.langchain.com/production-agents-self-heal/"),
    ("githubblog", "https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont"),
    ("githubblog", "https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-agentic-workflows/"),
    ("githubblog", "https://github.blog/security/community-powered-security-with-ai-an-open-source-framework-for-security-research/"),
    ("cursor", "https://cursor.com/blog/agent-sandboxing"),
    ("vercel", "https://vercel.com/blog/making-agent-friendly-pages-with-content-negotiation"),
    ("mcp", "https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations"),
    ("mcp", "https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap"),
    ("redhat", "https://developers.redhat.com/articles/2026/04/07/harness-engineering-structured-workflows-ai-assisted-development"),
    ("google", "https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications"),
    ("google", "https://developers.googleblog.com/en/supercharge-your-ai-agents-adk-integrations-ecosystem"),
    ("google", "https://developers.googleblog.com/en/developers-guide-to-ai-agent-protocols"),
    ("google", "https://cloud.google.com/blog/products/ai-machine-learning/a-devs-guide-to-production-ready-ai-agents"),
    ("google", "https://cloud.google.com/blog/products/ai-machine-learning/new-enhanced-tool-governance-in-vertex-ai-agent-builder"),
    ("claudecode", "https://okhlopkov.com/claude-code-compaction-explained"),
    ("nvidia", "https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/"),
    ("infoworld", "https://www.infoworld.com/article/4138748/finops-for-agents-loop-limits-tool-call-caps-and-the-new-unit-economics-of-agentic-saas.html"),
]

BATCHES = {
    "01_critical": CRITICAL,
    "02_arxiv": HIGH_ARXIV,
    "03_msft_meta": HIGH_MSFT_META,
    "04_blogs": MEDIUM_BLOG,
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; research-bott/1.0; +https://github.com/ai-boost/awesome-harness-engineering)"
}

async def fetch_one(session, sem, cat, url, outdir):
    path = outdir / f"{cat}_{slug(url)}.txt"
    if path.exists() and path.stat().st_size > 100:
        return f"SKIP {url}"
    async with sem:
        try:
            async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=30)) as r:
                if r.status == 403:
                    return f"BLOCKED {url}"
                text = await r.text()
                if len(text) > 500:
                    path.write_text(text)
                    return f"OK {len(text):6d} {url}"
                return f"TOO_SHORT({len(text)}) {url}"
        except Exception as e:
            return f"ERR {type(e).__name__}: {url}"

async def fetch_batch(name, items, outdir, concurrency=8):
    sem = asyncio.Semaphore(concurrency)
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, sem, cat, url, outdir) for cat, url in items]
        results = await asyncio.gather(*tasks)
    
    ok = sum(1 for r in results if r.startswith("OK"))
    skip = sum(1 for r in results if r.startswith("SKIP"))
    err = len(results) - ok - skip
    print(f"\n{name}: OK={ok} SKIP={skip} ERR={err}")
    for r in results:
        if not r.startswith("OK") and not r.startswith("SKIP"):
            print(f"  {r}")
    return results

async def main():
    for batch_name, items in BATCHES.items():
        outdir = BASE / batch_name
        print(f"\n{'='*60}")
        print(f"Fetching {batch_name}: {len(items)} URLs -> {outdir}")
        await fetch_batch(batch_name, items, outdir)

if __name__ == "__main__":
    asyncio.run(main())
