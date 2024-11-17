from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from context import ApplicationContext
from shared import utils
from users.dependencies import user_token_data
from users.model import UserTokenData

router = APIRouter(prefix="/user", tags=["user"])
application_context = ApplicationContext()


@router.post("/auth")
async def authenticate(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]):
    user = application_context.users.get_by_credentials(
        username=form_data.username, password=form_data.password)

    token = utils.create_access_token({"id": user.id})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"access_token": token, "token_type": "bearer"}
                        )


@router.get("/")
def list_users(_: Annotated[UserTokenData, Depends(user_token_data)]):
    return application_context.users.get_all()


@router.get("/{user_id}")
def get_user(user_id: str, _: Annotated[UserTokenData, Depends(user_token_data)]):
    return application_context.users.get(id=user_id)
