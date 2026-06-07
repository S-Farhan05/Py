from fastapi import Body, FastAPI, Path,Query,HTTPException
from validation import Book_Request
from starlette import status

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

@app.get('/books',status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS

@app.get('/books/',status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating : int = Query(gt=0,lt=6)):
    book_ratings = []
    for book in BOOKS:
        if book.rating == rating:
            book_ratings.append(book)
    
    return book_ratings

@app.get('/books/{book_id}',status_code=status.HTTP_200_OK)
async def get_books_by_id(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
        
    raise HTTPException(status_code=404,detail="Book not found")

@app.get('/books/publish/{published_date}',status_code=status.HTTP_200_OK)
async def get_books_by_published_date(published_date:int=Path(gt=1000,lt=2027)):
    books_by_date=[]
    for i in range(len(BOOKS)):
        if BOOKS[i].published_date == published_date:
            books_by_date.append(BOOKS[i])
    return books_by_date

# @app.post('/create_book')
# async def create_book(new_book = Body()):
#     BOOKS.append(new_book)

@app.post('/books/create_book',status_code=status.HTTP_201_CREATED)
async def create_book(new_book : Book_Request):
    book = Book(**new_book.model_dump())
    #model_dump -> Make a json object validation to a dict , ** unpacks dict to pass as parameters Book(id=1,name='burger) 
    print(type(book))
    BOOKS.append(find_book_id(book))


@app.put('/books/update_book',status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:Book_Request):
    book_update=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.model_dump())
            # book.dict()
            # return 200
            book_update=True

    if not book_update:
        raise HTTPException(status_code=404,detail="No book found")



@app.delete('/books/delete_book',status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id :int=Query(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return f"Book successfully deleted with id -> {book_id}"
        
    raise HTTPException(status_code=404,detail="No book found to delete with that id")

def find_book_id(book:Book):

    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    
    # else:
    #     book.id = 1

    # Whole book new created passed we reassign its id value
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

