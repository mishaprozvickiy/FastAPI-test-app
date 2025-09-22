from fastapi import FastAPI, HTTPException, Response, Path, Body
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel, Field, ConfigDict, EmailStr

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

books = [
    {
        "id": 1,
        "title": "Асинхронность в python",
        "author": "Мэттью"
    },
    {
        "id": 2,
        "title": "Backend разработка в python",
        "author": "Артём"
    }
]


class NewBook(BaseModel):
    title: str = Field(max_length=100)
    author: str = Field(max_length=50)


@app.get("/books", tags=["Книги"], summary="Считывание всех книг")
def read_books():
    return books

@app.get("/books/{book_id}", tags=["Книги"], summary="Получить книгу по id")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=404, detail=f"Не смогли найти книгу с id = {book_id}")

@app.post("/books", tags=["Книги"], summary="Добавление книги")
def create_book(new_book: NewBook):
    books.append({
        "id": len(books) + 1,
        "title": new_book.title,
        "author": new_book.author
    })

    return {"status": "ok", "message": "книга успешно добавлена"}

@app.get("/", summary="Главная ручка", tags=["Основные ручки"])
def root():
    return "Hello, world!"

@app.get("/test")
def test():
    html_content = "<h2>Hello, World!</h2>"
    return HTMLResponse(content=html_content)

@app.get("/test2")
def test2():
    data = {"message": "Hello, World!"}
    json_data = jsonable_encoder(data)
    return JSONResponse(content=json_data)

@app.get("/test3")
def test3():
    return JSONResponse(content={"message": "Hello, World!"})

@app.get("/test4", response_class=HTMLResponse)
def test4():
    return "<h2>Hello, World!</h2>"

@app.get("/test5")
def test5():
    return "<h2>Hello, World!</h2>"

@app.get("/test6")
def test6(name):
    return {"message": f"Hello, {name}!"}

if __name__ == "__main__":
    uvicorn.run("fastAPI_app:app", reload=True)