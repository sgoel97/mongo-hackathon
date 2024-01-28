from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

load_dotenv()


@app.on_event("startup")
def on_startup():
    pass
