"""
Database configuration for Tortoise ORM
"""
from config.settings import settings


TORTOISE_ORM = {
    "connections": {
        "default": settings.database_url
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_db():
    """Initialize database connection"""
    from tortoise import Tortoise
    
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["app.models", "aerich.models"]}
    )
    await Tortoise.generate_schemas()


async def close_db():
    """Close database connection"""
    from tortoise import Tortoise
    await Tortoise.close_connections()
