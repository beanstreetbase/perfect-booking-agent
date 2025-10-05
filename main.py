    from fastapi import FastAPI, Request
    import os
    from twilio.rest import Client
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    app = FastAPI(title="Perfect Booking Agent")

    # Check if environment variables are loaded
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

    @app.get("/")
    async def root():
        # Check which environment variables are set
        env_status = {
            "deepseek_loaded": bool(DEEPSEEK_API_KEY),
            "twilio_sid_loaded": bool(TWILIO_ACCOUNT_SID),
            "twilio_token_loaded": bool(TWILIO_AUTH_TOKEN),
            "twilio_number_loaded": bool(TWILIO_WHATSAPP_NUMBER)
        }

        return {
            "message": "🚀 Perfect Booking Agent is running!",
            "status": "active",
            "environment_status": env_status,
            "next_steps": [
                "1. Add API keys to .env file",
                "2. Connect WhatsApp webhook", 
                "3. Test messaging"
            ]
        }

    @app.post("/webhook/whatsapp")
    async def whatsapp_webhook(request: Request):
        """WhatsApp webhook handler"""
        try:
            # Check if Twilio credentials are available
            if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER]):
                return {"error": "Twilio credentials not configured"}

            twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            form_data = await request.form()
            from_number = form_data.get('From', '')
            message_body = form_data.get('Body', '')

            print(f"📱 WhatsApp message from {from_number}: {message_body}")

            response_text = f"🤖 Thanks for your message: '{message_body}'. I'm your booking assistant!"

            message = twilio_client.messages.create(
                body=response_text,
                from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
                to=from_number
            )

            return {"status": "processed", "message_sid": message.sid}

        except Exception as e:
            return {"error": str(e)}

    @app.get("/env-check")
    async def env_check():
        """Check if environment variables are loaded"""
        return {
            "deepseek_key_loaded": bool(DEEPSEEK_API_KEY),
            "twilio_sid_loaded": bool(TWILIO_ACCOUNT_SID),
            "twilio_token_loaded": bool(TWILIO_AUTH_TOKEN), 
            "twilio_number_loaded": bool(TWILIO_WHATSAPP_NUMBER)
        }

    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)