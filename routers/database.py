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
