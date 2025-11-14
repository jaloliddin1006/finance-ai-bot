"""
Gemini API service for voice transcription and text processing
"""
import json
import logging
from typing import Dict, Any

import google.generativeai as genai
from config.settings import settings

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.gemini_api_key)


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
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def transcribe_audio(self, audio_data: bytes) -> str:
        """
        Transcribe audio to text using Gemini API
        
        Args:
            audio_data: Audio file bytes
            
        Returns:
            Transcribed text
        """
        try:
            # Note: Gemini Pro doesn't directly support audio transcription
            # For real implementation, you would need to use Gemini Pro Vision
            # or another audio API. This is a placeholder implementation.
            logger.info("Audio transcription requested")
            
            # For now, return a message indicating audio processing
            # In production, you would use appropriate Gemini API for audio
            return "Audio transcription not fully implemented. Please use Gemini Pro Vision or Speech-to-Text API."
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
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
            
            response = self.model.generate_content(prompt)
            
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
