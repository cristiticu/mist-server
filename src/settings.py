import os
from dotenv import load_dotenv

load_dotenv('./.env')

GAMES_FILEPATH = os.environ.get('GAMES_FILEPATH')
PERSIST_GAMES_JSON = os.environ.get('PERSIST_GAMES_JSON') == 'True'
START_BACKGROUND_ADDER = os.environ.get('START_BACKGROUND_ADDER') == 'True'
