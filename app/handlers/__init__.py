"""
Handlers module
"""
from aiogram import Router

from . import start, help, login, voice


def setup_routers() -> Router:
    """
    Setup all routers
    """
    main_router = Router()
    
    # Include all routers
    main_router.include_router(start.router)
    main_router.include_router(help.router)
    main_router.include_router(login.router)
    main_router.include_router(voice.router)
    
    return main_router
