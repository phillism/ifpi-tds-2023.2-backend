from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from persistence.utils import obter_engine
from presentation.controllers.ambientes_controller import \
    router as ambientes_router
from presentation.controllers.dispositivos_controller import \
    router as dispositivos_router
from presentation.viewmodels.models import *

app = FastAPI()

# Ativar CORS
origins = ['http://localhost:5500',
           'http://127.0.0.1:5500',
           'https://smarthome-web-8sqp.onrender.com']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = obter_engine()
SQLModel.metadata.create_all(engine)

# Registrar Roteadores
app.include_router(ambientes_router)
app.include_router(dispositivos_router)
