from fastapi import FastAPI

from app.roles.routes import router as role_router
from app.sites.routes import router as site_router
from app.users.routes import router as user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(role_router)
app.include_router(site_router)
