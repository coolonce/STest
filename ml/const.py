import os
LOCAL_STORAGE = os.environ.get('LOCAL_STORAGE')
MODEL_PATH = os.environ.get('MODEL_PATH', 'model.sav')

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_QUEUE = os.environ.get("REDIS_QUEUE")

REDIS_STATUS_ORDER = os.environ.get("REDIS_STATUS_ORDER", '2')

DB_DRIVER = os.environ.get("DB_DRIVER", "postgresql")
DB_USER = os.environ.get("DB_USER", "user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "sber")

DB_TABLE = os.environ.get("DB_TABLE", "order")

SQLALCHEMY_DATABASE_URL = (
    f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

CODE_DIR_NOT_FOUND = -1
CODE_FILE_NOT_FOUND = -2
CODE_MODEL_NOTFOUND = -3
CODE_PREDICT_FAIL = -4
CODE_PREDICT_SUCCESS = 1