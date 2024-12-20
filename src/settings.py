import os
from dotenv import load_dotenv

load_dotenv('./.env')

GAMES_FILEPATH = os.environ.get('GAMES_FILEPATH')
USERS_FILEPATH = os.environ.get('USERS_FILEPATH')
LICENSES_FILEPATH = os.environ.get('LICENSES_FILEPATH')
PERSIST_GAMES_JSON = os.environ.get('PERSIST_GAMES_JSON') == 'True'
PERSIST_USERS_JSON = os.environ.get('PERSIST_USERS_JSON') == 'True'
PERSIST_LICENSES_JSON = os.environ.get('PERSIST_LICENSES_JSON') == 'True'
START_BACKGROUND_ADDER = os.environ.get('START_BACKGROUND_ADDER') == 'True'

SECRET_KEY = "b386aaadd83435c99d40d96234972bf3330506473c6a41d081565a6cc39d1b7c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
