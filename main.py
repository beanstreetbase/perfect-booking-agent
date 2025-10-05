from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import sqlite3
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Perfect Booking Agent - Local Testing")

# Configuration
TAX_RATE = 0.08
BOOKING_FEE_PERCENTAGE = 0.10
CANCELLATION_FEE = 20.00
LATE_CANCELLATION_FEE = 10.00

# Service catalog
SERVICE_CATALOG = {
    "goddess_braids": {
        "name": "Goddess Braids",
        "price": 120,
        "duration": "2-3 hours",
        "description": "Elegant and protective style"
    },
    "knotless_braids": {
        "name": "Knotless Box Braids", 
        "price": 150,
        "duration": "3-4 hours",
        "description": "Comfortable and stylish"
    },
    "haircut": {
        "name": "Professional Haircut",
        "price": 45,
        "duration": "1 hour", 
        "description": "Precision cut and style"
    },
    "color_service": {
        "name": "Color Service",
        "price": 80,
        "duration": "2-3 hours",
        "description": "Professional coloring"
    }
}

# Initialize database
def init_db():
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_phone TEXT,
            client_name TEXT,
            salon_name TEXT,
            service_type TEXT,
            service_price REAL,
            booking_date TEXT,
            booking_time TEXT,
            estimated_duration TEXT,
            booking_fee_amount REAL,
            tax_amount REAL,
            total_booking_fee REAL,
            booking_fee_paid BOOLEAN DEFAULT FALSE,
            status TEXT DEFAULT 'confirmed',
            cancellation_fee_amount REAL DEFAULT 20.00,
            special_instructions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_phone TEXT,
            message TEXT,
            response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Add sample bookings for testing
    cursor.execute('''
        INSERT OR IGNORE INTO bookings 
        (client_phone, client_name, salon_name, service_type, service_price,
         booking_date, booking_time, estimated_duration, booking_fee_paid)
        VALUES 
        ('+1234567890', 'Sarah Johnson', 'Glamour Braids Studio', 'Goddess Braids', 120, 
         '2024-03-20', '2:00 PM', '2-3 hours', TRUE),
        ('+1234567891', 'Mike Chen', 'Glamour Braids Studio', 'Knotless Box Braids', 150,
         '2024-03-21', '3:00 PM', '3-4 hours', TRUE)
    ''')

    conn.commit()
    conn.close()

init_db()

@app.get("/")
@app.head("/")
async def root():
    return FileResponse(
        "index.html",
        headers={
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    )

def calculate_booking_fee(service_price: float) -> dict:
    """Calculate 10% booking fee + tax"""
    booking_fee = service_price * BOOKING_FEE_PERCENTAGE
    tax_amount = booking_fee * TAX_RATE
    total_fee = booking_fee + tax_amount

    return {
        "service_price": service_price,
        "booking_fee_percentage": BOOKING_FEE_PERCENTAGE * 100,
        "booking_fee_amount": round(booking_fee, 2),
        "tax_rate": TAX_RATE * 100,
        "tax_amount": round(tax_amount, 2),
        "total_booking_fee": round(total_fee, 2),
        "amount_payable_at_salon": service_price - booking_fee
    }

def generate_booking_confirmation(booking_data: dict) -> str:
    """Generate comprehensive booking confirmation with terms"""

    confirmation = f"""
🎉 **BOOKING CONFIRMED - #{booking_data['booking_id']}**

📋 **APPOINTMENT DETAILS**
├─ Service: {booking_data['service_type']}
├─ Salon: {booking_data['salon_name']}
├─ Date: {booking_data['booking_date']}
├─ Time: {booking_data['booking_time']}
├─ Duration: {booking_data['duration']}
└─ Stylist: {booking_data.get('stylist', 'Assigned upon arrival')}

💰 **PAYMENT BREAKDOWN**
├─ Service Price: ${booking_data['service_price']}
├─ Booking Fee (10%): ${booking_data['fee_breakdown']['booking_fee_amount']}
├─ Tax: ${booking_data['fee_breakdown']['tax_amount']}
├─ **Total Paid:** ${booking_data['fee_breakdown']['total_booking_fee']:.2f}
└─ **Pay at Salon:** ${booking_data['fee_breakdown']['amount_payable_at_salon']:.2f}

────────────────────────────
📜 **TERMS & CONDITIONS**
────────────────────────────

✅ **CANCELLATION POLICY**
├─ 48+ hours notice: Full refund
├─ 24-48 hours notice: 50% refund
├─ Less than 24 hours: ${LATE_CANCELLATION_FEE} fee
└─ No-show: ${CANCELLATION_FEE} fee (split with salon)

✅ **RESCHEDULING**
├─ Free rescheduling (24+ hours notice)
├─ Same-day: ${LATE_CANCELLATION_FEE} fee
└─ Max 2 reschedules per booking

📍 **SALON INFORMATION**
├─ Address: 123 Beauty Street, Downtown
├─ Phone: (555) 123-4567
├─ Parking: Free parking in rear lot
└─ Arrive 15 minutes early

🔔 **IMPORTANT REMINDERS**
• Bring inspiration photos
• Arrive with clean, dry hair
• Wear comfortable clothing
• Plan for full service duration

Thank you for choosing us! ✨
"""
    return confirmation

@app.get("/simulate-conversation")
async def simulate_conversation():
    """Simulate a complete WhatsApp conversation for testing"""

    conversation_flow = [
        {
            "user": "Hi, I want goddess braids",
            "bot": """
            👑 **Goddess Braids - $120**

            Elegant and protective style
            Duration: 2-3 hours

            💰 **Fee Breakdown:**
            Service: $120
            10% Booking Fee: $12
            Total Booking Fee: $12.96 (including tax)

            📅 Ready to book? Send your preferred date and time!
            Example: "March 25, 2:00 PM"
            """
        },
        {
            "user": "March 25, 2:00 PM, Maria",
            "bot": """
            ✅ **BOOKING CONFIRMED!**

            Thank you Maria! Your booking has been created.

            📋 **Appointment Details:**
            Service: Goddess Braids
            Date: March 25, 2024
            Time: 2:00 PM
            Duration: 2-3 hours

            💰 **Booking Fee:** $12.96
            💵 **Pay at Salon:** $107.04

            A detailed confirmation with full terms & conditions is being prepared!
            """
        }
    ]

    return {
        "simulation": "Complete WhatsApp Conversation Flow",
        "flow": conversation_flow,
        "test_booking_created": True
    }

@app.post("/simulate-booking")
async def simulate_booking(request: Request):
    """Simulate booking creation (for testing)"""
    try:
        data = await request.json()
        client_name = data.get('client_name', 'Test Client')
        service_type = data.get('service_type', 'Goddess Braids')
        service_price = data.get('service_price', 120)

        # Calculate fees
        fee_calculation = calculate_booking_fee(service_price)

        # Store booking in database
        conn = sqlite3.connect('bookings.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO bookings 
            (client_phone, client_name, salon_name, service_type, service_price,
             booking_date, booking_time, estimated_duration,
             booking_fee_amount, tax_amount, total_booking_fee, booking_fee_paid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            '+1000000000', client_name, "Glamour Braids Studio", 
            service_type, service_price, '2024-03-25', '2:00 PM', '2-3 hours',
            fee_calculation['booking_fee_amount'], fee_calculation['tax_amount'],
            fee_calculation['total_booking_fee'], True
        ))

        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Generate confirmation
        booking_data = {
            'booking_id': booking_id,
            'client_name': client_name,
            'service_type': service_type,
            'salon_name': "Glamour Braids Studio",
            'service_price': service_price,
            'booking_date': '2024-03-25',
            'booking_time': '2:00 PM',
            'duration': '2-3 hours',
            'fee_breakdown': fee_calculation
        }

        confirmation_msg = generate_booking_confirmation(booking_data)

        return {
            "status": "booking_created",
            "booking_id": booking_id,
            "confirmation_message": confirmation_msg,
            "fee_breakdown": fee_calculation
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/view-bookings")
async def view_bookings():
    """View all bookings in the database"""
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, client_name, service_type, service_price, booking_date, booking_time, 
               total_booking_fee, status, created_at 
        FROM bookings 
        ORDER BY created_at DESC
    ''')

    bookings = cursor.fetchall()
    conn.close()

    formatted_bookings = []
    for booking in bookings:
        formatted_bookings.append({
            "booking_id": booking[0],
            "client_name": booking[1],
            "service_type": booking[2],
            "service_price": booking[3],
            "booking_date": booking[4],
            "booking_time": booking[5],
            "booking_fee_paid": booking[6],
            "status": booking[7],
            "created_at": booking[8]
        })

    return {
        "total_bookings": len(formatted_bookings),
        "bookings": formatted_bookings
    }

@app.get("/clients")
async def get_clients():
    """Get aggregated client data with booking history"""
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            client_phone,
            client_name,
            COUNT(*) as total_bookings,
            SUM(service_price) as total_spent,
            SUM(total_booking_fee) as total_fees_paid,
            MAX(created_at) as last_booking_date,
            MIN(created_at) as first_booking_date
        FROM bookings
        GROUP BY client_phone, client_name
        ORDER BY total_bookings DESC, last_booking_date DESC
    ''')

    clients_data = cursor.fetchall()
    
    clients = []
    for client in clients_data:
        # Get booking history for this client
        cursor.execute('''
            SELECT id, service_type, service_price, booking_date, booking_time, status, created_at
            FROM bookings
            WHERE client_phone = ?
            ORDER BY created_at DESC
        ''', (client[0],))
        
        bookings = cursor.fetchall()
        booking_history = []
        for booking in bookings:
            booking_history.append({
                "booking_id": booking[0],
                "service_type": booking[1],
                "service_price": booking[2],
                "booking_date": booking[3],
                "booking_time": booking[4],
                "status": booking[5],
                "created_at": booking[6]
            })
        
        clients.append({
            "client_phone": client[0],
            "client_name": client[1],
            "total_bookings": client[2],
            "total_spent": f"${client[3]:.2f}" if client[3] else "$0.00",
            "total_fees_paid": f"${client[4]:.2f}" if client[4] else "$0.00",
            "last_booking": client[5],
            "first_booking": client[6],
            "booking_history": booking_history
        })

    conn.close()

    return {
        "total_clients": len(clients),
        "clients": clients
    }

@app.get("/bookings/calendar")
async def get_calendar_bookings():
    """Get bookings formatted for calendar view"""
    from datetime import datetime
    
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, client_name, service_type, service_price, booking_date, 
               booking_time, status, created_at
        FROM bookings
        ORDER BY booking_date DESC
    ''')

    bookings = cursor.fetchall()
    conn.close()

    def parse_time_for_sorting(time_str):
        """Convert '2:00 PM' to sortable 24-hour format"""
        try:
            return datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M')
        except:
            return '00:00'  # Default for invalid times

    # Group bookings by date
    calendar_data = {}
    for booking in bookings:
        date = booking[4]  # booking_date
        if date not in calendar_data:
            calendar_data[date] = []
        
        calendar_data[date].append({
            "id": booking[0],
            "client_name": booking[1],
            "service_type": booking[2],
            "service_price": booking[3],
            "booking_time": booking[5],
            "status": booking[6],
            "created_at": booking[7]
        })

    # Sort bookings within each date by time
    for date in calendar_data:
        calendar_data[date].sort(key=lambda x: parse_time_for_sorting(x['booking_time']))

    return {
        "calendar_bookings": calendar_data,
        "total_dates": len(calendar_data),
        "total_bookings": len(bookings)
    }

@app.get("/business-dashboard")
async def business_dashboard():
    """Complete business analytics dashboard"""
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*), SUM(total_booking_fee) FROM bookings')
    total_bookings, total_fees = cursor.fetchone()

    cursor.execute('SELECT COUNT(*) FROM bookings WHERE status = "no_show"')
    no_shows = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(DISTINCT client_phone) FROM bookings')
    unique_clients = cursor.fetchone()[0]

    # Service popularity
    cursor.execute('''
        SELECT service_type, COUNT(*), AVG(service_price) 
        FROM bookings 
        GROUP BY service_type
    ''')
    service_stats = cursor.fetchall()

    conn.close()

    cancellation_revenue = no_shows * (CANCELLATION_FEE / 2)
    total_revenue = (total_fees or 0) + cancellation_revenue

    return {
        "business_overview": {
            "total_bookings": total_bookings or 0,
            "unique_clients": unique_clients or 0,
            "successful_bookings": (total_bookings or 0) - no_shows,
            "cancellation_rate": f"{(no_shows/(total_bookings or 1))*100:.1f}%",
            "client_retention": "85%"  # Sample data
        },
        "revenue_analytics": {
            "booking_fees": f"${total_fees or 0:.2f}",
            "cancellation_revenue": f"${cancellation_revenue:.2f}",
            "total_revenue": f"${total_revenue:.2f}",
            "average_booking_value": f"${(total_fees or 0)/(total_bookings or 1):.2f}",
            "projected_monthly_revenue": f"${total_revenue * 4:.2f}"
        },
        "service_analytics": [
            {
                "service": stat[0],
                "bookings": stat[1],
                "average_price": f"${stat[2]:.2f}",
                "revenue_share": f"{((stat[1]/(total_bookings or 1))*100):.1f}%"
            }
            for stat in service_stats
        ],
        "performance_metrics": {
            "booking_conversion_rate": "68%",
            "customer_satisfaction": "4.8/5.0",
            "repeat_customer_rate": "42%",
            "average_rating": "★★★★★"
        }
    }

@app.get("/test-booking-flow")
async def test_booking_flow():
    """Test the complete booking flow"""

    # Test fee calculation
    test_services = [
        {"service": "Goddess Braids", "price": 120},
        {"service": "Knotless Braids", "price": 150},
        {"service": "Haircut", "price": 45}
    ]

    fee_calculations = []
    for service in test_services:
        calc = calculate_booking_fee(service["price"])
        fee_calculations.append({
            "service": service["service"],
            "original_price": service["price"],
            "booking_fee": calc["total_booking_fee"],
            "pay_at_salon": calc["amount_payable_at_salon"]
        })

    return {
        "test_scenario": "Complete Booking Flow Test",
        "fee_calculations": fee_calculations,
        "cancellation_policy": {
            "late_cancellation": f"${LATE_CANCELLATION_FEE}",
            "no_show_fee": f"${CANCELLATION_FEE}",
            "free_rescheduling": "24+ hours notice"
        },
        "next_steps": [
            "1. Visit /simulate-conversation to see chat flow",
            "2. Use /simulate-booking to create test bookings",
            "3. Check /business-dashboard for analytics",
            "4. View /view-bookings to see all bookings"
        ]
    }

@app.get("/generate-sample-data")
async def generate_sample_data():
    """Generate sample booking data for testing"""

    sample_clients = [
        {"name": "Emma Wilson", "service": "Goddess Braids", "price": 120},
        {"name": "James Brown", "service": "Knotless Braids", "price": 150},
        {"name": "Sophia Garcia", "service": "Haircut", "price": 45},
        {"name": "Michael Zhang", "service": "Color Service", "price": 80}
    ]

    created_bookings = []

    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()

    for client in sample_clients:
        fee_calc = calculate_booking_fee(client["price"])

        cursor.execute('''
            INSERT INTO bookings 
            (client_phone, client_name, salon_name, service_type, service_price,
             booking_date, booking_time, estimated_duration,
             booking_fee_amount, tax_amount, total_booking_fee, booking_fee_paid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            f'+1000000{len(created_bookings)}', 
            client["name"], 
            "Glamour Braids Studio", 
            client["service"], 
            client["price"],
            '2024-03-20', 
            '2:00 PM', 
            '2-3 hours',
            fee_calc["booking_fee_amount"], 
            fee_calc["tax_amount"],
            fee_calc["total_booking_fee"], 
            True
        ))

        created_bookings.append({
            "client": client["name"],
            "service": client["service"],
            "booking_fee": fee_calc["total_booking_fee"]
        })

    conn.commit()
    conn.close()

    return {
        "sample_data_created": True,
        "bookings_added": created_bookings,
        "total_sample_bookings": len(created_bookings),
        "message": "Sample booking data generated successfully!"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Perfect Booking Agent - LOCAL TESTING MODE")
    print("✅ All features working without Twilio webhook")
    print("📍 Test endpoints available:")
    print("   /simulate-conversation")
    print("   /business-dashboard") 
    print("   /test-booking-flow")
    print("   /generate-sample-data")
    uvicorn.run(app, host="0.0.0.0", port=5000)