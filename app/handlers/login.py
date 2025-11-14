"""
Login command handler
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.models import User

router = Router()


@router.message(Command("login"))
async def cmd_login(message: Message):
    """
    Handle /login command
    Check if user is registered and show login status
    """
    user = message.from_user
    
    try:
        # Check if user exists in database
        db_user = await User.get_or_none(telegram_id=user.id)
        
        if db_user:
            login_text = (
                f"✅ Siz tizimga kirdingiz!\n\n"
                f"👤 Foydalanuvchi: {db_user.first_name or 'N/A'}\n"
                f"🆔 Telegram ID: {db_user.telegram_id}\n"
                f"📅 Ro'yxatdan o'tgan: {db_user.created_at.strftime('%Y-%m-%d %H:%M')}\n"
                f"🔄 Oxirgi yangilanish: {db_user.updated_at.strftime('%Y-%m-%d %H:%M')}\n\n"
                f"Status: {'Faol' if db_user.is_active else 'Nofaol'}"
            )
        else:
            login_text = (
                "❌ Siz hali ro'yxatdan o'tmagansiz.\n\n"
                "Iltimos, /start komandasini yuboring."
            )
        
        await message.answer(login_text)
        
    except Exception as e:
        await message.answer(
            "❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring."
        )
