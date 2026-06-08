from fastapi import FastAPI, Depends, HTTPException, status

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from typing import Optional

from .models import *
from .schemas import *
from .database import get_db

app = FastAPI(title="Novelists API")


###########################################################################
#                               ПИСАТЕЛИ                                  #
###########################################################################

@app.get("/")
async def root():
    return {"message": "Novelists API is running"}

@app.get("/writers")
async def get_writers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Writer))
    writers = result.scalars().all()
    return writers

@app.get("/writers", response_model=list[WriterOut])
async def get_writers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Writer))
    writers = result.scalars().all()
    return writers

@app.get("/writers/{writer_id}", response_model=WriterOut)
async def get_writer(writer_id: int, db: AsyncSession = Depends(get_db)):
    writer = await db.get(Writer, writer_id)
    if not writer:
        raise HTTPException(status_code=404, detail="Писатель не найден")
    return writer

@app.post("/writers", response_model=WriterOut, status_code=status.HTTP_201_CREATED)
async def create_writer(writer: WriterCreate, db: AsyncSession = Depends(get_db)):
    new_writer = Writer(**writer.model_dump())
    db.add(new_writer)
    await db.commit()
    await db.refresh(new_writer)
    return new_writer

@app.put("/writers/{writer_id}", response_model=WriterOut)
async def update_writer(writer_id: int, writer_data: WriterUpdate, db: AsyncSession = Depends(get_db)):
    writer = await db.get(Writer, writer_id)
    if not writer:
        raise HTTPException(status_code=404, detail="Писатель не найден")
    for key, value in writer_data.model_dump(exclude_unset=True).items():
        setattr(writer, key, value)
    await db.commit()
    await db.refresh(writer)
    return writer

@app.delete("/writers/{writer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_writer(writer_id: int, db: AsyncSession = Depends(get_db)):
    writer = await db.get(Writer, writer_id)
    if not writer:
        raise HTTPException(status_code=404, detail="Писатель не найден")
    await db.delete(writer)
    await db.commit()
    return None

###########################################################################
#                               ПРОИЗВЕДЕНИЯ                              #
###########################################################################

@app.get("/works")
async def get_works(
    author_id: Optional[int] = None,
    genre_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Work).options(selectinload(Work.genre))
    if author_id:
        query = query.join(WriterWork).where(WriterWork.id_писателя == author_id)
    if genre_id:
        query = query.where(Work.id_жанра == genre_id)
    result = await db.execute(query)
    works = result.scalars().all()
    return works

@app.post("/works", status_code=201)
async def create_work(work: WorkCreate, db: AsyncSession = Depends(get_db)):
    genre = await db.get(Genre, work.id_жанра)
    if not genre:
        raise HTTPException(400, "Жанр не найден")
    author = await db.get(Writer, work.автор_id)
    if not author:
        raise HTTPException(400, "Автор не найден")
    
    new_work = Work(
        название_произведения=work.название_произведения,
        id_жанра=work.id_жанра,
        год_написания=work.год_написания
    )
    db.add(new_work)
    await db.flush()
    writer_work = WriterWork(id_писателя=work.автор_id, id_произведения=new_work.id_произведения)
    db.add(writer_work)
    await db.commit()
    await db.refresh(new_work)
    return new_work

@app.delete("/works/{work_id}")
async def delete_work(work_id: int, db: AsyncSession = Depends(get_db)):
    work = await db.get(Work, work_id)
    if not work:
        raise HTTPException(404, "Произведение не найдено")
    await db.delete(work)
    await db.commit()
    return {"ok": True}

###########################################################################
#                             ИЗДАНИЯ                                     #
###########################################################################

@app.post("/editions", status_code=201)
async def create_edition(edition: EditionCreate, db: AsyncSession = Depends(get_db)):
    # проверка существования произведения и страны
    work = await db.get(Work, edition.id_произведения)
    if not work:
        raise HTTPException(400, "Произведение не найдено")
    country = await db.get(Country, edition.страна_где_издавалось)
    if not country:
        raise HTTPException(400, "Страна не найдена")
    new_edition = Edition(
        id_произведения=edition.id_произведения,
        страна_где_издавалось=edition.страна_где_издавалось,
        год_издания=edition.год_издания,
        тираж_издания=edition.тираж_издания,
        издательство=edition.издательство
    )
    db.add(new_edition)
    await db.commit()
    await db.refresh(new_edition)
    return new_edition

###########################################################################
#                                 ЖАНРЫ                                   #
###########################################################################

@app.get("/genres")
async def get_genres(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Genre))
    genres = result.scalars().all()
    return [{"id_жанра": g.id_жанра, "жанр": g.жанр} for g in genres]

###########################################################################
#                                СТРАНЫ                                   #
###########################################################################

@app.get("/countries")
async def get_countries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country))
    countries = result.scalars().all()
    return [{"id_страны": c.id_страны, "название_страны": c.название_страны} for c in countries]

###########################################################################
#                               СТАТИСТИКА                                #
###########################################################################

@app.get("/authors/popular")
async def popular_authors(limit: int = 5, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(
            Writer.id_писателя,
            Writer.фамилия,
            Writer.имя,
            func.sum(Edition.тираж_издания).label("total_circulation")
        )
        .join(WriterWork, Writer.id_писателя == WriterWork.id_писателя)
        .join(Work, WriterWork.id_произведения == Work.id_произведения)
        .join(Edition, Work.id_произведения == Edition.id_произведения)
        .group_by(Writer.id_писателя)
        .order_by(func.sum(Edition.тираж_издания).desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    authors = result.all()
    return [
        {
            "id": a[0],
            "фамилия": a[1],
            "имя": a[2],
            "total_circulation": a[3] or 0
        }
        for a in authors
    ]

@app.get("/editions/statistics")
async def editions_by_year(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Edition.год_издания, func.sum(Edition.тираж_издания).label("total_circulation"))
        .where(Edition.год_издания.isnot(None))
        .group_by(Edition.год_издания)
        .order_by(Edition.год_издания)
    )
    stats = [{"year": row[0], "total_circulation": row[1]} for row in result.all()]
    return stats
