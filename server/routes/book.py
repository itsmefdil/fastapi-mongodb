from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder


from server.database import (
    add_book,
    delete_book,
    retrieve_book,
    retrieve_books,
    update_book,
)


from server.models.book import (
    ErrorResponseModel,
    ResponseModel,
    BookSchema,
    UpdateBookModel,
)

router = APIRouter()


@router.post("/", response_description="Book data added into the database")
async def add_book_data(book: BookSchema = Body(...)):
    book = jsonable_encoder(book)
    new_book = await add_book(book)
    return ResponseModel(new_book, "book added Successfully")


@router.get("/", response_description="Book retrieved")
async def get_book():
    book = await retrieve_books()
    if book:
        return ResponseModel(book, "Book data retrieved successfully")
    return ResponseModel(book, "Empty list returned")


@router.get("/{id}", response_description="Book data retrieved")
async def get_book_data(id):
    book = await retrieve_book(id)
    if book:
        return ResponseModel(book, "Book data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "book doesn't exist.")


@router.put("/{id}", response_description="Book data updated")
async def update_book_data(id: str, req: UpdateBookModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_book = await update_book(id, req)
    if updated_book:
        return ResponseModel(
            "book with ID: {} update is successful".format(id),
            "book name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the book data.",
    )
