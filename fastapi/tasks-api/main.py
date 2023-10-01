from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from persistence.database import load_tables
from presentation.controllers.auth_controller import router as auth_router
from presentation.controllers.task_controller import router as task_router

app = FastAPI()

origins = [
	"http://127.0.0.1:5500"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(task_router)

load_tables()
