import importlib
import pkgutil
from fastapi import FastAPI
from app.db import Base, engine
from app import routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="App Builder Backend")

# Automatically discover and register all routers in app/routes
for _, module_name, _ in pkgutil.iter_modules(routes.__path__):
    module = importlib.import_module(f"app.routes.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)

@app.get("/health")
def health():
    return {"status": "ok"}
