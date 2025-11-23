from fastapi import FastAPI

from app.db.session import init_db
from app.api.v1 import auth, blogs


def create_app() -> FastAPI:
    app = FastAPI(title="Secure FastAPI App", version="1.0.0")

    # For UAT / dev: ensure tables exist (still use Alembic for real migrations)
    init_db()

    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(blogs.router, prefix="/api/v1")

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app


app = create_app()
