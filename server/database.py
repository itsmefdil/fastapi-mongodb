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

student_collection = database.get_collection(MONGO_COLLECTION)


# helper
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
    }


# Retrieve all students present in the database
async def retrieve_students():
    students: []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students


# Add a new student into to the database
async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


# Retrieve a student with a matching ID
async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


# Update a student with a matching ID
async def update_student(id: str, data: dict):
    if len(data) < 1:
        return false
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        update_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if update_student:
            return True
        return False


async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True
