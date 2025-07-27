from aiogram import Bot, Dispatcher

from .middlewares import (
    LoggingMiddleware    
)

import asyncio
import dotenv
import os 
import sys
import logging

# Configure logging in console and logfile
logging.basicConfig(
    level=logging.INFO,
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

# Initialize a bot 
bot = Bot(token=BOT_TOKEN)
logger.info("Object of bot is initialize")

# Main point
async def main() -> None:

    # Initialize a dispatcher
    dp = Dispatcher()
    logger.info("Object of dispatcher is initialize")
    
    # Use dispactcher all middlewares
    dp.update.middleware(LoggingMiddleware())

    try:
        # Start bot on poolling
        logger.info("Starting polling of updates")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error: {e}")

    finally: 
        await bot.close()
        logger.info("Bot session is closed")


if __name__ == '__main__':
    try:
        logger.info("Run async main function")
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.info("Bot stopped of ctrl + c")

    except Exception as e:
        logger.error(f"Error with start main function: {e}")

    finally: 
        logger.info("Programm finished")