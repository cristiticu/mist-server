from fastapi import APIRouter, HTTPException, status
from context import ApplicationContext
from games.exceptions import GameNotFound


router = APIRouter(prefix="/game", tags=["game"])
application_context = ApplicationContext()


@router.get("")
def list_games(limit: int, offset: int):
    return application_context.games.get_page(limit=limit, offset=offset)


@router.get("/{game_id}")
def get_game(game_id: str):
    return application_context.games.get(id=game_id)
