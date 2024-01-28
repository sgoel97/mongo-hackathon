from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

from .routers import data, chat

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router)
app.include_router(chat.router)


@app.on_event("startup")
def on_startup():
    with open("./message_history.json", "w") as f:
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
    pass
