import sqlite3

from fastapi import APIRouter

database = APIRouter()
database.__name__ = "DataBase"


@database.on_event("startup")
async def startup():
    database.connection = sqlite3.connect("Database/database.db")


@database.on_event("shutdown")
async def shutdown():
    database.connection.close()
