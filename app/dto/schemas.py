from pydantic import BaseModel, Field, constr
from typing import List


class CreateAuthorDTO(BaseModel):
    username: constr(min_length=1, max_length=50) = Field(..., pattern=r'^[a-zA-Z]+$', example='Admin')
    password: str = Field(..., example='bestpassword')


class CreateArticleDTO(BaseModel):
    Title: constr(min_length=3, max_length=100) = Field(..., pattern=r'^[a-zA-Z]+$', example='London')
    Content: constr(max_length=200) = Field(..., pattern=r'^[a-zA-Z\s]+$',
                                            example='London is the capital of Great Britain')
    author_id: int = Field(..., example=1)


class ArticleDTO(BaseModel):
    title: str = Field(..., example='London')
    content: str = Field(..., example='London is the capital of Great Britain')


class AuthorDTO(BaseModel):
    username: str = Field(..., example='Admin')
    articles: List[ArticleDTO]

    class Config:
        from_attributes = True
