#Req/res schemas for the chatAPI
from typing import List, Optional

from pydantic import BaseModel


class Query(BaseModel):
    question: str


class Chunk(BaseModel):
    text: str
    page: Optional[int] = None
    score: float


class Answer(BaseModel):
    question: str
    answer: str
    confidence: float
    chunks: List[Chunk]
