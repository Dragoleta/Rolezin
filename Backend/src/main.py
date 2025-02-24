from fastapi import Body, Depends, FastAPI

from .context.groups_context import groups_router
from .context.user_context import user_router
from .helpers.returnTypes import Success
from .infra.database import get_test_db
from .infra.models.group import GroupModel

app = FastAPI()

app.include_router(groups_router)
app.include_router(user_router)


@app.get("/")
async def health(
    db=Depends(get_test_db),
):
    return Success(code=200, data="Server is fine")
