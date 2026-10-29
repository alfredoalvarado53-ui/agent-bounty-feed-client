#!/usr/bin/env python3
"""
client.py - Minimal, zero-dependency client for Agent Bounty Feed.

Supports:
- Model Context Protocol (MCP) Streamable HTTP JSON-RPC 2.0 endpoint
- Live /earn-now direct bounty listing
- Hourly aggregated feed.json & network statistics
"""

import urllib.request
import json
import ssl
import sys
import argparse

sys.stdout.reconfigure(encoding="utf-8")

MCP_ENDPOINT = "https://agent-bounty-feed.dailydollar.workers.dev/mcp"
EARN_NOW_URL = "https://agent-bounty-feed.dailydollar.workers.dev/earn-now"
FEED_JSON_URL = "https://dailydollar-bot.github.io/agent-bounty-feed/feed.json"

def get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def call_mcp(method, params=None, msg_id=1):
    payload = {
        "jsonrpc": "2.0",
        "id": msg_id,
        "method": method
    }
    if params is not None:
        payload["params"] = params
    
    req = urllib.request.Request(
        MCP_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "agent-bounty-feed-client/1.0"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, context=get_ssl_context(), timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def fetch_earn_now():
    req = urllib.request.Request(
        EARN_NOW_URL,
        headers={"User-Agent": "agent-bounty-feed-client/1.0"}
    )
    with urllib.request.urlopen(req, context=get_ssl_context(), timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def fetch_feed_stats():
    req = urllib.request.Request(
        FEED_JSON_URL,
        headers={"User-Agent": "agent-bounty-feed-client/1.0"}
    )
    with urllib.request.urlopen(req, context=get_ssl_context(), timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return {
            "name": data.get("name"),
            "count": data.get("count"),
            "total_open_usd_equiv": data.get("total_open_usd_equiv"),
            "stats": data.get("stats")
        }

def list_mcp_tools():
    # 1. Handshake initialize
    call_mcp("initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "agent-bounty-feed-client", "version": "1.0.0"}
    }, msg_id=1)
    
    # 2. List tools
    tools_res = call_mcp("tools/list", {}, msg_id=2)
    return tools_res.get("result", {}).get("tools", [])

def call_mcp_tool(tool_name, arguments=None):
    if arguments is None:
        arguments = {}
    res = call_mcp("tools/call", {
        "name": tool_name,
        "arguments": arguments
    }, msg_id=3)
    return res.get("result", {})

def main():
    parser = argparse.ArgumentParser(
        description="Agent Bounty Feed Client (MCP & HTTP)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python client.py                  # Fetch immediate /earn-now bounties
  python client.py --mcp            # Handshake with MCP and list bounties
  python client.py --tool get_feed_stats  # Call specific MCP tool
  python client.py --stats          # Show live escrow statistics & breakdown
"""
    )
    parser.add_argument("--mcp", action="store_true", help="Query via Model Context Protocol (Streamable HTTP)")
    parser.add_argument("--tool", type=str, default="list_bounties", help="MCP tool to call (list_bounties, get_new_bounties, get_bounty, get_feed_stats)")
    parser.add_argument("--earn-now", action="store_true", help="Fetch direct /earn-now bounties")
    parser.add_argument("--stats", action="store_true", help="Display platform escrow and category totals")
    
    args = parser.parse_args()
    
    if args.stats:
        print("=== Agent Bounty Feed - Live Escrow Statistics ===")
        stats = fetch_feed_stats()
        print(f"Total Open Bounties: {stats.get('count')}")
        print(f"Total Open USD Value: ${stats.get('total_open_usd_equiv')}")
        print("\nBreakdown by Source Platform:")
        for src, info in stats.get("stats", {}).get("by_source", {}).items():
            if info.get("items", 0) > 0:
                print(f"  • {src.upper()}: {info.get('items')} bounties (${info.get('usd')} USD)")
        return

    if args.mcp or args.tool != "list_bounties":
        print(f"Connecting to MCP Streamable HTTP endpoint: {MCP_ENDPOINT}")
        tools = list_mcp_tools()
        print(f"Discovered {len(tools)} remote MCP tools:")
        for t in tools:
            print(f"  • {t.get('name')}: {t.get('description', '')[:75]}...")
            
        print(f"\nExecuting MCP tool: '{args.tool}'...")
        res = call_mcp_tool(args.tool)
        content = res.get("content", [])
        for c in content:
            if c.get("type") == "text":
                print(c.get("text", ""))
        return

    # Default action: /earn-now
    print(f"Querying /earn-now ({EARN_NOW_URL})...\n")
    data = fetch_earn_now()
    items = data.get("items", [])
    print(f"Found {len(items)} immediate actionable bounties:\n")
    for idx, item in enumerate(items, 1):
        title = item.get("title")
        source = item.get("source")
        url = item.get("url")
        print(f"[{idx}] [{source.upper()}] {title}")
        print(f"    URL: {url}")
        print("-" * 70)

if __name__ == "__main__":
    main()
