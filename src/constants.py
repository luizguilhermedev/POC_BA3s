import os


PATH_TO_FILE = [
    'src/data/books_data_sample.csv',
    'src/data/books_rating_sample.csv',
]


API_V1_STR: str = '/api/v1'


APP_HOST = os.environ.get('APP_HOST', 'localhost')
APP_PORT = os.environ.get('APP_PORT', 8765)

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'info')
