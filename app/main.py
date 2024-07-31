from fastapi import FastAPI

from app.users.routes import router as user_router

app = FastAPI()
app.include_router(user_router)
