from fastapi import FastAPI

from app.api.roles import router as role_router
from app.api.sites import router as site_router
from app.api.users import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(role_router)
app.include_router(site_router)
