from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jwt import InvalidTokenError, ExpiredSignatureError

from users.model import UserTokenData
from exceptions import CredentialsException
from shared import utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth")


def user_token_data(token: Annotated[str, Depends(oauth2_scheme)]) -> UserTokenData:
    try:
        payload = utils.decode_access_token(token)
        user_id = payload.get("id")

        if user_id is None:
            raise CredentialsException()

    except ExpiredSignatureError:
        raise CredentialsException(msg="Expired signature")
    except InvalidTokenError:
        raise CredentialsException(msg="Corrupt signature")

    return UserTokenData(raw_token=token, id=user_id)


def user_token_query(token: str) -> UserTokenData:
    try:
        payload = utils.decode_access_token(token)
        user_id = payload.get("id")

        if user_id is None:
            raise CredentialsException()

    except ExpiredSignatureError:
        raise CredentialsException(msg="Expired signature")
    except InvalidTokenError:
        raise CredentialsException(msg="Corrupt signature")

    return UserTokenData(raw_token=token, id=user_id)
