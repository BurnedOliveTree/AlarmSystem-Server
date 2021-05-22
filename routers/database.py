import sqlite3
from time import time

from fastapi import APIRouter

database = APIRouter()
database.__name__ = "DataBase"


@database.on_event("startup")
async def startup():
    database.connection = sqlite3.connect("Database/database.db")


@database.on_event("shutdown")
async def shutdown():
    database.connection.close()


async def db_report_alarm(device_id: int):
    insert = database.connection.execute(
        "INSERT INTO ALARMS VALUES (NULL, ?, ?)", (int(time()), device_id),
    )
    database.connection.commit()
    alarm_id = int(insert.lastrowid)
    return alarm_id


async def db_add_record(alarm_id: int, path_to_file: str):
    insert = database.connection.execute(
        "INSERT INTO RECORDS VALUES (NULL, ?, ?)", (path_to_file, alarm_id),
    )
    database.connection.commit()
    record_id = int(insert.lastrowid)
    return record_id


async def db_get_last_alarm_time():
    response = database.connection.execute(
        "SELECT occur_time FROM ALARMS ORDER BY id DESC",
    ).fetchone()
    return response[0]


async def db_get_alarms(time_l: int = None, time_r: int = None):
    if time_l is None:
        time_l = 0
    if time_r is None:
        time_r = int(time())

    response = database.connection.execute(
        """
        SELECT id, occur_time, datetime(occur_time, 'unixepoch'), device FROM ALARMS
        WHERE occur_time BETWEEN (?) AND (?)
        ORDER BY occur_time DESC
        """, (time_l, time_r),
    ).fetchall()

    alarms = [Alarm(index, occur_time, human_time, device) for index, occur_time, human_time, device in response]
    return alarms


async def db_get_records_for_alarm(alarm_id: int):
    response = database.connection.execute(
        f"""
        SELECT id, path, alarm_id FROM RECORDS
        WHERE alarm_id = {alarm_id}
        ORDER BY id
        """
    ).fetchall()

    records = [Record(index, path, alarm_id) for index, path, alarm_id in response]
    return records


class Alarm:
    def __init__(self, index, occur_time, human_time, device):
        self.index: int = index
        self.occur_time: int = occur_time
        self.human_time: str = human_time
        self.device: int = device
        self.records: list = []

    async def get_records(self):
        self.records = await db_get_records_for_alarm(self.index)


class Record:
    def __init__(self, index, path, alarm_id):
        self.index: int = index
        self.path: str = path
        self.alarm_id: int = alarm_id
        self.extension = self.path.split(".")[-1]
        self.type = "audio/mpeg" if self.extension == "mp3" else "audio/wav"


async def db_get_device_settings(device_id: int):
    response = database.connection.execute(
        f"""
        SELECT id, name, is_armed, recording_time* FROM DEVICES
        WHERE id = {device_id}
        """
    ).fetchone()

    index, name, is_armed, recording_time = response
    settings = {"device_id": index, "name": name, "is_armed": is_armed, "recording_time": recording_time}
    return settings


async def db_update_device_settings(device_id: int, name: str, is_armed: bool, recording_time: int):
    is_armed_int = await bool_to_int(is_armed)
    database.connection.execute(
        f"""
        UPDATE DEVICES SET name = ?, is_armed = ?, recording_time = ? 
        WHERE id = {device_id}
        """, (name, is_armed_int, recording_time),
    )
    database.connection.commit()


async def bool_to_int(value):
    return 1 if value else 0
