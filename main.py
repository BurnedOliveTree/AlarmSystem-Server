from time import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers.database import database, db_get_last_alarm_time, db_get_alarms
from routers.device import device

app = FastAPI()
app.include_router(device, tags=["device-endpoints"], prefix="/device")
app.include_router(database, tags=["database-endpoints"], prefix="/db")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    alarm_recently = await check_if_alarm_recently()
    return templates.TemplateResponse(
        "index.html.j2",
        {"request": request, "alarm": alarm_recently},
    )


@app.get("/history")
async def history(request: Request):
    alarms = await db_get_alarms()
    for alarm in alarms:
        await alarm.get_records()
    return templates.TemplateResponse(
        "history.html.j2",
        {"request": request, "alarms": alarms},
    )


@app.get("/settings")
async def settings(request: Request):
    settings
    return templates.TemplateResponse(
        "settings.html.j2",
        {"request": request},
    )


@app.get('/records/{name}')
def audio(name: str):
    au = open(f"records/{name}", mode='rb')
    extension = name.split('.')[-1]
    if extension == 'mp3':
        return StreamingResponse(au, media_type="audio/mpeg")
    if extension == 'wav':
        return StreamingResponse(au, media_type="audio/wav")


async def check_if_alarm_recently():
    now = int(time())
    then = await db_get_last_alarm_time()
    difference = 10 * 60  # 10 minutes
    if now - then <= difference:
        return True
    return False


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")
