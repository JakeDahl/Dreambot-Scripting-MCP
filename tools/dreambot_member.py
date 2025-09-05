"""
DreamBot package tool implementation.
"""
from typing import Any
import requests
import mcp.types as types
from bs4 import BeautifulSoup


async def handle_dreambot_member_tool(arguments: dict[str, Any] | None) -> list[types.TextContent]:
    """Handle the dreambot_member tool."""
    try:
        if not arguments or 'package' not in arguments:
            if 'package' not in arguments:
                return [
                    types.TextContent(
                        type="text",
                        text="Error: Package parameter is required"
                    )
                ]
            if 'href' not in arguments:
                return [
                    types.TextContent(
                        type="text",
                        text="Error: href parameter is required"
                    )
                ]
        
        package = arguments['package']
        href = arguments['href']

        package_path = package.replace('.', '/')

        url = f"https://dreambot.org/javadocs/{package_path}/{href}"
        
        response = requests.get(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0'
            },
            timeout=10
        )
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        deets = soup.find('div', {'class': 'details'})

        details = ''
        for row in deets.find_all('ul'):
            details += row.text.strip() + '\n\n'

        return [
            types.TextContent(
                type="text",
                text=f"DreamBot JavaDocs Package Member details \n: {details.strip()}"
            )
        ]
        
    except requests.RequestException as e:
        return [
            types.TextContent(
                type="text",
                text=f"Error fetching DreamBot package '{arguments.get('package', 'unknown')}': {str(e)}"
            )
        ]
    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"Unexpected error processing package '{arguments.get('package', 'unknown')}': {str(e)}"
            )
        ]
