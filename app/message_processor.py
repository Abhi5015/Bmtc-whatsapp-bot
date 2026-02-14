# app/message_processor.py

import logging
from app.nlp import nlp_service
from app.responses import response_builder

logger = logging.getLogger(__name__)


class MessageProcessor:

    def process(self, user_message: str, from_number: str = None) -> str:
        """
        Main message routing logic
        """

        if not user_message:
            logger.warning("Empty message received")
            return response_builder.unknown()["reply"]

        # Normalize once
        clean_message = user_message.strip()
        lower_message = clean_message.lower()

        logger.info(f"Processing message: {clean_message}")

        # -------------------------
        # Fast rule-based responses
        # -------------------------

        if lower_message in {"hi", "hello", "hey"}:
            return response_builder.greeting()["reply"]

        if lower_message == "help":
            return response_builder.help()["reply"]

        if lower_message in {"thanks", "thank you"}:
            return "You're welcome! 😊"

        # -------------------------
        # AI (Mistral) fallback
        # -------------------------

        try:
            reply = nlp_service.generate_reply(clean_message)

            if not reply:
                logger.warning("Empty reply from NLP")
                return response_builder.unknown()["reply"]

            return reply

        except Exception:
            logger.exception("Message processing failed")
            return (
                "⚠️ I'm having trouble responding right now. "
                "Please try again shortly."
            )


# Singleton instance
message_processor = MessageProcessor()
