from typing import Annotated
from fastapi import APIRouter, Depends

from users.dependencies import user_token_data
from users.model import UserTokenData

from context import ApplicationContext


router = APIRouter(prefix="/license", tags=["license"])
application_context = ApplicationContext()


@router.get("")
def list_licenses(user: Annotated[UserTokenData, Depends(user_token_data)]):
    return application_context.licenses.get_all_for_user(
        user_id=user.id)


@router.post("")
def create_user_license(game_id: str, user: Annotated[UserTokenData, Depends(user_token_data)]):
    return application_context.licenses.create(game_id=game_id, user_id=user.id)
