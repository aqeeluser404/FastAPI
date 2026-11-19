import uvicorn
# host is the domain, 0.0.0.0 is the localhost, 
# anyone can access on local environment

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)
    
# http://127.0.0.1:8000/hello-world
# http://localhost:8000/hello-world