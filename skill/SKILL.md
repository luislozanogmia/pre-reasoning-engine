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

## Why It Works (Mechanism)

**The rewind problem:** LLMs commit to a conclusion in their first tokens. Everything after is justification, not reasoning. Once committed, the model cannot rewind. The trace runs BEFORE the model's first token — it changes the starting position, not the reasoning quality. The model doesn't think better; it starts somewhere else.

**The re-prompt loop:** When using the trace manually:
1. The model reasons just enough to understand the shape of the problem (not the answer)
2. It writes that shape as structural blocks
3. The engine processes them deterministically in <100ms
4. The trace re-prompts the model before it commits — different starting position, different path

**Breaking prompt dependency:** Without the engine, AI output quality is capped by human prompt quality. The engine replaces human perception as the source of the model's starting conditions. The model is prompted by structure, not by human framing — uncontaminated by human bias or the model's own defaults.

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
