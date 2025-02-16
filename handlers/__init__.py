from aiogram import Router
from .com_handlers import command_router
from .kb_handlers import kb_router

router = Router()
router.include_routers(command_router, kb_router)

__all__ = [
    'router',
]
