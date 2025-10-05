# Perfect Booking Agent

## Overview
AI-powered salon booking system with WhatsApp and SMS integration. Built with FastAPI and Python, this system provides automated booking conversations using AI (DeepSeek), payment processing via Stripe, and multi-channel communication through Twilio.

## Current State
- **Status**: ✅ Running and operational
- **Server**: FastAPI application on port 5000
- **Framework**: FastAPI with Uvicorn server
- **Python Version**: 3.11
- **Database**: SQLite with booking and conversation tracking
- **Dashboard**: Full-featured admin dashboard with Clients, Calendar, Reports, and Settings

## Recent Changes
- **2025-10-05**: Implemented global search functionality to filter bookings and clients in real-time
- **2025-10-05**: Implemented notification panel showing recent booking activity with badge counter
- **2025-10-05**: Implemented user dropdown menu with Profile, Settings, Help, and Logout options
- **2025-10-05**: Enhanced backend to accept all booking form parameters (phone, date, time)
- **2025-10-05**: Implemented complete Clients section with aggregated client data and booking history
- **2025-10-05**: Implemented Calendar section with chronologically sorted booking display
- **2025-10-05**: Enhanced Reports section with revenue analytics and service performance metrics
- **2025-10-05**: Implemented Settings section with system configuration display
- **2025-10-05**: Fixed Replit webview connection issue by reconfiguring workflow
- **2025-10-05**: Updated admin dashboard to display real booking data from database
- **2025-10-05**: Fixed stat card labels to match actual data
- **2025-10-05**: Configured auto-refresh for dashboard (updates every 30 seconds)

## Project Architecture

### Main Components
- **main.py**: FastAPI application with booking system, fee calculation, and API endpoints
- **index.html**: Full-featured admin dashboard with real-time data visualization
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
- `/clients` - Client aggregation with booking history (JSON)
- `/bookings/calendar` - Calendar-formatted bookings (JSON)
- `/simulate-booking` - Create test booking (POST)

### Dashboard Features

#### Dashboard Section (Main)
- Total bookings, revenue, success rate, active clients
- Recent activity feed showing latest bookings
- Real-time data updates every 30 seconds

#### Clients Section
- Client list with total bookings and revenue per client
- Statistics: Total clients, repeat clients, average bookings per client
- Detailed client view with complete booking history
- Search and sort functionality

#### Calendar Section
- Bookings organized by date
- Chronologically sorted by appointment time within each date
- Shows booking count per date
- Visual timeline of all appointments

#### Reports Section
- Revenue metrics: Total revenue, booking fees, average value
- Client retention rate
- Service performance breakdown with revenue share visualization
- Detailed analytics per service type

#### Settings Section
- Business information display (salon name, fees, tax rates)
- Auto-refresh configuration status
- Database information and statistics

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
- Dashboard fetches live data from multiple API endpoints
- Cache-control headers prevent stale data display in Replit webview
- Calendar bookings sorted chronologically using Python datetime parsing
- Client data aggregated with SQL GROUP BY for performance
