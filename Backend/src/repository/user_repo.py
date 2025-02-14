from bson import ObjectId

from ..helpers.returnTypes import Failure, Success
from ..infra.models.user import UserModel


async def register_user(user: UserModel, db):
    try:
        col = db["user_test_col"]
        result = col.insert_one(user.model_dump(by_alias=True, exclude=["id"]))

        return Success(code=201, data=str(result.inserted_id))

    except Exception as exc:
        print("ERROR: ", exc)
        return Failure(code=400, data="Some error")


async def get_user_by_name(user_name: str, db):
    try:
        col = db["user_test_col"]
        result = col.find_one({"name": user_name})

        if result == None:
            return Failure(code=404, data="Could not find the user")

        return result

    except Exception as exc:
        print("ERROR: ", exc)
        return Failure(code=400, data="Some error")
