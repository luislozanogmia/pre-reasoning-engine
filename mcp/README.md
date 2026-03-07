# MCP Integration

Connect the Mia Labs Reasoning Engine to any MCP-compatible AI client.

## Remote MCP (SSE Transport)

The engine is hosted at `https://mia-labs.com/api/engine/mcp` and supports SSE transport.

### Claude Web (Settings > Connectors)

1. Go to Settings > Connectors > Add Custom Connector
2. Enter:
   - **Name**: Mia Labs Reasoning Engine
   - **URL**: `https://mia-labs.com/api/engine/mcp`
3. Save

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mia-reasoning-engine": {
      "transport": "sse",
      "url": "https://mia-labs.com/api/engine/mcp"
    }
  }
}
```

Config file locations:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Claude Code CLI

```bash
claude mcp add --transport http mia-reasoning-engine https://mia-labs.com/api/engine/mcp
```

### Cursor / Windsurf / Other MCP Clients

Use the SSE endpoint URL: `https://mia-labs.com/api/engine/mcp`

Consult your client's documentation for how to add remote MCP servers.

## Available Tools

Once connected, these tools become available:

### `analyze_problem`

Analyze an ambiguous problem and surface hidden structural dependencies.

**Input**: Natural language description of a problem (at least 20 characters).

**Output**: Structured trace with ROOT BLOCKERS, UNLOCK SEQUENCE, PARALLEL WORK, and CROSS-TYPE INTERACTIONS.

### `analyze_blocks`

Analyze pre-parsed blocks (for advanced users who build their own adapter).

**Input**: JSON array of block objects with `family`, `entities`, `roles`, and `source_clause`.

### `engine_info`

Return engine metadata and version info.

## Example Usage

Once connected, the engine tool is available in your conversations:

> "I need to decide whether to migrate our monolith to microservices. The CTO wants to move fast, but our senior dev warns about complexity. We have 4 engineers and a 6-week deadline. The payment service is timing out under load."

The `analyze_problem` tool will surface:
- ROOT BLOCKER: Payment service stability (fix this first)
- CONFLICT: CTO vs senior dev on architecture
- CONSTRAINT: Team of 4, deadline 6 weeks
- UNLOCK SEQUENCE: Fix payment stability -> then evaluate architecture options
