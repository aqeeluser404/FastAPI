from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imageKit
# from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import uuid
import tempfile

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
    temp_file_path = None
    # try:
    #     # create temp file, if a user uploads jpeg, we create a temp jpeg
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splittext(file.filename)[1]) as temp_file:
    #         temp_file_path = temp_file.name
    #         shutil.copyfileobj(file.file, temp_file)
            
    #     upload_result = imageKit.upload_file(
    #         file=open(temp_file_path, "rb")
    #         file_name=file.filename,
    #         options=UploadFileRequestOptions(
    #             use_unique_file_name=True,
    #             tags=["backend-upload"]
    #         )
    #     )
            
        
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

@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session) 
):
    # select and get them in the order they were created
    # await session.execute(select(Post).order_by(Post.created_at.desc()).filter_by())
    # result = await session.execute(select(Post))
    # look up sqlalchemy for various ways to select data
    
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()] 
    # converts them into a list, 
    # FastAPI returns them as a cursor object where you stepping through the database
    # so a list allows us to loop through the values and storing them
    
    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()
            }
        )
    return {"posts": posts_data}
    
    