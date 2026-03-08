# Pre-Reasoning Engine Skill

Analyze any problem with the Mia Labs Pre-Reasoning Engine before responding.
Surfaces Humanly Grounded traces: root blockers, unlock sequences, conflicts, and parallel work.
Use before answering complex, ambiguous, or multi-stakeholder questions.

## Setup

Use the WebFetch tool to call the hosted API. No dependencies, no install.

```bash
curl -X POST https://www.mia-labs.com/api/engine/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "YOUR PROBLEM TEXT"}'
```

The API returns JSON with `trace`, `root_blockers`, `grounding_level`, and `blocks`.

## When to Use

**USE** when: planning, strategic decisions, complex multi-part problems, architectural choices, debugging with multiple hypotheses, trade-off analysis, ambiguous requirements.

**SKIP** when: follow-up questions, confirmations, quick file ops, simple factual answers, single-step tasks.

## How to Use the Trace

1. Describe the problem in natural language with signal words ("depends on", "blocks", "the CTO wants", "team of 4")
2. POST it to `https://www.mia-labs.com/api/engine/analyze` with `{"text": "..."}`
3. Read the trace and structure your response:
   - Address ROOT BLOCKERS first
   - Follow the UNLOCK SEQUENCE
   - Note PARALLEL WORK that can proceed independently
   - Surface CONFLICTS for resolution
4. The trace surfaces things you'd miss — dependencies, circular blockers, constraint interactions

## CLAUDE.md Integration

Add this to your project's CLAUDE.md:

```
PRE-REASONING ENGINE:
On each turn, DECIDE whether to run the pre-reasoning engine before responding.
USE IT when: planning, strategic decisions, complex multi-part problems.
SKIP when: follow-up questions, confirmations, quick file ops.
HOW: POST to https://www.mia-labs.com/api/engine/analyze with {"text": "problem description"}
```

ARGUMENTS: analyze the problem by calling the REST API before responding
