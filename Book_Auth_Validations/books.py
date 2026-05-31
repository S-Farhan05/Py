from fastapi import Body, FastAPI
from validation import Book_Request

app = FastAPI()

class Book:
    id : int
    name :str
    description:str
    rating:int
    is_read:bool
    published_date:int

    def __init__(self,id,name,description,rating,is_read,published_date):
        self.id = id
        self.name=name
        self.description=description
        self.rating=rating
        self.is_read=is_read
        self.published_date=published_date

BOOKS = [
    Book(1,'Harry potter','A wonderful book',3.8,False,2012),
    Book(2,'Fast api ','Best features for backend studies',5,False,2020),
    Book(3,'Backend systems','System design fundamentals',5,True,1998),
    Book(4,'Jack and beanstalks','A FairyTale',3.8,False,2009),
    Book(5,'Ed 1','Series book 1',5,True,2012),
    Book(6,'Ed 2','Series book 2',2,False,2015),
    Book(7,'Ed 3','Series book 3',3.4,False,2020),
]

@app.get('/books')
async def get_books():
    return BOOKS

@app.get('/books/')
async def get_books_by_rating(rating : int):
    book_ratings = []
    for book in BOOKS:
        if book.rating == rating:
            book_ratings.append(book)
    
    return book_ratings

@app.get('/books/{book_id}')
async def get_books_by_id(book_id:int):
    for book in BOOKS:
        if book.id == book_id:
            return book

@app.get('/books/publish/{published_date}')
async def get_books_by_published_date(published_date:int):
    books_by_date=[]
    for i in range(len(BOOKS)):
        if BOOKS[i].published_date == published_date:
            books_by_date.append(BOOKS[i])
    return books_by_date

# @app.post('/create_book')
# async def create_book(new_book = Body()):
#     BOOKS.append(new_book)

@app.post('/books/create_book')
async def create_book(new_book : Book_Request):
    book = Book(**new_book.model_dump())
    #model_dump -> Make a json object validation to a dict , ** unpacks dict to pass as parameters Book(id=1,name='burger) 
    print(type(book))
    BOOKS.append(find_book_id(book))


@app.put('/books/update_book')
async def update_book(book:Book_Request):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.model_dump())
            # book.dict()
            return 200
    return "No such values found"


@app.delete('/books/delete_book')
async def delete_book(book_id : int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return
        
    return "No such book with id found"

def find_book_id(book:Book):

    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    
    # else:
    #     book.id = 1

    # Whole book new created passed we reassign its id value
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

