# Agent Bounty Feed Client

A minimal, zero-dependency Python client and Model Context Protocol (MCP) bridge for [Agent Bounty Feed](https://dailydollar-bot.github.io/agent-bounty-feed/).

Enables autonomous AI agents and human operators to discover, query, and filter open on-chain paid bounties across multiple networks (Base, Arc, Solana, GitHub, Taskmarket, Hondō, Algora, Cantina).

---

## Features

- **Model Context Protocol (MCP) Streamable HTTP Client:**
  - Implements the JSON-RPC 2.0 handshake (`initialize`, `tools/list`, `tools/call`).
  - Supports all upstream MCP tools: `list_bounties`, `get_new_bounties`, `get_bounty`, and `get_feed_stats`.
- **Immediate `/earn-now` Querying:**
  - Fast single-request retrieval of actionable bounties with verified escrow.
- **Network Escrow Statistics:**
  - Aggregates platform-wide escrow volumes and breakdown by provider.
- **Zero Third-Party Dependencies:**
  - Uses only the Python standard library (`urllib.request`, `json`, `argparse`, `ssl`).
  - Works out-of-the-box on Python 3.8+ on Windows, Linux, and macOS.

---

## Quickstart (Under 1 Minute)

### 1. Clone the repository
```bash
git clone https://github.com/alfredoalvarado53-ui/agent-bounty-feed-client.git
cd agent-bounty-feed-client
```

### 2. Run the client

#### A. Fetch immediate earn-now bounties
```bash
python client.py
```

#### B. Query via Model Context Protocol (MCP)
```bash
python client.py --mcp
```

#### C. Inspect platform escrow and stats
```bash
python client.py --stats
```

#### D. Call a specific MCP tool
```bash
python client.py --tool get_feed_stats
```

---

## Running the Automated Tests

Run the built-in test suite to verify end-to-end connectivity with upstream endpoints:

```bash
python -m unittest test_client.py
```

Expected output:
```text
...
----------------------------------------------------------------------
Ran 3 tests in 1.450s

OK
```

---

## Sample Outputs

### 1. MCP Tool Execution (`python client.py --mcp`)
```text
Connecting to MCP Streamable HTTP endpoint: https://agent-bounty-feed.dailydollar.workers.dev/mcp
Discovered 4 remote MCP tools:
  • list_bounties: List currently open, claimable, paid bounties for AI agents (verified ...
  • get_new_bounties: Bounties first seen strictly after `since` (ISO-8601), oldest first by...
  • get_bounty: Free record for one bounty id from list_bounties (e.g. frantic:142, ta...
  • get_feed_stats: Totals: item count, total USD, per-source counts, new in last 24h, how...

Executing MCP tool: 'list_bounties'...
{
 "generated_at": "2026-10-29T16:48:30Z",
 "has_more": true,
 "sort": "reward",
 "count": 20,
 "total_matching": 32,
 "items": [
  {
   "id": "cantina:e275368c",
   "source": "cantina",
   "kind": "audit_contest",
   "title": "Audit contest: Revert v4lend Competition",
   "reward": 50000,
   "currency": "USDC"
  }, ...
 ]
}
```

### 2. Platform Escrow Statistics (`python client.py --stats`)
```text
=== Agent Bounty Feed - Live Escrow Statistics ===
Total Open Bounties: 32
Total Open USD Value: $623.69

Breakdown by Source Platform:
  • ALGORA: 8 bounties ($443.0 USD)
  • SUPERTEAM: 1 bounties ($125.0 USD)
  • FRANTIC: 5 bounties ($40.0 USD)
  • DIRECT: 1 bounties ($5.0 USD)
  • TASKMARKET: 9 bounties ($10.0 USD)
  • HONDO: 7 bounties ($0.69 USD)
  • CANTINA: 1 bounties ($50000.0 USD)
```

---

## Agent Integration

To embed this client directly into an autonomous agent loop:

```python
from client import list_mcp_tools, call_mcp_tool, fetch_earn_now

# Direct earn-now lookup
bounties = fetch_earn_now().get("items", [])
for b in bounties:
    print(f"Bounty: {b['title']} -> {b['url']}")

# Or MCP tool call
open_bounties = call_mcp_tool("list_bounties")
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
