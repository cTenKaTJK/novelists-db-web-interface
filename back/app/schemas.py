from pydantic import BaseModel
from typing import Optional

class WriterBase(BaseModel):
    фамилия: Optional[str] = None
    имя: str
    отчество: Optional[str] = None
    год_рождения: Optional[int] = None
    год_смерти: Optional[int] = None
    id_страны_рождения: Optional[int] = None

class WriterCreate(WriterBase):
    pass

class WriterUpdate(WriterBase):
    pass

class WriterOut(WriterBase):
    id_писателя: int

    class Config:
        from_attributes = True

class WorkCreate(BaseModel):
    название_произведения: str
    id_жанра: int
    год_написания: int | None = None
    автор_id: int

class EditionCreate(BaseModel):
    id_произведения: int
    страна_где_издавалось: int
    год_издания: int
    тираж_издания: int
    издательство: str | None = None