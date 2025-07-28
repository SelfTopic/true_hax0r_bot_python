from aiogram import Router 
from aiogram.types import Message 
from aiogram.filters import CommandStart

from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import AsyncSession

from ..containers import Container
from ..i18n import t
import logging 

# Setting logger 
logger = logging.getLogger(__name__)

# Initialize a object of router 
router = Router(name=__name__)


# Handler for handling the /start command as a decorator
@router.message(CommandStart(deep_link=False))
@inject
async def start_handler(
    message: Message,
    db_session: AsyncSession = Provide[Container.db_session]
):
    """Processes the /start command"""

    # User is definitely not equal to none
    if not message.from_user:
        logger.error("User not found")
        raise ValueError("User not found")
    
    logger.debug(f"db_session equal {db_session}")

    await message.answer(
        text=t(
            key="start", 
            name=message.from_user.first_name or "User",
            locale="ru"
        )    
    )

__all__ = ["router"]

