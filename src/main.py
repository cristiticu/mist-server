import os
from fastapi import FastAPI

app = FastAPI(title='Mist')

# USERS_FILEPATH = os.environ.get('USERS_FILEPATH')

# if USERS_FILEPATH is not None:
#     users = UsersFileRepository(filepath=USERS_FILEPATH)
#     users_service = UsersService(usersRepository=users)
# else:
#     print('Users storage file path not found!')
#     exit(-1)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/users")
# def get_users():
#     return users_service.get_users()


# @app.get("/users/{user_id}")
# def get_user(user_id: str):
#     return users_service.get(id=user_id)


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
