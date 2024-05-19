from fastapi import FastAPI
from server.routes.student import router as StudentRouter

app = FastAPI()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to your new API"}


app.include_router(StudentRouter, tags=["Student"], prefix="/student")
