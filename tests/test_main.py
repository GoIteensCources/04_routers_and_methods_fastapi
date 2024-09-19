from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "Brave New World", "author": "Aldous Huxley"},
    {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee"}
]


def test_all_books():
    resp = client.get('/books')
    assert resp.status_code == 200
    assert resp.json() == {
        "library": books
    }


def test_get_book_by_id():
    resp = client.get("/books/2")
    assert resp.status_code == 200
    assert resp.json() == {
        "book": {"id": 2, "title": "Brave New World", "author": "Aldous Huxley"},
    }


def test_get_book_by_id_exception():
    resp = client.get("/books/10")
    assert resp.status_code == 400
    assert resp.json() == {
        "detail": f"Book with id 10 not found"
    }


def test_create_book():
    book_id = 4
    title = "Clear Code"
    author = "R.Martin"

    resp = client.post(f"/books/{book_id}",
                       params={"title": title, "author": author}
                       )
    assert resp.status_code == 201
    assert resp.json() == {
        "new book": {"id": book_id, "title": title, "author": author},
    }


def test_delete_book():
    resp = client.delete(f"/books/3")
    assert resp.status_code == 204
