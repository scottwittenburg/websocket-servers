import os

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

import uvicorn


STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'dist')

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_FILES_PATH), name="static")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    print("WebSocket opened")

    try:
        while True:
            data = await websocket.receive_text()

            if data == 'close':
                await websocket.close()
            else:
                await websocket.send_text(f"You said: {data}")
    # https://fastapi.tiangolo.com/advanced/websockets/#handling-disconnections-and-multiple-clients
    except WebSocketDisconnect:
        print('WebSocket closed')


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8080)
