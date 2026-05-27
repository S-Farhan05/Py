from fastapi import Body, FastAPI
from validation import Book_Request

app = FastAPI()

class Book:
    id : int
    name :str
    description:str
    rating:int
    is_read:bool

    def __init__(self,id,name,description,rating,is_read):
        self.id = id
        self.name=name
        self.description=description
        self.rating=rating
        self.is_read=is_read


BOOKS = [
    Book(1,'Harry potter','A wonderful book',3.8,False),
    Book(2,'Fast api ','Best features for backend studies',5,False),
    Book(3,'Backend systems','System design fundamentals',5,True),
    Book(4,'Jack and beanstalks','A FairyTale',3.8,False),
    Book(5,'Ed 1','Series book 1',5,True),
    Book(6,'Ed 2','Series book 2',2,False),
    Book(7,'Ed 3','Series book 3',3.4,False),
]

@app.get('/books')
async def get_books():
    return BOOKS

@app.get('/books/')
async def get_books_by_rating(rating : int):
    book_ratings = [
    ]
    for book in BOOKS:
        if book.rating == rating:
            book_ratings.append(book)
    
    return book_ratings

@app.get('/books/{book_id}')
async def get_books_by_id(book_id:int):
    for book in BOOKS:
        if book.id == book_id:
            return book

# @app.post('/create_book')
# async def create_book(new_book = Body()):
#     BOOKS.append(new_book)

@app.post('/create_book')
async def create_book(new_book : Book_Request):
    book = Book(**new_book.model_dump())
    #model_dump -> Make a json object validation to a dict , ** unpacks dict to pass as parameters Book(id=1,name='burger) 
    print(type(book))
    BOOKS.append(find_book_id(book))


def find_book_id(book:Book):

    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    
    # else:
    #     book.id = 1

    # Whole book new created passed we reassign its id value
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

