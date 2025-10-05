# Perfect Booking Agent

## Overview
AI-powered salon booking system with WhatsApp and SMS integration. Built with FastAPI and Python, this system provides automated booking conversations using AI (DeepSeek), payment processing via Stripe, and multi-channel communication through Twilio.

## Current State
- **Status**: Running and operational
- **Server**: FastAPI application on port 5000
- **Framework**: FastAPI with Uvicorn server
- **Python Version**: 3.11

## Recent Changes
- **2025-10-05**: Fixed Python format string error in HTML template by escaping CSS curly braces
- **2025-10-05**: Updated server port from 8000 to 5000 for Replit compatibility
- **2025-10-05**: Configured workflow for automatic server startup

## Project Architecture

### Main Components
- **main.py**: FastAPI application with HTML dashboard and API endpoints
- **Dependencies**: FastAPI, Uvicorn, Twilio SDK, python-dotenv, requests

### API Endpoints
- `/` - HTML dashboard showing system status
- `/health` - Health check endpoint
- `/env-check` - Environment variables status check
- `/setup-guide` - Setup instructions

### Environment Variables Required
The following environment variables need to be configured in the Replit Secrets:
- `DEEPSEEK_API_KEY` - DeepSeek AI API key for booking conversations
- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `TWILIO_AUTH_TOKEN` - Twilio authentication token
- `TWILIO_WHATSAPP_NUMBER` - Twilio WhatsApp number (e.g., +14155238886)
- `GOOGLE_MAPS_API_KEY` - Google Maps API key for location services
- `STRIPE_SECRET_KEY` - Stripe API key for payment processing

See `.env.example` for reference.

## User Preferences
None specified yet.

## Technical Notes
- Server runs on port 5000 (Replit requirement for frontend)
- Uses 0.0.0.0 as host for external accessibility
- HTML templates use escaped curly braces ({{ }}) for CSS to avoid Python format string conflicts
