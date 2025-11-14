"""
Start command handler
"""
import logging
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.models import User

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Handle /start command
    Save user to database and send welcome message
    """
    user = message.from_user
    
    try:
        # Get or create user in database
        db_user, created = await User.get_or_create(
            telegram_id=user.id,
            defaults={
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )
        
        if not created:
            # Update user info if already exists
            db_user.username = user.username
            db_user.first_name = user.first_name
            db_user.last_name = user.last_name
            await db_user.save()
            logger.info(f"Updated user: {user.id}")
        else:
            logger.info(f"Created new user: {user.id}")
        
        welcome_text = (
            f"👋 Salom, {user.first_name}!\n\n"
            "Men Finance AI Bot'man. Men sizga moliyaviy operatsiyalaringizni "
            "boshqarishda yordam beraman.\n\n"
            "📝 Ovozli habar yuboring va men uni matn ko'rinishiga o'tkazib, "
            "moliyaviy ma'lumotlarni JSON formatda qaytaraman.\n\n"
            "📌 Mavjud komandalar:\n"
            "/start - Botni qayta ishga tushirish\n"
            "/help - Yordam olish\n"
            "/login - Tizimga kirish"
        )
        
        await message.answer(welcome_text)
        
    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        await message.answer(
            "❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring."
        )
