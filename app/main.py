from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []
words = []

@app.get("/")
async def root_get():
    return {"message": "Server is alive"}
    
@app.post("/")
async def root_post():
    return {"message": "Server is alive"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    await websocket.send_json(words)
    try:
        while True:
            data = await websocket.receive_text()
            word = data.strip()
            if word:
                words.append(word)
                for client in clients:
                    await client.send_json(words)
    except WebSocketDisconnect:
        clients.remove(websocket)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080)
