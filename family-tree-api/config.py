from os import getenv, path

from dotenv import load_dotenv, find_dotenv

BASE_DIR = path.join(path.dirname(__file__), ".env.local")
if path.exists(BASE_DIR):
    load_dotenv(BASE_DIR)
else:
    load_dotenv(find_dotenv())


class Config:
    TESTING = False
    MYSQL_HOST = getenv("MYSQL_HOST")
    MYSQL_USER = getenv("MYSQL_USER")
    MYSQL_PASSWORD = getenv("MYSQL_PASSWORD")
    MYSQL_DB = getenv("MYSQL_DB")
