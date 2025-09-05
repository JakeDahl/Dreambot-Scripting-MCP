"""
DreamBot overview tool implementation.
"""
from typing import Any
import requests
import mcp.types as types
from bs4 import BeautifulSoup


async def handle_dreambot_overview_tool(arguments: dict[str, Any] | None) -> list[types.TextContent]:
    try:
        response = requests.get(
            "https://dreambot.org/javadocs/overview-summary.html",
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0'
            },
            timeout=10
        )

        soup = BeautifulSoup(response.text, 'html.parser')
        package_summary = soup.find('table', {'class': 'overviewSummary'})
        trs = package_summary.find_all('tr')
        packages = []
        for tr in trs:
            try:
                packages.append(tr.find('a', href=True).text)
            except:
                continue
        response.raise_for_status()
        
        return [
            types.TextContent(
                type="text",
                text=f"DreamBot JavaDocs Overview (Status: {packages}):\n"
            )
        ]
    except requests.RequestException as e:
        return [
            types.TextContent(
                type="text",
                text=f"Error fetching DreamBot overview: {str(e)}"
            )
        ]
