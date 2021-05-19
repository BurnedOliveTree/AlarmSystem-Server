from os import listdir
from time import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

from routers.database import database, db_get_last_alarm_time
from routers.device import device

app = FastAPI()
app.include_router(device, tags=["device-endpoints"], prefix="/device")
app.include_router(database, tags=["database-endpoints"], prefix="/db")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    alarm_recently = await check_if_alarm_recently()
    return templates.TemplateResponse(
        "index.html.j2",
        {"request": request, "alarm": alarm_recently},
    )


@app.get('/records/{name}')
def audio(name: str):
    au = open(f"records/{name}", mode='rb')
    extension = name.split('.')[-1]
    if extension == 'mp3':
        return StreamingResponse(au, media_type="audio/mpeg")
    if extension == 'wav':
        return StreamingResponse(au, media_type="audio/wav")


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


async def check_if_alarm_recently():
    now = int(time())
    then = await db_get_last_alarm_time()
    difference = 10 * 60  # 10 minutes
    if now - then <= difference:
        return True
    return False


class File:
    def __init__(self, filename: str):
        x = filename.split('.')
        self.filename: str = filename
        self.name: str = x[0]
        self.extension: str = x[1]
        if self.extension == "mp3":
            self.type: str = "audio/mpeg"
        elif self.extension == "wav":
            self.type: str = "audio/wav"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")
