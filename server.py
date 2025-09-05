import asyncio
from typing import Any

import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio

from tools.dreambot_overview import handle_dreambot_overview_tool
from tools.dreambot_package import handle_dreambot_package_tool
from tools.dreambot_member import handle_dreambot_member_tool

server = Server("dreambot-dev-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="dreambot_overview",
            description="Fetch the root DreamBot JavaDocs overview page. Returns the overall package structure in:"
                        "org.dreambot.<>.<> to be used within code. These are only packages to be used in dreambot_package tool.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="dreambot_package",
            description="Fetch a DreamBot JavaDocs package page for a given package name. Only used to fetch package details.",
            inputSchema={
                "type": "object",
                "properties": {
                    "package": {
                        "type": "string",
                        "description": "The package name (e.g., 'org.dreambot.api.methods.cs2')"
                    }
                },
                "required": ["package"],
            },
        ),
        types.Tool(
            name="dreambot_member",
            description="Fetch a dreambot member from a package and get the details for it.",
            inputSchema={
                "type": "object",
                "properties": {
                    "package": {
                        "type": "string",
                        "description": "The package name (e.g., 'org.dreambot.api.methods.cs2')"
                    },
                    "href": {
                        "type": "string",
                        "description": "The href (e.g., 'Combat.html')"
                    }
                },
                "required": ["package", 'href'],
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    if name == "dreambot_overview":
        return await handle_dreambot_overview_tool(arguments)
    elif name == "dreambot_package":
        return await handle_dreambot_package_tool(arguments)
    elif name == "dreambot_member":
        return await handle_dreambot_member_tool(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="dreambot-dev-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
