from fastapi import APIRouter, Depends

from ..helpers.generalHelpers import generateCode
from ..helpers.returnTypes import Failure, Success
from ..infra.database import get_test_db
from ..infra.models.group import GroupModel
from ..infra.models.user import UserForGroup, UserModel
from ..repository.groups import add_user_to_group_repo, create_group_repo, find_by_code

groups_router = APIRouter()


@groups_router.post("/new_group")
async def create_group(group: GroupModel, db=Depends(get_test_db)) -> Success | Failure:

    group.code = generateCode()

    return await create_group_repo(group=group, db=db)


@groups_router.get(
    "/find_group",
    response_model_by_alias=False,
)
async def find_group_by_code(
    group_code: str, db=Depends(get_test_db)
) -> GroupModel | Failure:

    result = await find_by_code(code=group_code, db=db)

    if isinstance(result, Failure):
        return result

    return result.data


# TODO: Change to recieve the user ID instead of the whole user
@groups_router.post("/subscribe")
async def add_user_to_group(
    group_code: str, user: UserForGroup, db=Depends(get_test_db)
) -> Success | Failure:

    group: Success | Failure = await find_by_code(code=group_code, db=db)

    if isinstance(group, Failure):
        return group

    result = await add_user_to_group_repo(group_id=group.data["_id"], user=user, db=db)

    return result
