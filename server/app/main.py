from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from pathlib import Path

from .routers import upload, data, chat

app = FastAPI()

origins = ["http://localhost:5173", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(data.router)
app.include_router(chat.router)
app.include_router(upload.router)

<<<<<<< HEAD

=======
>>>>>>> 1962557977b056e40b734cf1630d36505516c057
@app.on_event("startup")
def on_startup():
    Path("./app/db/messages").mkdir(parents=True, exist_ok=True)
    with open("./app/db/messages/message_history.json", "w") as f:
        json.dump(
            {
                "messages": [
                    {"role": "system", "message": "You are a helpful assistant."}
                ]
            },
            f,
        )


@app.on_event("shutdown")
def on_shutdown():
    os.remove("./app/db/messages/message_history.json")


@app.get("/")
def root():
    return {"message": "Hello World"}
