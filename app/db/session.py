from sqlmodel import SQLModel, create_engine, Session
from app.core.config import get_settings

settings = get_settings()
engine = create_engine(settings.DATABASE_URL, echo=False)


def init_db() -> None:
    # For dev/UAT, you can create all tables here.
    # In production, rely on Alembic migrations.
    from app.models import user, blog, token  # noqa: F401

    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session

