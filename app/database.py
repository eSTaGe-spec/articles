from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import Annotated

SQLALCHEMY_DATABASE_URL = "sqlite:///app/article.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}, echo=False
)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
str_256 = Annotated[str, 256]
str_100 = Annotated[str, 100]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256),
        str_100: String(100),
    }


def create_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()

