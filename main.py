from os import path, listdir

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

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


@app.get('/records/{name}')
def audio(name: str):
    au = open(f"records/{name}", mode='rb')
    return StreamingResponse(au, media_type="audio/mpeg")


@app.get('/available_records')
def available_records(request: Request):
    files = []
    for filename in listdir("./records"):
        if filename.endswith(".mp3") or filename.endswith(".wav"):
            files.append(File(filename))

    return templates.TemplateResponse(
        "available_records.html.j2",
        {"request": request, "files": files},
    )


class File:
    def __init__(self, filename: str):
        x = filename.split('.')
        self.filename: str = filename
        self.name: str = x[0]
        self.extension: str = x[1]
