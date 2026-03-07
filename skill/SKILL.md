# Pre-Reasoning Engine Skill

Analyze any problem with the Mia Labs Pre-Reasoning Engine before responding.
Surfaces root blockers, unlock sequences, conflicts, and parallel work.
Use before answering complex, ambiguous, or multi-stakeholder questions.

## Setup

### Option A: MCP Tool (recommended)

If `mia-reasoning-engine` MCP is connected, use the `analyze_problem` tool directly.

### Option B: REST API

```bash
curl -X POST https://mia-labs.com/api/engine/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "YOUR PROBLEM TEXT"}'
```

### Option C: Local Engine

```python
from reasoning_engine import analyze
result = analyze("YOUR PROBLEM TEXT")
print(result["trace"])
```

## When to Use

**USE** when: planning, strategic decisions, complex multi-part problems, architectural choices, debugging with multiple hypotheses, trade-off analysis, ambiguous requirements.

**SKIP** when: follow-up questions, confirmations, quick file ops, simple factual answers, single-step tasks.

## How to Use the Trace

1. Decompose the problem into the engine's input format (natural language with signal words)
2. Feed to the engine, get the structural trace
3. Structure your response following the trace:
   - Address ROOT BLOCKERS first
   - Follow the UNLOCK SEQUENCE
   - Note PARALLEL WORK that can proceed independently
   - Surface CONFLICTS for resolution
4. The trace surfaces things you'd miss — dependencies, circular blockers, constraint interactions

## CLAUDE.md Integration

Add this to your project's CLAUDE.md:

```
REASONING ENGINE:
On each turn, DECIDE whether to run the reasoning engine before responding.
USE IT when: planning, strategic decisions, complex multi-part problems.
SKIP when: follow-up questions, confirmations, quick file ops.
```

ARGUMENTS: analyze the problem using the MCP tool or REST API before responding
