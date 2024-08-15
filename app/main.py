from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, create_db
from app.dto.schemas import AuthorDTO, CreateAuthorDTO, ArticleDTO, CreateArticleDTO
from app.models.models import Author, Article
from app.jwt_auth import hash_password, create_access_token, get_current_user

create_db()
app = FastAPI()


@app.post('/register',  response_model=CreateAuthorDTO, tags=['user'])
def register(author: CreateAuthorDTO, db: Session = Depends(get_db)):
    existing_user = db.query(Author).filter(Author.username == author.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким именем уже зарегистрирован',
        )

    hashed_password = hash_password(author.password)
    user = Author(username=author.username, password=hashed_password)
    db.add(user)
    db.commit()

    access_token = create_access_token(data={'sub': user.username})
    return user


@app.post('/articles', response_model=CreateArticleDTO, tags=['article'])
def create_article(article: CreateArticleDTO, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == article.author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Автор с таким id не найден'
        )

    new_article = Article(title=article.Title, content=article.Content, author_id=author.id)
    db.add(new_article)
    db.commit()
    return ArticleDTO(Title=new_article.title, Content=new_article.content)


@app.get('/all', response_model=List[AuthorDTO], tags=['user'])
def get_all_authors(db: Session = Depends(get_db)):
    authors = db.query(Author).all()
    return [
        AuthorDTO(
            username=author.username,
            articles=[
                ArticleDTO(
                    title=article.title,
                    content=article.content
                ) for article in author.article
            ]
        ) for author in authors
    ]
