import asyncio
import logging
import os
import sys

from app.bot import main
from config.config import get_config

config = get_config()

logging.basicConfig(
    level=logging.getLevelName(config.logs.level_name), format=config.logs.format
)

if sys.platform.startswith("win") or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
