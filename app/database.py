from typing import Optional
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine


_engine: Optional[Engine] = None


def get_engine() -> Engine:
    global _engine

    # In this example, we are using SQLite as our database, but we can use any other database by utilizing the database credentials from our settings object, for example:
    # database_host = settings.database.host
    # database_port = settings.database.port
    # database_name = settings.database.name
    # etc.

    if _engine is None:
        _engine = create_engine(
            url="sqlite:///",
            connect_args={"check_same_thread": False},
            echo=True,  # remove this in production
        )

    return _engine


def create_all():
    # Importing models to ensure tables are created automatically when the app runs
    from app.models import Users  # noqa

    SQLModel.metadata.create_all(get_engine())


def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session
