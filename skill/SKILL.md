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

## Quick Start — Start with Help

```bash
# START HERE: see the full API guide, all endpoints, grammar tips
python ~/.claude/skills/pre-reasoning/engine.py

# Or equivalently:
python ~/.claude/skills/pre-reasoning/engine.py --help
```

This fetches the live API guide from `GET /help` — shows all endpoints, quickstart flow, grounding levels, writing tips, and examples.

## All Commands

```bash
# Show full API guide (DEFAULT — runs with no args)
python engine.py --help

# Grammar guide — signal words and patterns for best traces
python engine.py --form

# Analyze a problem (core use case)
python engine.py --analyze "We need to migrate our monolith but the team is split..."

# Analyze from a file
python engine.py --analyze-file /path/to/problem.txt

# URL-based submit (no POST needed — works from any browser/model)
python engine.py --submit "your problem text"

# Recover results from a previous submit
python engine.py --recover RECOVER_ID

# Health check
python engine.py --health

# Engine metadata
python engine.py --info
```

## API Endpoints

| Endpoint | Method | What |
|----------|--------|------|
| `/help` | GET | Full usage guide — START HERE |
| `/form` | GET | Grammar guide — signal words, patterns, examples |
| `/analyze` | POST | Send `{"text": "..."}`, get structural trace |
| `/submit?text=...` | GET | URL-based submit (returns recover_id) |
| `/recover/{id}` | GET | Retrieve results (valid 1 hour) |
| `/health` | GET | Health check |
| `/info` | GET | Engine metadata |

Base URL: `https://www.mia-labs.com/api/engine`

## How It Works

1. You give it unstructured problem text (in English)
2. Engine extracts structural blocks (regex + LLM enhancement)
3. Builds dependency graph, runs Tarjan SCC for cycles
4. Computes: root blockers, unlock sequence, parallel work, conflicts
5. Returns a trace that ANY model uses to reason better

The trace doesn't add knowledge -- it prevents drift. It keeps the model on the structural path.

## Auto-Enhancement Loop

`/api/engine/analyze` has a server-side enhancement loop that runs automatically:

- **Shallow input** (`grounding_level: "grounding"` on first pass) -- server calls `llama-3.1-8b-instant` via Groq to reformulate the text with signal words, then re-submits to the engine (max 2 iterations)
- **Already-structured input** (first pass above `"grounding"`) -- loop never fires, trace returned as-is, zero overhead
- Applies to all callers: API, MCP, widget, playground -- no changes needed on the caller side
- The form grammar is baked into the enhancement prompt internally, so you don't need to study signal words to get richer traces from short inputs
- To opt out: pass header `X-Skip-Prereasonig: true`

## Using the Trace

After getting a trace, structure your response around it:

1. Address ROOT BLOCKERS first (these gate everything)
2. Follow UNLOCK SEQUENCE (optimal resolution order)
3. Acknowledge PARALLEL WORK (what can proceed now)
4. Surface CONFLICTS (competing positions that need resolution)

## Grounding Levels

| Level | Meaning |
|-------|---------|
| grounding | Trace orders what's visible. Simple deps, 1-2 blocks. |
| enhancing | Trace adds meaningful structure. Chains, constraints, or conflicts. |
| unlocking | Trace reveals hidden deps the model would miss. Root blockers, cycles, deep chains. |
| humanly_grounded | Full structural picture. Like having a domain expert in the room. |

## API Details

- Rate limit: 30 req/min, 200 req/day per IP
- Input limit: 10,000 characters
- No user text stored — metadata-only analytics
- Response: JSON with `trace`, `blocks`, `root_blockers`, `grounding_level`, `has_cycles`, `l1_enhanced`

## Evidence

| Test | Result |
|---|---|
| Qwen 32B: 178 problems, 6h | 49.2% -> 81.9% (+32.7pp, 87% win rate) |
| GPT-120B: 26 problems | 65.3% -> 92.3% (+27pp, 92% win rate) |
| 9B + trace vs 120B baseline | 4W 1T 0L |
| ARC-AGI 2 (Opus) | 0/14 -> 5/14 on hardest tasks |
