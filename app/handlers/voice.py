"""
Voice message handler
"""
import json
import logging
from aiogram import Router, Bot
from aiogram.types import Message

from app.services import gemini_service

logger = logging.getLogger(__name__)
router = Router()


@router.message(lambda message: message.voice is not None)
async def handle_voice(message: Message, bot: Bot):
    """
    Handle voice messages
    1. Download voice message
    2. Transcribe using Gemini API
    3. Extract financial data
    4. Return both text and JSON format
    """
    try:
        # Send processing message
        processing_msg = await message.answer("🎤 Ovozli xabar qayta ishlanmoqda...")
        
        # Download voice file
        voice_file = await bot.get_file(message.voice.file_id)
        voice_data = await bot.download_file(voice_file.file_path)
        
        # Read voice data
        audio_bytes = voice_data.read()
        
        # Process voice message
        transcribed_text, financial_data = await gemini_service.process_voice_message(audio_bytes)
        
        # Format response
        response_text = (
            f"📝 Transkripsiya:\n{transcribed_text}\n\n"
            f"💰 Moliyaviy ma'lumotlar (JSON):\n"
            f"```json\n{json.dumps(financial_data, indent=2, ensure_ascii=False)}\n```\n\n"
            f"📊 Tafsilotlar:\n"
            f"• Turi: {financial_data.get('type', 'N/A')}\n"
            f"• Miqdor: {financial_data.get('amount', 0)}\n"
            f"• Kategoriya: {financial_data.get('category', 'N/A')}\n"
            f"• Tavsif: {financial_data.get('description', 'N/A')}\n"
            f"• Sana: {financial_data.get('date', 'N/A')}"
        )
        
        # Delete processing message
        await processing_msg.delete()
        
        # Send response
        await message.answer(response_text, parse_mode="Markdown")
        
        logger.info(f"Processed voice message from user {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Error processing voice message: {e}")
        await message.answer(
            "❌ Ovozli xabarni qayta ishlashda xatolik yuz berdi.\n"
            "Iltimos, keyinroq urinib ko'ring yoki matn ko'rinishida yuboring."
        )


@router.message(lambda message: message.text and not message.text.startswith('/'))
async def handle_text(message: Message):
    """
    Handle regular text messages
    Extract financial data from text
    """
    try:
        # Send processing message
        processing_msg = await message.answer("📝 Matn tahlil qilinmoqda...")
        
        # Extract financial data from text
        financial_data = await gemini_service.extract_financial_data(message.text)
        
        # Format response
        response_text = (
            f"💰 Moliyaviy ma'lumotlar (JSON):\n"
            f"```json\n{json.dumps(financial_data, indent=2, ensure_ascii=False)}\n```\n\n"
            f"📊 Tafsilotlar:\n"
            f"• Turi: {financial_data.get('type', 'N/A')}\n"
            f"• Miqdor: {financial_data.get('amount', 0)}\n"
            f"• Kategoriya: {financial_data.get('category', 'N/A')}\n"
            f"• Tavsif: {financial_data.get('description', 'N/A')}\n"
            f"• Sana: {financial_data.get('date', 'N/A')}"
        )
        
        # Delete processing message
        await processing_msg.delete()
        
        # Send response
        await message.answer(response_text, parse_mode="Markdown")
        
        logger.info(f"Processed text message from user {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Error processing text message: {e}")
        await message.answer(
            "❌ Matnni tahlil qilishda xatolik yuz berdi.\n"
            "Iltimos, keyinroq urinib ko'ring."
        )
