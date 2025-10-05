from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import os

app = FastAPI(title="Perfect Booking Agent")

        # Force HTML response to trigger web preview
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
<!DOCTYPE html>
            <html>
            <head>
                <title>Perfect Booking Agent</title>
                <style>
                    body {{ 
                        font-family: Arial, sans-serif; 
                        margin: 40px; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                    }}
                    .container {{
                        max-width: 800px;
                        margin: 0 auto;
                        background: rgba(255,255,255,0.1);
                        padding: 30px;
                        border-radius: 15px;
                        backdrop-filter: blur(10px);
                    }}
                    .status {{ 
                        color: #4CAF50; 
                        font-weight: bold;
                        font-size: 1.2em;
                    }}
                    .endpoint {{
                        background: rgba(255,255,255,0.2);
                        padding: 10px;
                        margin: 10px 0;
                        border-radius: 5px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🚀 Perfect Booking Agent</h1>
                    <p class="status">Status: <span style="color: #4CAF50;">ACTIVE & RUNNING</span></p>
                    <p>Your AI-powered salon booking system is successfully deployed!</p>

                    <h3>📊 System Status</h3>
                    <div class="endpoint">
                        <strong>Environment Variables Loaded:</strong><br>
                        - DeepSeek API: {deepseek_status}<br>
                        - Twilio SMS: {twilio_status}<br>
                        - WhatsApp: {whatsapp_status}
                    </div>

                    <h3>🔗 Test Endpoints</h3>
                    <div class="endpoint">
                        <a href="/health" style="color: #FFD700;">/health</a> - Health check
                    </div>
                    <div class="endpoint">
                        <a href="/env-check" style="color: #FFD700;">/env-check</a> - Environment status
                    </div>
                    <div class="endpoint">
                        <a href="/setup-guide" style="color: #FFD700;">/setup-guide</a> - Setup instructions
                    </div>

                    <h3>🎯 Next Steps</h3>
                    <ol>
                        <li>Configure WhatsApp webhook in Twilio</li>
                        <li>Test AI booking conversations</li>
                        <li>Set up payment system</li>
                        <li>Deploy to production</li>
                    </ol>
                </div>
            </body>
            </html>
            """.format(
                deepseek_status="✅" if os.getenv('DEEPSEEK_API_KEY') else "❌",
                twilio_status="✅" if os.getenv('TWILIO_ACCOUNT_SID') else "❌", 
                whatsapp_status="✅" if os.getenv('TWILIO_WHATSAPP_NUMBER') else "❌"
            )

@app.get("/health")
async def health():
            return {"status": "healthy", "service": "booking_agent"}

@app.get("/env-check")
async def env_check():
            return {
                "DEEPSEEK_API_KEY": "✅ LOADED" if os.getenv('DEEPSEEK_API_KEY') else "❌ MISSING",
                "TWILIO_ACCOUNT_SID": "✅ LOADED" if os.getenv('TWILIO_ACCOUNT_SID') else "❌ MISSING",
                "TWILIO_AUTH_TOKEN": "✅ LOADED" if os.getenv('TWILIO_AUTH_TOKEN') else "❌ MISSING",
                "TWILIO_WHATSAPP_NUMBER": "✅ LOADED" if os.getenv('TWILIO_WHATSAPP_NUMBER') else "❌ MISSING"
            }

@app.get("/setup-guide")
async def setup_guide():
            return {
                "message": "Setup Instructions",
                "steps": [
                    "1. Add API keys to .env file",
                    "2. Configure Twilio WhatsApp webhook",
                    "3. Test the /webhook/whatsapp endpoint", 
                    "4. Connect your phone to WhatsApp sandbox"
                ]
            }

if __name__ == "__main__":
    print("🚀 Starting server... Looking for web preview...")
    print("📱 If web preview doesn't appear, use the URL above manually")
    uvicorn.run(app, host="0.0.0.0", port=5000)