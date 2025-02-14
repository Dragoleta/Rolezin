from bson import ObjectId

from ..helpers.returnTypes import Failure, Success
from ..infra.models.group import GroupModel
from ..infra.models.user import UserForGroup


async def create_group_repo(group: GroupModel, db):
    try:
        col = db["test_col"]

        result = col.insert_one(group.model_dump(by_alias=True, exclude=["id"]))

        return Success(code=201, data=str(result.inserted_id))
    except Exception as exc:
        print("ERROR: ", exc)
        return Failure(code=400, data="Some error")


async def find_by_code(code: str, db) -> Success | Failure:
    try:
        col = db["test_col"]
        result: GroupModel = col.find_one({"code": code})

        if result == None:
            return Failure(code=404, data="Could not find the group")

        return Success(code=200, data=result)

    except Exception as exc:
        return Failure(code=404, data="Could not find the group")


async def add_user_to_group_repo(group_id: str, user: UserForGroup, db):
    try:
        col = db["test_col"]

        user = user.model_dump(by_alias=True)

        result = col.update_one(
            {"_id": group_id},
            {
                "$push": {"participants": user},
            },
        )
        return Success(code=201, data="Okay!")

    except Exception as exc:
        print("ERROR: ", exc)
        return Failure(code=405, data="Could not add user to the group")
