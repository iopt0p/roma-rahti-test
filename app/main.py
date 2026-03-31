from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
def read_root():
    return { "msg": "Hello Docker", "v": "0.2" }


@app.get("/api/ip")
def read_ip(request: Request):
    ip = request.client.host
    return { "ip": ip }

@app.get("/ip", response_class=HTMLResponse)
def read_ip(request: Request):
    ip = request.client.host
    return f"<h1>Your IP is {ip}</h1>"

@app.get("/api/rooms")
def read_rooms():
    rooms = [
        {"number": 1, "type": "Single"},
        {"number": 2, "type": "Single"},
        {"number": 3, "type": "Single"},
        {"number": 4, "type": "Single"},
        {"number": 5, "type": "Double"},
        {"number": 6, "type": "Double"},
        {"number": 7, "type": "Double"},
        {"number": 8, "type": "Double"},
        {"number": 9, "type": "Family"},
        {"number": 10, "type": "Family"},
        {"number": 11, "type": "Family"},
        {"number": 12, "type": "Family"},
        {"number": 13, "type": "Suite"},
        {"number": 14, "type": "Suite"},
        {"number": 15, "type": "Suite"},
        {"number": 16, "type": "Suite"},
        {"number": 17, "type": "Presidential"},
        {"number": 18, "type": "Presidential"},
    ]

    return rooms
