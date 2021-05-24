import asyncio
import json
from shutil import copyfileobj
from datetime import datetime

from fastapi import APIRouter, status, File, UploadFile
from fastapi.responses import RedirectResponse

from routers.database import db_report_alarm, db_add_record, db_update_device_settings

device = APIRouter()
device.__name__ = "DeviceEndpoints"
device.settings_broadcast = None

RECORDS_PATH = "records"


@device.post("/upload-record", status_code=status.HTTP_201_CREATED)
async def create_upload_file(alarm_id: int, record: UploadFile = File(...)):
    new_file_name = f"{RECORDS_PATH}/{alarm_id}_{record.filename}"
    with open(new_file_name, "wb") as new_file:
        copyfileobj(record.file, new_file)
    record_id = await db_add_record(alarm_id, new_file_name)
    return {"filename": new_file_name, "record_id": record_id}


@device.post("/report-alarm", status_code=status.HTTP_201_CREATED)
async def report_alarm(device_id: int):
    alarm_id: int = await db_report_alarm(device_id)
    print(f'<time>  Alarm report received: {datetime.now().time()}')
    return {"id": alarm_id}


@device.get("/update_settings")
async def update_settings(device_id: int, name: str, is_armed: bool, recording_time: int):
    await db_update_device_settings(device_id, name, is_armed, recording_time)
    device.settings_broadcast = {"device_id": device_id, "is_armed": is_armed, "recording_time": recording_time}
    url = f"/settings?device_id={device_id}&name={name}&is_armed={is_armed}&recording_time={recording_time}"
    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)


@device.on_event("startup")
async def startup_event():
    device.task = asyncio.create_task(start_settings_server())
    device.settings_broadcast = None


async def send_settings():
    while not device.settings_broadcast:
        await asyncio.sleep(5)
        continue
    data = device.settings_broadcast
    device.settings_broadcast = None
    return data


async def settings_sender(reader, writer):
    data = await send_settings()
    byte_data = json.dumps(data).encode('utf-8')

    writer.write(byte_data)
    await writer.drain()

    print(f'<time>  New settings send: {datetime.now().time()}')
    print("Device received data")
    writer.close()


async def start_settings_server():
    server = await asyncio.start_server(settings_sender, '0.0.0.0', 8888)
    addr = server.sockets[0].getsockname()
    print(f'Settings server running on {addr}')

    async with server:
        await asyncio.gather(server.serve_forever())
