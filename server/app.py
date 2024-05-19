from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to your new API"}
