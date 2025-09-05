import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.dreambot_package import handle_dreambot_package_tool


async def test_dreambot_overview_none_args():
    result = await handle_dreambot_package_tool({'package': 'org.dreambot.api.methods.diary'})
    print(result)


async def test_dreambot_overview_empty_args():
    result = await handle_dreambot_package_tool({})
    print(result)


async def main():
    await test_dreambot_overview_none_args()


if __name__ == "__main__":
    asyncio.run(main())
