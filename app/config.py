from pydantic import BaseSettings

# import os


# this a settings class which takes care of env variables (reads both environment variables and vales from dotenv file)
class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_hostname: str
    database_port: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"  # get env variables from .env file
        env_file_encoding = "utf-8"


settings = Settings()
# print(settings.access_token_expire_minutes)
# print(os.environ.get("database_name"))    # returns None, because pydantic with dotenv does not set env variables mentioned in .env file. It just reads it.
