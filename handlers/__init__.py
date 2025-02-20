from aiogram import Router
from .com_handlers import command_router
from .kb_handlers import kb_router
from .ai_handlers import ai_router

router = Router()
router.include_routers(command_router, kb_router, ai_router)

__all__ = [
    'router',
]
