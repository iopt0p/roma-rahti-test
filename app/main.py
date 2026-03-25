from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def read_root():
    return { "msg": "Hello Docker", "v": "0.2" }


@app.get("/api/ip", response_class=HTMLResponse)
def read_ip(request: Request):
    ip = request.client.host
    return f"<h1>Your IP is {ip}</h1>"
