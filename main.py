from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.get('/')
def root():
    return {'msg': 'Hello world'}