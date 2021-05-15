from fastapi import APIRouter, Request, Response, File, UploadFile
from shutil import copyfileobj

device = APIRouter()
device.__name__ = "DeviceEndpoints"

RECORDS_PATH = "records"


@device.post("/device/upload-record")
async def create_upload_file(record: UploadFile = File(...)):
    with open(f"{RECORDS_PATH}/{record.filename}", "wb") as new_file:
        copyfileobj(record.file, new_file)
    return {"filename": record.filename}
