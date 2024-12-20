from typing import Annotated
from fastapi import APIRouter, Depends

from games.model import Game
from licenses.model import LicensePatch
from users.dependencies import user_token_data
from users.model import UserTokenData

from context import ApplicationContext


router = APIRouter(prefix="/license", tags=["license"])
application_context = ApplicationContext()


@router.get("")
def list_licenses(user: Annotated[UserTokenData, Depends(user_token_data)]):
    return application_context.licenses.get_all_for_user(user_id=user.id)


@router.post("")
def create_license(game_id: str, user: Annotated[UserTokenData, Depends(user_token_data)]):
    return application_context.licenses.create(game_id=game_id, user_id=user.id)


@router.get("/{game_id}")
def get_license_for_game(game_id: str, user: Annotated[UserTokenData, Depends(user_token_data)]):
    return application_context.licenses.get_by_data(user_id=user.id, game_id=game_id)


@router.patch("/{game_id}")
def update_license(game_id: str, license_patch: LicensePatch, user: Annotated[UserTokenData, Depends(user_token_data)]):
    license = application_context.licenses.get_by_data(
        user_id=user.id, game_id=game_id)

    return application_context.licenses.update(id=license.id, patch=license_patch)


@router.get("/aggregate/owned-games")
def list_owned_games(user: Annotated[UserTokenData, Depends(user_token_data)]):
    licenses = application_context.licenses.get_all_for_user(
        user_id=user.id)
    owned_games = application_context.games.get_many(
        ids=[license.game_id for license in licenses])

    patched_games = [Game(**{**owned_game.model_dump(), "image_src": licenses[index].custom_image_src or owned_game.image_src})
                     for index, owned_game in enumerate(owned_games)]

    return patched_games
