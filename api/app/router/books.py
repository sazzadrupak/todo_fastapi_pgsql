"""
URL mappings for the books
"""

from fastapi import APIRouter, Path, Query, HTTPException
from starlette import status

from app.schemas.books import BookRequest


router = APIRouter(
    prefix='/books',
    tags=['books']
)


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


BOOKS = [
    Book(1, 'Title One', 'Author one', 'science', 1, 2000),
    Book(2, 'Title two', 'Author two', 'science', 2, 2020),
    Book(3, 'Title three', 'Author three', 'history', 3, 2021),
    Book(4, 'Title four', 'Author four', 'math', 4, 2022),
    Book(5, 'Title five', 'Author five', 'math', 5, 2023),
    Book(6, 'Title six', 'Author six', 'math', 5, 2024)
]


@router.get(
    "/",
    summary="Retrieve all books",
    description="This API call simulates fetching all books",
    response_description="The list of available books",
    status_code=status.HTTP_200_OK
)
def index():
    '''Return all books'''
    return BOOKS


@router.get(
    '/{book_id}',
    status_code=status.HTTP_200_OK
)
async def get_book_by_id(book_id: int = Path(gt=0)):
    '''Return a book by id'''
    book = list(filter(lambda obj: obj.id == book_id, BOOKS))
    if len(book) == 0:
        raise HTTPException(status_code=404, detail='Item not found')
    return book[0]


@router.get('/')
async def read_books_by_publish_date(publish_date: int = Query(gt=1999, lt=2031)):
    '''Get books by publish date and return'''
    print(publish_date)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    '''Create new book'''
    new_book = Book(**book_request.model_dump())
    print(new_book)


@router.put('/', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    '''Update a book'''
    print(book)


@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    '''Delete a book'''
    print(book_id)
