from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from presentation.controllers.people_controller import router as people_router
from persistence.utils import get_engine

from presentation.models.person_model import *

app = FastAPI()

origins = ['http://localhost:5500',
           'http://127.0.0.1:5500']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = get_engine()
SQLModel.metadata.create_all(engine)

app.include_router(people_router)
