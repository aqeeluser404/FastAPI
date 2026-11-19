from fastapi import FastAPI

app = FastAPI()

# dictionaries work similar to json objects

@app.get("/hello-world")

def hello_word():
    return {"message": "Hello World"}
