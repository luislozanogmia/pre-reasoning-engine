# Pre-Reasoning Engine

**Humanly Grounded decisions for any LLM.** You love working with your AI — give it humanly grounding to make decisions that just make sense.

0-param deterministic pre-reasoning that surfaces hidden structure — root blockers, dependency chains, conflicts, constraints — in ambiguous problems before any model speaks.

Built by [Mia Labs](https://mia-labs.com).

## What It Does

You describe an ambiguous problem in plain text. The pre-reasoning engine analyzes structural dependencies and returns:

- **ROOT BLOCKERS** — what must be resolved first (highest impact)
- **UNLOCK SEQUENCE** — optimal order to address issues
- **PARALLEL WORK** — what can proceed independently right now
- **CONFLICTS** — competing positions that need resolution
- **CIRCULAR DEPENDENCIES** — deadlocks detected via Tarjan's SCC

The engine uses **zero ML parameters**. It's pure algorithm — deterministic, fast (<100ms), and model-agnostic. When it finds enough structure, it reports the trace as **Humanly Grounded** — the full structural picture a human expert would surface.

## Why It Works

LLMs default to the statistically most likely answer. The trace changes the **starting point**, not the knowledge:

| Setup | Result |
|-------|--------|
| Claudio 9B + trace vs Qwen 32B baseline | **3W 2T 0L** |
| Claudio 9B + trace vs GPT 120B baseline | **4W 1T 0L** |
| GPT 120B + trace vs GPT 120B baseline | **3W 2T 0L** |

A well-traced 9B model beats an unguided 120B model. The trace advantage **increases** with model size — bigger models have more trapped knowledge behind their default reasoning path.

Three mechanisms (backed by literature):
1. **Path Redirection** — trace changes the LLM's starting prefix, redirecting from "statistically likely" to "structurally correct"
2. **System 2 Forcing** — trace acts as external deliberate scaffold, forcing analytical reasoning
3. **Anchor Replacement** — trace replaces the problem's implicit framing with a structural anchor

Full analysis: [WHY_TRACES_WORK.md](docs/WHY_TRACES_WORK.md)

## How to Use

### Option 1: REST API (hosted)

**Start here:** [mia-labs.com/api/engine/help](https://www.mia-labs.com/api/engine/help) — full usage guide and grammar reference.

```bash
# GET /help — start here, see all endpoints and examples
curl https://www.mia-labs.com/api/engine/help

# GET /form — learn the grammar (signal words that produce the best traces)
curl https://www.mia-labs.com/api/engine/form

# POST /analyze — send problem, get trace
curl -X POST https://www.mia-labs.com/api/engine/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Frontend depends on API gateway. API gateway depends on Auth. The CTO wants microservices but the senior dev warns about complexity. We have a team of 5 and a deadline of 8 weeks."}'

# GET /submit — URL-based (no POST needed, any browser/model can use)
curl "https://www.mia-labs.com/api/engine/submit?text=Frontend+depends+on+API.+CTO+wants+microservices+but+senior+dev+warns+about+complexity."

# GET /recover/{id} — retrieve results
curl "https://www.mia-labs.com/api/engine/recover/abc12345"
```

### Option 2: MCP (Claude Web, Claude Desktop, Cursor, Windsurf)

Connect any MCP-compatible client to the Streamable HTTP endpoint:

```
URL: https://www.mia-labs.com/api/engine/mcp
```

> **Note:** Claude.ai and some AI connectors cannot reach `www.mia-labs.com` through Cloudflare. If you get "Couldn't reach the MCP server", use the direct Replit URL instead: `https://mia-labs-landing.replit.app/api/engine/mcp`. ChatGPT, coding agents (Claude Code, Cursor, Windsurf), and direct API calls work fine with `mia-labs.com`.

**Claude Web** — go to Settings > Connectors > Add Custom Connector:
```
Name: Mia Labs Pre-Reasoning Engine
URL: https://www.mia-labs.com/api/engine/mcp
```

**Claude Desktop** — add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "mia-pre-reasoning": {
      "transport": "streamable-http",
      "url": "https://www.mia-labs.com/api/engine/mcp"
    }
  }
}
```

**Claude Code CLI**:
```bash
claude mcp add --transport http mia-pre-reasoning https://www.mia-labs.com/api/engine/mcp
```

> **Note:** The CLI sends explicit HTTP headers (`User-Agent`, `Accept`) for Cloudflare compatibility. If you fork the client, preserve these headers or requests may be blocked with a 403.

### Option 3: Claude Code Skill

Copy the [skill/](skill/) directory to `~/.claude/skills/pre-reasoning/` and add to your CLAUDE.md:

```
PRE-REASONING ENGINE:
On each turn, DECIDE whether to run the pre-reasoning engine before responding.
USE IT when: planning, strategic decisions, complex multi-part problems.
SKIP when: follow-up questions, confirmations, quick file ops.
```

### Option 4: Direct Python (pip install)

```bash
pip install pre-reasoning-engine
```

```python
from reasoning_engine import analyze

result = analyze(
    "Frontend depends on API gateway. API gateway depends on Auth. "
    "The CTO wants microservices but the senior dev warns about complexity. "
    "We have a team of 5 and a deadline of 8 weeks."
)
print(result["trace"])
# ROOT BLOCKERS (must resolve FIRST):
#   Block [3]: DEADLINE, SOLUTION_FEASIBILITY
#     Impact: unblocks 1 downstream steps
#     Evidence: 'Constraint: deadline = 8 weeks'
# ...
```

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/engine/help` | GET | Start here. Full usage guide. |
| `/api/engine/form` | GET | Grammar guide — signal words that produce the best traces. |
| `/api/engine/analyze` | POST | Send `{"text": "..."}`, get full structural trace. |
| `/api/engine/submit` | GET | URL-based submit. `?text=...` Returns `recover_id`. |
| `/api/engine/recover/{id}` | GET | Retrieve results from `/submit`. Valid 1 hour. |
| `/api/engine/health` | GET | Health check. |
| `/api/engine/info` | GET | Engine metadata. |
| `/api/engine/docs` | GET | Interactive Swagger UI (OpenAPI). |

## Writing Tips for Better Traces

The engine detects structure from **signal words**. The more you include, the richer the trace:

| Pattern | Signal Words | Example |
|---------|-------------|---------|
| Dependencies | depends on, requires, needs, calls, relies on | "The frontend depends on the API gateway." |
| Blockers | is slow, fails, blocks, crashes, times out | "When the database is slow, everything times out." |
| Options | Option A/B/C: ... | "Option A: rewrite. Option B: refactor." |
| Stakeholders | CTO wants, senior dev warns, founder insists | "The CTO wants microservices but the senior dev warns about complexity." |
| Constraints | team of N, deadline of N weeks, budget $X | "We have a team of 4 and a deadline of 6 weeks." |
| Pain points | 1) ... 2) ... 3) ... | "1) No CI/CD. 2) No monitoring. 3) Manual deploys." |

Call `GET /api/engine/form` for the complete grammar reference.

## Grounding Levels

The engine reports how much structure it found:

| Level | Meaning |
|-------|---------|
| `grounding` | Trace orders what's visible. Simple deps, 1-2 blocks. |
| `enhancing` | Trace adds meaningful structure. Chains, constraints, or conflicts. |
| `unlocking` | Trace reveals hidden deps the model would miss. Root blockers, cycles, deep chains. |
| `humanly_grounded` | **Humanly Grounded.** Full structural picture. Dependencies + conflicts + constraints — the level a human expert would reach. |

## Benchmarks

See [benchmarks/](benchmarks/) for full cross-model validation results.

## License

MIT — see [LICENSE](LICENSE).
