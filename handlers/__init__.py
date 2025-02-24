from aiogram import Router
from .com_handlers import command_router
from .ai_handlers import ai_router
from .cb_handlers import cb_router

router = Router()
router.include_routers(command_router, ai_router, cb_router)

__all__ = [
    'router',
]
