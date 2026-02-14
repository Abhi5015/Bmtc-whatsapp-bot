# app/nlp.py
"""
NLP Module using Mistral AI
Generates natural replies for BMTC WhatsApp bot
"""

import logging
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from config import config

logger = logging.getLogger(__name__)


class NLPService:
    def __init__(self):
        if not config.MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY is missing")

        # Correct client initialization
        self.client = MistralClient(api_key=config.MISTRAL_API_KEY)
        self.model = config.MISTRAL_MODEL

        logger.info("✅ [NLP] Mistral client initialized")

    def generate_reply(self, user_message: str) -> str:
        """
        Generate reply using Mistral chat completion
        """
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    ChatMessage(
                        role="system",
                        content=(
                            "You are a BMTC bus assistant for Bangalore.\n"
                            "Be short, clear and helpful.\n"
                            "Help with bus routes, timings and fares.\n"
                            "If unsure, suggest practical guidance.\n"
                            "Keep replies WhatsApp-friendly."
                        ),
                    ),
                    ChatMessage(
                        role="user",
                        content=user_message,
                    ),
                ],
                temperature=0.4,
                max_tokens=200,
            )

            if not response.choices:
                logger.warning("[NLP] Empty response from Mistral")
                return "⚠️ I couldn't process that. Please try again."

            reply = response.choices[0].message.content

            if not reply:
                logger.warning("[NLP] Empty message content")
                return "⚠️ I couldn't generate a response."

            return reply.strip()

        except Exception:
            logger.exception("[NLP] Mistral error")
            return (
                "⚠️ I'm having trouble right now. "
                "Please try again in a moment."
            )


# Singleton instance
nlp_service = NLPService()
