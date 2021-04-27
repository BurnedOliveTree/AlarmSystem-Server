from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, StreamingResponse
from os import path

app = FastAPI()

html = ''
if path.isfile('index.html'):
    with open('index.html') as file:
        html = file.read()

@app.get("/")
async def root():
    return HTMLResponse(html)

@app.get('/audio')
def audio():
    au = open('file.wav', mode='rb')
    return StreamingResponse(au, media_type="audio/wav")