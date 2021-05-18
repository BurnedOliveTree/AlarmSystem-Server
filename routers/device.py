from fastapi import APIRouter, Request, Response, status, File, UploadFile
from shutil import copyfileobj
from routers.database import db_report_alarm, db_add_record

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
