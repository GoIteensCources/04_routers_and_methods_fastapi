from fastapi import FastAPI, HTTPException, status, Query, Path
import uvicorn

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "Brave New World", "author": "Aldous Huxley"},
    {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee"}
]

app = FastAPI()


@app.get('/books')
async def all_books():
    return {"library": books}


@app.get('/books/{book_id}')
async def get_book_by_id(book_id: int, requests):
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        return {"book": book}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Book with id {book_id} not found")


@app.post("/books/{book_id}", status_code=status.HTTP_201_CREATED)
async def create_item(book_id: int = Path(gt=max([i["id"] for i in books])),
                      title: str = Query(description="enter title of book"),
                      author: str = Query(description="enter author of book")):
    book = {"id": book_id, "title": title, "author": author}
    books.append(book)
    return {"new book": book}


@app.put("/books/{book_id}", status_code=status.HTTP_201_CREATED)
async def create_item(book_id: int = Path(gt=max([i["id"] for i in books])),
                      title: str = Query(description="enter title of book"),
                      author: str = Query(description="enter author of book")):
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        book["title"] = title
        book["author"] = author
    return {f"book {book_id} updated": book}


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(book_id: int):
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        books.remove(book)
        return {"book is deleted": book}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Book with id {book_id} not found")


if __name__ == '__main__':
    uvicorn.run("__main__:app", reload=True)
