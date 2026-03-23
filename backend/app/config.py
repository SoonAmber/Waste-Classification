from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os

class Settings(BaseSettings):
    server_host: str = os.getenv("SERVER_HOST", "127.0.0.1")
    server_port: int = int(os.getenv("SERVER_PORT", 8000))
    secret_key: str = os.getenv("SECRET_KEY", "secret")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./users.db")
    inference_device: str = os.getenv("MODEL_DEVICE", "cuda")

    model_config = ConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()
