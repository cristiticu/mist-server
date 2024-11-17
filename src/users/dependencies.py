from typing import Annotated
from fastapi import Depends

from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from users.model import UserTokenData
from exceptions import CredentialsException
from shared import utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth")


def user_token_data(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = utils.decode_access_token(token)
        user_id = payload.get("id")

        if user_id is None:
            raise CredentialsException()
    except InvalidTokenError:
        raise CredentialsException()

    return UserTokenData(id=user_id)
