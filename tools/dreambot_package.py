"""
DreamBot package tool implementation.
"""
from typing import Any
import requests
import mcp.types as types
from bs4 import BeautifulSoup


async def handle_dreambot_package_tool(arguments: dict[str, Any] | None) -> list[types.TextContent]:
    try:
        if not arguments or 'package' not in arguments:
            return [
                types.TextContent(
                    type="text",
                    text="Error: Package parameter is required"
                )
            ]
        
        package = arguments['package']
        package_path = package.replace('.', '/')

        url = f"https://dreambot.org/javadocs/{package_path}/package-summary.html"
        
        response = requests.get(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0'
            },
            timeout=10
        )
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        typeSummarys = soup.find_all('table', {'class': 'typeSummary'})
        type_summary_return = ''

        for summary in typeSummarys:
            summary_type = summary.find('span').text
            type_summary_return += '{} hrefs: \n'.format(summary_type)

            for row in summary.find_all('tr'):
                try:
                    href = row.find('a', href=True)['href']
                except:
                    continue
                type_summary_return += (href + '  #  ' + row.text.strip().split('\n')[-1] + '\n')

            type_summary_return += '\n'

        return [
            types.TextContent(
                type="text",
                text=f"DreamBot JavaDocs Package '{package}' \n {type_summary_return}"
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
