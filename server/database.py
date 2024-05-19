import motor.motor_asyncio
from bson.objectid import ObjectId
from dotenv import dotenv_values

config = dotenv_values(".env")

MONGO_HOST = config["MONGO_HOST"]
MONGO_PORT = config["MONGO_PORT"]
MONGO_USER = config["MONGO_USER"]
MONGO_PASS = config["MONGO_PASS"]
MONGO_COLLECTION = config["MONGO_COLLECTION"]
MONGO_DB = config["MONGO_DB"]

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

database = client[MONGO_DB]

book_collection = database.get_collection(MONGO_COLLECTION)


# helper
def book_helper(book) -> dict:
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "year": book["year"],
    }


# Retrieve all book present in the database
async def retrieve_books():
    books = []
    async for book in book_collection.find():
        books.append(book_helper(book))
    return books


# Add a new book into to the database
async def add_book(book_data: dict) -> dict:
    book = await book_collection.insert_one(book_data)
    new_book = await book_collection.find_one({"_id": book.inserted_id})
    return book_helper(new_book)


# Retrieve a book with a matching ID
async def retrieve_book(id: str) -> dict:
    book = await book_collection.find_one({"_id": ObjectId(id)})
    if book:
        return book_helper(book)


# Update a book with a matching ID
async def update_book(id: str, data: dict):
    if len(data) < 1:
        return false
    book = await book_collection.find_one({"_id": ObjectId(id)})
    if book:
        update_book = await book_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if update_book:
            return True
        return False


async def delete_book(id: str):
    book = await book_collection.find_one({"_id": ObjectId(id)})
    if book:
        await book_collection.delete_one({"_id": ObjectId(id)})
        return True
