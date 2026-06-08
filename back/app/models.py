from sqlalchemy import Column, BigInteger, Integer, SmallInteger, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from .database import Base


class Country(Base):
    __tablename__ = "страны"
    __table_args__ = {"schema": "novelists"}
    id_страны = Column(Integer, primary_key=True)
    название_страны = Column(String(120), nullable=False)


class Genre(Base):
    __tablename__ = "жанры"
    __table_args__ = {"schema": "novelists"}
    id_жанра = Column(Integer, primary_key=True)
    жанр = Column(String(34), nullable=False, unique=True)


class Writer(Base):
    __tablename__ = "писатели"
    __table_args__ = {"schema": "novelists"}
    id_писателя = Column(BigInteger, primary_key=True)
    фамилия = Column(String(34))
    имя = Column(String(34), nullable=False)
    отчество = Column(String(34))
    год_рождения = Column(SmallInteger)
    год_смерти = Column(SmallInteger)
    id_страны_рождения = Column(Integer, ForeignKey("novelists.страны.id_страны"))
    country = relationship("Country")


class Work(Base):
    __tablename__ = "произведения"
    __table_args__ = {"schema": "novelists"}
    id_произведения = Column(BigInteger, primary_key=True)
    id_жанра = Column(Integer, ForeignKey("novelists.жанры.id_жанра"))
    год_написания = Column(SmallInteger)
    название_произведения = Column(String(200), nullable=False)
    где_хранится_оригинал = Column(BigInteger)
    genre = relationship("Genre")


class Edition(Base):
    __tablename__ = "издания"
    __table_args__ = {"schema": "novelists"}

    id_издания = Column(BigInteger, primary_key=True)
    год_издания = Column(SmallInteger)
    страна_где_издавалось = Column(Integer, ForeignKey("novelists.страны.id_страны"))
    тираж_издания = Column(BigInteger, default=0)
    id_произведения = Column(BigInteger, ForeignKey("novelists.произведения.id_произведения"), nullable=False)
    издательство = Column(String(100))
    work = relationship("Work")
    country = relationship("Country")


class WriterWork(Base):
    __tablename__ = "писатель_произведение"
    __table_args__ = (
        PrimaryKeyConstraint("id_писателя", "id_произведения"),
        {"schema": "novelists"}
    )
    id_писателя = Column(BigInteger, ForeignKey("novelists.писатели.id_писателя"))
    id_произведения = Column(BigInteger, ForeignKey("novelists.произведения.id_произведения"))

    writer = relationship("Writer")
    work = relationship("Work")