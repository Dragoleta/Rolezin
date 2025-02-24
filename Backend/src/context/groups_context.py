from fastapi import APIRouter, Depends

from ..helpers.generalHelpers import generateCode
from ..helpers.returnTypes import Failure, Success
from ..infra.database import get_test_db
from ..infra.models.group import GroupModel
from ..infra.models.user import UserForGroup, UserModel
from ..repository.groups import add_user_to_group_repo, create_group_repo, find_by_code
from ..repository.user_repo import get_user_by_id

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
    group_code: str,
    db=Depends(get_test_db),
) -> GroupModel | Failure:

    result = await find_by_code(code=group_code, db=db)

    if isinstance(result, Failure):
        return result

    return result.data


@groups_router.post("/subscribe")
async def add_user_to_group(
    group_code: str,
    user_id: str,
    db=Depends(get_test_db),
) -> Success | Failure:

    if not group_code and not user_id:
        return Failure(code=404, data="Must have user id and group code")

    group: Success | Failure = await find_by_code(code=group_code, db=db)

    if isinstance(group, Failure):
        return group

    user: UserModel | Failure = await get_user_by_id(user_id=user_id, db=db)

    if isinstance(user, Failure):
        return user

    user_for_group = UserForGroup(
        id=user["_id"],
        name=user["name"],
        calendar=user["calendar"],
        preferences=user["preferences"],
    )

    assert isinstance(
        user_for_group, UserForGroup
    ), "User must be UserForGroup before adding to the group"

    result = await add_user_to_group_repo(
        group_id=group.data["_id"],
        user=user_for_group,
        db=db,
    )

    return result
