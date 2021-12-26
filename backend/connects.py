from os import environ
import databases

import redis

DB_DRIVER = environ.get("DB_DRIVER", "postgresql")
DB_USER = environ.get("DB_USER", "user")
DB_PASSWORD = environ.get("DB_PASSWORD", "password")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_PORT = environ.get("DB_PORT", "5432")
DB_NAME = environ.get("DB_NAME", "sber")

LOCAL_STORAGE = environ.get("LOCAL_STORAGE", "storage")

SQLALCHEMY_DATABASE_URL = (
    f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
# создаем объект database, который будет использоваться для выполнения запросов
database = databases.Database(SQLALCHEMY_DATABASE_URL)


REDIS_HOST =  environ.get("REDIS_HOST", "127.0.0.1")
REDIS_QUEUE =  environ.get("REDIS_QUEUE", "")

redis = redis.StrictRedis(host=REDIS_HOST)
