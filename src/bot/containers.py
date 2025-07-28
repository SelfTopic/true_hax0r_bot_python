from aiogram import Bot

from dependency_injector import containers, providers 

from contextvars import ContextVar
from sqlalchemy.ext.asyncio import AsyncSession

session_context: ContextVar[AsyncSession] = ContextVar("session_context")

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    bot = providers.Dependency(instance_of=Bot)

    db_session = providers.Factory(lambda: session_context.get())