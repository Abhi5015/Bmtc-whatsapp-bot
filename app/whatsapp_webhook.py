# app/whatsapp_webhook.py

import logging
from fastapi import Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from app.message_processor import message_processor

logger = logging.getLogger(__name__)


class WhatsAppWebhook:
    def __init__(self):
        self.processor = message_processor

    async def handle_incoming_message(self, request: Request):
        try:
            form = await request.form()

            user_message = form.get("Body", "")
            from_number = form.get("From", "")

            logger.info(f"Received message from {from_number}: {user_message}")

            reply_text = self.processor.process(
                user_message=user_message,
                from_number=from_number
            )

            logger.info(f"Sending reply: {reply_text}")

            # Build TwiML response
            resp = MessagingResponse()
            resp.message(reply_text)

            twiml_str = str(resp)

            logger.info(f"TwiML Response: {twiml_str}")

            return Response(
                content=twiml_str,
                media_type="text/xml"
            )

        except Exception as e:
            logger.exception("Webhook error")

            # ALWAYS return valid TwiML even on error
            resp = MessagingResponse()
            resp.message("⚠️ Something went wrong.")
            return Response(
                content=str(resp),
                media_type="text/xml"
            )


whatsapp_webhook = WhatsAppWebhook()
