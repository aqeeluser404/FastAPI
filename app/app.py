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
    try:
        # create temp file, if a user uploads jpeg, we create a temp jpeg
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]
        ) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        # upload file
        with open(temp_file_path, "rb") as f:
            upload_result = imageKit.files.upload(
                file=f,
                file_name=file.filename,
                use_unique_file_name=True,
                tags=["backend-upload"],
            )

        post = Post(
            caption=caption,
            url=upload_result.url,
            file_type="video" if file.content_type.startswith("video/") else "image",
            file_name=upload_result.name,
        )
        session.add(post)  # staging basically
        await session.commit()  # !!!
        await session.refresh(post)
        return post

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()

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
    
    