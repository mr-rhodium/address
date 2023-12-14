from pydantic import AnyUrl, MySQLDsn, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    database_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

conf = Settings()