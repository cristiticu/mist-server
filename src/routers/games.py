from fastapi import APIRouter, HTTPException, status
from context import ApplicationContext
from games.exceptions import GameNotFound


router = APIRouter(prefix="/game", tags=["game"])
application_context = ApplicationContext()


@router.get("")
def list_games(offset: int | None = None, limit: int | None = None):
    if not limit:
        return application_context.games.get_all()

    if not offset:
        offset = 0

    return application_context.games.get_page(offset=offset, limit=limit)


@router.get("/{game_id}")
def get_game(game_id: str):
    return application_context.games.get(id=game_id)
