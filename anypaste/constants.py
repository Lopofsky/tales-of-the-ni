from os import environ, path as os_path
from dotenv import load_dotenv

env_path = os_path.join(os_path.dirname(__file__), '.env')

if os_path.exists(env_path):
    load_dotenv(dotenv_path=env_path, override=True)
    print("Loaded environment variables from {0}".format(env_path))
else:
    print(
        "Warning: {0} not found. Environment variables were not loaded.".format(env_path))

not_the_best_idea = {
    'a': environ.get('a'),
    'b': environ.get('b'),
    'rms': environ.get('rms'),
}

PREFIX = ""
SUFFIX = ""
ENDING_STRING = 'e'
LOGGER_TEXT = "[LOG START]"

