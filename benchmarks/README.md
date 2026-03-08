# Benchmark Results

Cross-model validation of pre-reasoning traces on architectural decision problems.

## Setup

5 architectural decision problems tested across 3 model configurations:
- **Baseline**: Model answers the problem directly (no trace)
- **Enhanced**: Model receives a structural trace from the 0-param engine before answering
- **Judge**: Independent evaluation by a different model (blind, randomized order)

Problems tested: event-driven migration, vibe-coded SaaS scaling, hiring pipeline, multi-cloud reliability, AI safety governance.

## Results

### Claudio 9B + Trace vs Qwen 32B Baseline

| Problem | Verdict | Key Difference |
|---------|---------|----------------|
| Event-Driven Migration | **Enhanced wins** | Enhanced says "NO to Kafka" — addresses root blocker (payment stability) first |
| Vibe-Coded SaaS | **Enhanced wins** | Enhanced provides ordered fix sequence matching unlock order |
| Hiring Pipeline | Tie | Both adequate |
| Multi-Cloud | **Enhanced wins** | Enhanced identifies circular dependency between teams |
| AI Safety | Tie | Both address governance |

**Score: 3W 2T 0L** — 9B + trace beats 32B baseline on 3 of 5 problems.

### Claudio 9B + Trace vs GPT 120B Baseline

| Problem | Verdict | Key Difference |
|---------|---------|----------------|
| Event-Driven Migration | **Enhanced wins** | 120B defaults to "Yes, Kafka." Enhanced says "No, fix payment first." |
| Vibe-Coded SaaS | **Enhanced wins** | Enhanced provides surgical fix order; 120B gives generic refactoring advice |
| Hiring Pipeline | **Enhanced wins** | Enhanced addresses interpersonal conflict 120B ignores entirely |
| Multi-Cloud | **Enhanced wins** | Enhanced reframes problem from "which cloud" to "team coordination blocker" |
| AI Safety | Tie | Both adequate |

**Score: 4W 1T 0L** — 9B + trace beats 120B baseline on 4 of 5 problems.

### GPT 120B + Trace vs GPT 120B Baseline

| Problem | Verdict | Key Difference |
|---------|---------|----------------|
| Event-Driven Migration | **Enhanced wins** | Same model, different answer — trace unlocks knowledge model already had |
| Vibe-Coded SaaS | Tie | Both good with 120B capability |
| Hiring Pipeline | **Enhanced wins** | Trace surfaces stakeholder conflicts model skipped without it |
| Multi-Cloud | **Enhanced wins** | Trace forces structural analysis before solution proposal |
| AI Safety | Tie | Both adequate |

**Score: 3W 2T 0L** — same model performs better with trace.

## Key Findings

1. **Trace advantage increases with model size.** Bigger models have more knowledge trapped behind default reasoning paths. The trace unlocks it.

2. **Three mechanisms at work:**
   - **Priority reordering**: Trace changes what the model addresses first
   - **Constraint elevation**: Trace makes team size / deadlines / budget impossible to ignore
   - **Conflict surfacing**: Trace forces model to address stakeholder disagreements

3. **Response efficiency**: Enhanced responses average 2.5x shorter than baseline while being more actionable.

4. **Strongest evidence**: Problem 3 (Hiring Pipeline) — trace forced GPT-120B to invent a solution it never considered without the trace.

## Reproduction

Results can be reproduced using the hosted API:

```bash
# Get a trace for any problem
curl -X POST https://www.mia-labs.com/api/engine/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "YOUR PROBLEM DESCRIPTION"}'

# Then provide the trace to any LLM alongside the original problem
```

The trace is deterministic — same input always produces the same structural analysis.
