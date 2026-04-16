from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from app.db import get_conn, create_schema

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_schema()

class Booking(BaseModel):
    guest_id: int
    room_id: int
    date_from: date
    date_to: date


@app.get("/")
def read_root():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT version()")
        result = cur.fetchone()

    return { "msg": "Hello Docker", "db_status": result }


@app.get("/api/ip")
def read_ip(request: Request):
    ip = request.client.host
    return { "ip": ip }

@app.get("/ip", response_class=HTMLResponse)
def read_ip(request: Request):
    ip = request.client.host
    return f"<h1>Your IP is {ip}</h1>"

@app.get("/api/rooms")
def get_rooms():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM rooms ORDER BY room_type DESC")
        result = cur.fetchall()
    return result

@app.get("/api/rooms/{id}")
def get_one_room(id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM rooms
            WHERE id = %s
        """, (id,))
        result = cur.fetchone()
    return result

@app.post("/api/bookings")
def create_booking(booking: Booking):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO bookings (
                guest_id,
                room_id,
                date_from,
                date_to
            ) VALUES (
                %s, %s, %s, %s
            ) RETURNING id
        """, [
            booking.guest_id,
            booking.room_id,
            booking.date_from,
            booking.date_to,
        ])
        result = cur.fetchone()

    return {
        "msg": "Booking created",
        "id": result['id']
    }

@app.get("/api/bookings")
def get_bookings():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT
                b.date_from,
                b.date_to,
                r.room_number,
                g.first_name,
                g.last_name
            FROM bookings b
                Left JOIN rooms r ON b.room_id = r.id
                LEFT JOIN guests g ON g.id = b.guest_id
        """)
        result = cur.fetchall()

    return result