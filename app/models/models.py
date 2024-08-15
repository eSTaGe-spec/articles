import re
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Annotated
from fastapi import HTTPException, status

from app.database import Base, str_100, str_256

int_pk = Annotated[int, mapped_column(primary_key=True)]


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int_pk]
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    article: Mapped[list['Article']] = relationship(back_populates='author')

    @classmethod
    def validate_username(cls, username: str):
        if not re.match(r'^[a-zA-z]+$', username):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='В имени пользователя должны быть только латинские буквы'
            )


class Article(Base):
    __tablename__ = 'articles'

    id: Mapped[int_pk]
    title: Mapped[str_100]
    content: Mapped[str_256]
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id', ondelete='CASCADE'))

    author: Mapped['Author'] = relationship(back_populates='article')

    @classmethod
    def validate_title(cls, title: str):
        if not re.match(r'^[a-zA-z]+$', title) or len(title) < 3 or len(title) > 100:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Заголовок должен содержать только латинские буквы, быть длиной не менее 3 символов и не '
                       'превышать 100 символов'
            )

    @classmethod
    def validate_content(cls, content: str):
        if not re.match(r'^[a-zA-z]+$', content):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Содержимое должно содержать только латинские буквы'
            )


