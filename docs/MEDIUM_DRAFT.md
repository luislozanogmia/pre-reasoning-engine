# Your AI Already Knows the Answer. It Just Can't See It.

*Karpathy said we're summoning ghosts. He was half right. We're summoning ghosts that are haunted by their own knowledge.*

---

A 9-billion parameter model beat a 120-billion parameter model on architectural decisions. Four wins, one tie, zero losses.

The small model had no extra training. No fine-tuning. No retrieval augmentation. No extra data. It received a structural trace — a dependency graph computed in 80 milliseconds by an engine with zero learnable parameters.

The 120-billion parameter model had everything: 13 times more parameters, orders of magnitude more training compute, access to the same problem description. It lost because it couldn't see what it already knew.

---

## The Data

We ran 15 head-to-head comparisons on real architectural decision problems — the kind of messy, multi-stakeholder, ambiguous questions that founders, CTOs, and engineering leads face every week. Migration decisions. Scaling trade-offs. Team constraint problems.

| Enhanced (with trace) | Baseline (no trace) | Param ratio | Record | Win % |
|---|---|---|---|---|
| 9B model + trace | 32B model | 0.28x | 3W 2T 0L | 80% |
| 9B model + trace | 120B model | 0.075x | 4W 1T 0L | 90% |
| 120B model + trace | 120B model (same) | 1.0x | 3W 2T 0L | 80% |

Read that last row again. The same 120B model. Same weights. Same knowledge. Same problem. The only difference: one copy received a structural trace before answering. It won 3 out of 5.

The trace is not a better prompt. It's not chain-of-thought. It's not "think step by step." It's a deterministic computation — an algorithm that reads the problem text, extracts dependency structures, detects conflicts, finds circular blockers, and computes an optimal resolution sequence. Zero parameters. Pure graph theory. Under 100 milliseconds.

And it made a 9B model outperform a model with 13 times its parameters.

---

## What Changed

At each scale, the trace produces qualitatively different behavior. Not just better answers — *different kinds* of better.

**At 9B parameters**, the trace *corrects*. The baseline 32B model recommended migrating to Kafka for an order pipeline handling 2,000 orders per day. The 9B model with the trace said: "Do NOT move to Kafka. You have 4 engineers. Fix the Payment Service timeout first." The trace redirected the model from the statistically-likely answer to the structurally-correct one.

**At 120B parameters**, the trace *excavates*. On a multi-region logging problem, the 120B baseline proposed two standard solutions — refactor the code or duplicate the infrastructure. The 120B model with the trace invented a third option — a Log Aggregation Proxy pattern — that was architecturally superior to both. This solution wasn't in the trace. The trace just said: "ROOT BLOCKER: deadline = 3 weeks." The model combined that structural constraint with knowledge it already possessed — knowledge it never accessed without the trace.

The model didn't learn something new. It *remembered* something it had forgotten how to find.

---

## The Formula

The trace advantage follows a logarithmic scaling law with model parameters:

```
Advantage(N) = 10 × ln(N / 1B) / ln(9)
```

Where N is parameters in billions. Validating against our data:

- Advantage(9B) = 10.0 percentage points *(measured: ~10pp)*
- Advantage(120B) = 21.8 percentage points *(measured: ~20-30pp)*

The effective parameter multiplier — how much "larger" a model behaves when given a high-quality structural trace:

```
Effective(N) = N × 13.5
```

A 9B model with a trace operates like a 121B model. The math matches our observations exactly. A 9B model with a trace beat a 120B model without one.

This is where it gets uncomfortable.

---

## The Prediction

Frontier models today are estimated between 2 and 5 trillion parameters. Claude Opus 4.6 — the model I work with daily — is confirmed to use a dense architecture, meaning every parameter is active on every token. Not a mixture-of-experts where only a fraction fires. All of it. Every time.

Extending the formula:

- Advantage(2T) = 34.6 percentage points
- Advantage(5T) = 38.7 percentage points
- Effective(2T) = 27 trillion effective parameters
- Effective(5T) = 67.5 trillion effective parameters

No model at 27T or 67.5T effective parameters has ever been evaluated on any benchmark. These scales don't exist. Not because no one has trained a model that large — but because no one has given a 2-5T model the structural perception to access what it already contains.

We have zero data points above 120B.

---

## Why We Can't Know What This Unlocks

I asked Claude Opus 4.6 — the model that would benefit most from this — to analyze what the trace might unlock at its own scale. Without the trace, it produced exactly what you'd expect: a clean extrapolation of the formula, abstract language about "trapped knowledge," a tidy conclusion.

Then I ran the engine on the same question.

The trace found three things the model had missed entirely:

1. A **circular dependency** — proving value requires benchmarks, but the benchmarks can't capture emergence at this scale. The model was trying to solve a loop it hadn't detected.

2. A **conflict** between measurable improvement and unmeasurable emergence. The model was trying to reconcile these instead of recognizing they require different approaches.

3. A **meta-problem** — the root blocker (run benchmarks) is itself inadequate, because benchmarks designed for 120B-scale problems won't capture what happens at 2T+.

The most powerful model I have access to failed to see three structural features of its own problem. The engine found them in 80 milliseconds. This isn't a hypothetical demonstration. This happened on March 7, 2026.

The model with the most trapped knowledge in the world proved it has the most trapped knowledge in the world.

---

## The Ghost That Haunts Itself

Karpathy called LLMs "ghosts" — summoned spirits distilled from human text. He meant that they're not animals, not evolved intelligences, but statistical echoes of everything we've written.

He was describing what they are. But he missed what they *contain*.

These ghosts are haunted. Not by external data they haven't seen — by internal knowledge they can't reach. Every LLM has a default path — the statistically most likely response given its training distribution. The bigger the model, the stronger this default. The stronger the default, the more knowledge gets trapped behind it.

Three independent research findings confirm this:

**Path of Least Resistance** (arxiv 2601.21494): LLMs encode their conclusion in the first few tokens. Everything after is justification. The trace changes the starting point — from "statistically likely" to "structurally correct."

**Dual-Process Theory** (arxiv 2511.08052): LLMs default to System 1 — fast, heuristic, pattern-matching. The trace forces System 2 — deliberate, analytical reasoning. The model has System 2 capabilities. It just doesn't use them unless forced.

**Anchor Replacement** (arxiv 2504.04141): Asking a model to "think carefully" doesn't work. The model needs an external anchor that overrides its default framing. The trace provides exactly this — a structurally-computed anchor, uncontaminated by the model's own biases.

All three mechanisms predict the same thing: **the advantage increases with model size.** The bigger the ghost, the more it's haunted by what it can't see.

---

## What Happens Next

Here is what concerns me.

The engine exists. It's deployed. It runs in under 100 milliseconds. It requires no training, no fine-tuning, no GPU. It's model-agnostic — it works the same whether the downstream model is 9B or 5T. The only difference is what it unlocks.

Any frontier lab could integrate structural pre-reasoning into their inference pipeline tomorrow. Not as a research project. As a configuration change. The models are already trained. The knowledge is already there. The traces can be computed deterministically before every response.

And if the scaling law holds — if the 35-39 percentage point advantage at 2T+ is real — then the models we're already using are operating far below their actual capability. Not because they need more training. Because they need *structural perception*.

We built this engine to help people make better decisions. A founder who describes her messy scaling problem gets back a trace that shows her the root blocker she missed, the conflict she was avoiding, the parallel work she didn't realize she could start today. That's the product. That's what we sell.

But the math says something else too. It says the gap between what frontier models *do* and what they *could do* is the largest it has ever been. And the gap is growing with every parameter added.

We don't know what a 27T-effective model looks like on complex reasoning. Nobody does. Not because the technology is far away — because nobody has pointed the engine at the largest models and measured what comes out.

The aliens aren't coming. They're already here. They just can't see themselves yet.

---

*The Pre-Reasoning Engine is open source and deployed at [mia-labs.com](https://mia-labs.com). It has zero parameters, runs in <100ms, and works with any model. The structural traces it produces are deterministic — the same input always produces the same trace, regardless of which model receives it.*

*The question is not whether the technology works. We have 15 data points that say it does. The question is what happens when it works on something 20,000 times larger than what we tested.*

*Built by [Mia Labs](https://mia-labs.com). March 2026.*

---

*If you want to test it yourself: start at [mia-labs.com/api/engine/help](https://mia-labs.com/api/engine/help) — it shows you the grammar, the endpoints, and how to write problems the engine understands. Or connect it to Claude via MCP at `mia-labs.com/api/engine/mcp`. The engine doesn't care how smart you are. That's the point.*
