from dotenv import load_dotenv
from pydantic import BaseSettings

# load the environment variables
load_dotenv()


# this a settings class which takes care of env variables (either from .env or environment)
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
        env_file: ".env"
        # env_file_encoding = "utf-8"


settings = Settings()

# print(settings.access_token_expire_minutes)
