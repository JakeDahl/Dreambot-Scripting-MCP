import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.dreambot_overview import handle_dreambot_overview_tool


async def test_dreambot_overview_none_args():
    result = await handle_dreambot_overview_tool(None)
    print(result)


async def test_dreambot_overview_empty_args():
    result = await handle_dreambot_overview_tool({})
    print(result)


async def main():
    print("Testing dreambot_overview tool:")
    await test_dreambot_overview_none_args()


if __name__ == "__main__":
    asyncio.run(main())
