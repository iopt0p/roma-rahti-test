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
