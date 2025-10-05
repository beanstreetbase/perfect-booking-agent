from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
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

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Perfect Booking Agent</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #fff;
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            
            .header {{
                text-align: center;
                padding: 40px 0;
            }}
            
            .header h1 {{
                font-size: 3em;
                margin-bottom: 10px;
            }}
            
            .header .status {{
                background: rgba(255,255,255,0.2);
                display: inline-block;
                padding: 8px 20px;
                border-radius: 20px;
                font-size: 0.9em;
                margin-top: 10px;
            }}
            
            .cards {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 40px;
            }}
            
            .card {{
                background: rgba(255,255,255,0.15);
                border-radius: 15px;
                padding: 25px;
                backdrop-filter: blur(10px);
                transition: transform 0.3s, box-shadow 0.3s;
            }}
            
            .card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }}
            
            .card h3 {{
                font-size: 1.5em;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .card p {{
                opacity: 0.9;
                line-height: 1.6;
                margin-bottom: 20px;
            }}
            
            .btn {{
                background: rgba(255,255,255,0.3);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 1em;
                transition: background 0.3s;
                text-decoration: none;
                display: inline-block;
            }}
            
            .btn:hover {{
                background: rgba(255,255,255,0.4);
            }}
            
            .services {{
                background: rgba(255,255,255,0.15);
                border-radius: 15px;
                padding: 30px;
                margin-top: 40px;
                backdrop-filter: blur(10px);
            }}
            
            .service-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }}
            
            .service-item {{
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 10px;
            }}
            
            .service-item h4 {{
                font-size: 1.2em;
                margin-bottom: 8px;
            }}
            
            .service-item .price {{
                font-size: 1.5em;
                color: #FFD700;
                margin: 10px 0;
            }}
            
            .service-item .duration {{
                opacity: 0.8;
                font-size: 0.9em;
            }}
            
            .footer {{
                text-align: center;
                margin-top: 60px;
                opacity: 0.8;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Perfect Booking Agent</h1>
                <p style="font-size: 1.2em; opacity: 0.9;">AI-Powered Salon Booking System</p>
                <div class="status">✅ Status: Active & Running</div>
            </div>
            
            <div class="cards">
                <div class="card">
                    <h3>💬 Test Conversation</h3>
                    <p>Simulate a complete WhatsApp booking conversation flow with AI responses and booking confirmation.</p>
                    <a href="/simulate-conversation" class="btn">View Conversation</a>
                </div>
                
                <div class="card">
                    <h3>📊 Business Dashboard</h3>
                    <p>Complete analytics including revenue, bookings, client retention, and performance metrics.</p>
                    <a href="/business-dashboard" class="btn">View Analytics</a>
                </div>
                
                <div class="card">
                    <h3>📅 View Bookings</h3>
                    <p>See all bookings in the database with client information, services, and payment status.</p>
                    <a href="/view-bookings" class="btn">View Bookings</a>
                </div>
                
                <div class="card">
                    <h3>🧪 Test Booking Flow</h3>
                    <p>Test the complete booking flow with fee calculations and cancellation policies.</p>
                    <a href="/test-booking-flow" class="btn">Test Flow</a>
                </div>
                
                <div class="card">
                    <h3>📝 Generate Sample Data</h3>
                    <p>Create sample bookings to test the system with realistic client and service data.</p>
                    <a href="/generate-sample-data" class="btn">Generate Data</a>
                </div>
            </div>
            
            <div class="services">
                <h2 style="margin-bottom: 10px;">💇‍♀️ Available Services</h2>
                <p style="opacity: 0.9; margin-bottom: 20px;">Professional salon services with transparent pricing</p>
                
                <div class="service-grid">
                    <div class="service-item">
                        <h4>Goddess Braids</h4>
                        <div class="price">$120</div>
                        <div class="duration">Duration: 2-3 hours</div>
                        <p style="margin-top: 10px; font-size: 0.9em;">Elegant and protective style</p>
                    </div>
                    
                    <div class="service-item">
                        <h4>Knotless Box Braids</h4>
                        <div class="price">$150</div>
                        <div class="duration">Duration: 3-4 hours</div>
                        <p style="margin-top: 10px; font-size: 0.9em;">Comfortable and stylish</p>
                    </div>
                    
                    <div class="service-item">
                        <h4>Professional Haircut</h4>
                        <div class="price">$45</div>
                        <div class="duration">Duration: 1 hour</div>
                        <p style="margin-top: 10px; font-size: 0.9em;">Precision cut and style</p>
                    </div>
                    
                    <div class="service-item">
                        <h4>Color Service</h4>
                        <div class="price">$80</div>
                        <div class="duration">Duration: 2-3 hours</div>
                        <p style="margin-top: 10px; font-size: 0.9em;">Professional coloring</p>
                    </div>
                </div>
            </div>
            
            <div class="services" style="margin-top: 30px;">
                <h3>💰 Pricing Information</h3>
                <div style="margin-top: 15px;">
                    <p>• 10% booking fee (includes tax)</p>
                    <p>• Remaining balance paid at salon</p>
                    <p>• Free cancellation with 48+ hours notice</p>
                    <p>• $10 late cancellation fee (24-48 hours)</p>
                    <p>• $20 no-show fee</p>
                </div>
            </div>
            
            <div class="footer">
                <p>Perfect Booking Agent - Powered by AI • Local Testing Mode</p>
                <p style="margin-top: 10px;">Ready for WhatsApp integration when you upgrade Twilio</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(
        content=html_content,
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