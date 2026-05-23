from fastapi import FastAPI,Body

app =FastAPI()

BOOKS = [
    {'title':'Title One','author':'Author one','category':'Maths'},
    {'title':'Title Two','author':'Author Two','category':'Maths'},
    {'title':'Title Three','author':'Author Two','category':'Maths'},
    {'title':'Title Four','author':'Author Three','category':'Literature'},
    {'title':'Title Five','author':'Author Two','category':'Maths'},
    {'title':'Title Six','author':'Author Five','category':'Urdu'},
]

@app.get("/books")
async def get_all_books():
    return BOOKS

@app.get('/books/author_by')
async def book_author_categories(author_by:str):
    filtered = []
    for book in BOOKS:
        if book.get('author').casefold() == author_by.casefold():
            filtered.append(book)
    
    return filtered

# @app.get("/books/{dynamic_param}")
# async def get_param(dynamic_param:str):
#     return {dynamic_param + " this was the Url"}


# -----   Dynamic params -> Of obj ------ 

# @app.get("/books/{book_title}")
# async def get_spec_book(book_title:str):
#     for book in BOOKS:
#         if book.get('title').casefold()==book_title.casefold():
#             return book
        
#     return{book_title : 'Not found'}

@app.get('/books/{author}')
async def get_spec_books(author:str):
    all_books=[]
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            all_books.append(book)
    
    return all_books




# ---- Query params with path params

@app.get('/books/category/{author}')
async def author_category(author : str , category:str):
    books_to_return = []
    for books in BOOKS:
        if books.get('author').casefold()==author.casefold() and books.get('category').casefold() == category.casefold():
            books_to_return.append(books)
    if len(books_to_return) > 0:
        return books_to_return  
    return f"No {author} books found in category of {category}"



@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    print(BOOKS) 


@app.put('/books/update_book')
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            return BOOKS
        

@app.delete('/books/delete_book/{book_title}')
async def delete_book(book_title : str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            return BOOKS
    
    return 'No such item in dict'
    
    
    
