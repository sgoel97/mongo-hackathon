from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

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
os.environ["TOGETHER_API_KEY"] = "63ab6eb41c340f7eafb146396ccc7bc9051daa395feef9a414204f322af63fcf"

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
