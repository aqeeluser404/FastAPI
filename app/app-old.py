from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse

app = FastAPI()

# dictionaries work similar to json objects
text_posts = {
    1: {"title": "New Post", "content": "cool test post"},
    2: {"title": "Second Post", "content": "cool test post"},
    3: {"title": "Third Post", "content": "cool test post"},
    4: {"title": "Forth Post", "content": "cool test post"},
    5: {"title": "Fifth Post", "content": "cool test post"}
}

# specify type parameters such as limit: int = None, content_length: int
# python type hint, must specify the type so fastapi can validate the data going into and coming out of the function

@app.get("/hello-world")
def hello_word():
    return {"message": "Hello World"}

@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
        # return text_posts[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int) -> PostResponse:
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)

# request body for posts
# indicating the type after -> tells FastAPI the type that will be returned

@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post