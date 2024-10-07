import os
from dotenv import load_dotenv
from fastapi import FastAPI

from games.persistence import GamesPersistence
from games.service import GamesService

load_dotenv('./.env')

app = FastAPI(title='Mist')

GAMES_FILEPATH = os.environ.get('GAMES_FILEPATH')

if GAMES_FILEPATH is not None:
    games = GamesPersistence(filepath=GAMES_FILEPATH)
    games_service = GamesService(games_persistence=games)
else:
    print('Games storage file path not found!')
    exit(-1)


@app.get("/games")
def get_users():
    return games_service.get_all()


@app.get("/games/{game_id}")
def get_user(game_id: str):
    return games_service.get(id=game_id)


# @app.post("/users")
# def create_user(create_user_request: CreateUserRequest):
#     return users_service.create(email=create_user_request.email,
#                                 password=create_user_request.password,
#                                 first_name=create_user_request.first_name,
#                                 last_name=create_user_request.last_name)


# @app.patch("/users/{user_id}")
# def update_user(user_id: str, patch_user_request: PatchUserRequest):
#     return users_service.update(id=user_id,
#                                 patch=patch_user_request)


# @app.delete("/users/{user_id}")
# def delete_user(user_id: str):
#     users_service.delete(id=user_id)
