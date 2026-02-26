import importlib
import pkgutil
from fastapi import FastAPI
from appforge.db import Base, engine
from appforge import routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="App Builder Backend")

# Automatically discover and register all routers in appforge/routes
for _, module_name, _ in pkgutil.iter_modules(routes.__path__):
    module = importlib.import_module(f"appforge.routes.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)

@app.get("/health")
def health():
    return {"status": "ok"}
