from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/post")
def read_post():
    return {"data":"This is your post"}