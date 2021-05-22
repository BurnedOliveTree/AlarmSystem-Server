from shutil import copyfileobj

from fastapi import APIRouter, status, File, UploadFile
from fastapi.responses import RedirectResponse

from routers.database import db_report_alarm, db_add_record, db_update_device_settings

device = APIRouter()
device.__name__ = "DeviceEndpoints"

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
    return {"id": alarm_id}


@device.get("/update_settings")
async def update_settings(device_id: int, name: str, is_armed: bool, recording_time: int):
    await db_update_device_settings(device_id, name, is_armed, recording_time)
    return RedirectResponse(f"/settings?device_id={device_id}&name={name}&is_armed={is_armed}&recording_time={recording_time}",
                            status_code=status.HTTP_303_SEE_OTHER)
