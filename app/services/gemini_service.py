"""
Gemini API service for voice transcription and text processing
"""
import json
import logging
from typing import Dict, Any

import google.genai as genai
from config.settings import settings

from google.genai.errors import APIError
# Fayl boshqaruvi uchun kerakli kutubxonalar
import tempfile
import os

logger = logging.getLogger(__name__)

# Configure Gemini API

# genai.Client(api_key=settings.gemini_api_key)
# Eslatma: genai.Client() ham API kalitini o'zi oladi, lekin bu usul ham ishlaydi.
# genai.configure(api_key=settings.gemini_api_key)


class GeminiService:
    """Service for working with Gemini API"""
    
    # JSON template for financial data extraction
    FINANCIAL_DATA_TEMPLATE = {
        "type": "income/expense",
        "amount": 0,
        "category": "",
        "description": "",
        "date": ""
    }
    
    def __init__(self):
        # Client obyekti (Fayl operatsiyalari va kontent yaratish uchun)
        self.client = genai.Client(api_key=settings.gemini_api_key)
        
       
    
    async def transcribe_audio(self, audio_data: bytes) -> str:
        """
        Transcribe audio to text using Gemini API
        """
        temp_file_path = None
        audio_file = None 
        try:
            logger.info("Audio transcription started")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            try:
                # Fayl yuklash
                logger.info(f"Uploading audio file: {temp_file_path}")
                audio_file = self.client.files.upload(file=temp_file_path)
                logger.info(f"Audio file uploaded successfully: {audio_file.name}")
                
                prompt = "Generate a transcript of the speech. Return only the transcribed text without any additional formatting or explanation."
                
                # Generate content using client
                response = self.client.models.generate_content(
                    model='gemini-2.0-flash-exp',
                    contents=[prompt, audio_file]
                )
                
                transcribed_text = response.text.strip()
                logger.info(f"Audio transcription completed: {transcribed_text[:100]}...")
                
                # Faylni Gemini serveridan o'chirish
                if audio_file:
                    try:
                        self.client.files.delete(audio_file.name)
                        logger.info("Uploaded file deleted from Gemini")
                    except Exception as e:
                        logger.warning(f"Could not delete file from Gemini: {e}")
                
                return transcribed_text
                
            except APIError as api_e:
                logger.error(f"Gemini API Error during transcription: {api_e}", exc_info=True)
                raise
            
            finally:
                # Vaqtinchalik mahalliy faylni o'chirish
                if temp_file_path and os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}", exc_info=True)
            raise
    
    
    async def extract_financial_data(self, text: str) -> Dict[str, Any]:
        """
        Extract financial data from text using Gemini API
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with extracted financial data
        """
        try:
            prompt = f"""
Analyze the following text and extract financial information.
Return the data in this exact JSON format:
{{
    "type": "income or expense",
    "amount": numeric_value,
    "category": "category_name",
    "description": "brief_description",
    "date": "date_if_mentioned or today"
}}

Text: {text}

Return only valid JSON, nothing else.
"""
            
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            # Parse the JSON response
            try:
                # Clean the response text
                response_text = response.text.strip()
                
                # Remove markdown code blocks if present
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                if response_text.startswith("```"):
                    response_text = response_text[3:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                
                response_text = response_text.strip()
                
                data = json.loads(response_text)
                return data
                
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON from Gemini response: {response.text}")
                # Return default template with original text
                return {
                    **self.FINANCIAL_DATA_TEMPLATE,
                    "description": text
                }
                
        except Exception as e:
            logger.error(f"Error extracting financial data: {e}")
            raise
    
    async def process_voice_message(self, audio_data: bytes) -> tuple[str, Dict[str, Any]]:
        """
        Process voice message: transcribe and extract financial data
        
        Args:
            audio_data: Audio file bytes
            
        Returns:
            Tuple of (transcribed_text, financial_data)
        """
        # Transcribe audio
        transcribed_text = await self.transcribe_audio(audio_data)
        
        # Extract financial data
        financial_data = await self.extract_financial_data(transcribed_text)
        
        return transcribed_text, financial_data


# Global service instance
gemini_service = GeminiService()
