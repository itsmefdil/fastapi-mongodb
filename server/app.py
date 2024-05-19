from fastapi import FastAPI
from server.routes.book import router as BookRouter

app = FastAPI()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to your new API"}


app.include_router(BookRouter, tags=["Book"], prefix="/book")
