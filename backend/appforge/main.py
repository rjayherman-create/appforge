from fastapi import FastAPI
from importlib import import_module
from pkgutil import iter_modules

from db import engine
from models import Base

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="App Builder Backend",
    version="0.1.0"
)

# Auto‑load all routers from backend/routes
for module in iter_modules(['routes']):
    module_name = module.name
    imported = import_module(f"routes.{module_name}")

    if hasattr(imported, "router"):
        app.include_router(imported.router)

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

