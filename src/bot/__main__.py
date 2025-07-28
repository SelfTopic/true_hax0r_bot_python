from aiogram import Bot, Dispatcher

from .middlewares import (
    LoggingMiddleware,
    DatabaseMiddleware
)

from .routers.routes import include_routers
from .containers import Container
from ..database import session_factory, flush_database, engine

import asyncio
import dotenv
import os 
import sys
import logging

# Configure logging in console and logfile
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs.log")    
    ]
)

logger = logging.getLogger(__name__)

# Configure envirion loading 
dotenv.load_dotenv()

# Getting token of bot from .env file
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    logger.fatal("Bot token is not found")
    sys.exit(1)


# Main point
async def main(bot_token: str) -> None:

    # Initialize a bot 
    bot = Bot(token=bot_token)
    logger.info("Object of bot is initialize")


    # Configure depedency injector container
    container = Container(bot=bot)
    container.wire(
        modules=[__name__, ".middlewares", ".routers"]    
    )

    # Initialize a dispatcher
    dp = Dispatcher()
    logger.info("Object of dispatcher is initialize")

    
    # Use dispactcher all middlewares
    dp.update.middleware(LoggingMiddleware())

    database_middleware = DatabaseMiddleware(session_factory=session_factory)
    dp.update.middleware(database_middleware)

    # Include all routers in the dispatcher 
    include_routers(dp)

    # Reset data of database (dev)
    await flush_database(engine=engine)

    try:
        # Start bot on poolling
        logger.info("Starting polling of updates")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error polling: {e}")

    finally: 
        await bot.close()
        logger.info("Bot session is closed")


if __name__ == '__main__':
    try:
        logger.info("Run async main function")
        asyncio.run(main(BOT_TOKEN))

    except KeyboardInterrupt:
        logger.info("Bot stopped of ctrl + c")

    except Exception as e:
        logger.error(f"Error with start main function: {e}")

    finally: 
        logger.info("Programm finished")