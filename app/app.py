from fastapi import FastAPI, HTTPException

app = FastAPI()

# dictionaries work similar to json objects

# @app.get("/hello-world")

# def hello_word():
#     return {"message": "Hello World"}

text_posts = {
    1: {"title": "New Post", "content": "cool test post"},
    1: {"title": "Second Post", "content": "cool test post"},
    1: {"title": "Third Post", "content": "cool test post"},
    1: {"title": "Forth Post", "content": "cool test post"},
    1: {"title": "Fifth Post", "content": "cool test post"}
}

# specify type parameters such as limit: int = None, content_length: int
# python type hint, must specify the type so fastapi can validate the data going into and coming out of the function

@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
        # return text_posts[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)

