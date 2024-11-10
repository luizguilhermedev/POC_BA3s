import os


PATH_TO_FILES = [
    'src/data/books_data_cleaned.csv',
    'src/data/books_rating_cleaned.csv',
]
PATH_TO_FILE = os.environ.get('PATH_TO_FILE', PATH_TO_FILES)

API_V1_STR: str = '/api/v1'


APP_HOST = os.environ.get('APP_HOST', 'localhost')
APP_PORT = os.environ.get('APP_PORT', 8765)

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'info')
