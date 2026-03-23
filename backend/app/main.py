from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models  # noqa: F401
from app.api.router import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


def create_app() -> FastAPI:
    Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)
    Path(settings.CHROMA_DIR).mkdir(exist_ok=True) 

    app = FastAPI(title=settings.APP_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup():
        Base.metadata.create_all(bind=engine)

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()