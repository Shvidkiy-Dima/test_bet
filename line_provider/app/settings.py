from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    MQ_HOST: str = "localhost"
    MQ_PORT: int = 5672
    MQ_USER: str = "user"
    MQ_PASS: str = "password"

    BET_MAKER_CALLBACK_URL: str = "http://localhost:8001/api/v1/callback/event"


settings = Settings()
