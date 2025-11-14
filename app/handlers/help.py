"""
Help command handler
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message):
    """
    Handle /help command
    Show available commands and usage instructions
    """
    help_text = (
        "📚 Finance AI Bot - Yordam\n\n"
        "🎤 Ovozli habar yuborish:\n"
        "Oddiy ovozli habar yuboring va men:\n"
        "1. Ovozingizni matnga o'tkazaman\n"
        "2. Moliyaviy ma'lumotlarni ajratib olaman\n"
        "3. Sizga JSON formatda qaytaraman\n\n"
        "📌 Mavjud komandalar:\n"
        "/start - Botni qayta ishga tushirish\n"
        "/help - Bu yordam xabarini ko'rish\n"
        "/login - Tizimga kirish\n\n"
        "💡 Misol:\n"
        "\"Men bugun 50000 so'm oziq-ovqatga sarfladim\"\n\n"
        "Bot javob qaytaradi:\n"
        "• Matn ko'rinishi\n"
        "• JSON format:\n"
        "  - type: expense\n"
        "  - amount: 50000\n"
        "  - category: food\n"
        "  - description: oziq-ovqat\n\n"
        "❓ Savol yoki muammo bo'lsa, admin bilan bog'laning."
    )
    
    await message.answer(help_text)
