import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Annotated
from sqlalchemy import String, Integer, select
from pydantic import BaseModel

app = FastAPI()

# Database
engine = create_async_engine("sqlite+aiosqlite:///db.sqlite", future=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    async with new_session() as session:
        yield session


# Base class
class Base(DeclarativeBase):
    pass


# ORM model
class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))


SessionDep = Annotated[AsyncSession, Depends(get_db)]


# Pydantic schemas
class BookAddSchema(BaseModel):
    title: str
    author: str


class BookSchema(BookAddSchema):
    id: int

    class Config:
        orm_mode = True


# Setup database
@app.post("/setup_db")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}


# Create
@app.post("/books", response_model=BookSchema)
async def create_book(data: BookAddSchema, session: SessionDep):
    new_book = Book(title=data.title, author=data.author)
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book


# Read all
@app.get("/books", response_model=list[BookSchema])
async def get_books(session: SessionDep):
    result = await session.execute(select(Book))
    return result.scalars().all()


# Read one
@app.get("/books/{id}", response_model=BookSchema)
async def get_book(id: int, session: SessionDep):
    result = await session.execute(select(Book).where(Book.id == id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# Delete
@app.delete("/books/{id}")
async def delete_book(id: int, session: SessionDep):
    result = await session.execute(select(Book).where(Book.id == id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    await session.delete(book)
    await session.commit()
    return {"ok": True}


# Update (PUT)
@app.put("/books/{id}", response_model=BookSchema)
async def update_book(id: int, data: BookAddSchema, session: SessionDep):
    result = await session.execute(select(Book).where(Book.id == id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = data.title
    book.author = data.author

    await session.commit()
    await session.refresh(book)
    return book


# Partial update (PATCH)
@app.patch("/books/{id}", response_model=BookSchema)
async def patch_book(id: int, data: BookAddSchema, session: SessionDep):
    result = await session.execute(select(Book).where(Book.id == id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if data.title:
        book.title = data.title
    if data.author:
        book.author = data.author

    await session.commit()
    await session.refresh(book)
    return book


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
