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
