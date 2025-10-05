from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
import uvicorn

print("🔍 DEBUG: Starting server...")
print("🔍 DEBUG: Current directory:", os.getcwd())
print("🔍 DEBUG: Files in directory:", os.listdir('.'))

# Try different ways to load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ dotenv loaded successfully")
except ImportError as e:
    print("❌ dotenv import failed:", e)

app = FastAPI(title="Perfect Booking Agent")

# Test environment variables directly
deepseek_key = os.getenv('DEEPSEEK_API_KEY')
twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_WHATSAPP_NUMBER')

print("🔍 DEBUG Environment Variables:")
print(f"DEEPSEEK_API_KEY: {'✅ LOADED' if deepseek_key else '❌ MISSING'}")
print(f"TWILIO_ACCOUNT_SID: {'✅ LOADED' if twilio_sid else '❌ MISSING'}")
print(f"TWILIO_AUTH_TOKEN: {'✅ LOADED' if twilio_token else '❌ MISSING'}")
print(f"TWILIO_WHATSAPP_NUMBER: {'✅ LOADED' if twilio_number else '❌ MISSING'}")

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <html>
        <head><title>Debug Environment</title></head>
        <body>
            <h1>🔍 Environment Debug</h1>
            <p>DEEPSEEK_API_KEY: {'✅ LOADED' if deepseek_key else '❌ MISSING'}</p>
            <p>TWILIO_ACCOUNT_SID: {'✅ LOADED' if twilio_sid else '❌ MISSING'}</p>
            <p>TWILIO_AUTH_TOKEN: {'✅ LOADED' if twilio_token else '❌ MISSING'}</p>
            <p>TWILIO_WHATSAPP_NUMBER: {'✅ LOADED' if twilio_number else '❌ MISSING'}</p>
            <hr>
            <h3>If keys are missing:</h3>
            <ol>
                <li>Check .env file exists at root level</li>
                <li>Check .env has exact variable names</li>
                <li>Restart server after changing .env</li>
                <li>Check for typos in variable names</li>
            </ol>
        </body>
    </html>
    """

@app.get("/raw-env")
async def raw_env():
    """Show raw environment variables"""
    return {
        "all_env_vars": dict(os.environ),
        "deepseek_key": deepseek_key,
        "twilio_sid": twilio_sid,
        "twilio_token": twilio_token,
        "twilio_number": twilio_number
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)