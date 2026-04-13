---
name: pre-reasoning
description: Analyze any problem with the Mia Labs Pre-Reasoning Engine before responding. Surfaces root blockers, unlock sequences, conflicts, and parallel work. Use before answering complex, ambiguous, or multi-stakeholder questions.
allowed-tools: Bash(python:*), Bash(python3:*), Read
---

# Pre-Reasoning Engine Skill

## When to Use
- Complex decisions with hidden trade-offs
- Multi-stakeholder problems (competing priorities)
- Architecture/design decisions
- Any problem where the LLM might take the "path of least resistance"
- Planning, strategy, debugging with multiple hypotheses
- NOT needed for: simple factual questions, confirmations, quick file ops

## Workflow

1. **Submit** — run `--analyze` (or `mcp__claude_ai_Mia_Labs__analyze_problem`) with the problem text. Conversational or short inputs are automatically enhanced server-side (see Auto-Enhancement Loop below).
2. **Or send a manually enhanced version yourself** — use the grammar below to rewrite the problem before submitting. This skips the enhancement loop entirely and produces the richest possible trace on the first pass.
3. **Respond** — address ROOT BLOCKERS first, follow the UNLOCK SEQUENCE, surface CONFLICTS.

## The Form (Signal Words Grammar)

Write your problem as natural text **in English**. The engine detects structure from these patterns. The more you include, the richer the trace.

**Dependencies** — what depends on what?
Signal words: `depends on`, `requires`, `needs`, `calls`, `relies on`, `talks to`, `sends to`, `connects to`, `reads from`, `writes to`, `is waiting on`, `cannot proceed until`
> "The frontend depends on the API gateway." / "Payment Service calls the Auth Service."

**Blockers** — what fails or slows down the system?
Signal words: `is slow`, `fails`, `blocks`, `breaks`, `times out`, `crashes`, `goes down`, `is unavailable`, `is missing`, `is invalid`
> "When the database is slow, everything times out." / "When Auth Service fails, no user can log in."

**Competing Options** — what choices are on the table?
Format: `Option A: ... Option B: ... Option C: ...`
> "Option A: rewrite in microservices. Option B: refactor the monolith. Option C: strangler fig pattern."

**Stakeholder Conflicts** — who wants what?
Signal words: `wants`, `says`, `warns`, `insists`, `believes`, `thinks`, `argues`
Detected roles: CTO, CEO, VP, architect, team lead, senior dev, senior engineer, founder, product manager, etc.
> "The CTO wants microservices but the senior dev warns about complexity."

**Constraints** — hard limits on the solution space.
Patterns: `team of N`, `deadline of N weeks/months`, `budget $X`, `N customers/users`, `can't afford X`
> "We have a team of 3 and a deadline of 4 weeks. 500 paying customers, can't afford downtime."

**Pain Points** — numbered list of issues.
Format: `1) ... 2) ... 3) ...`
> "1) Deployments take 2 hours. 2) No monitoring. 3) Database locks under load."

**Full example input combining all patterns:**
```
We run a SaaS with 200 paying customers. Our monolith is getting slow.
The API gateway depends on the auth service which depends on PostgreSQL.
When PostgreSQL is slow, the whole system times out.
Option A: rewrite as microservices. Option B: optimize the monolith. Option C: strangler fig migration.
The CTO wants microservices but the senior dev warns about complexity.
We have a team of 4 and a deadline of 6 weeks.
1) No CI/CD pipeline. 2) No monitoring. 3) Manual deployments.
```

## Quick Start

```bash
python ~/.claude/skills/pre-reasoning/engine.py --analyze "Your problem text here"
```

## Commands

```bash
# Analyze a problem (core use case)
python engine.py --analyze "We need to migrate our monolith but the team is split..."

# Analyze from a file
python engine.py --analyze-file /path/to/problem.txt

# Health check (is the API reachable?)
python engine.py --health

# Get engine info (version, capabilities)
python engine.py --info

# Get writing tips (how to write better inputs)
python engine.py --form

# Full help with examples
python engine.py --help
```

## How It Works

1. You give it unstructured problem text
2. Engine extracts structural blocks (regex + LLM enhancement)
3. Builds dependency graph, runs Tarjan SCC for cycles
4. Computes: root blockers, unlock sequence, parallel work, conflicts
5. Returns a trace that ANY model uses to reason better

The trace doesn't add knowledge — it prevents drift. It keeps the model on the structural path.

## Auto-Enhancement Loop (deployed 2026-04-12)

`/api/engine/analyze` has an automatic enhancement loop server-side:

- **Shallow input** (`grounding_level: "grounding"` on first pass) -- server calls `llama-3.1-8b-instant` via Groq to reformulate the text with signal words, re-submits to the engine (max 2 iterations)
- **Already-structured input** (first pass above `"grounding"`) -- loop never fires, trace returned as-is, zero overhead
- Applies to all callers: API, MCP, widget, playground -- no changes needed on the caller side
- `get_form` grammar is baked into the enhancement prompt internally
- To opt out: pass header `X-Skip-Prereasonig: true`

## Using the Trace

After getting a trace, prepend it to your prompt or use it to structure your response:

1. Address ROOT BLOCKERS first (these gate everything)
2. Follow UNLOCK SEQUENCE (optimal resolution order)
3. Acknowledge PARALLEL WORK (what can proceed now)
4. Surface CONFLICTS (competing positions that need resolution)

## Testing the Engine

To verify the API is live, hit it directly with curl:

```bash
# Health check
curl -s https://www.mia-labs.com/api/engine/health

# Test analyze with a real problem
curl -s -X POST https://www.mia-labs.com/api/engine/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "We need to migrate our database but the team is split on PostgreSQL vs MongoDB. The CTO wants MongoDB for flexibility but the senior dev warns about transaction support. Deadline is 3 weeks."}'
```

Expected: JSON with `trace`, `blocks`, `root_blockers`, `grounding_level`, `has_cycles`, `l1_enhanced`. The `grounding_level` is one of: grounding, enhancing, unlocking, humanly_grounded — indicating how much structural depth the trace provides. If `l1_enhanced: true`, the LLM extraction layer (Maverick) is active. If `false`, it fell back to regex-only (still works, fewer blocks).

Do NOT rely on `ps aux` or process inspection to check if the engine is running — the host may manage processes differently. Always test the API directly.

## API Details

- Endpoint: `https://www.mia-labs.com/api/engine/analyze`
- Method: POST with `{"text": "..."}`
- Rate limit: 30 req/min, 200 req/day per IP
- Input limit: 10,000 characters
- No user text stored — metadata-only analytics

## Evidence

| Test | Result |
|---|---|
| Qwen 32B: 178 problems, 6h | 49.2% -> 81.9% (+32.7pp, 87% win rate) |
| GPT-120B: 26 problems | 65.3% -> 92.3% (+27pp, 92% win rate) |
| 9B + trace vs 120B baseline | 4W 1T 0L |
| ARC-AGI 2 (Opus) | 0/14 -> 5/14 on hardest tasks |
