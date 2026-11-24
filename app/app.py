from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""), # receiving caption as form data, can be of many other types
    session: AsyncSession = Depends(get_async_session) 
    # dependency injection - get_async_session will be the dependency as it allows access to db
):
    post = Post(
        caption=caption,
        url="dummyurl",
        file_type="photo",
        file_name="dummy name"
    )
    session.add(post) # staging basically
    await session.commit() # !!!
    await session.refresh(post)
    return post # not needed though


    