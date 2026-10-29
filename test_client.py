#!/usr/bin/env python3
"""
test_client.py - Unit test suite verifying MCP and REST functionality.
"""

import unittest
from client import list_mcp_tools, call_mcp_tool, fetch_earn_now, fetch_feed_stats

class TestAgentBountyFeedClient(unittest.TestCase):

    def test_mcp_discovery_and_call(self):
        tools = list_mcp_tools()
        self.assertGreaterEqual(len(tools), 4)
        tool_names = [t.get("name") for t in tools]
        self.assertIn("list_bounties", tool_names)
        self.assertIn("get_feed_stats", tool_names)

        # Call get_feed_stats
        res = call_mcp_tool("get_feed_stats")
        self.assertIn("content", res)
        self.assertTrue(len(res["content"]) > 0)

    def test_earn_now_endpoint(self):
        data = fetch_earn_now()
        self.assertIn("items", data)
        self.assertIsInstance(data["items"], list)
        self.assertGreater(len(data["items"]), 0)

    def test_feed_stats(self):
        stats = fetch_feed_stats()
        self.assertIn("count", stats)
        self.assertIn("total_open_usd_equiv", stats)
        self.assertGreater(stats["count"], 0)

if __name__ == "__main__":
    unittest.main()
