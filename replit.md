# Perfect Booking Agent

## Overview
AI-powered salon booking system with WhatsApp and SMS integration. Built with FastAPI and Python, this system provides automated booking conversations using AI (DeepSeek), payment processing via Stripe, and multi-channel communication through Twilio.

## Current State
- **Status**: ✅ Running and operational
- **Server**: FastAPI application on port 5000
- **Framework**: FastAPI with Uvicorn server
- **Python Version**: 3.11
- **Database**: SQLite with booking and conversation tracking

## Recent Changes
- **2025-10-05**: Fixed Replit webview connection issue by reconfiguring workflow
- **2025-10-05**: Updated admin dashboard to display real booking data from database
- **2025-10-05**: Fixed stat card labels to match actual data (Total Bookings, Total Revenue, Cancellation Rate, Unique Clients)
- **2025-10-05**: Configured auto-refresh for dashboard (updates every 30 seconds)
- **2025-10-05**: Fixed Python format string error in HTML template by escaping CSS curly braces
- **2025-10-05**: Updated server port from 8000 to 5000 for Replit compatibility
- **2025-10-05**: Configured workflow for automatic server startup

## Project Architecture

### Main Components
- **main.py**: FastAPI application with booking system, fee calculation, and API endpoints
- **index.html**: Admin dashboard with real-time data visualization
- **bookings.db**: SQLite database storing bookings and AI conversations
- **Dependencies**: FastAPI, Uvicorn, Twilio SDK, python-dotenv, requests

### Database Schema
- **bookings**: Stores booking details, fees, status, and timestamps
- **conversations**: Tracks AI conversation history for each booking

### API Endpoints
- `/` - Admin dashboard (HTML interface with live data)
- `/health` - Health check endpoint
- `/env-check` - Environment variables status check
- `/setup-guide` - Setup instructions
- `/business-dashboard` - Business analytics API (JSON)
- `/view-bookings` - All bookings API (JSON)
- `/simulate-booking` - Create test booking (POST)

### Booking System Features
- **Fee Calculation**: 10% booking fee + 8% tax on service price
- **Cancellation Policy**: 
  - 100% refund if cancelled 48+ hours before appointment
  - 50% refund if cancelled 24-48 hours before
  - No refund if cancelled <24 hours before
- **Real-time Dashboard**: Auto-updates every 30 seconds with live booking data

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
- Dashboard fetches live data from `/business-dashboard` and `/view-bookings` endpoints
- Cache-control headers prevent stale data display in Replit webview
