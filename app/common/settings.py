from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    DB_ENDPOINT: str = "db.sqlite"
