from fastapi import FastAPI
from controllers.milhas_controller import router

app = FastAPI()
app.include_router(router)
