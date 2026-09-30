from fastapi import FastAPI
import models
from database import Engine

from router import auth , todos ,admin ,users

app =FastAPI()

# models.Base.metadata.create_all(bind=Engine)

@app.get('/health')
async def get_backend_health():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

