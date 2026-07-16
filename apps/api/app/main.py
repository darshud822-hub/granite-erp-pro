from fastapi import FastAPI

from app.modules.auth.router import router as auth_router


app = FastAPI(
    title="Granite ERP Pro API"
)


app.include_router(
    auth_router
)


@app.get("/")
def root():

    return {
        "message": "Granite ERP Pro API",
        "status": "running"
    }