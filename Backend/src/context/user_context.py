from fastapi import APIRouter, Depends

from ..helpers.authHelpres import check_user_token, generate_token
from ..helpers.encryptionHelper import hash_password, verify_password
from ..helpers.returnTypes import Failure, Success
from ..infra.database import get_test_db
from ..infra.models.group import GroupModel
from ..infra.models.user import UserAuth, UserModel
from ..repository.user_repo import get_user_by_name, register_user

user_router = APIRouter()


@user_router.post("/register")
async def create_user(user: UserModel, db=Depends(get_test_db)) -> Success | Failure:

    user.password = hash_password(user.password)
    result = await register_user(user=user, db=db)

    return result


@user_router.post("/login")
async def user_login(auth: UserAuth, db=Depends(get_test_db)):

    user: UserModel = await get_user_by_name(user_name=auth.name, db=db)

    if not user:
        return Failure(code=404, data="User not found")

    is_user = verify_password(
        plain_password=auth.password, hashed_password=user["password"]
    )

    if not is_user:
        return Failure(code=404, data="Incorrect Data")

    jwt_token = await generate_token(user_id=str(user["_id"]), user_name=user["name"])

    return jwt_token


@user_router.get("/info")
async def user_info(user_name: str, db=Depends(get_test_db)) -> UserModel | Failure:

    result = await get_user_by_name(user_name=user_name, db=db)

    return result


@user_router.get("/info_polished")
async def user_info_polished(db=Depends(get_test_db)):
    pass


@user_router.put("/update_calendar")
async def update_user_calendar(db=Depends(get_test_db)):
    pass


@user_router.put("/update")
async def update_user_info(db=Depends(get_test_db)):
    pass
